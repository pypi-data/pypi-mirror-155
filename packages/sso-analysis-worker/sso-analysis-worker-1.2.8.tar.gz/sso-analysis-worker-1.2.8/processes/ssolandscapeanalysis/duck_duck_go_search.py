from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import exceptions
from logmgmt import logger

duckduckgo_url = "https://duckduckgo.com/?q="
xpath = '//*[@id="r1-%linknumber%"]/div/div[1]/a'


def test_search(driver: WebDriver) -> bool:
    driver.get(duckduckgo_url + "+test")
    try:
        el = driver.find_element(By.XPATH, xpath.replace("%linknumber%", "0"))
        return el is not None
    except NoSuchElementException:
        return False


def get_duckduckgo_login_pages(driver: WebDriver, base_page, count_of_results=1, login_search_term="login",
                               max_tries=3, include_just_sub_domains=True) -> list:
    logger.info("Starting DuckDuckGo search")
    if count_of_results > 10:
        raise Exception("Maximum of 10 results is possible for duckduckgo search!")
    search_term = base_page + "+" + login_search_term
    if include_just_sub_domains:
        search_term += "+site:" + base_page
    logger.info("Searching DuckDuckGo with term \"" + search_term + "\"")
    url = duckduckgo_url + search_term
    counter = 1
    while counter <= max_tries:
        counter += 1
        try:
            driver.get(url)
            logger.info("Taking first " + str(count_of_results) + " result(s)")
            links = []
            links_counter = 0
            while links_counter < count_of_results:
                try:
                    el = driver.find_element(By.XPATH, xpath.replace("%linknumber%", str(links_counter)))
                    link = el.get_attribute("href")
                    links.append(link)
                    logger.info("Got " + link)
                except NoSuchElementException:
                    el = None
                if el is None:
                    if links_counter == 0:
                        logger.warning("We could not find first link of DuckDuckGos search results! "
                                       "Checking if test search is working!")
                        if not test_search(driver):
                            raise exceptions.DuckDuckGoHasChangedException()
                        logger.info("Looks like no links are found by DuckDuckGo for the original request.")
                        if counter <= max_tries:
                            logger.info("Retrying getting results")
                            raise exceptions.RetryException()
                        logger.info("Returning empty list")
                        return links
                    return links
                links_counter += 1
            return links
        except WebDriverException as e:
            logger.error(e)
            logger.error("We got an unknown Webdriverexception.")
        except exceptions.DuckDuckGoHasChangedException as e:
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
    raise exceptions.DuckDuckGoHasChangedException()

# if __name__ == "__main__":
#    driver = DriverManager.generate_driver()
#    print(get_duckduckgo_login_pages(driver, "google.com", count_of_results=3))
#    driver.quit()
