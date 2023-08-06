import math
import os
import shutil
import tempfile
import time
from multiprocessing import Process
from time import sleep

from selenium.common.exceptions import WebDriverException, TimeoutException, ElementNotInteractableException, \
    NoSuchElementException

from exceptions import ManualAnalysisNeededException, WebDriverInitialisationException, NoLoginCandidatesFoundException
from exceptions import RenewalRequestNeededException
from exceptions import SiteNotResolvableException
from input.input_management import InputManager
from logmgmt import logger
from model.backend_information import BackendInformation
from model.login_path_information import LoginPathInformation
from model.process_type import ProcessType
from model.ssodetection.search_algorithm import SearchAlgorithm
from model.ssodetection.search_engine import SearchEngine
from model.ssodetection.sso_detection_strategy import SSODetectionStrategy
from processes import generic_process
from processes.generic_process import GenericAnalysisProcess
from processes.process_helper import ProcessHelper
from processes.ssolandscapeanalysis import startpage_search, duck_duck_go_search, bing_search
from processes.ssolandscapeanalysis.logorecognition.logo_recognizer import LogoReconizer
from processes.ssolandscapeanalysis.sso_detection_service import SSODetectionService
from services.driver_manager import DriverManager
from services.rest_client import RestClient

temp_folder = tempfile.tempdir + "/ssoworker/landscape-analysis/"
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)


