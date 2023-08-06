import base64
import json
import os.path
from time import sleep

import requests

from exceptions import RetryException
from logmgmt import logger
from input.input_management import InputManager
from model.process_type import ProcessType
from services.rest_helper import RestHelper


class RestClient:
    # region Path Variables
    # region Global, Tranco, Misc Paths
    path_check_version = "/client/version.txt"
    path_check_token = "/rest/global/validateToken"
    path_tranco_entries_between = "/rest/tranco/between"
    path_get_tranco_id_for_site = "/rest/tranco/idforsite"
    path_known_sso_providers = "/rest/knownproviders/all"
    path_file_upload_login_path_detection = "/rest/files/loginlocationdetection"
    path_post_timing_results = "/rest/timing/new"

    # endregion
    # region Login Page Locations Paths
    path_next_page_of_tranco_domains_with_no_login_path_detection = "/rest/loginlocation/getNextNotAnalysedPage"
    path_next_page_to_renew_login_path_information = "/rest/loginlocation/getNextPageToRenew"
    path_next_broken_page_to_renew_login_path_information = "/rest/loginlocation/getNextBrokenToRenew"
    path_latest_login_page_location = "/rest/loginlocation/latestForPage"
    path_latest_login_page_location_by_page_id = "/rest/loginlocation/latestForPageByPageId"
    path_additional_steps_for_login_path_location = "/rest/loginlocation/getAdditionalSteps"
    path_add_new_login_page_location = "/rest/loginlocation/addNew"
    path_create_login_location_renew_request = "/rest/loginlocation/generateRenewRequest"
    # endregion
    # region Analysis Runs Paths
    path_exists_analysis_run = "/rest/analysisrun/existsid"
    path_get_analysis_run_type = "/rest/analysisrun/type"
    path_analysis_run_additional_information = "/rest/analysisrun/additionalInformationForAnalysisRun"
    path_has_configuration = "/rest/analysisrun/hasConfiguration"
    path_get_configuration = "/rest/analysisrun/configuration"
    # endregion
    # region SSO Detection Paths
    path_get_next_page_to_detect_sso = "/rest/ssodetection/nextPageToAnalyse"
    path_save_sso_analysis = "/rest/ssodetection/new"
    # endregion
    # region Currently in Work Paths
    path_unfinished_work = "/rest/currentlyinwork/unfinishedWork"
    path_unregister_currently_in_work_site_and_block = "/rest/currentlyinwork/unregisterCurrentlyInWorkAndBlockForTime"
    path_unregister_currently_in_work_site = "/rest/currentlyinwork/unregisterCurrentlyInWork"
    path_update_currently_in_work_site_progress = "/rest/currentlyinwork/reportProgress"
    path_update_sso_security_analysis_progress = "/rest/currentlyinwork/reportSSOSecurityAnalysisProgress"
    path_unregister_currently_in_work_sso_det = "/rest/currentlyinwork/unregisterCurrentlyInWorkSSODetection"
    path_unregister_currently_in_work_sso_det_and_block = "/rest/currentlyinwork/unregisterCurrentlyInWorkSSODetectionAndBlockForTime"
    # endregion
    # region Privacy Detection
    path_get_next_privacy_page_to_analyze = "/rest/privacy/nextDetectionToAnalyse"
    path_save_privacy_detection = "/rest/privacy/new"

    # region SSO Security Analysis
    path_get_next_sso_detection_for_security_analysis = "/rest/ssosecurityanalysis/nextDetectionToAnalyse"
    path_save_sso_security_analysis = "/rest/ssosecurityanalysis/new"
    # endregion
    # region Daemon
    path_daemon_start = "/rest/daemon/wakeup"
    path_daemon_get_current_job = "/rest/daemon/job"
    path_daemon_stop = "/rest/daemon/stopped"
    path_daemon_ping = "/rest/daemon/ping"
    path_daemon_update_activity = "/rest/daemon/activity"

    # endregion
    # region Debug Paths
    debug_path_sso_security_analysis = "/rest/ssosecurityanalysis/debug"
    # endregion
    # endregion

    retry_max_tries = 3

    def __init__(self, backend_url, backend_port, token=None):
        self.backend_url = backend_url
        self.port = backend_port
        self.url = self.backend_url + ":" + str(self.port)
        if token is not None:
            self.auth_bearer_header = {'Authorization': 'Bearer ' + token}
        else:
            self.auth_bearer_header = {}

    # region Global, Tranco, Misc
    def get_remote_client_version(self):
        response = self.send_get_request(self.path_check_version)
        if response.status_code == 200 and len(response.text) > 0:
            return response.text.split("\n")[0]
        logger.error(
            "Something went wrong while checking version (" + str(response.status_code) + ") " + response.text)
        return None

    def check_token(self, token):
        response = self.send_post_request(self.path_check_token, {'token': token})
        if response.status_code == 200 and response.text.startswith("valid"):
            return True
        logger.error("Something went wrong while checking (" + str(response.status_code) + "): " + response.text)
        return False

    def get_list_of_tranco_domains(self, lower_bound, upper_bound):
        url = self.url + self.path_tranco_entries_between
        response = requests.get(url, params={'lower': lower_bound, 'upper': upper_bound},
                                headers=self.auth_bearer_header)
        if not response.status_code == 200:
            logger.error("Something went wrong (code " + str(response.status_code) + "): " + response.text)
            return []
        return_list = []
        for entry in response.json():
            return_list.append(RestHelper.tranco_page_info_from_json(entry))
        return return_list

    def get_tranco_id_for_site(self, site):
        response = self.send_get_request(self.path_get_tranco_id_for_site, {'site': site})
        if response.status_code == 200 and response.text.isnumeric():
            return response.text
        logger.error("Something went wrong")
        return "UNKNOWN"

    def get_known_sso_provider(self):
        response = self.send_get_request(self.path_known_sso_providers)
        return RestHelper.convert_json_to_list_of_sso_provider(response)

    def post_timing_results(self, analysis_run_id, base_page, time_login_site_detection, time_keyword_based_analysis,
                            time_image_analysis, time_combined_analyses, time_complete_process,
                            time_complete_process_with_upload, sites_analysed):
        post_data = {'analysisrunid': analysis_run_id, 'basepage': base_page,
                     "timeloginsitedetection": time_login_site_detection,
                     "timekeywordbasedanalysis": time_keyword_based_analysis, "timeimageanalysis": time_image_analysis,
                     "timecombinedanalyses": time_combined_analyses, "timecompleteprocess": time_complete_process,
                     "timecompleteprocesswithupload": time_complete_process_with_upload,
                     "sitesanalysed": sites_analysed}
        response = self.send_post_request(self.path_post_timing_results, post_data)
        if response.status_code == 200:
            logger.info("Successfully saved timing results")
            return True
        else:
            logger.error("Something went wrong (code " + str(response.status_code) + ")")
            return False

    # endregion

    # region Login Page Locations
    def get_next_broken_path_detection_to_renew(self):
        response = self.send_get_request(self.path_next_broken_page_to_renew_login_path_information)
        if len(response.text) == 0:
            return None
        return RestHelper.page_info_from_json(response.json())

    def get_next_login_path_detection_to_renew(self):
        response = self.send_get_request(self.path_next_page_to_renew_login_path_information)
        if len(response.text) == 0:
            return None
        return RestHelper.page_info_from_json(response.json())

    def get_next_page_of_tranco_domains_with_no_login_path_detection(self, lower_bound, upper_bound):
        response = self.send_get_request(self.path_next_page_of_tranco_domains_with_no_login_path_detection,
                                         {'lower': lower_bound, 'upper': upper_bound})
        if len(response.text) == 0:
            return None
        return RestHelper.page_info_from_json(response.json())

    def get_latest_login_location_for_page(self, base_page):
        response = self.send_get_request(self.path_latest_login_page_location, {'basepage': base_page})
        if response.content.__len__() == 0:
            return None
        return RestHelper.manual_login_page_location_from_json(response.json(), self)

    def get_latest_login_location_for_page_by_page_id(self, index):
        response = self.send_get_request(self.path_latest_login_page_location_by_page_id, {'basepageid': index})
        if response.content.__len__() == 0:
            return None
        return RestHelper.manual_login_page_location_from_json(response.json(), self)

    def save_login_page_location(self, basepage, loginPage, hasLogin, additionalStepsToShowLogin, broken,
                                 finding_strategy, har_content):
        additionalStepsData = []
        counter = 0
        if additionalStepsToShowLogin is not None:
            for addStep in additionalStepsToShowLogin:
                additionalStepsData.append(
                    {"additionalStepValue": InputManager.get_additional_step_value_from_user_input(addStep),
                     "additionalStepType": InputManager.get_additional_step_type_from_user_input(addStep),
                     "additionalStepOrderIndex": counter})
                counter += 1

        post_data = {'basepage': basepage, 'loginpage': loginPage, 'haslogin': hasLogin, 'broken': broken,
                     'additionalsteps': base64.b64encode(json.dumps(additionalStepsData).encode()),
                     'findingstrategy': finding_strategy.name}
        response = self.send_post_request(self.path_add_new_login_page_location, post_data)
        if response.status_code == 200 and response.text.isnumeric():
            logger.info("Successfully saved login location!")
            if har_content is not None:
                logger.info("Uploading HAR file...")
                if self.upload_har_files(response.text, har_content, ProcessType.LOGIN_PATH_DETECTION):
                    logger.info("Uploading HAR file finished!")
            else:
                logger.info("No HAR content was given. Not going to upload har file!")
            return response.text
        else:
            logger.error("Something went wrong (code " + str(response.status_code) + ")")
            return False

    def get_additional_steps_for_login_path_location(self, login_path_detection_id):
        response = self.send_get_request(self.path_additional_steps_for_login_path_location,
                                         {'loginpagelocationid': login_path_detection_id})
        return RestHelper.convert_json_to_list_of_additional_steps(response)

    def upload_har_files(self, saved_item_id, har_content, file_type):
        logger.info("Uploading har content")
        if file_type == ProcessType.LOGIN_PATH_DETECTION:
            path = self.path_file_upload_login_path_detection
        else:
            raise Exception("Unknown har file type")
        response = self.send_post_file_request(path, {saved_item_id: base64.b64encode(har_content.encode("utf-8"))})
        if response.status_code == 200 and response.text == "success":
            logger.info("File uploaded successfully!")
            return True
        else:
            logger.error("Something went wrong (code " + str(response.status_code) + ")")
            return False

    def create_renew_login_location_request(self, page_id):
        response = self.send_post_request(self.path_create_login_location_renew_request, {"pageid": page_id})
        if response.status_code == 200:
            if response.text == "created":
                logger.info("Renew request created")
            elif response.text == "exists":
                logger.info("Renew request already exists")
            else:
                logger.error("Something went wrong!")
            return True
        else:
            logger.error("Something went wrong (code " + str(response.status_code) + ")")
            return False

    # endregion

    # region SSO Detection
    def save_analysed_supported_sso_provider(self, trancosite, ids, analysis_session, results, har_files):
        transformed_ids = []
        for id in ids:
            tid = [id[0]]
            if len(id) > 1:
                if id[1] is not None:
                    tid.append(id[1]['x'])
                    tid.append(id[1]['y'])
                else:
                    tid.extend([None, None])
                if id[2] is not None:
                    tid.append(id[2]['width'])
                    tid.append(id[2]['height'])
                else:
                    tid.extend([None, None])
                tid.append(id[3])
                tid.append(id[4].name)
                tid.append(id[5])
            transformed_ids.append(tid)
        post_data = {'analysisrunid': analysis_session, 'trancosite': trancosite,
                     'supportedproviderids': transformed_ids, "loginpages": []}
        if results is not None:
            for result in results:
                post_data['loginpages'].append(result['info'].loginPath)
        files = []
        size = 0
        if har_files is not None and len(har_files) > 0:
            for har_file in har_files:
                size += os.path.getsize(har_file)
                files.append((os.path.basename(har_file), open(har_file, mode="rb")))
        if results is not None:
            for result in results:
                size += len(result['screen'])
                files.append(('screenshot', result['screen']))
        if len(files) > 0:
            logger.info("Upload size of files (har, screen, ...): " + str(size * 0.000001) + " MB")
        if len(files) == 0:
            files = dict(mock='file')  # Forcing multipart upload
        response = self.send_post_request_with_files(self.path_save_sso_analysis, post_data, files)
        if response.status_code == 200 and response.text == "success":
            logger.info("File uploaded successfully!")
            return True
        else:
            logger.error("Something went wrong (code " + str(response.status_code) + ")")
            return False

    def get_next_ssodetection_page_to_analyse_for_run(self, analysis_run_id):
        return self.get_next_page_to_analyse_for_run(self.path_get_next_page_to_detect_sso, analysis_run_id)

    def get_search_engine_mode_for_run(self, run_id):
        return self.get_additional_analysis_run_information(run_id, "SEARCH_ENGINE")

    def get_search_algorithms_for_run(self, run_id):
        return self.get_additional_analysis_run_information(run_id, "SEARCH_ALGORITHM")

    # endregion

    # region Privacy Detection
    def save_privacy_detection(self, sso_det_index, analysis_session, screenshot, har_content):
        post_data = {'analysisrunid': analysis_session, 'ssodetectionid': sso_det_index}
        files = {}
        if har_content is not None:
            files['sso_privacy_detection.har'] = har_content
        if screenshot is not None:
            files['screenshot'] = screenshot
        response = self.send_post_request_with_files(self.path_save_privacy_detection, post_data,
                                                     files)
        if response.status_code == 200 and response.text == "success":
            logger.info("Privacy detection with HAR and Screenshot uploaded was successful!")
            return True
        else:
            logger.error("Something went wrong (code " + str(response.status_code) + ")")
            return False

    def get_next_privacy_detection_page_to_analyse_for_run(self, analysis_run_id):
        response = self.send_get_request(self.path_get_next_privacy_page_to_analyze, {'analysisrunid': analysis_run_id})
        if response.status_code == 200:
            if response.text is not None and len(response.text) != 0:
                return response.json()
            else:
                return None  # No more sites left!
        if response.status_code == 409:
            logger.info("Server requested a retry")
            raise RetryException()
        logger.error("Something went wrong (code " + str(response.status_code) + ")")

    # endregion

    # region SSO Security Analysis
    def get_debug_info_sso_security_analysis(self, analysis_run_id, page):
        response = self.send_get_request(self.debug_path_sso_security_analysis,
                                         {'analysisrunid': analysis_run_id, 'page': page})
        return self.extract_response_as_json(response)

    def get_next_sso_detection_for_security_analysis_for_run(self, analysis_run_id):
        response = self.send_get_request(self.path_get_next_sso_detection_for_security_analysis,
                                         {'analysisrunid': analysis_run_id})
        return self.extract_response_as_json(response)

    def save_sso_security_analysis(self, analysis_run_id, sso_detection_index: int, result: tuple, screen: bytes, har,
                                   success=True, error=None, error_screenshot=None):
        post_data = {'analysisrunid': analysis_run_id, 'ssodetectionid': sso_detection_index, 'authreq': result[0],
                     'authres': result[1], 'success': success, 'error': error}
        files = {}
        if har is not None:
            files['sso_security_analysis.har'] = har
        if screen is not None:
            files['screenshot'] = screen
        if error_screenshot is not None:
            files['potentialerrorscreenshot'] = error_screenshot
        response = self.send_post_request_with_files(self.path_save_sso_security_analysis, post_data,
                                                     files)
        if response.status_code == 200 and response.text == "success":
            logger.info("Saving SSO Security analysis with HAR and Screenshot uploaded was successful!")
            return True
        else:
            logger.error("Something went wrong (code " + str(response.status_code) + ")")
            return False

    # endregion

    # region Currently in Work Pages
    def unregister_page_in_work_and_block_for_time(self, analysisrunid, basepage, cause="Unknown"):
        response = self.send_post_request(self.path_unregister_currently_in_work_site_and_block,
                                          {'analysisrunid': analysisrunid, 'basepage': basepage, 'cause': cause})
        if response.status_code == 200:
            return True
        logger.error("Something went wrong (" + str(response.status_code) + ")!")
        return False

    def unregister_page_in_work(self, analysisrunid, basepage):
        response = self.send_post_request(self.path_unregister_currently_in_work_site,
                                          {'analysisrunid': analysisrunid, 'basepage': basepage})
        if response.status_code == 200:
            return True
        logger.error("Something went wrong (" + str(response.status_code) + ")!")
        return False

    def unregister_currently_in_work_sso_det(self, analysisrunid, detid):
        response = self.send_post_request(self.path_unregister_currently_in_work_sso_det,
                                          {'analysisrunid': analysisrunid, 'ssodetectionid': detid})
        if response.status_code == 200:
            return True
        logger.error("Something went wrong (" + str(response.status_code) + ")")
        return False

    def unregister_currently_in_work_sso_det_and_block(self, analysisrunid, detid, cause="Unknown"):
        response = self.send_post_request(self.path_unregister_currently_in_work_sso_det_and_block,
                                          {'analysisrunid': analysisrunid, 'ssodetectionid': detid, 'cause': cause})
        if response.status_code == 200:
            return True
        logger.error("Something went wrong (" + str(response.status_code) + ")")
        return False

    def update_progress_of_analysis(self, analysisrunid: int, basepage: str, percent: int, status: str):
        response = self.send_post_request(self.path_update_currently_in_work_site_progress,
                                          {'analysisrunid': analysisrunid, 'basepage': basepage,
                                           'percent': int(percent), 'status': status})
        if response.status_code == 200:
            return True
        logger.error("Something went wrong updating progress status (" + str(response.status_code) + ")!")
        return False

    def update_progress_of_analysis_using_sso_detection(self, analysis_run_id, sso_detection_id, percent: int,
                                                        status: str):
        response = self.send_post_request(self.path_update_sso_security_analysis_progress,
                                          {'analysisrunid': analysis_run_id, 'ssodetectionid': sso_detection_id,
                                           'percent': int(percent), 'status': status})
        if response.status_code == 200:
            return True
        logger.error("Something went wrong updating progress status (" + str(response.status_code) + ")!")
        return False

    def get_unfinished_work(self):
        response = self.send_get_request(self.path_unfinished_work)
        if response.status_code == 200:
            return response.json()
        logger.error("Something went wrong ")
        return False

    # endregion

    # region Analysis Runs
    def exists_analysis_session(self, analysis_run_id):
        response = self.send_get_request(self.path_exists_analysis_run,
                                         {'analysisrunid': analysis_run_id})
        return response.status_code == 200 and response.text == 'success'

    def get_analysis_run_type(self, analysis_run_id):
        response = self.send_get_request(self.path_get_analysis_run_type, {'analysisrunid': analysis_run_id})
        if response.status_code == 200 and response.text is not None and len(response.text) != 0:
            return response.text
        logger.error("Something went wrong (code " + str(response.status_code) + ")")
        return None

    def get_configuration_for_run(self, analysis_run_id):
        response = self.send_get_request(self.path_has_configuration, {'analysisrunid': analysis_run_id})
        if response.status_code != 200 or response.text is None or response.text != "true":
            return None
        response = self.send_get_request(self.path_get_configuration, {'analysisrunid': analysis_run_id})
        if response.status_code != 200:
            return None
        return response.content

    # endregion

    # region Generic Methods
    def get_next_page_to_analyse_for_run(self, path, analysis_run_id):
        response = self.send_get_request(path, {'analysisrunid': analysis_run_id})
        if response.status_code == 200:
            if response.text is not None and len(response.text) != 0:
                return RestHelper.page_info_from_json(response.json())
            else:
                return None  # No more sites left!
        if response.status_code == 409:
            logger.info("Server requested a retry")
            raise RetryException()
        logger.error("Something went wrong (code " + str(response.status_code) + ")")
        return None

    def get_additional_analysis_run_information(self, analysis_run_id, key):
        response = self.send_get_request(self.path_analysis_run_additional_information,
                                         {'analysisrunid': analysis_run_id, 'key': key})
        if response.status_code == 200 and response.text is not None and len(response.text) != 0:
            return response.text
        elif response.status_code == 404:
            return None
        logger.error("Something went wrong (code " + str(response.status_code) + ")")
        return None

    def extract_response_as_json(self, response):
        if response.status_code == 200:
            if response.text is not None and len(response.text) != 0:
                return response.json()
            else:
                return None  # No more sites left!
        if response.status_code == 409:
            logger.info("Server requested a retry")
            raise RetryException()
        logger.error("Something went wrong (code " + str(response.status_code) + ")")

    # endregion

    # region DAEMON METHODS
    def get_notify_daemon_start_get_token(self, name, identifier):
        if name is None:
            response = self.send_post_request(self.path_daemon_start, {'identifier': identifier})
        else:
            response = self.send_post_request(self.path_daemon_start, {'name': name, 'identifier': identifier})
        if response.status_code == 200 and response.text is not None and len(response.text) != 0:
            return response.text
        elif response.status_code != 200:
            logger.error("Something went wrong! (code: " + str(response.status_code) + ")")
        return None

    def get_job_for_daemon_client(self):
        response = self.send_get_request(self.path_daemon_get_current_job)
        if response.status_code == 200 and response.text is not None and len(
                response.text) != 0 and response.text.lstrip("-").isnumeric():
            return response.text
        return None

    def send_daemon_ping(self):
        self.send_get_request(self.path_daemon_ping)

    def update_latest_activity(self, activity: str):
        self.send_post_request(self.path_daemon_update_activity, {'activity': activity})

    # endregion

    # region REQUEST METHODS
    def send_get_request(self, path, parameters=None):
        attempts_counter = 0
        while attempts_counter < RestClient.retry_max_tries:
            attempts_counter += 1
            try:
                if parameters is None:
                    return requests.get(self.url + path, headers=self.auth_bearer_header, allow_redirects=False)
                else:
                    return requests.get(self.url + path, params=parameters, headers=self.auth_bearer_header,
                                        allow_redirects=False)
            except Exception as e:
                self.handle_send_error(e, attempts_counter)

    def send_post_request(self, path, postdata):
        attempts_counter = 0
        while attempts_counter < RestClient.retry_max_tries:
            attempts_counter += 1
            try:
                return requests.post(self.url + path, data=postdata, headers=self.auth_bearer_header,
                                     allow_redirects=False)
            except Exception as e:
                self.handle_send_error(e, attempts_counter)

    def send_post_file_request(self, path, files):
        attempts_counter = 0
        while attempts_counter < RestClient.retry_max_tries:
            attempts_counter += 1
            try:
                logger.info("Size of fileupload: " + str(len(str(files)) * 0.000001) + " MB")
                return requests.post(self.url + path, files=files, headers=self.auth_bearer_header,
                                     allow_redirects=False)
            except Exception as e:
                self.handle_send_error(e, attempts_counter)

    def send_post_request_with_files(self, path, postdata, files):
        attempts_counter = 0
        while attempts_counter < RestClient.retry_max_tries:
            attempts_counter += 1
            try:
                return requests.post(self.url + path, data=postdata, files=files, headers=self.auth_bearer_header,
                                     allow_redirects=False)
            except Exception as e:
                self.handle_send_error(e, attempts_counter)

    def handle_send_error(self, error, attempt):
        if attempt < RestClient.retry_max_tries:
            time_to_wait = 1 if attempt < (RestClient.retry_max_tries - 1) else 5
            logger.error("Got an exception (" + str(
                error.__class__.__name__) + ") when trying to send request. Will wait " + str(
                time_to_wait) + " min and retry it")
            sleep(time_to_wait * 60)
        else:
            logger.error("Could not send request after " + str(
                RestClient.retry_max_tries) + " attempts. Will raise original error.")
            raise error

    # endregion
