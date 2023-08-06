import argparse
import os.path
import threading
import uuid
from time import sleep

from pyvirtualdisplay import Display

from logmgmt import logger
from model.backend_information import BackendInformation
from processes.process_helper import ProcessHelper
from services.rest_client import RestClient
from ssoanalysisworker import __version__

cli = argparse.ArgumentParser()
cli.add_argument("--server-host", type=str,
                 help="Host of the backend. If not given, env variable SERVER_HOST must be set")
cli.add_argument("--server-port", type=int,
                 help="Port of the backend. If not given, env variable SERVER_PORT must be set")
cli.add_argument('--dev-mode', help="Disables the use of a virtual display. Can be used when running on a local "
                                    "machine with display enabled", action="store_true")
cli.add_argument('--name', help="The name displayed at the brain. This is temporary and will not be stored!",
                 required=False, default=None)
cli.add_argument('--uuid-file', help="Define the place of the file where the client stores the unique client id",
                 default=os.path.realpath(os.path.dirname(os.path.abspath(__file__))) + "/.uuid")


def start(running_check_element: threading.Event, webdriver_initialisation_error_check_element: threading.Event,
          analysis_id: int, backend_info: BackendInformation, invalid_config_error_check_element: threading.Event):
    ProcessHelper.prepare_and_run_analysis(backend_info, analysis_id, None, running_check_element,
                                           webdriver_initialisation_error_check_element,
                                           invalid_config_error_check_element)


def stop_job(job, rest_client, running_check):
    if job is not None:
        logger.info("Stopping current job...")
        try:
            rest_client.update_latest_activity("Stopping job")
        except Exception as err:
            logger.error("Could not report stopping action to brain" + str(err.__class__.__name__ + "!"))
        running_check.clear()
        while job.is_alive():
            sleep(10)
            try:
                rest_client.send_daemon_ping()
            except Exception as err:
                logger.error("Could not ping brain" + str(err.__class__.__name__))
        logger.info("Successfully stopped")


def get_uuid_of_current_client(path) -> str:
    if not os.path.exists(path):
        with open(path, "w") as file:
            file.write(uuid.uuid4().hex)
    with open(path) as file:
        return file.readline()


def check_version(remote_version: str) -> bool:
    return remote_version == __version__


def run():
    args = cli.parse_args()
    if args.server_host is None:
        args.server_host = os.getenv("SERVER_HOST")
    if args.server_port is None:
        args.server_port = os.getenv("SERVER_PORT")
    if args.name is None:
        args.name = os.getenv("WORKER_NAME")
    if args.server_host is None or args.server_port is None:
        logger.error("No server host or port was given!")
        exit(293)
    rest_client = RestClient(args.server_host, args.server_port)
    remote_version = rest_client.get_remote_client_version()
    if not check_version(remote_version):
        logger.error(
            "You are not using the latest supported version by the brain (remote: " + remote_version + " | local: "
            + __version__ + "). Please update the client (e.g. pip3 install sso-analysis-worker -U)")
        exit(0)
    client_identifier = get_uuid_of_current_client(args.uuid_file)
    disp = None
    if not args.dev_mode:
        try:
            logger.info("Start virtual display...")
            disp = Display(visible=False, size=(1920, 1080))
            disp.start()
        except Exception as err:
            logger.error("Something went wrong: " + err.__str__())
            exit(8787)
    logger.info("Running in daemon mode!")
    run_again = True
    while run_again:
        run_again = False
        try:
            token = None
            while token is None:
                logger.info("Checking if registered at brain " + args.server_host)
                try:
                    token = rest_client.get_notify_daemon_start_get_token(args.name, client_identifier)
                except OSError:
                    logger.error("Could not connect to server " + args.server_host + ":" + str(
                        args.server_port) + ". Sleeping 30 sec")
                finally:
                    if token is None:
                        logger.info("Client not registered yet. Sleeping 30 sec")
                        sleep(30)

            logger.info("Got token. Client is initialized")
            rest_client = RestClient(args.server_host, args.server_port, token)
            logger.info("Checking unfinished work")
            ProcessHelper.check_for_unfinished_work(rest_client)
            logger.info("Waiting for job...")
            prev_job_id = '-1'
            running_check = threading.Event()
            running_check.set()
            webdriver_initialisation_error_check = threading.Event()
            webdriver_initialisation_error_check.set()
            invalid_config_error_check = threading.Event()
            invalid_config_error_check.set()
            job = None
            stopping_reason = "Shutdown"
            try:
                while True:
                    remote_version = rest_client.get_remote_client_version()
                    if not check_version(remote_version):
                        logger.info("The client's code received an update (remote: " + remote_version + " | local: " +
                                    __version__ + "). Stopping this client. Please update before restarting "
                                                  "(e.g. pip3 install sso-analysis-worker -U)!")
                        stopping_reason = "Shutdown due to outdated client"
                        break
                    current_job_id = rest_client.get_job_for_daemon_client()
                    if current_job_id == "-1000":
                        logger.info("Received shutdown command! Will initialize shutdown...")
                        break
                    if current_job_id is None:
                        logger.error("Looks like this client was not cleanly removed from the brain (please stop this "
                                     "client before removing it from the brain). Shutting down...")
                        break
                    rest_client.send_daemon_ping()
                    current_activity = "Idle"
                    if job is not None and job.is_alive() and running_check.is_set():
                        current_activity = "Running"
                    if job is not None and not job.is_alive() and current_job_id != "-1":
                        if not webdriver_initialisation_error_check.is_set():
                            stopping_reason = "Client Error Shutdown!"
                            exit(75)
                        elif not invalid_config_error_check.is_set():
                            current_activity = "Config is invalid. Reassign after config update"
                        else:
                            current_activity = "Finished"
                    rest_client.update_latest_activity(current_activity)
                    if current_job_id == prev_job_id:
                        sleep(30)
                        continue
                    else:
                        logger.info("Job info changed! (" + str(prev_job_id) + " --> " + str(current_job_id) + ")")
                        stop_job(job, rest_client, running_check)
                        if current_job_id != "-1":
                            rest_client.update_latest_activity("Starting")
                            job = threading.Thread(target=start, args=(
                                running_check, webdriver_initialisation_error_check, current_job_id,
                                BackendInformation(args.server_host, args.server_port, token),
                                invalid_config_error_check))
                            running_check.set()
                            job.start()
                        prev_job_id = current_job_id
            finally:
                logger.info("Stopping daemon...")
                stop_job(job, rest_client, running_check)
                try:
                    rest_client.update_latest_activity(stopping_reason)
                except Exception as err:
                    logger.error("Could not report stopping reason " + stopping_reason + " to brain (" + str(
                        err.__class__.__name__) + ")!")
                logger.info("Current job finished")
                if disp is not None:
                    logger.info("Stopping virtual display")
                    disp.stop()
        except OSError as err:
            logger.error(err)
            logger.error("Got an error. Sleeping 30 sec and start again")
            run_again = True
            sleep(30)
        except KeyboardInterrupt:
            pass
    logger.info("Shutdown completed. Bye!")


if __name__ == "__main__":
    run()
