import time

from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains

from logmgmt import logger


class LocatorHelper:
    @staticmethod
    def current_url_excluded(driver, excluded_urls):
        url = driver.current_url.replace("www.", "").replace("http://", "").replace("https://", "")
        for text in excluded_urls:
            if url.startswith(text):
                return True
        return False

    @staticmethod
    def click_element_with_fallback_clicking_on_coordinates(driver, element):
        try:
            element.click()
        except (ElementNotInteractableException, ElementClickInterceptedException):
            logger.info("Element was not clickable. Trying to click on coordinates")
            action = ActionChains(driver)
            try:
                x = element.location['x']
                y = element.location['y']
                action.move_by_offset(x, y).click().move_by_offset(x * -1, y * -1).perform()
            except Exception:
                raise ElementNotInteractableException()

    @staticmethod
    def click_url_check_location(driver, element, valid_locations, must_have_text_parts):
        LocatorHelper.click_element_with_fallback_clicking_on_coordinates(driver, element)
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        valid_url_found = False,
        for valid_location in valid_locations:
            if driver.current_url.startswith(valid_location):
                valid_url_found = True, driver.current_url
                for must_have_option in must_have_text_parts:
                    # must_have_option is an array (e.g ["client_id", "app_id"]) for which at least one must exists
                    if not LocatorHelper.url_contains_any_text_of_options(driver.current_url, must_have_option):
                        valid_url_found = False,
                        break
                break
        while len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        return valid_url_found

    @staticmethod
    def url_contains_any_text_of_options(url, options):
        for option in options:
            if url.__contains__(option):
                return True
        return False

    @staticmethod
    def check_low_validity_elements(driver, low_validity_elements, valid_login_urls):
        pass
