class LoginPathInformation:
    def __init__(self, page_information, index, login_path, additional_steps, has_login, broken, gatheringtime,
                 other_infos={}):
        self.pageInformation = page_information
        self.index = index
        self.loginPath = login_path
        self.additionalSteps = additional_steps
        self.hasLogin = has_login
        self.broken = broken
        self.gatheringtime = gatheringtime
        self.other_information = other_infos
