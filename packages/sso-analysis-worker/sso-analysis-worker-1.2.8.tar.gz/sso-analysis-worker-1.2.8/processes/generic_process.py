import threading
from abc import ABC, abstractmethod
from multiprocessing import Process
from time import sleep

from exceptions import RetryException
from logmgmt import logger


def handle_webdriver_initialisation_exception(rest_client, e, analysis_run_id, site):
    logger.error(e)
    logger.error(
        "Webdriver could not be initialized (" + e.thrown_exception.__class__.__name__ + "). This client looks broken. Exit with error code")
    try:
        rest_client.unregister_page_in_work(analysis_run_id, site.base_page)
        rest_client.update_latest_activity("ERROR!")
    except Exception as err:
        logger.error("Could not unregister page and send ERROR status to brain: " +
                     str(err.__class__.__name__) + ": " + str(err))
        pass
    exit(75)


class GenericAnalysisProcess(ABC):

    def start_process(self, running_check: threading.Event = None,
                      webdriver_initialisation_error_check: threading.Event = None,
                      invalid_config_error_check: threading.Event = None):
        logger.info("Starting process")
        counter = 0
        error_counter = 0
        max_errors = 3
        while running_check is None or running_check.is_set():
            try:
                self.prepare()
                object_to_analyse = self.get_next_object_to_analyse()
                if object_to_analyse is None:
                    break
            except RetryException:
                continue
            counter += 1
            p = self.generate_process(object_to_analyse)
            p.start()
            p.join()
            if p.exitcode == 75 or p.exitcode == 70:
                error_counter += 1
                if p.exitcode == 75 and error_counter >= 3:
                    logger.error("Client can not initialize webdriver anymore. Looks broken (last " + str(max_errors) +
                                 " processes exited abnormally)! Quitting!")
                    if webdriver_initialisation_error_check is not None:
                        webdriver_initialisation_error_check.clear()
                    exit(p.exitcode)
                elif p.exitcode == 70:
                    logger.error("Client configuration seems faulty (no account is logged in)!")
                    if invalid_config_error_check is not None:
                        invalid_config_error_check.clear()
                    exit(p.exitcode)
                else:
                    logger.error("Last process exited abnormally (error code " + str(
                        p.exitcode) + "). Will try again (error counter: " + str(error_counter) + "/" + str(
                        max_errors) + ") after one minute.")
                    sleep(60)
            else:
                error_counter = 0
                logger.info("Process finished")
        if running_check is not None and not running_check.is_set():
            logger.info("Process was stopped by brain")
        else:
            logger.info("No more sites left. Finished work here!")

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def get_next_object_to_analyse(self):
        pass

    @abstractmethod
    def generate_process(self, object_to_analyse) -> Process:
        pass
