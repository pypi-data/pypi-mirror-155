from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import exceptions
from logmgmt import logger

startpage_url = "https://startpage.com/"
startpage_search_input_xpath = "/html/body/div[2]/section[1]/div[3]/div[2]/div/form/input[1]"
startpage_search_button_xpath = "/html/body/div[2]/section[1]/div[3]/div[2]/div/form/button[2]"
startpage_first_search_result_wo_did_you_mean_xpath = '/html/body/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/section[2]/div[%linknumber%]/div[1]/div[2]/a'
startpage_first_search_result_w_did_you_mean_xpath = '/html/body/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/section[3]/div[%linknumber%]/div[1]/div[2]/a'
startpage_did_you_mean_container_class = 'sp-gl__container'
startpage_family_filter_check_xpath = "/html/body/div[2]/div/div[2]/div[1]/div[1]/div/div/div/div/div[3]/div/form/button/span"
startpage_family_filter_button_xpath = "/html/body/div[2]/div/div[2]/div[1]/div[1]/div/div/div/div/div[3]/div/form/button"


class StartPageException(Exception):
    pass


def test_search(driver: WebDriver) -> bool:
    driver.get(startpage_url)
    try:
        search_input = driver.find_element(By.XPATH, startpage_search_input_xpath)
        search_term = "test"
        search_input.send_keys(search_term)
        driver.find_element(By.XPATH, startpage_search_button_xpath).click()
        el = driver.find_element(By.XPATH,
                                 startpage_first_search_result_wo_did_you_mean_xpath.replace("%linknumber%", "1"))
        return el is not None
    except NoSuchElementException:
        return False


def get_startpage_login_pages(driver, base_page, count_of_results=1, login_search_term="login", max_tries=3,
                              include_just_sub_domains=True) -> list:
    logger.info("Starting Startpage search")
    if count_of_results > 10:
        raise Exception("Maximum of 10 results is possible for startpage search!")
    search_term = base_page + " " + login_search_term
    if include_just_sub_domains:
        search_term += " site:" + base_page
    logger.info("Searching Startpage with term \"" + search_term + "\"")
    counter = 1
    while counter <= max_tries:
        counter += 1
        try:
            driver.get(startpage_url)
            search_input = driver.find_element(By.XPATH, startpage_search_input_xpath)
            search_input.send_keys(search_term)
            driver.find_element(By.XPATH, startpage_search_button_xpath).click()
            logger.info("Taking first " + str(count_of_results) + " result(s)")
            links = []
            links_counter = 0
            while links_counter < count_of_results:
                try:
                    did_you_mean_container_exists = False
                    try:
                        el = driver.find_element(By.CLASS_NAME, startpage_did_you_mean_container_class)
                        did_you_mean_container_exists = el is not None
                    except NoSuchElementException:
                        pass
                    xpath = startpage_first_search_result_w_did_you_mean_xpath if did_you_mean_container_exists else startpage_first_search_result_wo_did_you_mean_xpath
                    el = driver.find_element(By.XPATH, xpath.replace("%linknumber%", str(links_counter + 1)))
                    link = el.get_attribute("href")
                    links.append(link)
                    logger.info("Got " + link)
                except NoSuchElementException:
                    if links_counter == 0:
                        logger.info("Could not find any search result element.")
                        fel = driver.find_element(By.XPATH, startpage_family_filter_check_xpath)
                        class_attr = fel.get_attribute("class")
                        if class_attr is not None and 'active' in class_attr.split():
                            logger.info("Found active family search. Will retry with disabled")
                            driver.find_element(By.XPATH, startpage_family_filter_button_xpath).click()
                            links_counter = 0
                            continue
                        else:
                            logger.info("Family search was not the problem. Checking test search")
                            if not test_search(driver):
                                raise exceptions.StartPageHasChangedException()
                            logger.info("Looks like no links are found by Startpage for the original request.")
                            if counter <= max_tries:
                                logger.info("Retrying getting results")
                                raise exceptions.RetryException()
                            logger.info("Returning empty list")
                        return links
                    else:
                        return links
                links_counter += 1
            return links
        except NoSuchElementException:
            raise exceptions.StartPageHasChangedException()
        except WebDriverException as e:
            logger.error(e)
            logger.error("We got an unknown Webdriverexception. Please manage this!")
        except exceptions.StartPageHasChangedException as e:
            raise e
        except exceptions.RetryException:
            logger.info("Retrying (attempt: " + str(counter) + ")")
            continue
        except Exception as e:
            logger.error(e)
            logger.error("We got an unknown Exception. Please manage this!")

        if counter <= max_tries:
            logger.info("Retrying (attempt: " + str(counter) + ")")
            continue
    raise exceptions.StartPageHasChangedException()

# if __name__ == "__main__":
#    driver = DriverManager.generate_driver()
#    print(get_startpage_login_pages(driver, "google.com", count_of_results=3))
#    driver.quit()
