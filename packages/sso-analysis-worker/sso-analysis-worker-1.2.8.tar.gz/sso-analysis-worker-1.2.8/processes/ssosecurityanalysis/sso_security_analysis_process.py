import json
import time
import urllib
from multiprocessing import Process
from time import sleep
from urllib.parse import urlparse, parse_qsl

from selenium.common.exceptions import TimeoutException, WebDriverException, MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains

from exceptions import SiteNotResolvableException, NoLoginCandidatesFoundException, ConfigInvalidException, \
    WebDriverInitialisationException
from logmgmt import logger
from model.backend_information import BackendInformation
from model.process_type import ProcessType
from model.ssodetection.sso_detection_strategy import SSODetectionStrategy
from processes import ProcessHelper
from processes.generic_process import GenericAnalysisProcess
from processes.ssolandscapeanalysis.locators.social_login_information import SocialLoginInformation
from processes.ssosecurityanalysis import png_helper
from services import RestClient, DriverManager


def scroll_to_position(driver, x: int, y: int) -> tuple:
    xOffset = driver.execute_script("return window.pageXOffset;")
    yOffset = driver.execute_script("return window.pageYOffset;")
    driver.execute_script("window.scrollBy(" + str(x - xOffset) + ", " + str(y - yOffset) + ");")
    xOffset = driver.execute_script("return window.pageXOffset;")
    yOffset = driver.execute_script("return window.pageYOffset;")
    return xOffset, yOffset


def get_auth_req(chromedriver, social_login_info_to_find):
    requests = chromedriver.requests
    counter = 0
    for request in requests:
        if "valid_login_urls_when_logged_in" in social_login_info_to_find:
            valid_login_urls = social_login_info_to_find["valid_login_urls_when_logged_in"]
        else:
            valid_login_urls = social_login_info_to_find["valid_login_urls"]
        if "invalid_paths_when_logged_in" in social_login_info_to_find:
            invalid_paths = social_login_info_to_find["invalid_paths_when_logged_in"]
        else:
            invalid_paths = []
        for valid_login_url in valid_login_urls:
            if request.url.startswith(valid_login_url):
                parsed_req = urlparse(request.url)
                if parsed_req.path in invalid_paths:
                    continue
                found_all = True
                for must_have_texts in social_login_info_to_find['must_have_texts_in_valid_login_urls']:
                    found = False
                    for must_have_text in must_have_texts:
                        if request.url.lower().__contains__(must_have_text):
                            found = True
                    if not found:
                        found_all = False
                if found_all:
                    if 'redirect_uri' in request.params:
                        return request, counter
        counter += 1
    counter = 0
    for request in requests:
        parsed = urlparse(request.url)
        if parsed.netloc == "malicious.com" and parsed.path == "/sso-in-the-wild":
            if len(request.body) == 0:
                continue
            json_obj = json.loads(request.body.decode('utf8'))
            for valid_login_url in social_login_info_to_find["valid_login_urls"]:
                if "documentLocation" in json_obj and json_obj["documentLocation"]["href"].startswith(
                        valid_login_url):
                    found_all = True
                    for must_have_texts in social_login_info_to_find['must_have_texts_in_valid_login_urls']:
                        found = False
                        for must_have_text in must_have_texts:
                            if json_obj["documentLocation"]["href"].__contains__(must_have_text):
                                found = True
                        if not found:
                            found_all = False
                    if found_all:
                        return request, counter
        counter += 1
    return None