def thread_process(site, backend_info: BackendInformation, process_type: ProcessType, search_engines: list,
                   analysis_run_id: int, count_of_websites_to_analyze_per_website: int, search_algorithms: list):
    success = False
    rest_client = None
    chromedriver = None
    har_files_location = temp_folder + "har-files/"
    if os.path.exists(har_files_location):
        logger.info("Found old temp har files directory (may be empty, could come from aborted run). Deleting... ")
        shutil.rmtree(har_files_location)
    os.makedirs(har_files_location, exist_ok=True)
    cause = "Unknown"
    try:
        site_no_proto = ProcessHelper.remove_protocol_if_existent(site.base_page)
        rest_client = RestClient(backend_info.host, backend_info.port, backend_info.token)
        known_sso_provider = rest_client.get_known_sso_provider()
        start_time = time.time()
        logger.info("Received site " + site.base_page + " to analyse. Starting chromedriver...")
        rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 0, "Starting chromedriver")
        chromedriver = None
        if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
            chromedriver = DriverManager.generate_driver()
            rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 5, "Resolving site")
            logger.info("Testing resolving of site")
            test_resolve = ProcessHelper.resolve_tld1(chromedriver, site.base_page)
            if test_resolve is None:
                raise SiteNotResolvableException()

        logger.info("Checking sso support for " + site.base_page + " (id:" + str(site.index) + "|trancoID:" + str(
            rest_client.get_tranco_id_for_site(site.base_page)) + ")")
        login_candidates = []
        time_login_site_detection = time.time()
        if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
            if chromedriver is None:
                chromedriver = DriverManager.generate_driver()
            for se in search_engines:
                if not [e for e in SearchEngine].__contains__(se):
                    raise Exception("Unknown search engine!")
            if search_engines.__contains__(SearchEngine.DUCKDUCKGO):
                rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 10,
                                                        "Identifying login pages by DuckDuckGo")
                login_candidates_ddg = duck_duck_go_search.get_duckduckgo_login_pages(chromedriver, site_no_proto,
                                                                                      count_of_results=count_of_websites_to_analyze_per_website)
                for lc in login_candidates_ddg:
                    login_candidates.append({'engine': "DUCKDUCKGO", 'site': lc})
            if search_engines.__contains__(SearchEngine.STARTPAGE):
                rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 15,
                                                        "Identifying login pages by Startpage")
                login_candidates_sp = startpage_search.get_startpage_login_pages(chromedriver, site_no_proto,
                                                                                 count_of_results=count_of_websites_to_analyze_per_website)
                for lc in login_candidates_sp:
                    login_candidates.append({'engine': "STARTPAGE", 'site': lc})
            if search_engines.__contains__(SearchEngine.BING):
                rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 20,
                                                        "Identifying login pages by Bing")
                login_candidates_bing = bing_search.get_bing_login_pages(chromedriver, site_no_proto,
                                                                         count_of_results=count_of_websites_to_analyze_per_website)
                for fc in login_candidates_bing:
                    login_candidates.append({'engine': "BING", 'site': fc})
            latest_login_infos = []
            for f_login in login_candidates:
                latest_login_infos.append(
                    LoginPathInformation(site, -1, f_login['site'], [], True, False, None, {'se': f_login['engine']}))
        else:
            logger.info("Loading login page information from brain")
            rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 20,
                                                    "Loading login page from brain")
            latest_login_infos = [rest_client.get_latest_login_location_for_page_by_page_id(site.index)]
            login_candidates.append({'engine': "BRAIN", 'site': latest_login_infos[0].loginPath})
        time_login_site_detection = time.time() - time_login_site_detection
        # Finished Login Gathering
        if chromedriver is not None:
            logger.info("Preparations are finished. Closing chrome instance which was started for preparation.")
            ProcessHelper.quit_chromedriver_correctly(chromedriver)
        results = []
        if len(latest_login_infos) == 0:
            raise NoLoginCandidatesFoundException()
        steps = 30 / len(latest_login_infos)
        last_progress = 20
        har_files = []

        # KEYWORD ANALYSIS
        time_combined_analyses = time.time()
        time_keyword_based_analysis = time.time()
        file_counter = 0
        if search_algorithms is None or search_algorithms.__contains__(SearchAlgorithm.KEYWORD_ANALYSIS):
            logger.info("Starting keyword based (or manual) analysis")
            for latest_login_info in latest_login_infos:
                logger.info("Starting analysis for " + latest_login_info.loginPath)
                already_analysed_login_page = False
                for res_logo in results:
                    if res_logo["info"].loginPath == latest_login_info.loginPath:
                        results.append(
                            {"ids": res_logo["ids"], "info": latest_login_info, "screen": res_logo["screen"]})
                        already_analysed_login_page = True
                        break
                if already_analysed_login_page:
                    last_progress += steps
                    continue
                logger.info("Starting chrome instance to analyse " + latest_login_info.loginPath)
                chromedriver = DriverManager.generate_driver()
                try:
                    last_progress += steps / 6
                    rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, last_progress,
                                                            "Preparing analysis of " + latest_login_info.loginPath)
                    DriverManager.prepare_webpage_with_steps_to_reproduce(chromedriver, latest_login_info, True)
                except (ElementNotInteractableException, NoSuchElementException):
                    if handle_preparation_error(process_type, site.index, site.base_page, rest_client):
                        raise RenewalRequestNeededException()
                last_progress = last_progress + steps / 6
                rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, last_progress,
                                                        "Taking screenshot of " + latest_login_info.loginPath)
                screen = wait_and_gather_screenshot_if_necessary(chromedriver, process_type)

                # No status update necessary because it will happen next in the callback

                def progress_callback(step: int, max: int, status: str):
                    rest_client.update_progress_of_analysis(analysis_run_id, site.base_page,
                                                            last_progress + ((steps / 1.5) / max * step), status)

                search_for_google = not ProcessHelper.contain_results_provider(results, "google", known_sso_provider)
                if not search_for_google:
                    logger.info("Google SSO Support already found. Skipping it in analysis")
                search_for_facebook = not ProcessHelper.contain_results_provider(results, "facebook",
                                                                                 known_sso_provider)
                if not search_for_facebook:
                    logger.info("Facebook SSO Support already found. Skipping it in analysis")
                search_for_apple = not ProcessHelper.contain_results_provider(results, "apple", known_sso_provider)
                if not search_for_apple:
                    logger.info("Apple SSO Support already found. Skipping it in analysis")

                ids = gather_sso_support(known_sso_provider, latest_login_info, chromedriver, process_type,
                                         search_for_google, search_for_facebook, search_for_apple, progress_callback)
                logger.info("Keyword based (or manual) analysis finished for " + latest_login_info.loginPath +
                            ". Exporting har and stopping chromedriver")
                file_counter += 1
                har_file = har_files_location + str(
                    file_counter) + "-keyword-alg-" + ProcessHelper.gen_filename_from_url(
                    latest_login_info.loginPath) + ".har"
                with open(har_file, mode="w") as file:
                    file.write(chromedriver.har)
                har_files.append(har_file)
                logger.info("Exported har to " + har_file)
                ProcessHelper.quit_chromedriver_correctly(chromedriver)
                last_progress = last_progress + steps / 1.5
                results.append({"ids": ids, "info": latest_login_info, "screen": screen})
        else:
            logger.info("Skipping keyword based analysis (not requested) and only taking screenshots")
            for latest_login_info in latest_login_infos:
                last_progress = last_progress + steps
                logger.info("Taking screenshots of " + latest_login_info.loginPath)
                rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, last_progress,
                                                        "Taking screenshot of " + latest_login_info.loginPath)
                chromedriver = DriverManager.generate_driver()
                DriverManager.prepare_webpage_with_steps_to_reproduce(chromedriver, latest_login_info, True)
                screen = wait_and_gather_screenshot_if_necessary(chromedriver, process_type)
                results.append({"ids": [(9999, None, None, None, SSODetectionStrategy.NONE, None)],
                                "info": latest_login_info, "screen": screen})
                ProcessHelper.quit_chromedriver_correctly(chromedriver)
        time_keyword_based_analysis = time.time() - time_keyword_based_analysis

        # IMAGE ANALYSIS
        time_image_analysis = time.time()
        image_analysis_percent = 30
        if search_algorithms is not None and search_algorithms.__contains__(SearchAlgorithm.IMAGE_ANALYSIS):
            logger.info("Starting logo detection analysis")
            urls_to_analyse = []
            for login_candidate in login_candidates:
                if not urls_to_analyse.__contains__(login_candidate):
                    urls_to_analyse.append(login_candidate['site'])

            def progress_callback_image_analysis(step: int, max: int, status: str):
                rest_client.update_progress_of_analysis(analysis_run_id, site.base_page,
                                                        last_progress + step * (image_analysis_percent / max), status)

            logoR = LogoReconizer(temp_folder)
            res_logo = logoR.analyseHybridLoginURL(
                domain_url=site.base_page.replace("https://", "").replace("http://", ""), login_urls=urls_to_analyse,
                init_recognition={
                    "facebook": ProcessHelper.contain_results_provider(results, "facebook", known_sso_provider),
                    "google": ProcessHelper.contain_results_provider(results, "google", known_sso_provider),
                    "apple": ProcessHelper.contain_results_provider(results, "apple", known_sso_provider)},
                callback=progress_callback_image_analysis)

            for r in res_logo["details"]:
                logger.info("Logo recognition found following sso provider %s", r["provider"])
                found = False
                for orig_results in results:
                    if orig_results['info'].loginPath == r['login_url']:
                        orig_results['ids'].append((ProcessHelper.get_provider_id_from_remote_known_providers(
                            known_sso_provider, r['provider']), {'x': math.ceil(r['coordinates'][0]),
                                                                 'y': math.ceil(r['coordinates'][1])},
                                                    None, r['login_url'], SSODetectionStrategy.IMAGE_ANALYSIS,
                                                    r['idp_url']))
                        logger.info("Exporting har")
                        file_counter += 1
                        har_file = har_files_location + str(file_counter) + "-image-alg-" + r[
                            'provider'] + "-" + ProcessHelper.gen_filename_from_url(r['login_url']) + ".har"
                        with open(har_file, mode="w") as file:
                            file.write(r['har'])
                        har_files.append(har_file)
                        logger.info("Exported har to " + har_file)
                        found = True
                        break
                if not found:
                    raise Exception("Could not find a corresponding login candidate for the webpage " + r['login_url'])
        elif search_algorithms is not None:
            logger.info("Skipping image analysis (not requested)")
        time_image_analysis = time.time() - time_image_analysis
        time_combined_analyses = time.time() - time_combined_analyses
        time_complete_process = time.time() - start_time
        rest_client.update_progress_of_analysis(analysis_run_id, site.base_page, 90, "Uploading results")
        success = save_supported_sso_provider(site, results, har_files, process_type, rest_client, analysis_run_id)
        time_complete_process_with_upload = time.time() - start_time
        logger.info("Successfully saved!" if success else "Could not save site")
        if success:
            logger.info("Sending timing results")
            try:
                rest_client.post_timing_results(analysis_run_id, site.base_page, time_login_site_detection,
                                                time_keyword_based_analysis, time_image_analysis,
                                                time_combined_analyses, time_complete_process,
                                                time_complete_process_with_upload, len(latest_login_infos))
            except Exception as e:
                logger.error(
                    "Could not send timing results. As this is only meta info. The process will not be aborted!" + str(
                        e))
        logger.info("Timing results:" + ((" LD " + str(
            time_login_site_detection) + " |") if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE else "") + " KBA " + str(
            time_keyword_based_analysis) + " | LRA " + str(time_image_analysis) + " | CBA " + str(
            time_combined_analyses) + " | CP " + str(
            time_complete_process) + " | CPWU " + str(time_complete_process_with_upload))
        logger.info("Timing results per page (" + str(len(latest_login_infos)) + " sites analysed):" + ((" LD " + str(
            time_login_site_detection / len(
                latest_login_infos)) + " |") if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE else "") + " KBA " + str(
            time_keyword_based_analysis / len(latest_login_infos)) + " | LRA " + str(
            time_image_analysis / len(latest_login_infos)) + " | CBA " + str(
            time_combined_analyses / len(latest_login_infos)) + " | CP " + str(
            time_complete_process / len(latest_login_infos)) + " | CPWU " + str(
            time_complete_process_with_upload / len(latest_login_infos)))
    except RenewalRequestNeededException:
        logger.error("Sending renewal request")
        rest_client.create_renew_login_location_request(site.index)
        return
    except TimeoutException as err:
        cause = "Timout: " + err.__class__.__name__
        logger.error("Timeout reached: " + err.msg)
    except WebDriverException as err:
        cause = "Webdriver problem: " + err.__class__.__name__
        logger.error("Could not finish analysing (" + err.msg + ")!")
    except ManualAnalysisNeededException as err:
        cause = "Unknown - manual analysis needed"
        logger.error("Could not finish analysing (" + str(err) + ")!.")
    except SiteNotResolvableException:
        cause = "Not resolvable"
        logger.error("Could not resolve site!")
    except NoLoginCandidatesFoundException:
        cause = "No login candidates found"
        logger.error("Could not find any login candidates for site")
    except KeyboardInterrupt as err:
        logger.info("Received interrupt. Will deregister current page:")
        logger.info("Done") if rest_client.unregister_page_in_work(analysis_run_id, site.base_page) \
            else logger.error("Failed!")
        success = True
        raise err
    except WebDriverInitialisationException as e:
        generic_process.handle_webdriver_initialisation_exception(rest_client, e, analysis_run_id, site)
    except Exception as err:
        cause = "Unknown error: " + err.__class__.__name__
        logger.error("Unknown error! This should be managed explicitly " +
                     str(err.__class__.__name__) + ": " + str(err))
    finally:
        if not success:
            rest_client.unregister_page_in_work_and_block_for_time(analysis_run_id, site.base_page, cause)
        if chromedriver is not None:
            ProcessHelper.quit_chromedriver_correctly(chromedriver)
            del chromedriver.requests, chromedriver
        if os.path.exists(temp_folder):
            logger.info("Cleaning up temporary folder")
            shutil.rmtree(temp_folder)


