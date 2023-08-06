class CancleCurrentSiteException(Exception):
    pass


class NoLoginCandidatesFoundException(Exception):
    pass


class ConfigInvalidException(Exception):
    pass


class ManualAnalysisNeededException(Exception):
    pass


class ParameterException(Exception):
    def __init__(self, msg):
        self.msg = msg


class RenewalRequestNeededException(Exception):
    pass


class ResetProcessException(Exception):
    pass


class RetryException(Exception):
    pass


class SiteNotResolvableException(Exception):
    pass


class DuckDuckGoHasChangedException(Exception):
    pass


class StartPageHasChangedException(Exception):
    pass


class BingHasChangedException(Exception):
    pass


class IdpPageOpenedOnClick(Exception):
    def __init__(self, opened_url, starting_point_next_try):
        self.opened_url = opened_url
        self.starting_point_next_try = starting_point_next_try


class WebDriverInitialisationException(Exception):
    def __init__(self, e):
        self.thrown_exception = e


class ScreenshotException(Exception):
    def __init__(self, domain_url, login_url, message="It was not possible to generate a screenshot!"):
        """Exception raised for errors during the screenshot recording.

        Attributes:
            domain_url -- domain of the tranco list
            login_url -- login URL of the website
            message -- exception message
        """
        self.domain_url = domain_url
        self.login_url = login_url
        self.message = message
        super().__init__(self.message)
