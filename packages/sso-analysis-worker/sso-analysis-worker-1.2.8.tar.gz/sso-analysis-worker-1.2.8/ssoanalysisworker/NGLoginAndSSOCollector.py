import argparse

from pyvirtualdisplay import Display

from logmgmt import logger
from model.backend_information import BackendInformation
from processes.process_helper import ProcessHelper
from services import command_line_validator

cli = argparse.ArgumentParser()
subparsers = cli.add_subparsers(dest="subcommand")


def create_backend_information(args):
    backend_info = BackendInformation(args.server_host, args.server_port, args.token)
    if not command_line_validator.check_backend_config(backend_info):
        logger.error("Invalid information!")
        exit(7002)
    return backend_info


def subcommand(args=None, parent=subparsers):
    if args is None:
        args = []

    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)

    return decorator


def argument(*name_or_flags, **kwargs):
    return [*name_or_flags], kwargs


@subcommand([argument("-t", "--token", type=str, help='The token to use for gathering information', required=True),
             argument('-b', '--bounds', help="The bounds of the tranco list", type=int, nargs=2),
             argument('-rr', '--renew-requested',
                      help="Analyse / locate all in login locations in range that are marked as 'needs renew'",
                      action="store_true"),
             argument('-rb', '--renew-broken',
                      help="Analyse currently broken login paths. This parameter can not be used with "
                           "--renew-requested", action="store_true"),
             argument('--server-host', help="Host of the backend. Default https://sso-scanner-mgmt.it.hs-heilbronn.de/",
                      default="https://sso-scanner-mgmt.it.hs-heilbronn.de"),
             argument('--server-port', help="Port of the backend. Default 443", type=int, default=443)])
def login_path_detection(args):
    if not command_line_validator.check_args_for_login_path_detection(args):
        exit(7001)
    from processes.locateloginpages.locate_login_page_process import LocateLoginPage
    backend_info = create_backend_information(args)
    locate_login_page_process = LocateLoginPage(backend_info)
    try:
        locate_login_page_process.start_process_tranco_list(args.bounds[0] if args.bounds else 1,
                                                            args.bounds[1] if args.bounds else 1000000,
                                                            args.renew_requested, args.renew_broken)
    except KeyboardInterrupt:
        logger.info("\n\nQuitting... Closing services connection and driver")
        locate_login_page_process.finish()


@subcommand([argument("-t", "--token", type=str, help='The token to use for gathering information', required=True),
             argument("-i", "--id", type=int, help="The id of the analysis run which was started at '--server-host'. "
                                                   "Required if not running in local mode", required=True),
             argument('--server-host', help="Host of the backend. Default https://sso-scanner-mgmt.it.hs-heilbronn.de/",
                      default="https://sso-scanner-mgmt.it.hs-heilbronn.de"),
             argument('--server-port', help="Port of the backend. Default 443", type=int, default=443),
             argument('--dev-mode', help="Disables the use of a virtual display. Can be used when running on a local "
                                         "machine with display enabled",
                      action="store_true")])
def run_analysis(args):
    disp = None
    if not args.dev_mode:
        try:
            logger.info("Start virtual display...")
            disp = Display(visible=False, size=(1920, 1080))
            disp.start()
        except Exception as err:
            logger.error("Something went wrong: " + err.__str__())
            exit(8787)
    backend_info = create_backend_information(args)
    ProcessHelper.prepare_and_run_analysis(backend_info, args.id, disp)


@subcommand(
    [argument('--no-google', help="Runs the tool in headless mode", action="store_true", required=False, default=False),
     argument('--no-facebook', help="Runs the tool in headless mode", action="store_true", required=False,
              default=False),
     argument('--no-apple', help="Runs the tool in headless mode", action="store_true", required=False, default=False),
     argument('--local-run-sites', help="The file from which the sites should be read. The format must match "
                                        "one site per line with no additional data", required=True),
     argument('--local-run-results', help="Defines where the results should be stored"),
     argument('--headless', help="Runs the tool in headless mode", action="store_true"),
     argument('--retry', help="Retry not existing already pages", action="store_true", required=False, default=False)])
def run_analysis_local(args):
    from processes.ssolandscapeanalysis.local_sso_detection_process import LocalSSODetectionProcess
    if not command_line_validator.check_local_run_config(args):
        exit(100)

    disp = None
    if args.headless:
        try:
            logger.info("Start virtual display...")
            disp = Display(visible=False, size=(1920, 1080))
            disp.start()
        except Exception as err:
            logger.error("Something went wrong: " + err.__str__())
            exit(8787)
    try:
        LocalSSODetectionProcess(args.local_run_sites, args.local_run_results, args.no_google,
                                 args.no_facebook, args.no_apple, args.retry).start_process()
    except KeyboardInterrupt:
        exit(1)
    except Exception as err:
        logger.error("Something went wrong!")
        logger.error(err)
        exit(100)
    finally:
        if args.headless and disp is not None:
            logger.info("Stopping virtual display")
            disp.stop()


pass


def run():
    args = cli.parse_args()
    if args.subcommand is None:
        cli.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    run()
