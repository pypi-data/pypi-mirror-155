from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from logmgmt import logger
from services.xpath_manager import XPathManager


class GenericTextLocator:
    # Elements with attribute if checks should search for explicit match
    element_attributes_to_check_low_validity = [["title", False], ["aria-label", False], ["value", False],
                                                ["id", False], ["class", False], ["action", False], ["href", False]]
    element_attributes_to_check_high_validity = [["title", False], ["aria-label", False], ["value", False],
                                                 ["id", False]]

    def __init__(self, sso_name, extra_texts):
        self.sso_name = sso_name
        self.extra_texts = extra_texts
        self.org_button_texts = ["use %s", "sign up with %s", "sign in with %s", "sign in using %s", "log in with %s",
                                 "login with %s", "continue with %s", "connect with %s", "weiter mit %s",
                                 "mit %s fortfahren", "mit %s fortsetzen", "mit %s anmelden", "anmelden mit %s",
                                 "mit %s einloggen", "über %s fortfahren", "masuk dengan %s", "entrar com %s",
                                 "continuar com o %s", "daftar/masuk lewat %s", "使用 %s 登录"]

    def check_elements_text_contains_search_element(self, elements, search_elements, exact_match=False):
        counter = 0
        return_array = []
        if len(elements) > 100:
            logger.info("Running Text Search for " + str(len(elements)) + " objects")
        for element in elements:
            try:
                el_text = element.text
                counter += 1
                if counter % 100 == 0:
                    logger.info(str(counter))
                for text in search_elements:
                    if self.check_text_in_str(text.replace("%s", self.sso_name), el_text, exact_match):
                        return_array.append(element)
            except StaleElementReferenceException:
                pass
        return return_array

    def check_elements_attributes_contain_search_element(self, elements, search_elements, attributes):
        counter = 0
        return_array = []
        if len(elements) > 100:
            logger.info("Running Attribute Search for " + str(len(elements)) + " objects")
        for element in elements:
            counter += 1
            if counter % 100 == 0:
                logger.info(str(counter))
            try:
                for attribute in attributes:
                    el_atr = element.get_attribute(attribute[0])
                    for text in search_elements:
                        if self.check_text_in_str(text.replace("%s", self.sso_name), el_atr, attribute[1]):
                            return_array.append(element)
            except StaleElementReferenceException:
                pass
        return return_array

    @staticmethod
    def check_text_in_str(search_text, base_text, exact_match):
        if not base_text:
            return False
        if exact_match:
            return search_text.strip().lower() == base_text.strip().lower()
        return search_text.strip().lower() in base_text.strip().lower()

    def locate_high_validity(self, driver):
        return_list = []
        check_texts = self.org_button_texts
        for text in self.extra_texts:
            check_texts.append(text)
        try:
            logger.info("Check XPath")
            xpath = XPathManager.get_xpath_find_search_term_in_text_and_attributes(
                self.element_attributes_to_check_high_validity, check_texts)
            xpath = xpath.replace("%s", self.sso_name.lower())
            els = driver.find_elements(By.XPATH, xpath)
            for el in els:
                if el.tag_name != "script":
                    return_list.append(el)
            logger.info("Found " + str(len(return_list)) + " potential elements")
        except NoSuchElementException:
            pass
        try:
            logger.info("Checking buttons")
            # Stackoverflow has problems with generic text lookup --> searching buttons manually
            xpath = XPathManager.get_xpath_find_elment_with_text_and_attributes("button",
                                                                                self.element_attributes_to_check_high_validity,
                                                                                check_texts)
            buttons = driver.find_elements(By.XPATH, xpath.replace("%s", self.sso_name.lower()))
            duplicates = 0
            for el in buttons:
                if el not in return_list:
                    return_list.append(el)
                else:
                    duplicates += 1
            logger.info("Found " + str(len(buttons)) + " potential buttons (" + str(duplicates) + " duplicates)")
            # Traditional way
            # buttons = driver.find_elements(By.XPATH,
            #                               "//button")
            # logger.info("Found " + str(len(buttons)) + " buttons")
            # for button in self.check_elements_text_contains_search_element(buttons, check_texts):
            #    return_list.append(button)
            # for button in self.check_elements_attributes_contain_search_element(buttons, check_texts,
            #                                                                    self.element_attributes_to_check_high_validity):
            #    return_list.append(button)
        except NoSuchElementException:
            pass
        try:
            logger.info("Checking links")
            # Etsy has problems with generic text lookup --> searching links manually
            xpath = XPathManager.get_xpath_find_elment_with_text_and_attributes("a",
                                                                                self.element_attributes_to_check_high_validity,
                                                                                check_texts)
            links = driver.find_elements(By.XPATH, xpath.replace("%s", self.sso_name.lower()))
            duplicates = 0
            for el in links:
                if el not in return_list:
                    return_list.append(el)
                else:
                    duplicates += 1
            logger.info("Found " + str(len(links)) + " potential links (" + str(duplicates) + " duplicates)")
            # Traditional way
            # links = driver.find_elements(By.XPATH, "//a")
            # logger.info("Found " + str(len(links)) + " links")
            # for link in self.check_elements_text_contains_search_element(links, check_texts):
            #    return_list.append(link)
            # for link in self.check_elements_attributes_contain_search_element(links, check_texts,
            #                                                                  self.element_attributes_to_check_high_validity):
            #    return_list.append(link)
        except NoSuchElementException:
            pass
        return list(dict.fromkeys(return_list))

    def locate_low_validity_elements(self, driver):
        return_list = []
        check_texts = [self.sso_name]
        try:
            logger.info("Check XPath (LV)")
            xpath = XPathManager.get_xpath_find_search_term_in_text_and_attributes(
                self.element_attributes_to_check_low_validity, check_texts, False)
            el = driver.find_elements(By.XPATH, xpath)
            for element in el:
                if element.tag_name == "script" or element.tag_name == "html" or element.tag_name == "body" or element.tag_name == "head":
                    continue
                return_list.append(element)
            logger.info("Found " + str(len(return_list)) + " potential LV generic elements")
        except NoSuchElementException:
            pass
        try:
            logger.info("Checking buttons (LV)")
            xpath = XPathManager.get_xpath_find_elment_with_text_and_attributes("button",
                                                                                self.element_attributes_to_check_high_validity,
                                                                                check_texts, False)
            buttons = driver.find_elements(By.XPATH, xpath)
            duplicates = 0
            for el in buttons:
                if el not in return_list:
                    return_list.append(el)
                else:
                    duplicates += 1
            logger.info("Found " + str(len(buttons)) + " potential LV buttons (" + str(duplicates) + " duplicates)")
            # Stackoverflow has problems with generic text lookup --> searching buttons manually
            # Traditional way
            # buttons = driver.find_elements(By.XPATH, "//button")
            # logger.info("Found " + str(len(buttons)) + " buttons (LV)")
            # for button in self.check_elements_text_contains_search_element(buttons, check_texts, False):
            #    return_list.append(button)
            # for button in self.check_elements_attributes_contain_search_element(buttons, check_texts,
            #                                                                    self.element_attributes_to_check_low_validity):
            #    return_list.append(button)
        except NoSuchElementException:
            pass
        try:
            # Etsy has problems with generic text lookup --> searching links manually
            logger.info("Checking links (LV)")
            xpath = XPathManager.get_xpath_find_elment_with_text_and_attributes("a",
                                                                                self.element_attributes_to_check_high_validity,
                                                                                check_texts, False)
            links = driver.find_elements(By.XPATH, xpath)
            duplicates = 0
            for el in links:
                if el not in return_list:
                    return_list.append(el)
                else:
                    duplicates += 1
            logger.info("Found " + str(len(links)) + " potential LV links (" + str(duplicates) + " duplicates)")
            # Traditional way
            # links = driver.find_elements(By.XPATH, "//a")
            # logger.info("Found " + str(len(links)) + " links (LV)")
            # for link in self.check_elements_text_contains_search_element(links, check_texts, False):
            #    return_list.append(link)
            # for link in self.check_elements_attributes_contain_search_element(links, check_texts,
            #                                                                  self.element_attributes_to_check_low_validity):
            #    return_list.append(link)
        except NoSuchElementException:
            pass
        return list(dict.fromkeys(return_list))