# Returns if the current site should be skipped
def handle_preparation_error(process_type, page_index, base_page, rest_client):
    logger.error("Site preparation for " + base_page + " failed!")
    if process_type == ProcessType.AUTOMATIC_SSO_DETECTION:
        logger.error("We will send a renewal request and skip this site!")
        handle_fail = 'y'
    elif process_type == ProcessType.MANUAL_SSO_DETECTION:
        handle_fail = InputManager.get_input_from_gui_with_specific_answer_values(
            "Do you want to send a renew request and skip this page or continue anyway?", ['y', 'n'])
    else:
        raise TypeError(process_type.__str__() + " should not land in this part of the code!")
    return handle_fail == 'y'


def wait_and_gather_screenshot_if_necessary(chromedriver, process_type):
    if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
        logger.info("Sleeping 10 sec to get best results in screenshot")
        sleep(10)
        logger.info("Taking screenshot...")
        return chromedriver.get_screenshot_as_png()
    elif process_type == ProcessType.AUTOMATIC_SSO_DETECTION:
        logger.info("Waiting 10 sec...")
        sleep(10)
    return None


def gather_sso_support(known_sso_provider, latest_login_info, chromedriver, process_type, google=True, facebook=True,
                       apple=True, progress_callback=None):
    logger.info("Starting SSO Detection algorithm")
    service = SSODetectionService(known_sso_provider)
    if process_type == ProcessType.AUTOMATIC_SSO_DETECTION or process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
        results = service.automatic_sso_detection(chromedriver, latest_login_info, progress_callback, google, facebook,
                                                  apple)
    else:
        results = service.manual_sso_detection()
    return results


