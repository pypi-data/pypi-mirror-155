import argparse

from logmgmt import logger
from model.backend_information import BackendInformation
from services import RestClient

cli = argparse.ArgumentParser()
subparsers = cli.add_subparsers(dest="subcommand")


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
             argument("-i", "--id", type=int, help="The id of the analysis run which was started at '--server-host'. "
                                                   "Required if not running in local mode", required=True),
             argument("-p", "--page", type=str, help="The page to debug"),
             argument('--server-host', help="Host of the backend. Default https://sso-scanner-mgmt.it.hs-heilbronn.de/",
                      default="https://sso-scanner-mgmt.it.hs-heilbronn.de"),
             argument('--server-port', help="Port of the backend. Default 443", type=int, default=443),
             argument('--dev-mode', help="Disables the use of a virtual display. Can be used when running on a local "
                                         "machine with display enabled",
                      action="store_true")])
def run_debug_for_site(args):
    rest_client = RestClient(args.server_host, args.server_port, args.token)
    analysis_info = rest_client.get_analysis_run_type(args.id)
    if analysis_info == "SSO_SECURITY_ANALYSIS":
        result = rest_client.get_debug_info_sso_security_analysis(args.id, args.page)
        config = rest_client.get_configuration_for_run(args.id)
        import tempfile
        import zipfile
        import io
        config_directory = tempfile.TemporaryDirectory()
        z = zipfile.ZipFile(io.BytesIO(config))
        z.extractall(config_directory.name)
        del z, config
        from processes.ssosecurityanalysis import sso_security_analysis_process
        sso_security_analysis_process.process_function(result, BackendInformation(args.server_host, args.server_port,
                                                                                  args.token), -100, config_directory)
        print("found")
        config_directory.cleanup()

    else:
        logger.info("UNSUPPORTED TYPE " + str(analysis_info) + " AT THE MOMENT")

if __name__ == "__main__":
    args = cli.parse_args()
    if args.subcommand is None:
        cli.print_help()
    else:
        args.func(args)
