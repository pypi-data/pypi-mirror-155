from time import sleep

from selenium.common.exceptions import NoSuchElementException, WebDriverException, ElementNotInteractableException, \
    ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from exceptions import ManualAnalysisNeededException
from logmgmt import logger
from model.ssodetection.sso_detection_strategy import SSODetectionStrategy
from processes.ssolandscapeanalysis.locators.generic_text_locator import GenericTextLocator
from processes.ssolandscapeanalysis.locators.locator_helper import LocatorHelper
from services.driver_manager import DriverManager


class SocialLoginLocator:
    def __init__(self, social_login_text, exclude_urls_starts_with, valid_login_urls,
                 must_have_texts_in_valid_login_urls, extra_texts):
        self.exclude_urls_starts_with = exclude_urls_starts_with

        self.extra_texts = extra_texts
        self.valid_login_urls = valid_login_urls
        self.must_have_texts_in_valid_login_urls = must_have_texts_in_valid_login_urls
        self.text_locator = GenericTextLocator(social_login_text, extra_texts)
        self.additional_xpath_searches_for_high_valid_found = []

    def add_xpath_for_high_valid_found_elements(self, xpath_text):
        self.additional_xpath_searches_for_high_valid_found.append(xpath_text)

    def reload_elements(self, driver, item, current_elements, high_validity):
        from services.driver_manager import DriverManager
        DriverManager.prepare_webpage_with_steps_to_reproduce(driver, item)
        sleep(5)
        logger.info("Site reloaded, elements must be reloaded!")
        if not high_validity:
            new_elements = self.text_locator.locate_low_validity_elements(driver)
        else:
            new_elements = self.text_locator.locate_high_validity(driver)
        if len(new_elements) != len(current_elements):
            logger.warning("Count of elements changed. Taking new size as max")
        return new_elements

    def locate_login(self, driver, item, special_check: callable = None) -> tuple:
        if LocatorHelper.current_url_excluded(driver, self.exclude_urls_starts_with):
            return False,
        high_validity_elements = self.text_locator.locate_high_validity(driver)
        if len(high_validity_elements) > 0:
            check = self.check_found_elements(driver, high_validity_elements, item, True, special_check)
            if check[0]:
                return check
        for xpath in self.additional_xpath_searches_for_high_valid_found:
            try:
                el = driver.find_element(By.XPATH, xpath)
                if el is not None:
                    check = self.check_found_elements(driver, [el], item, True, special_check)
                    if check[0]:
                        return check
            except NoSuchElementException:
                pass
        sleep(5)
        low_validity_elements = self.text_locator.locate_low_validity_elements(driver)
        if len(low_validity_elements) > 0:
            return self.check_found_elements(driver, low_validity_elements, item, False, special_check)
        return False,

    def check_found_elements(self, driver, elements, item, high_validity, special_check: callable = None) -> tuple:
        base_url_checks = driver.current_url
        logger.info("Possible elements found. Will test them (" + str(len(elements)) + ")")
        counter = 0
        stale_element_reference_execption_thrown = False
        while counter < len(elements):
            logger.info("Checking element #" + str(counter + 1) + " from " + str(len(elements)))
            try:
                element_coordinates = elements[counter].location
                element_size = elements[counter].size
                if special_check is None:
                    element_found = LocatorHelper.click_url_check_location(driver, elements[
                        counter], self.valid_login_urls, self.must_have_texts_in_valid_login_urls)
                else:
                    LocatorHelper.click_element_with_fallback_clicking_on_coordinates(driver, elements[counter])
                    element_found = special_check(driver)
            except (ElementNotInteractableException, ElementClickInterceptedException):
                logger.warning("Element was still not clickable!")
                counter += 1
                continue
            except TimeoutException:
                logger.warning("Loading of element took too long!")
                counter += 1
                self.reload_elements(driver, item, elements, high_validity)
                continue
            except StaleElementReferenceException:
                if not stale_element_reference_execption_thrown:
                    logger.info("Site seems to have changed without url changed. Reloading elements and try again...")
                    stale_element_reference_execption_thrown = True
                    elements = self.reload_elements(driver, item, elements, high_validity)
                    continue
                else:
                    logger.error("Reload did not work. Will not cancel but maybe we lost a valid element here")
                    counter += 1
                    continue
            except WebDriverException as err:
                logger.error(err.msg)
                raise ManualAnalysisNeededException(err.msg)
            if element_found[0]:
                logger.info("Found login redirect from low validity element! Reloading the page...")
                DriverManager.prepare_webpage_with_steps_to_reproduce(driver, item)
                return True, element_coordinates, element_size, SSODetectionStrategy.ELEMENT_SEARCH, element_found[1]
            if driver.current_url != base_url_checks:
                logger.info("Click changed base page. Must reload site..")
                elements = self.reload_elements(driver, item, elements, high_validity)
            counter += 1
            stale_element_reference_execption_thrown = False
        return False,
