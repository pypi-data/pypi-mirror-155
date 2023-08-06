from selenium.common.exceptions import WebDriverException, NoSuchElementException, ElementNotInteractableException

from logmgmt import logger
from exceptions import ResetProcessException
from input.input_management import InputManager
from model.locateloginpages.finding_strategy import FindingStrategy
from processes.ssolandscapeanalysis import duck_duck_go_search
from services.driver_manager import DriverManager
from services.rest_client import RestClient
from services.xpath_manager import XPathManager


class LocateLoginPage:

    def __init__(self, backend_info, chromedriver=None, good_luck_search_terms=None):
        if chromedriver is None:
            chromedriver = DriverManager.generate_driver()
            self.close_on_end = True
        else:
            del chromedriver.requests
            self.close_on_end = False
        if good_luck_search_terms is None:
            good_luck_search_terms = ["login", "signin"]
        self.driver = chromedriver
        self.good_luck_search_terms = good_luck_search_terms
        self.rest_client = RestClient(backend_info.host, backend_info.port, backend_info.token)

    def gather_additional_steps_for_login_page(self, login_page):
        self.driver.get(login_page)
        seeLoginPage = InputManager.get_input_with_specific_answer_values("Do you see the login page? ", ["y", "n"])
        if seeLoginPage == "y":
            return []
        gathered_steps = []
        user_input_value = input(
            "Which steps are necessary (will be executed by chrome driver)\n"
            "[(text:)<text>, <attribute>:<value>, @cookie name value, @wait seconds]. "
            "If finished type in :finished. If you want to regather the loginpage type :reset. ")
        while user_input_value != ":finished":
            try:
                if not InputManager.input_valid_additional_step_type(user_input_value):
                    user_input_value = input("Invalid Input! Try again: ")
                    continue
                if user_input_value.startswith("@cookie"):
                    DriverManager.set_cookie(self.driver, user_input_value.split(" ")[1],
                                             user_input_value.split(" ")[2])
                elif user_input_value.startswith("@wait"):
                    try:
                        logger.info("When performing the steps to show login page, the process will sleep for " + str(
                            int(user_input_value.split(" ")[1])) + " seconds")
                    except ValueError:
                        user_input_value = input("Invalid Input! Try again: ")
                        continue
                elif user_input_value == ":clearsteps":
                    gathered_steps.clear()
                    self.driver.get(login_page)
                    logger.info("Cleared all recorded steps. You can now start again")
                    user_input_value = input(
                        "Which steps are necessary (will be executed by chrome driver)\n"
                        "[(text:)<text>, <attribute>:<value>, @cookie name value, @wait seconds]. "
                        "If finished type in :finished. ")
                    continue
                elif user_input_value == ":reset":
                    raise ResetProcessException()
                else:
                    DriverManager.execute_driver_step(self.driver,
                                                      XPathManager.get_xpath_for_input_type(user_input_value))
                gathered_steps.append(user_input_value)
                user_input_value = input(
                    "Step recorded. What to do next? [(text:)<text>, id:<id>, :clearsteps, :finished] ")
            except ResetProcessException as e:
                raise e
            except NoSuchElementException:
                user_input_value = input("Could not find el for " + user_input_value + ". Please try again")
            except ElementNotInteractableException:
                user_input_value = input("The element you chose is not intractable. Please try again or use id instead")
            except Exception as err:
                logger.error("We ran into trouble")
                logger.error(err)
                user_input_value = input(
                    "Please try again. What to do next? [(text:)<text>, id:<id>, :clearsteps, :finished] ")
        logger.info("We will save the following steps to reach the login:")
        for s in gathered_steps:
            logger.info(s)
        return gathered_steps

    def gather_login_page_location(self, base_page, start_with_good_luck_search=True):
        if start_with_good_luck_search:
            logger.info("We will try to find the login page for " + base_page + " with google's good luck search")
        else:
            logger.info("Calling the base_page " + base_page + " to start check for login")
        logger.info("- You can try different search terms by just pressing enter (login, signin, ...)")
        logger.info("- When the login page where the login is located type \"f\" and press enter")
        logger.info("- When the login page already is shown (no additional steps needed) you can shortcut the next "
                     "step by typing \"ff\"")
        logger.info("- When you want to insert the login url manually type \"manual\"")
        logger.info("- When the website is broken type \"broken\"")
        logger.info("- When the website does not have a login type 'nologin'")
        logger.info("- When you want to get to the start page type \"base\"")
        logger.info("- For skipping type \"skip\"")
        gathered = False

        good_luck_search_terms_counter = 0
        try:
            if start_with_good_luck_search:
                self.driver.get(duck_duck_go_search.get_duckduckgo_login_pages(self.driver, base_page,
                                                                               self.good_luck_search_terms[
                                                                                   good_luck_search_terms_counter]))
                good_luck_search_terms_counter += 1
            else:
                self.driver.set_page_load_timeout(10)
                self.driver.get(base_page)
                self.driver.set_page_load_timeout(300)
        except WebDriverException as error:
            self.manage_webdriver_exception_insert_as_broke(error, base_page)
            return
        while not gathered:
            inp = InputManager.get_input_with_specific_answer_values("Input: ",
                                                                     ('f', 'ff', '', 'GL', 'manual', 'broken',
                                                                      'nologin', 'base', 'skip'))

            if inp == "" or inp == "GL":
                if good_luck_search_terms_counter >= len(self.good_luck_search_terms):
                    if inp == "GL":
                        good_luck_search_terms_counter = 0
                    else:
                        logger.info(
                            "Sorry, we have no more good luck search terms. Please try to locate the page manually. "
                            "If you want to get to the base page type \"base\". "
                            "If you want to restart GL search, type \"GL\"")
                if good_luck_search_terms_counter < len(self.good_luck_search_terms):
                    self.driver.get(
                        duck_duck_go_search.get_duckduckgo_login_pages(self.driver, base_page,
                                                                       self.good_luck_search_terms[
                                                                           good_luck_search_terms_counter]))
                    good_luck_search_terms_counter += 1
            elif inp == "base":
                try:
                    self.driver.set_page_load_timeout(10)
                    self.driver.get(base_page)
                    self.driver.set_page_load_timeout(300)
                except WebDriverException as error:
                    self.driver.set_page_load_timeout(300)
                    self.manage_webdriver_exception_insert_as_broke(error, base_page)
                    return
            elif inp == "broken":
                self.rest_client.save_login_page_location(base_page, None, None, None, True, FindingStrategy.NONE, None)
                gathered = True
            elif inp == "nologin":
                self.rest_client.save_login_page_location(base_page, None, False, None, False, FindingStrategy.MANUAL,
                                                          self.driver.har)
                gathered = True
            elif inp == "manual":
                try:
                    manual_url = input(
                        "Please type in the manual URL (the inputted url will be saved NOT the target url "
                        "which was reached by redirects or similar automatic actions): ")
                    self.driver.get(manual_url)
                    if InputManager.get_input_with_specific_answer_values("Is the correct login page shown?",
                                                                          ['y', 'n'],
                                                                          case_sensitive=False) == 'y':
                        try:
                            self.rest_client.save_login_page_location(base_page, manual_url, True,
                                                                      self.gather_additional_steps_for_login_page(
                                                                          manual_url), False, FindingStrategy.MANUAL,
                                                                      self.driver.har)
                        except ResetProcessException:
                            logger.info("Reset done!")
                            continue
                        gathered = True
                except WebDriverException as error:
                    logger.error("Something went wrong, please retry... (" + error.msg + ")")
                    continue
            elif inp == "f" or inp == "ff":
                if self.driver.current_window_handle != self.driver.window_handles[len(self.driver.window_handles) - 1]:
                    self.driver.switch_to.window(self.driver.window_handles[len(self.driver.window_handles) - 1])
                login_page = self.driver.current_url
                additional_steps = []
                if inp == "f":
                    try:
                        additional_steps = self.gather_additional_steps_for_login_page(self.driver.current_url)
                    except ResetProcessException:
                        logger.info("Reset done!")
                        continue
                strat = FindingStrategy.MANUAL
                if InputManager.get_input_with_specific_answer_values(
                        "Did googles good luck search find the login page?", ['y', 'n']) == 'y':
                    if len(additional_steps) > 0:
                        strat = FindingStrategy.GOOD_LUCK_EXTRA_STEPS
                    else:
                        strat = FindingStrategy.GOOD_LUCK_AUTOMATIC
                self.rest_client.save_login_page_location(base_page, login_page, True, additional_steps, False, strat,
                                                          self.driver.har)
                while len(self.driver.window_handles) > 1:
                    self.driver.switch_to.window(self.driver.window_handles[len(self.driver.window_handles) - 1])
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                gathered = True
            elif inp == "skip":
                self.rest_client.unregister_page_in_work_and_block_for_time(-1, base_page)
                return

    def manage_webdriver_exception_insert_as_broke(self, thrown_err, base_page):
        logger.error("Got an webdriver exception")
        logger.error(thrown_err.msg)
        inp = InputManager.get_input_with_specific_answer_values("Insert this page as broken into database?",
                                                                 ["y", "n"])
        if inp == "y":
            self.rest_client.save_login_page_location(base_page, None, None, None, True, FindingStrategy.NONE, None)
        else:
            self.rest_client.unregister_page_in_work_and_block_for_time(-1, base_page)

    def start_process_tranco_list(self, tranco_lower_bound, tranco_upper_bound, renew_req=False,
                                  retest_broken=False):

        counter = 0
        while (site := self.get_next_page_for_process(tranco_lower_bound, tranco_upper_bound, renew_req,
                                                      retest_broken)) is not None:
            try:
                counter += 1
                del self.driver.requests
                logger.info("Counter: " + str(counter) + "/" + str(tranco_upper_bound - tranco_lower_bound + 1) +
                             " | TrancoID: " + self.rest_client.get_tranco_id_for_site(site.base_page))
                sites_info_raw = site.base_page.replace("\n", "")
                if not sites_info_raw.startswith("https://") and not sites_info_raw.startswith("http://"):
                    sites_info_raw = "https://" + sites_info_raw
                login_path_information = self.rest_client.get_latest_login_location_for_page(sites_info_raw)
                if login_path_information is None:
                    self.gather_login_page_location(sites_info_raw)
                if login_path_information is not None and (renew_req or retest_broken):
                    logger.info("Found site with specific request to renew information")
                    self.gather_login_page_location(sites_info_raw, start_with_good_luck_search=not retest_broken)
            except WebDriverException as err:
                logger.error(err)
                input("What should we do (with the drunken sailors)")
            except KeyboardInterrupt as err:
                logger.info("Received interrupt. Will deregister current page:")
                logger.info("Done") if self.rest_client.unregister_page_in_work(-1, site.base_page) else logger.error(
                    "Failed!")
                raise err
        logger.info("No more sites to analyse.")
        self.finish()
        logger.info("Bye!")

    def finish(self):
        try:
            if self.close_on_end:
                self.driver.quit()
        except WebDriverException:
            pass

    def get_next_page_for_process(self, tranco_lower_bound, tranco_upper_bound, renew_req, retest_broken):
        if renew_req:
            return self.rest_client.get_next_login_path_detection_to_renew()
        elif retest_broken:
            return self.rest_client.get_next_broken_path_detection_to_renew()
        else:
            return self.rest_client.get_next_page_of_tranco_domains_with_no_login_path_detection(tranco_lower_bound,
                                                                                                 tranco_upper_bound)
