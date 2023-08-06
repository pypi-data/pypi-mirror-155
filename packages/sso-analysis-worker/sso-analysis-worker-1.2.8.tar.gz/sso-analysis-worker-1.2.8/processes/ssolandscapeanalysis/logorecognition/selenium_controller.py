import os
import time
from typing import Tuple

from selenium.webdriver.common.action_chains import ActionChains
from seleniumwire import webdriver

from exceptions import ScreenshotException
from logmgmt import logger
from processes.ssolandscapeanalysis.logorecognition.configuration_logo_recognition import Config as config
from services import driver_manager


class SeleniumController():
    """The Selenium Controller implements the following two features:
    - creates screenshots of a login page
    - verifies if a LoginButton-Candidate redirects to the corresponding IdP

    The SeleniumController starts a Chromium Browser with a prepared configuration: otpions and extensions and navigates to the corresponding websites.
    """

    def __init__(self, path_driver="/usr/local/bin/chromedriver", width=1920, height=1080, timeout=10,
                 path_screenshots=config.SeleniumPaths["screenshots"]):
        """Default Configuration of the Selenium Controller 

        Args:
            path_driver (str, optional): Path to the Browser (Chromium Browser). Defaults to "/usr/local/bin/chromedriver".
            width (int, optional): Width of the browser window. Defaults to 1900.
            height (int, optional): Heght of the browser window.. Defaults to 1080.
            timeout (int, optional): Timeout waiting a website to be loaded. Defaults to 10 sec.
            path_screenshots (str, optional): Path to store the screenshots. Defaults to "./logo-recognition/recordings/screenshots/".
        """
        self.path_driver = path_driver
        # During tests, we estimated that one extension is sufficient to avoid the existing problems (cookie banners, privacy configurations)
        self.path_extensions = []
        for filename in os.listdir(driver_manager.extensions_folder):
            if filename.endswith(".crx"):
                self.path_extensions.append(driver_manager.extensions_folder + "/" + filename)

        self.window_width = width
        self.window_height = height
        self.timeout = timeout

        self.path_screenshots = path_screenshots

        # Creates the corresponding folder to store the screenshots
        try:
            os.mkdir(self.path_screenshots)
        except (FileExistsError, FileNotFoundError) as e:
            logger.debug("Folder exists: " + self.path_screenshots)

    def getSeleniumDriver(self) -> webdriver:
        return driver_manager.DriverManager.generate_driver()

    def create_recordings(self, domain_url: str, login_url: str, timeout=None) -> str:
        """Creates a screenshot of the login URL of a domain

        Args:
            domain_url (str): tranco domain
            login_url (str): Login URL of a website
            timeout (int, optional): Timeout to load a website. Defaults to None.

        Raises:
            ScreenshotException: A Screenshot could not be created for a domain/login URL

        Returns:
            str: Filename of the created screenshot
        """
        if timeout is not None:
            self.timeout = timeout

        logger.debug("Starting Google Chrome for %s", domain_url)
        driver = self.getSeleniumDriver()

        try:
            driver.get(login_url)
            time.sleep(self.timeout)

            screenshot_filename = self.path_screenshots + domain_url + ".png"
            logger.debug("Storing Screenshot: " + screenshot_filename)
            driver.save_screenshot(screenshot_filename)
            driver.quit()
            return screenshot_filename
        except Exception as ex:
            logger.error("Exception in Screenshot Generation for: " + login_url)
            logger.error(ex)
            driver.quit()
            raise ScreenshotException(domain_url=domain_url, login_url=login_url, message=ex.msg)

    def verfyLoginButton(self, login_url: str, xCoordinate: float, yCoordinate: float, idpName: str) -> Tuple[
        str, bool, str]:
        """_summary_

        Args:
            login_url (str): _description_
            xCoordinate (float): _description_
            yCoordinate (float): _description_
            idpName (str): _description_

        Returns:
            Tuple[str, bool]: URL of the IdP after clicking on the button, verification status of the SSO button
        """

        driver = self.getSeleniumDriver()
        logger.debug("Starting Google Chrome")
        verificationStatus = False
        idp_url = ""

        try:
            driver.get(login_url)
            time.sleep(self.timeout)

            action = ActionChains(driver)
            action.move_by_offset(xCoordinate, yCoordinate).click().perform()
            time.sleep(self.timeout)

            # OLD: driver.switch_to.window(driver.window_handles[-1])

            # iterate over all opened windows and evalaute the URL
            # the iteration is needed if the SSO is executed in a PopUp
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                idp_url = driver.current_url
                verificationStatus |= self.verifyIdPUrl(idp_url, idpName)
                if verificationStatus:
                    break
        except Exception as ex:
            logger.error("Selenium: Cannot verify SSO Button for: %s", login_url)
            logger.error(ex)
        har = driver.har
        driver.quit()
        return idp_url, verificationStatus, har

    def verifyIdPUrl(self, idp_url: str, idpName: str) -> bool:
        """Gets the URL after clicking on a SSO button and verifies if SSO authentication is started.

        Args:
            idp_url (str): The Query String from the browser
            idpName (str): Expected IdP

        Returns:
            bool: SSO detection correct/incorrect
        """

        # fetches the information regarding the recognition patterns
        conf = config.SocialLoginInformation[idpName]

        # iterates over the expected login URLs (an IdP could have many)
        for validURLs in conf["valid_login_urls"]:
            if validURLs in idp_url:
                # checks for SSO params (OAuth/OIDC)
                for validParams in conf["must_have_texts_in_valid_login_urls"]:
                    if validParams in idp_url:
                        return True
        return False