def get_no_sso_login_item(ids: list):
    for id in ids:
        if id[0] == 9999:
            return id
    return None


def save_supported_sso_provider(site, results, har_files, process_type, rest_client, analysis_run_id):
    ids = []
    for result in results:
        if result['info'].other_information.__contains__("se"):
            result['info'].loginPath = "<<" + result['info'].other_information['se'] + ">>" + result['info'].loginPath
        for id_container in result['ids']:
            id_already_exists = False
            for already_existing_id in ids:
                if id_container[0] == already_existing_id[0]:
                    id_already_exists = True
                    break
            if not id_already_exists:
                ids.append(id_container)

    if len(ids) > 1 and get_no_sso_login_item(ids) is not None:
        ids.remove(get_no_sso_login_item(ids))
    if len(ids) == 0:
        ids.append((9999, None, None, None, SSODetectionStrategy.MANUAL))
    if process_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
        logger.info("Saving login candidates (" + str(
            len(results)) + ") and the following sso support for " + site.base_page + ": " + str(ids))
        return rest_client.save_analysed_supported_sso_provider(site.base_page, ids, analysis_run_id,
                                                                results, har_files)
    else:
        logger.info("Saving the following sso support for " + site.base_page + ": " + str(ids))
        return rest_client.save_analysed_supported_sso_provider(site.base_page, ids, analysis_run_id,
                                                                None, har_files)


