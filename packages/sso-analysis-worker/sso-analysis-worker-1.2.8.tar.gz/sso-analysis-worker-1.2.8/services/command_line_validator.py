from os import path

from exceptions import ParameterException
from logmgmt import logger
from services.rest_client import RestClient


def check_args_for_login_path_detection(args):
    try:
        if (args.bounds and (args.renew_requested or args.renew_broken) or
                (args.renew_requested and (args.bounds or args.renew_broken)) or
                (args.renew_broken and (args.bounds or args.renew_requested))):
            raise ParameterException(
                "-b/--bounds, -rr/--renew-requested and -rb/--renew-broken can not be used together")
        if not args.bounds and not args.renew_broken and not args.renew_requested:
            raise ParameterException("At least one parameter (-b/--bounds, -rr/--renew-requested, -rb/--renew-broken) "
                                     "must be set")
    except ParameterException as err:
        logger.error(err.msg)
        return False
    return True


def check_backend_config(backend_info):
    if not RestClient(backend_info.host, backend_info.port, None).check_token(backend_info.token):
        logger.error("Token could not be validated.")
        return False
    return True


def check_backend_config_with_id(backend_info, analysis_run_id):
    if not check_backend_config(backend_info):
        return False
    if not RestClient(backend_info.host, backend_info.port, backend_info.token).exists_analysis_session(
            analysis_run_id):
        logger.error("Analysis id does not exits")
        return False
    return True


def check_args_for_id_existence(args):
    if not args.local_run and not args.id:
        logger.error("-i/--id is required")
        return False
    return True


def check_local_run_config(args):
    if not path.isfile(args.local_run_sites):
        logger.error(args.local_run_sites + " does not exist!")
        return False
    if path.isfile(args.local_run_results) and not args.retry:
        logger.error("Results file at " + args.local_run_results + " already exists!")
        return False
    return True
