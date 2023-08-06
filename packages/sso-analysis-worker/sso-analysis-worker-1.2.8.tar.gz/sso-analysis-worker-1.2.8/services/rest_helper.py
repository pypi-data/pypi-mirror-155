from model.locateloginpages.additional_steps_to_show_login import AdditionalStepToShowLogin
from model.login_path_information import LoginPathInformation
from model.page_information import PageInformation
from logmgmt import logger


class RestHelper:
    @staticmethod
    def tranco_page_info_from_json(json_entry):
        return PageInformation(json_entry['index'], json_entry['site'])

    @staticmethod
    def page_info_from_json(json_entry):
        return PageInformation(json_entry['index'], json_entry['basePage'])

    @staticmethod
    def manual_login_page_location_from_json(json_entry, rest_client):
        if json_entry is None:
            return None
        addSteps = []
        if json_entry['needsAdditionalStepsToShowLogin']:
            addSteps = rest_client.get_additional_steps_for_login_path_location(json_entry['index'])
        return LoginPathInformation(RestHelper.page_info_from_json(json_entry['page']), json_entry['index'],
                                    json_entry['loginPage'], addSteps, json_entry['hasLogin'], json_entry['broken'],
                                    json_entry['gatheringTime'])

    @staticmethod
    def convert_json_to_list_of_tranco(response):
        if not response.status_code == 200:
            logger.error("Something went wrong (code " + str(response.status_code) + "): " + response.text)
            return []
        return_list = []
        for entry in response.json():
            return_list.append(RestHelper.tranco_page_info_from_json(entry))
        return return_list

    @staticmethod
    def convert_json_to_list_of_pages(response):
        if not response.status_code == 200:
            logger.error("Something went wrong (code " + str(response.status_code) + "): " + response.text)
            return []
        return_list = []
        for entry in response.json():
            return_list.append(RestHelper.page_info_from_json(entry))
        return return_list

    @staticmethod
    def convert_json_to_list_of_additional_steps(response):
        if not response.status_code == 200:
            logger.error("Something went wrong (code " + str(response.status_code) + "): " + response.text)
            return []
        steps = []
        for entry in response.json():
            steps.append(
                AdditionalStepToShowLogin(entry['index'], entry['additionalStepValue'], entry['additionalStepType'],
                                          entry['additionalStepOrderIndex']))
        return steps

    @staticmethod
    def convert_json_to_list_of_sso_provider(response):
        if not response.status_code == 200:
            logger.error("Something went wrong (code " + str(response.status_code) + "): " + response.text)
            return []
        return_res = []
        for entry in response.json():
            prov = entry['providerName'][0:1].upper() + entry['providerName'][1:len(entry['providerName'])].lower()
            return_res.append([entry['index'], prov])
        return return_res