class SSODetectionProcess(GenericAnalysisProcess):

    def __init__(self, backend_info: BackendInformation, analysis_run_id: int, process_type: ProcessType,
                 search_engines: list = None, count_of_websites_to_analyze_per_website: int = 3,
                 search_algorithms: list = None):
        if not [ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE, ProcessType.AUTOMATIC_SSO_DETECTION,
                ProcessType.MANUAL_SSO_DETECTION].__contains__(process_type):
            raise TypeError(str(process_type) + " is not supported for single sign on analysis!")
        self.backend_info = backend_info
        self.rest_client = RestClient(backend_info.host, backend_info.port, backend_info.token)
        self.search_engines = search_engines
        self.analysis_run_id = analysis_run_id
        self.process_type = process_type
        self.count_of_websites_to_analyze_per_website = count_of_websites_to_analyze_per_website
        self.search_algorithms = search_algorithms

    def prepare(self):
        ProcessHelper.check_for_unfinished_work(self.rest_client)

    def get_next_object_to_analyse(self):
        return self.rest_client.get_next_ssodetection_page_to_analyse_for_run(self.analysis_run_id)

    def generate_process(self, object_to_analyse) -> Process:
        return Process(target=thread_process, args=(
            object_to_analyse, self.backend_info, self.process_type, self.search_engines, self.analysis_run_id,
            self.count_of_websites_to_analyze_per_website, self.search_algorithms))