def get_auth_resp(chromedriver, tuple_url_and_counter):
    auth_req = tuple_url_and_counter[0]
    parsed_auth_req = urlparse(auth_req.url)
    counter_req = tuple_url_and_counter[1]
    counter = 0
    has_redirect_req = 'redirect_uri' in auth_req.params
    postmessage_req = parsed_auth_req.netloc == "malicious.com"
    storagerelay = parsed_auth_req.query.lower().__contains__("redirect_uri=storagerelay")
    staticxx_facebook = 'redirect_uri' in auth_req.params and auth_req.params['redirect_uri'].startswith(
        "https://staticxx.facebook.com/x/connect/xd_arbiter")
    web_message_request = 'response_mode' in auth_req.params and auth_req.params[
        'response_mode'].lower() == "web_message"
    form_post_request = 'response_mode' in auth_req.params and auth_req.params['response_mode'].lower() == "form_post"
    for request in chromedriver.requests:
        parsed_req = urlparse(request.url)
        if counter < counter_req:
            counter += 1
            continue
        postmessage_res = parsed_req.netloc == "malicious.com"
        has_location_header_res = request.response is not None and 'location' in request.response.headers
        fragment_mock_request = request.url.startswith("https://pocs.work")
        if postmessage_req and postmessage_res:
            try:
                json_obj = json.loads(request.body.decode('utf8'))
                auth_req_json_obj = json.loads(auth_req.body.decode("utf8"))
                if json_obj["origin"] == auth_req_json_obj["documentLocation"]["origin"] and "type" in json_obj[
                    "data"] and json_obj["data"]["type"].lower() == "response":
                    return request
            except Exception:
                # Nothing to do --> wrong message format
                pass
        elif storagerelay and postmessage_res:
            if len(request.body) > 0:
                try:
                    json_obj = json.loads(request.body.decode('utf8'))
                    d = json.loads(json_obj['data'])['result']
                    if "code" in d or "access_token" in d or "id_token" in d:
                        return request
                except Exception:
                    # Nothing to do --> wrong message format
                    pass
        elif staticxx_facebook and postmessage_res:
            try:
                tuples = parse_qsl(json.loads(request.body)['data'])
                for t in tuples:
                    if t[0].lower() == "code" or t[0].lower() == 'access_token' or t[0].lower() == 'id_token':
                        return request
            except Exception:
                # Nothing to do --> wrong message format
                pass
        elif web_message_request and postmessage_res:
            try:
                data = json.loads(json.loads(request.body)['data'])['data']['authorization']
                if 'code' in data or 'access_token' in data or 'id_token' in data:
                    return request
            except Exception:
                # Nothing to do --> wrong message format
                pass
        elif has_redirect_req:
            u = request.url
            decoded_body = None
            if fragment_mock_request:
                frag_url = urllib.parse.unquote(request.params["oreq"])
                if ProcessHelper.find_redirect_uri_in_request(frag_url, request.params["oreq"]):
                    return request
            if form_post_request and len(request.body) > 0:
                try:
                    decoded_body = request.body.decode("utf-8")
                except Exception:
                    # Nothing to do --> wrong message format
                    pass
            if ProcessHelper.find_redirect_uri_in_request(u, auth_req.params['redirect_uri'], decoded_body):
                return request
            if has_location_header_res and ProcessHelper.find_redirect_uri_in_request(
                    request.response.headers['location'], auth_req.params['redirect_uri']):
                return request


def check_login_successfully(chromedriver, social_login_info_to_find):
    auth_req = get_auth_req(chromedriver, social_login_info_to_find)
    if auth_req is None:
        return False, None, None
    if "auth_type" in auth_req[0].params.keys():
        if auth_req[0].params['auth_type'] == "reauthenticate":
            logger.info("Found a auth. request which needs reauthentication. Will resend it without this parameter")
            chromedriver.get(auth_req[0].url.replace('auth_type', 'disabled_parameter'))
            sleep(20)
    if urlparse(auth_req[0].url).netloc == "malicious.com":
        return_req = auth_req[0].body.decode("utf8")
    else:
        return_req = auth_req[0].url
    auth_res = get_auth_resp(chromedriver, auth_req)
    if auth_res is None:
        return False, return_req, None
    if urlparse(auth_res.url).netloc == "malicious.com":
        return_res = auth_res.body.decode("utf8")
    elif 'response_mode' in auth_req[0].params and auth_req[0].params['response_mode'].lower() == "form_post" and len(
            auth_res.body) > 0:
        try:
            return_res = auth_res.body.decode("utf-8")
        except Exception:
            return_res = auth_res.url
    elif auth_req is not None and 'location' in auth_req[0].response.headers and (
            auth_req[0].response.headers['location'].__contains__("code") or auth_req[0].response.headers[
        'location'].__contains__("access_token") or auth_req[0].response.headers['location'].__contains__("id_token")):
        return_res = auth_req[0].response.headers['location']
    elif auth_res.url.startswith("https://pocs.work"):
        return_res = auth_res.params['oreq']
    else:
        return_res = auth_res.url
    return True, return_req, return_res


