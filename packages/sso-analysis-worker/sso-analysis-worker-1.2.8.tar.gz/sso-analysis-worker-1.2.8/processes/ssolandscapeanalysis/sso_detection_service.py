import time

from selenium.common.exceptions import TimeoutException

from logmgmt import logger
from exceptions import RenewalRequestNeededException
from input.input_management import InputManager
from model.ssodetection.sso_detection_strategy import SSODetectionStrategy
from processes.ssolandscapeanalysis.locators.social_login_information import SocialLoginInformation
from processes.ssolandscapeanalysis.locators.social_login_locator import SocialLoginLocator


def get_max_steps_for_detection(run_google, run_facebook, run_apple):
    steps = 0
    if run_google:
        steps += 1
    if run_facebook:
        steps += 1
    if run_apple:
        steps += 1
    return steps


class SSODetectionService:

    def __init__(self, known_sso_providers):
        self.known_sso_providers = known_sso_providers
        self.provider_ids = {
            'google': self.find_id_for_provider("google"),
            'facebook': self.find_id_for_provider("facebook"),
            'apple': self.find_id_for_provider("apple"),
            'none': self.find_id_for_provider("none")
        }
        self.locators = {
            'google': self.load_social_login_locater("Google"),
            'facebook': self.load_social_login_locater("Facebook"),
            'apple': self.load_social_login_locater("Apple"),
        }

    def automatic_sso_detection(self, chromedriver, latest_login_info, progress_callback=None, run_google=True,
                                run_facebook=True, run_apple=True, special_check: callable = None) -> [tuple]:
        ids = []
        max_steps = get_max_steps_for_detection(run_google, run_facebook, run_apple)
        current_step = 0
        if run_google:
            current_step += 1
            if progress_callback is not None:
                progress_callback(current_step, max_steps,
                                  "Identifying Google SSO Support for " + latest_login_info.loginPath)
            logger.info("--- Google ---")
            start_time = time.time()
            try:
                google_locate_result = self.locators['google'].locate_login(chromedriver, latest_login_info,
                                                                            special_check)
                logger.info("--- Finished Google in " + str(round(time.time() - start_time, 2)) + "s ---")
            except TimeoutException:
                google_locate_result = False,
                logger.info("--- Analysis for Google failed after " + str(round(time.time() - start_time, 2)) + "s ---")
            if google_locate_result[0]:
                ids.append((self.provider_ids['google'], google_locate_result[1], google_locate_result[2],
                            latest_login_info.loginPath, google_locate_result[3], google_locate_result[4]))

        if run_facebook:
            current_step += 1
            if progress_callback is not None:
                progress_callback(current_step, max_steps,
                                  "Identifying Facebook SSO Support for " + latest_login_info.loginPath)
            logger.info("--- Facebook ---")
            start_time = time.time()
            try:
                facebook_locate_result = self.locators['facebook'].locate_login(chromedriver, latest_login_info,
                                                                                special_check)
                logger.info("--- Finished Facebook in " + str(round(time.time() - start_time, 2)) + "s ---")
            except TimeoutException:
                facebook_locate_result = False,
                logger.info(
                    "--- Analysis for Facebook failed after " + str(round(time.time() - start_time, 2)) + "s ---")

            if facebook_locate_result[0]:
                ids.append((self.provider_ids['facebook'], facebook_locate_result[1], facebook_locate_result[2],
                            latest_login_info.loginPath, facebook_locate_result[3], facebook_locate_result[4]))

        if run_apple:
            current_step += 1
            if progress_callback is not None:
                progress_callback(current_step, max_steps,
                                  "Identifying Apple SSO Support for " + latest_login_info.loginPath)
            logger.info("--- Apple ---")
            start_time = time.time()
            try:
                apple_locate_result = self.locators['apple'].locate_login(chromedriver, latest_login_info,
                                                                          special_check)
                logger.info("--- Finished Apple in " + str(round(time.time() - start_time, 2)) + "s ---")
            except TimeoutException:
                apple_locate_result = False,
                logger.info("--- Analysis for Apple failed after " + str(round(time.time() - start_time, 2)) + "s ---")
            if apple_locate_result[0]:
                ids.append((self.provider_ids['apple'], apple_locate_result[1], apple_locate_result[2],
                            latest_login_info.loginPath, apple_locate_result[3], apple_locate_result[4]))
        if len(ids) == 0:
            ids.append((self.provider_ids['none'], None, None, None, SSODetectionStrategy.ELEMENT_SEARCH, None))
        return ids

    def manual_sso_detection(self) -> [tuple]:
        supported_sso = []
        inp = ""
        while inp != "Finish" and inp != "None" and inp != "Skip" and inp != "Send Renewal Request":
            valid = self.create_valid_inputs_from_already_gathered_sso(supported_sso)
            if len(supported_sso) == 0:
                valid.append("Skip")
                valid.append("Send Renewal Request")
            if len(supported_sso) > 0:
                valid.append("Finish")
                valid.append("Reset")
            inp = InputManager.get_input_from_gui_with_specific_answer_values("Input", valid, False)
            if inp == "Reset":
                supported_sso.clear()
            if inp == "Send Renewal Request":
                raise RenewalRequestNeededException()
            elif inp != "Finish":
                supported_sso.append(inp)
            if inp == "Finish" or inp == "None" or inp == "Skip":
                savable_sso_providers = []
                for supported_sso_provider in supported_sso:
                    for backend_sso_provider in self.known_sso_providers:
                        if backend_sso_provider[1].startswith(supported_sso_provider):
                            savable_sso_providers.append(backend_sso_provider)
                text = ""
                ids = []
                for save_sso_provider in savable_sso_providers:
                    text += " " + save_sso_provider[1]
                    ids.append((save_sso_provider[0], None, None, None, SSODetectionStrategy.MANUAL))
                if len(ids) > 1 or ids[0][0] != 9999:
                    if InputManager.get_input_from_gui_with_specific_answer_values(
                            "Saving:" + text + ". Correct?", ["y", "n"], False) == "n":
                        logger.info("Restarting gathering process...")
                        supported_sso.clear()
                        inp = ""
                    else:
                        return ids
                else:
                    return ids

    def create_valid_inputs_from_already_gathered_sso(self, supported_sso):
        valid_inputs_raw = InputManager.create_supported_sso_user_inputs(self.known_sso_providers)
        return_list = []
        for inp in valid_inputs_raw:
            # inp_to_check = inp[0][0:1].upper() + inp[0][1:len(inp)]
            inp_to_check = inp[1]
            if inp_to_check not in supported_sso:
                if inp[1].lower() != "none" or len(supported_sso) == 0:
                    return_list.append(inp[1])  # Change this to 0 and change commented line above for short form
        return return_list

    def find_id_for_provider(self, provider_name):
        for sso in self.known_sso_providers:
            if sso[1].lower() == provider_name.lower():
                return sso[0]
        raise Exception("Unknown provider")

    @staticmethod
    def load_social_login_locater(social_login_name):
        return SocialLoginLocator(SocialLoginInformation[social_login_name]["name"],
                                  SocialLoginInformation[social_login_name]["exclude_url_starts_with"],
                                  SocialLoginInformation[social_login_name]["valid_login_urls"],
                                  SocialLoginInformation[social_login_name]["must_have_texts_in_valid_login_urls"],
                                  SocialLoginInformation[social_login_name]["extra_texts"])
