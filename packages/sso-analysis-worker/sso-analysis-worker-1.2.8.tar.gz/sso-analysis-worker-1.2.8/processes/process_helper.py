import threading
from urllib.parse import urlparse, urlencode, parse_qsl, quote

from seleniumwire import webdriver

from logmgmt import logger
from model.backend_information import BackendInformation
from model.process_type import ProcessType
from model.ssodetection.search_algorithm import SearchAlgorithm
from services.rest_client import RestClient


class ProcessHelper:
    google_check_url = "https://myaccount.google.com/"
    facebook_check_url = "https://www.facebook.com/settings/?tab=account"
    apple_check_url = "https://appleid.apple.com/"

    @staticmethod
    def find_redirect_uri_in_request(url, redirect_uri, body=None):
        parsed_redirect_uri_url = url
        try:
            parsed_redirect_uri = urlparse(redirect_uri)
            parsed_redirect_uri = parsed_redirect_uri._replace(query=urlencode(parse_qsl(parsed_redirect_uri.query)))
            parsed_redirect_uri = parsed_redirect_uri._replace(
                netloc=parsed_redirect_uri.netloc.replace(":443", "").replace(":80", ""))
            parsed_redirect_uri_url = parsed_redirect_uri.geturl()
        except Exception as e:
            logger.warn(str(e))
            pass
        if url.startswith(redirect_uri) or url.startswith(parsed_redirect_uri_url):
            if url.__contains__("code") or url.__contains__("access_token") or url.__contains__("id_token"):
                return True
            if body is not None:
                return body.__contains__("code=") or body.__contains__("access_token=") or body.__contains__(
                    "id_token=")
        return False

    @staticmethod
    def contain_results_provider(results, provider, known_sso_provider):
        provider_id = ProcessHelper.get_provider_id_from_remote_known_providers(known_sso_provider, provider)
        for r in results:
            for id in r['ids']:
                if id[0] == provider_id:
                    return True
        return False

    @staticmethod
    def get_provider_id_from_remote_known_providers(known_sso_provider: list, provider: str) -> int:
        for p in known_sso_provider:
            if p[1].lower() == provider.lower():
                return p[0]

    @staticmethod
    def remove_protocol_if_existent(page: str) -> str:
        return page.replace("https://", "").replace("http://", "")

    @staticmethod
    def check_for_unfinished_work(rest_client: RestClient):
        unfinished_work = rest_client.get_unfinished_work()
        if len(unfinished_work) > 0:
            logger.info("Looks like unfinished work was left after last shutdown. Will deregister with blocking for"
                        " 24h")
            for w in unfinished_work:
                logger.info("Deregister currently in work page " + str(w))
                rest_client.unregister_page_in_work_and_block_for_time(
                    w['fkAnalysisRun']['index'], w['trancoPageEntry'],
                    "Client crashed last time analysing this page")

    @staticmethod
    def prepare_and_run_analysis(backend_info: BackendInformation, analysis_id: int, virtual_display=None,
                                 threading_stop_event: threading.Event = None,
                                 webdriver_initialization_error_check: threading.Event = None,
                                 invalid_config_error_check=None):
        config_directory = None
        try:
            rc = RestClient(backend_info.host, backend_info.port, backend_info.token)
            analysis_run_type = ProcessType[rc.get_analysis_run_type(analysis_id)]
            logger.info("The analysis run is of type " + analysis_run_type.__str__())
            config = rc.get_configuration_for_run(analysis_id)
            if config is not None:
                import tempfile
                import zipfile
                import io
                config_directory = tempfile.TemporaryDirectory()
                z = zipfile.ZipFile(io.BytesIO(config))
                z.extractall(config_directory.name)
                del z, config

            if analysis_run_type == ProcessType.AUTOMATIC_SSO_DETECTION_BY_SEARCH_ENGINE:
                from model.ssodetection.search_engine import SearchEngine
                from processes.ssolandscapeanalysis.sso_detection_process import SSODetectionProcess
                logger.info(
                    "Request algorithm(s) and engine(s) for automatic analysis with search engine and count of websites")
                raw_ses = rc.get_search_engine_mode_for_run(analysis_id)[1:-1].split(",")
                count_of_websites = rc.get_additional_analysis_run_information(analysis_id,
                                                                               "COUNT_OF_WEBSITES_TO_ANALYSE_PER_SEARCH_ENGINE")
                raw_alg = rc.get_search_algorithms_for_run(analysis_id)
                if raw_alg is None:
                    raw_alg = ["KEYWORD_ANALYSIS", "IMAGE_ANALYSIS"]
                else:
                    raw_alg = raw_alg[1:-1].split(",")
                if count_of_websites is not None:
                    count_of_websites = int(count_of_websites)
                else:
                    count_of_websites = 3
                ses = []
                alg = []
                for i in range(0, len(raw_ses)):
                    ses.append(SearchEngine[raw_ses[i].strip()])
                for i in range(0, len(raw_alg)):
                    alg.append(SearchAlgorithm[raw_alg[i].strip()])
                analysis_process = SSODetectionProcess(backend_info, analysis_id, analysis_run_type, ses,
                                                       count_of_websites, alg)
            elif analysis_run_type == ProcessType.AUTOMATIC_SSO_DETECTION:
                from processes.ssolandscapeanalysis.sso_detection_process import SSODetectionProcess
                logger.info("Request algorithm(s) for automatic analysis")
                raw_alg = rc.get_search_algorithms_for_run(analysis_id)
                if raw_alg is None:
                    raw_alg = ["KEYWORD_ANALYSIS", "IMAGE_ANALYSIS"]
                else:
                    raw_alg = raw_alg[1:-1].split(",")
                alg = []
                for i in range(0, len(raw_alg)):
                    alg.append(SearchAlgorithm[raw_alg[i].strip()])
                analysis_process = SSODetectionProcess(backend_info, analysis_id, analysis_run_type, None, 3, alg)
            elif analysis_run_type == ProcessType.MANUAL_SSO_DETECTION:
                from processes.ssolandscapeanalysis.sso_detection_process import SSODetectionProcess
                analysis_process = SSODetectionProcess(backend_info, analysis_id, analysis_run_type)
            elif analysis_run_type == ProcessType.PRIVACY_DETECTION:
                from processes.privacydetection.privacy_detection_process import PrivacyDetectionProcess
                analysis_process = PrivacyDetectionProcess(backend_info, analysis_id, analysis_run_type,
                                                           config_directory)
            elif analysis_run_type == ProcessType.SSO_SECURITY_ANALYSIS:
                from processes.ssosecurityanalysis.sso_security_analysis_process import SSOSecurityProcess
                analysis_process = SSOSecurityProcess(backend_info, analysis_id, analysis_run_type, config_directory)
            else:
                raise TypeError("Unsupported analysis type: " + analysis_run_type.__str__())
            try:
                analysis_process.start_process(running_check=threading_stop_event,
                                               webdriver_initialisation_error_check=webdriver_initialization_error_check,
                                               invalid_config_error_check=invalid_config_error_check)
            except KeyboardInterrupt:
                logger.info("\n\nQuitting... Closing services connection and driver")
        finally:
            if virtual_display is not None:
                logger.info("Stopping virtual display")
                virtual_display.stop()
            if config_directory is not None:
                config_directory.cleanup()

    @staticmethod
    def check_log_in_state(chromedriver: webdriver):
        logger.info("Checking login state for Google, Facebook and Apple")
        google_logged_in, facebook_logged_in, apple_logged_in, login_count = False, False, False, 0
        logger.info("Checking Google")
        chromedriver.get(ProcessHelper.google_check_url)
        code = ProcessHelper.get_status_code_for_requested_site(chromedriver, ProcessHelper.google_check_url, False)
        google_logged_in = 200 <= code < 300
        if google_logged_in:
            login_count += 1
        del chromedriver.requests
        logger.info("Checking Facebook")
        chromedriver.get(ProcessHelper.facebook_check_url)
        code = ProcessHelper.get_status_code_for_requested_site(chromedriver, ProcessHelper.facebook_check_url, False)
        facebook_logged_in = 200 <= code < 300
        if facebook_logged_in:
            login_count += 1
        del chromedriver.requests
        logger.info("Checking Apple")
        chromedriver.get(ProcessHelper.apple_check_url)
        for cookie in chromedriver.get_cookies():
            if cookie['name'].startswith("DES"):
                apple_logged_in = True
                break
        if apple_logged_in:
            login_count += 1
        logger.info("Test of logged in site returned following results:")
        logger.info("Google: " + str(google_logged_in) + " | Facebook: " + str(facebook_logged_in) + " | Apple: " +
                    str(apple_logged_in))
        return login_count == 1

    @staticmethod
    def resolve_tld1(chromedriver: webdriver, https_tranco_domain: str) -> tuple:
        import tldextract
        from selenium.common.exceptions import WebDriverException

        # try with https first
        try:
            chromedriver.get(https_tranco_domain)
            status_code = ProcessHelper.get_status_code_for_requested_site(chromedriver, https_tranco_domain, True)
            logger.info(https_tranco_domain + " returned (after possible redirects) status code " + str(status_code))
            if not 200 <= status_code < 300:
                raise WebDriverException()
            resolved = tldextract.extract(chromedriver.current_url)
            resolved_url = chromedriver.current_url
            resolved_domain = '.'.join(resolved)  # foo.example.co.uk
            resolved_tld1 = resolved.registered_domain  # example.co.uk
            resolved_servicename = resolved.domain  # example
            return 'https', resolved_url, resolved_domain, resolved_tld1, resolved_servicename
        except WebDriverException:
            # fallback to http
            try:
                http_domain = https_tranco_domain.replace("https://", "http://")
                chromedriver.get(http_domain)
                status_code = ProcessHelper.get_status_code_for_requested_site(chromedriver, http_domain, True)
                logger.info(http_domain + " returned (after possible redirects) status code " + str(status_code))
                if not 200 <= status_code < 300:
                    return None
                resolved = tldextract.extract(chromedriver.current_url)
                resolved_url = chromedriver.current_url
                resolved_domain = '.'.join(resolved)
                resolved_tld1 = resolved.registered_domain
                resolved_servicename = resolved.domain
                return 'http', resolved_url, resolved_domain, resolved_tld1, resolved_servicename
            except WebDriverException:
                return None

    @staticmethod
    def get_status_code_for_requested_site(chromedriver: webdriver, site: str, follow_redirects: bool):
        site_found = False
        for request in chromedriver.requests:
            if request.url == site or request.url == site + "/":
                site_found = True
            if site_found and hasattr(request.response, "status_code") and (
                    300 <= request.response.status_code < 400 and follow_redirects):
                continue
            elif site_found and not hasattr(request.response, "status_code"):
                logger.warning("Looks like the request is running in endless mode or has canceled abnormally. "
                               "No status_code for response was found.")
                return -1
            elif site_found:
                return request.response.status_code
        logger.warning("Could not find request for site " + site + (
            ". Maybe http request was send but HSTS Header was set previously" if site.startswith(
                "http://") else ". Maybe connection was canceled"))
        return -1

    @staticmethod
    def quit_chromedriver_correctly(chromedriver: webdriver):
        import urllib3
        if hasattr(chromedriver, "killed"):
            logger.info("Quitting chromedriver not needed as it was already quit")
            return
        try:
            logger.info("Quitting chromedriver with " + str(len(chromedriver.window_handles)) + " windows")
            for handle in chromedriver.window_handles:
                chromedriver.switch_to.window(handle)
                chromedriver.close()
            chromedriver.quit()
            logger.info("Done")
            chromedriver.killed = True
        except urllib3.exceptions.MaxRetryError:
            logger.info("Looks like chromedriver was already closed (e.g. by interrupt signal)")
        except Exception as err:
            logger.error("Something went wrong quitting chromedriver!")
            logger.error(str(err.__class__) + str(err))

    @staticmethod
    def gen_filename_from_url(url):
        parsed_url = urlparse(url)
        url_filename = parsed_url.netloc.replace(".", "-")
        url_filename += parsed_url.path.replace("/", "-")
        return quote(url_filename)
