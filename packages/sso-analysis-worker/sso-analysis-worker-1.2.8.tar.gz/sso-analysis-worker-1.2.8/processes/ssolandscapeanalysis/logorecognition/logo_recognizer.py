import os
from contextlib import suppress
from datetime import datetime

from exceptions import ScreenshotException
from logmgmt import logger
from processes.ssolandscapeanalysis.logorecognition.configuration_logo_recognition import Config as config
from processes.ssolandscapeanalysis.logorecognition.logo_recognition import PatternMatcher
from processes.ssolandscapeanalysis.logorecognition.selenium_controller import SeleniumController


class LogoReconizer():
    def __init__(self, PATH=config.AnalysisPaths["base"]):
        self.PATH = PATH
        self.ANALYSIS_PATH = PATH + datetime.now().strftime('%Y-%m-%d') + "/"
        self.ANALYSIS_PATH_SCREENSHOTS = self.ANALYSIS_PATH + "screenshots/"
        self.ANALYSIS_PATH_SCREENSHOTS__RECOGNITION = self.ANALYSIS_PATH + "screenshots_recognition/"
        self.ANALYSIS_PATH_evaluation = self.ANALYSIS_PATH + "evaluation/"

        logger.info("Logo recognizer uses " + os.path.abspath(self.PATH) + " for the analysis")

        # Activate this if you want to improve the logo recognition rates. If added: the screenshot will be scaled (instead of the logo). 
        # This approach consumes much more time and ressources, but the imrpvements are minimal. 
        self.EXTENDED_ANALYSIS = False

        """
        Creates all output folders storing temporary results needed for the analysis
        """
        with suppress(FileExistsError):
            os.makedirs(self.PATH)
        with suppress(FileExistsError):
            os.makedirs(self.ANALYSIS_PATH)
        with suppress(FileExistsError):
            os.makedirs(self.ANALYSIS_PATH_SCREENSHOTS)
        with suppress(FileExistsError):
            os.makedirs(self.ANALYSIS_PATH_SCREENSHOTS__RECOGNITION)
        with suppress(FileExistsError):
            os.makedirs(self.ANALYSIS_PATH_evaluation)

    def scan_needed(self, recognition: dict()) -> bool:
        scan_not_needed = True
        for entry in recognition.values():
            scan_not_needed &= entry

        return scan_not_needed

    def analyseHybridLoginURL(self, domain_url: str, login_urls: list(),
                              init_recognition: dict = {"facebook": False, "google": False, "apple": False},
                              callback=None) -> dict:

        recognition = init_recognition.copy()
        results = {"details": []}
        counter = 0

        for login_url in login_urls:
            counter += 1
            # the scan is skipped if ALL providers are recognized
            if self.scan_needed(recognition=recognition):
                return results

            if callback is not None:
                callback(counter, len(login_urls), "Running image analysis for " + login_url)

            seleniumController = SeleniumController(path_screenshots=self.ANALYSIS_PATH_SCREENSHOTS)
            try:
                # Try to capture a screenshot of the Login URL
                logger.info("domain_url=%s - Screenshot creation with login_url=%s", domain_url, login_url)
                screenshot_filename = seleniumController.create_recordings(domain_url=domain_url, login_url=login_url)
            except ScreenshotException as ex:
                # Something went wrong. We repeat the screenshot capturing with an increased timeout = 20 seconds (some websites are really slow)
                logger.info("domain_url=%s - Second Try: Screenshot creation with login_url=%s", domain_url, login_url)
                logger.error(ex.message)
                screenshot_filename = seleniumController.create_recordings(domain_url=domain_url, login_url=login_url,
                                                                           timeout=20)

            # Start the Logo recognition
            logger.info("Starting logo recognition process")
            patternMatcher = PatternMatcher()
            templateMatchingResults = patternMatcher.logoTeamplateMatching(
                screenshot_filename=screenshot_filename,
                analysis_path=self.ANALYSIS_PATH_SCREENSHOTS__RECOGNITION,
                domain_url=domain_url,
                login_url=login_url,
                comprehensive_search=self.EXTENDED_ANALYSIS,
                init_recognition=recognition)
            logger.info("Logo recognition process finished")

            for idp in recognition.keys():
                if templateMatchingResults[idp] == True and recognition[idp] == False:
                    recognition[idp] |= templateMatchingResults[idp]
                    results["details"].append({"provider": idp, "login_url": login_url,
                                               "coordinates": templateMatchingResults["logoCoordinates"][idp],
                                               "har": templateMatchingResults['har'][idp],
                                               "idp_url": templateMatchingResults['idp_url'][idp]})

        return results
