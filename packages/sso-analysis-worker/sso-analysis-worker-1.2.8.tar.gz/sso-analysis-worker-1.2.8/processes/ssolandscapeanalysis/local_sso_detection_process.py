from multiprocessing import Process
from os.path import exists
from time import sleep

from selenium.common.exceptions import TimeoutException, WebDriverException

from logmgmt import logger
from exceptions import ManualAnalysisNeededException
from exceptions import RenewalRequestNeededException
from model.login_path_information import LoginPathInformation
from model.page_information import PageInformation
from processes.ssolandscapeanalysis.sso_detection_service import SSODetectionService
from services import file_service
from services.driver_manager import DriverManager


def thread_process(site, sso_detection_service, local_run_results, google, facebook, apple):
    try:
        site = site.replace("\n", "")
        if not site.startswith("https://") and not site.startswith("http://"):
            site = "https://" + site
        logger.info("Analyzing site " + site)
        chromedriver = DriverManager.generate_driver()
        chromedriver.get(site)
        sleep(10)
        ids = sso_detection_service.automatic_sso_detection(
            chromedriver, LoginPathInformation(PageInformation(-1, site), -1, site, [], True, False, None),
            run_google=google, run_facebook=facebook, run_apple=apple)
        ids_only = []
        for id in ids:
            ids_only.append(id[0])
        file_service.save_to_file(local_run_results, site, ids)
        chromedriver.close()
        chromedriver.quit()
    except (RenewalRequestNeededException, TimeoutException, WebDriverException,
            ManualAnalysisNeededException) as err:
        logger.error("Problems while analysing website " + site + "! Skipping...")
        logger.error(err)
    except KeyboardInterrupt as err:
        logger.info("Received interrupt")
        raise err
    except Exception as err:
        logger.error("Unknown error! This should be managed explicitly " + str(err))


class LocalSSODetectionProcess:

    def __init__(self, local_run_sites: str, local_run_results: str, ignore_google: bool, ignore_facebook: bool,
                 ignore_apple: bool, retry: bool):
        self.local_run_sites = local_run_sites
        self.local_run_results = local_run_results
        self.sso_detection_service = SSODetectionService(
            [[1, "Google"], [2, "Facebook"], [3, "Apple"], [9998, "Others"], [9999, "None"]])
        self.google = not ignore_google
        self.facebook = not ignore_facebook
        self.apple = not ignore_apple
        self.retry = retry

    def start_process(self):
        lines = []
        if self.retry and exists(self.local_run_results):
            with open(self.local_run_results) as file:
                lines = file.readlines()

        counter = 0
        while (site := file_service.read_line_from_file(self.local_run_sites, counter)) is not None:
            if self.retry and exists(self.local_run_results):
                already_analysed = False
                for line in lines:
                    if line.replace("\n", "").startswith(site.replace("\n", "")):
                        already_analysed = True
                        print("Already analyesd: " + site)
                        break
                if already_analysed:
                    counter += 1
                    continue
            p = Process(target=thread_process, args=(
                site, self.sso_detection_service, self.local_run_results, self.google, self.facebook, self.apple))
            p.start()
            p.join()
            counter += 1
            logger.info("Process finished")
        logger.info("No more sites left!")