def wait_for_result(chromedriver, social_login_info, timeout: int = 30):
    start_time = time.time()
    result = check_login_successfully(chromedriver, social_login_info)
    while result[0] is False and time.time() - start_time < timeout:
        sleep(5)
        result = check_login_successfully(chromedriver, social_login_info)
    return result


def handle_result_found(result, rest_client, analysis_run_id, sso_detection_index, screen, har):
    rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 90,
                                                                "Uploading results")
    logger.info("Found login:")
    logger.info((result[1], result[2]))
    logger.info("Saving results")
    if rest_client.save_sso_security_analysis(analysis_run_id, sso_detection_index, (result[1], result[2]), screen,
                                              har):
        return True
    else:
        logger.error("Could not save results after successfully found authRes and authResp")
        return False


def process_function(sso_detection, backend_info: BackendInformation, analysis_run_id: int,
                     config_directory):
    success = False
    rest_client = RestClient(backend_info.host, backend_info.port, backend_info.token)
    chromedriver = None
    cause = "Unknown"
    try:
        sso_detection_index = sso_detection['index']
        sso_detection_strategy = SSODetectionStrategy[sso_detection['detectionStrategy']]
        finding_url = sso_detection['findingPage']
        element_x = sso_detection['elementLocationX']
        element_y = sso_detection['elementLocationY']
        element_width = sso_detection['elementWidth']
        element_height = sso_detection['elementHeight']
        offset = (0, 0)
        sso_provider_name = sso_detection['ssoProvider']['providerName'].title()
        logger.info("Got " + finding_url + " to analyse sso security for provider " + sso_provider_name)
        social_login_info = SocialLoginInformation[sso_provider_name]
        logger.info("Starting chromedriver")
        rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 0,
                                                                    "Preparing analysis")
        chromedriver = DriverManager.generate_driver(config_directory, allow_running_insecure_content=True,
                                                     remove_response_csp_headers=True)
        chromedriver.execute_cdp_cmd('Network.setBlockedURLs',
                                     {"urls": social_login_info['block_requests_if_logged_in']})
        chromedriver.execute_cdp_cmd('Network.enable', {})

        logger.info("Checking login state")
        rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 5,
                                                                    "Checking profile")
        if not ProcessHelper().check_log_in_state(chromedriver):
            raise ConfigInvalidException()
        logger.info("Opening finding page")
        rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 10,
                                                                    "Opening finding page " + finding_url)
        chromedriver.get(finding_url)
        if chromedriver.get_window_size()['width'] < element_x or chromedriver.get_window_size()['height'] < element_y:
            offset = scroll_to_position(chromedriver, element_x, element_y)
            element_x -= offset[0]
            element_y -= offset[1]
        rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 15,
                                                                    "Taking screenshot of " + finding_url)
        logger.info("Taking screenshot")
        sleep(10)
        screen = chromedriver.get_screenshot_as_png()
        screen = png_helper.draw_circle_at_position(screen, element_x, element_y, color="green")
        rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 20,
                                                                    "Pressing element coordinates")
        logger.info("Pressing coordinates")
        action = ActionChains(chromedriver)
        try:
            action.move_by_offset(element_x, element_y).click().move_by_offset(element_x * -1, element_y * -1).perform()
            logger.info("Waiting for login finished")
            rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 25,
                                                                        "Waiting for finished login after pressing element coordinates")
            sleep(1)
            result = wait_for_result(chromedriver, social_login_info)
            if result[0]:
                success = handle_result_found(result, rest_client, analysis_run_id, sso_detection_index, screen,
                                              chromedriver.har)
                return
        except MoveTargetOutOfBoundsException:
            logger.warn(
                "Looks like original coordinates are no longer valid for the current login page. Will use fallback")
            element_width = None
            element_height = None
        error_screen = chromedriver.get_screenshot_as_png()
        if element_width is not None and element_height is not None:
            logger.info("Pressing at coordinates did not get a valid result. Trying to press in center of element")
            rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 30,
                                                                        "Pressing element's center")
            chromedriver.get(finding_url)
            sleep(10)
            newx = element_x + element_width / 2
            newy = element_y + element_height / 2
            screen = png_helper.draw_circle_at_position(screen, newx, newy, color="yellow")
            action.move_by_offset(newx, newy).click().move_by_offset(newx * -1, newy * -1).perform()
            logger.info("Waiting for login finished")
            rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 35,
                                                                        "Waiting for finished login after pressing element's center")
            result = wait_for_result(chromedriver, social_login_info)
            if result[0]:
                success = handle_result_found(result, rest_client, analysis_run_id, sso_detection_index, screen,
                                              chromedriver.har)
                return
        if sso_detection_strategy == SSODetectionStrategy.IMAGE_ANALYSIS or sso_detection_strategy == SSODetectionStrategy.ELEMENT_SEARCH:
            logger.info("Nothing found! Falling back to pressing around the coordinates")
            rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 40,
                                                                        "Fallback pressing around the elements location")
            result = False,
            trips = 0
            colors = ["orange", "brown", "red", "purple"]
            while trips < 4:
                if trips == 0:
                    element_y += 20
                if trips == 1 or trips == 3:
                    element_x += 10
                if trips == 2:
                    element_y += 10
                screen = png_helper.draw_circle_at_position(screen, element_x, element_y, color=colors[trips])
                trips += 1
                action.move_by_offset(element_x, element_y).click().move_by_offset(element_x * -1,
                                                                                   element_y * -1).perform()
                logger.info(
                    "Waiting for login finished at positions down and right to original coordinates (round " + str(
                        trips) + ")")
                rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index,
                                                                            40 + (trips * 5),
                                                                            "Waiting for finished login after pressing around the elements location (" + str(
                                                                                trips) + "/4)")
                result = wait_for_result(chromedriver, social_login_info)
                if result[0]:
                    success = handle_result_found(result, rest_client, analysis_run_id, sso_detection_index, screen,
                                                  chromedriver.har)
                    return
        if sso_detection_strategy == SSODetectionStrategy.ELEMENT_SEARCH:
            from processes import SSODetectionService
            from model.login_path_information import LoginPathInformation
            from model.page_information import PageInformation
            logger.info("Nothing found! Falling back to identify login element")
            rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 65,
                                                                        "Preparing fallback identification for sso element")
            chromedriver.get(finding_url)
            service = SSODetectionService(rest_client.get_known_sso_provider())
            page = PageInformation(sso_detection['page']['index'], sso_detection['page']['basePage'])
            mock_latest_login_info = LoginPathInformation(page, -1, sso_detection['findingPage'], [], True, False, None)

            def progress_callback(step: int, max: int, status: str):
                rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index,
                                                                            int(65 + (20 * (step / max))), status)

            def special_check(d):
                return wait_for_result(d, social_login_info, 15)[0]

            run_google = social_login_info['name'] == "Google"
            run_facebook = social_login_info['name'] == "Facebook"
            run_apple = social_login_info['name'] == 'Apple'
            if not run_google and not run_facebook and not run_apple:
                logger.error("Something went wrong when falling back to element location! Neither google, facebook"
                             ", nor apple were requested")
            rawres = service.automatic_sso_detection(chromedriver, mock_latest_login_info, progress_callback,
                                                     run_google, run_facebook, run_apple, special_check)[0]
            result = wait_for_result(chromedriver, social_login_info)
            if result[0] is True:
                logger.info("Fallback located element successfully, saving results")
                rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 90,
                                                                            "Uploading results")
                screen = png_helper.draw_rectangle_at_position(screen, rawres[1]['x'] - offset[0],
                                                               rawres[1]['y'] - offset[1], rawres[2]['width'],
                                                               rawres[2]['height'])
                logger.info(result)
                rest_client.save_sso_security_analysis(analysis_run_id, sso_detection_index, (result[1], result[2]),
                                                       screen, chromedriver.har)
                return
        logger.warning("Fallback also did not find valid login button. Saving as error")
        rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 90,
                                                                    "Uploading failed analysis data")
        rest_client.save_sso_security_analysis(analysis_run_id, sso_detection_index, (result[1], result[2]),
                                               screen, chromedriver.har, False, "Did not find auth req and res",
                                               error_screenshot=error_screen)


    except TimeoutException as err:
        cause = "Timout: " + err.__class__.__name__
        logger.error("Timeout reached: " + err.msg)
    except SiteNotResolvableException:
        cause = "Not resolvable"
        logger.error("Could not resolve site!")
    except NoLoginCandidatesFoundException:
        cause = "No login candidates found"
        logger.error("Could not find any login candidates for site")
    except WebDriverException as err:
        cause = "Webdriver problem: " + err.__class__.__name__
        logger.error("Could not finish analysing (" + err.msg + ")!")
    except ConfigInvalidException:
        cause = "Invalid config"
        if rest_client.unregister_page_in_work(analysis_run_id, sso_detection['index']):
            logger.error("Unregistered page at brain.")
            success = True
        else:
            logger.error("Failed unregistering page at brain")
        exit(70)
    except KeyboardInterrupt as err:
        logger.info("Received interrupt. Will deregister current page:")
        logger.info("Done") if rest_client.unregister_currently_in_work_sso_det(analysis_run_id, sso_detection[
            'index']) else logger.error("Failed!")
        success = True
        raise err
    except WebDriverInitialisationException as e:
        logger.error(e)
        logger.error(
            "Webdriver could not be initialized (" + e.thrown_exception.__class__.__name__ + "). This client looks broken. Exit with error code")
        try:
            rest_client.unregister_currently_in_work_sso_det(analysis_run_id, sso_detection['index'])
            rest_client.update_latest_activity("ERROR!")
        except Exception as err:
            logger.error("Could not unregister sso detection and send ERROR status to brain: " +
                         str(err.__class__.__name__) + ": " + str(err))
            pass
        exit(75)
    except Exception as err:
        cause = "Unknown error: " + err.__class__.__name__
        logger.error("Unknown error! This should be managed explicitly " +
                     str(err.__class__.__name__) + ": " + str(err))
    finally:
        if not success:
            try:
                rest_client.unregister_currently_in_work_sso_det_and_block(analysis_run_id, sso_detection['index'],
                                                                           cause)
            except Exception:
                logger.error("Unregistering page at brain did fail!")
        if chromedriver is not None:
            ProcessHelper.quit_chromedriver_correctly(chromedriver)
            del chromedriver.requests, chromedriver


class SSOSecurityProcess(GenericAnalysisProcess):

    def prepare(self):
        ProcessHelper.check_for_unfinished_work(self.rest_client)

    def get_next_object_to_analyse(self):
        return self.rest_client.get_next_sso_detection_for_security_analysis_for_run(self.analysis_run_id)

    def generate_process(self, object_to_analyse) -> Process:
        return Process(target=process_function,
                       args=(object_to_analyse, self.backend_info, self.analysis_run_id, self.config_directory))

    def __init__(self, backend_info: BackendInformation, analysis_run_id: int, process_type: ProcessType,
                 config_directory):
        if process_type is not ProcessType.SSO_SECURITY_ANALYSIS:
            raise TypeError(str(process_type) + " is not supported for sso security analyses")
        self.backend_info = backend_info
        self.rest_client = RestClient(backend_info.host, backend_info.port, backend_info.token)
        self.analysis_run_id = analysis_run_id
        self.process_type = process_type
        self.config_directory = config_directory
