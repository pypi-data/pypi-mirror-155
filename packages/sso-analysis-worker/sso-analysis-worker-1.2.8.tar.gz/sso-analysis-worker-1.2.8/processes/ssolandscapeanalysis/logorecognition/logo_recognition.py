import os
from datetime import datetime

import cv2 as cv2
import imutils
import numpy as np

from logmgmt import logger
from processes.ssolandscapeanalysis.logorecognition.configuration_logo_recognition import Config as config
from processes.ssolandscapeanalysis.logorecognition.selenium_controller import SeleniumController


class PatternMatcher():

    def __init__(self, max_matching=0.9, upper_bound=0.8, lower_bound=0.7, scale_upper_bound=17, scale_lower_bound=10,
                 match_intensity=4, match_algorithm=cv2.TM_CCOEFF_NORMED):
        """_summary_

        Args:
            max_matching (float, optional): Max matching results stops the search and returns the finding directly. Defaults to 0.9.
            upper_bound (float, optional): Findings above this bound are considered as a valid SSO recognition (but the search proceeds with finding a better matching). Defaults to 0.8.
            lower_bound (float, optional): Findings below this bound are considered as not successful SSO recognition. Defaults to 0.7.
            scale_upper_bound (int, optional): Upper bound of the scale factor of the pattern. Defaults to 17.
            scale_lower_bound (int, optional): Lower bound of the scale factor of the pattern. Defaults to 10.
            match_intensity (int, optional): Number of iteration with different scale factors. Defaults to 4.
            match_algorithm (_type_, optional): OpenCV matching algorithm. Defaults to cv2.TM_CCOEFF_NORMED.
        """

        self.supported_idps = config.SocialLoginInformation.keys()
        self.max_matching = max_matching
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.scale_upper_bound = scale_upper_bound
        self.scale_lower_bound = scale_lower_bound
        self.match_intensity = match_intensity
        self.match_algorithm = match_algorithm

        self.dt = datetime.now()
        self.foldername = self.dt.strftime('%Y%m%d%H%M/')

    def matchTemplate_scaleScreenshot(self, image_path: str, logos: dict, result_path: str, website: str,
                                      recognition: dict = {"facebook": False, "google": False, "apple": False}) -> dict:
        """Find the best matching of all logos. 
        We scale the screenshot and search for the logo within the screenshot
        Highlight the finding in the screenshot and store the results into the database

        Args:
            image_path (str): Path to the screenshot that should be analyzed
            logos (dict): Array of all logos
            result_path (str): Folder where the highlighted screenshots will be stored
            website (str): Name of the tranco domain
            recognition (_type_, optional): Init dictionary storing the results of the recogntion. Defaults to {"facebook":False,"google":False,"apple":False}.

        Returns:
            dict: Recognition pattern for all IdPs we support
        """

        # Reading the screenshot
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Storing the raw results from the logo recognition
        found = {}

        # loop over different scale factors
        for scale in np.linspace(self.scale_lower_bound, self.scale_upper_bound, self.match_intensity)[::-1]:

            # resize image to the chosen scale factor
            for idpName in logos.keys():
                if recognition[idpName]:
                    continue

                resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
                r = gray.shape[1] / float(resized.shape[1])
                counter = 1

                # loop over the different logos
                for template in logos[idpName]:
                    # Check if a matching over the max value is already found
                    # Then break the search
                    if bool(found) and idpName in found and found[idpName]['maxValue'] > self.max_matching:
                        logger.debug(
                            "....The found matching is above the max matching [" + str(
                                self.max_matching) + "]. Skip searching.")
                        break

                    # Break if the image is smaller than the template and break the search
                    (tH, tW) = template["logo_raw"].shape[:2]
                    if resized.shape[0] < tH or resized.shape[1] < tW:
                        logger.debug(
                            "The image is smaller than the template. Skip searching")
                        break

                    try:
                        logger.debug("...Scale: " + str(scale) + "\tIdP: " +
                                     idpName + "\tTemplate: " + template["filename"])
                        counter = counter + 1

                        # Find Matchings
                        result = cv2.matchTemplate(
                            resized, template["logo_raw"], self.match_algorithm)
                        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
                        logger.debug("....minVal:" + str(minVal) +
                                     "\tmaxVal:" + str(maxVal))

                        # Checking if the new findings are better than the previous ones
                        if not bool(found) or idpName not in found or maxVal > found[idpName]['maxValue']:
                            logger.debug(
                                "....The matching improved previous matchings. Storing new values.")
                            found[idpName] = {'minValue': minVal, 'maxValue': maxVal, 'minLoc': minLoc,
                                              'maxLoc': maxLoc,
                                              'r': r, 'scale': scale, 'tH': tH, 'tW': tW,
                                              'supported': True if maxVal > self.lower_bound else False,
                                              "logo": template["filename"]}

                            logger.debug("...." + str(found[idpName]))

                            # If we found somethind above the 'maxVal', we stop searching
                            if maxVal >= self.max_matching:
                                logger.debug(
                                    "....The found matching is above the upper bound [" + str(
                                        self.upper_bound) + "]. Stop searching.")
                                break
                    except Exception as e:
                        logger.error(e)

        # Store the best restuls in a dictionary and preare the results to return
        result = self.prepareMatchingResults(found=found, image_path=image_path)
        # Store the results into the database
        self.writeRecognizedPatterns(image=image, found=found, result_path=result_path, color=(255, 255, 0))
        return result

    def matchTemplate_scaleLogo(self, image_path: str, logos: dict, result_path: str, website: str,
                                recognition: dict = {"facebook": False, "google": False, "apple": False}) -> dict:
        """Find the best matching of all logos. 
        We scale the logos and search for the matching patterns within the screenshot
        Highlight the finding in the screenshot and store the results into the database

        Args:
            image_path (str): Path to the screenshot that should be analyzed
            logos (dict): Array of all logos
            result_path (str): Folder where the highlighted screenshots will be stored
            website (str): Name of the tranco domain
            recognition (_type_, optional): Init dictionary storing the results of the recogntion. Defaults to {"facebook":False,"google":False,"apple":False}.

        Returns:
            dict: Recognition pattern for all IdPs we support
        """

        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gray = image
        gray = imutils.resize(gray, width=int(gray.shape[1] * 2))
        r = image.shape[1] / float(gray.shape[1])
        # r = 1
        found = {}

        # Iterate over the supported IdPs
        for idpName in logos.keys():
            if recognition[idpName]:
                continue

            # Iterate over the configured logos for the corresponding IdP
            for template_orig in logos[idpName]:
                # loop over different scale factors
                for scale in np.linspace(self.scale_lower_bound, self.scale_upper_bound, self.match_intensity)[::-1]:

                    # resize image to the chosen scale factor
                    template = imutils.resize(
                        template_orig["logo_raw"], width=int(template_orig["logo_raw"].shape[1] * scale))
                    # r = template_orig.shape[1] / float(template.shape[1])

                    # Check if a matching over the max value is already found
                    # Then break the search
                    if bool(found) and idpName in found and found[idpName]['maxValue'] > self.max_matching:
                        logger.debug("....The found matching is above the max matching [" + str(
                            self.max_matching) + "]. Skip searching.")
                        break

                    # Break if the image is smaller than the template and break the search
                    (tH, tW) = template.shape[:2]
                    if gray.shape[0] < tH or gray.shape[1] < tW:
                        logger.debug("The image is smaller than the template. Skip searching. (%d,%d) < (%d,%d)",
                                     gray.shape[0], gray.shape[1], tH, tW)
                        break

                    try:
                        logger.debug("...Scale: " + str(scale) + "\tIdP: " + idpName + "\tTemplate: " + template_orig[
                            "filename"])

                        # Find Matchings
                        result = cv2.matchTemplate(gray, template, self.match_algorithm)
                        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
                        logger.debug("....minVal:" + str(minVal) + "\tmaxVal:" + str(maxVal))

                        if not bool(found) or idpName not in found or maxVal > found[idpName]['maxValue']:
                            logger.debug("....The matching improved previous matchings. Storing new values.")
                            found[idpName] = {'minValue': minVal, 'maxValue': maxVal, 'minLoc': minLoc,
                                              'maxLoc': maxLoc, 'r': r, 'scale': scale, 'tH': tH, 'tW': tW,
                                              'supported': True if maxVal > self.lower_bound else False,
                                              'logo': template_orig["filename"]}

                            logger.debug("...." + str(found[idpName]))
                            if maxVal >= self.max_matching:
                                logger.debug(
                                    "....The found matching is above the upper bound [" + str(
                                        self.upper_bound) + "]. Stop searching.")
                                break


                    except Exception as e:
                        logger.error(e)

        result = self.prepareMatchingResults(found=found, image_path=image_path)
        self.writeRecognizedPatterns(image=image, found=found, result_path=result_path, color=(0, 0, 255))
        return result

    def prepareMatchingResults(self, found: dict, image_path: str) -> dict:
        """Receives the raw matching results as input and prepares a better/less noisy output which is stored in the database

        Args:
            found (dict): Raw matching results
            image_path (str): Name of the screenshot file

        Returns:
            dict: Output for the report stored in the database
        """

        result = {
            "image": os.path.basename(image_path),
            "facebook": False,
            "google": False,
            "apple": False,
            "max_matching": self.max_matching,
            "upper_bound": self.upper_bound,
            "lower_bound": self.lower_bound,
            "scale_upper_bound": self.scale_upper_bound,
            "scale_lower_bound": self.scale_lower_bound,
            "match_intensity": self.match_intensity,
            "match_algorithm": self.match_algorithm,
            "logo_match": {},
            "scale": {},
            "matching_score": {},
            "logoCoordinates": {},
        }

        # Iterate over the findings for each IdP
        for idpName in found.keys():
            (minVal, maxVal, minLoc, maxLoc, r, scale, tH, tW, supported, logo) = found[idpName].values()
            (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
            (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

            result[idpName] = found[idpName]['supported']
            if result[idpName]:
                result["logo_match"][idpName] = found[idpName]['logo']
                result["scale"][idpName] = found[idpName]['scale']
                result["matching_score"][idpName] = found[idpName]['maxValue']
                result["logoCoordinates"][idpName] = [(startX + endX) / 2, (startY + endY) / 2]

        return result

    def writeRecognizedPatterns(self, image, found, result_path, color=(0, 0, 255)):

        for idpName in found.keys():
            (minVal, maxVal, minLoc, maxLoc, r, scale, tH, tW, supported, logo) = found[idpName].values()
            (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
            (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

            if maxVal > self.lower_bound:
                logger.debug("...Write found logo for: " + idpName)
                cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
            else:
                logger.debug("...No template matching found for " + idpName + ".")

        cv2.imwrite(result_path + "_recognition.png", image)

    def logoTeamplateMatching(self, screenshot_filename, analysis_path, domain_url, login_url,
                              match_intensity_scale_logo=35, match_intesity_scale_screenshot=4,
                              comprehensive_search=False,
                              init_recognition: dict = {"facebook": False, "google": False, "apple": False}) -> dict:
        start = datetime.now()
        logoLoader = LogoLoader()
        seleniumController = SeleniumController()
        result_image = analysis_path + domain_url

        self.__init__(scale_lower_bound=0.12, scale_upper_bound=0.8, match_intensity=match_intensity_scale_logo)
        recognition = self.matchTemplate_scaleLogo(logos=logoLoader.logosFiles, image_path=screenshot_filename,
                                                   result_path=result_image, website=domain_url,
                                                   recognition=init_recognition)
        recognition["duration_logo_match"] = (datetime.now() - start).seconds

        start2 = datetime.now()

        logger.info("Recognition finished. Starting verification")
        logger.info("domain_url=%s - Login Recognition before verification - google=%s - facebook=%s - apple=%s",
                    domain_url, recognition["google"], recognition["facebook"], recognition["apple"])

        verified_recognition = recognition.copy()
        verified_recognition["har"] = {}
        verified_recognition["idp_url"] = {}
        for idpName in self.supported_idps:
            if recognition[idpName]:
                idp_url, verificationStatus, har = seleniumController.verfyLoginButton(login_url=login_url, xCoordinate=
                verified_recognition["logoCoordinates"][idpName][0], yCoordinate=verified_recognition[
                    "logoCoordinates"][idpName][1], idpName=idpName, )
                verified_recognition[idpName] = verificationStatus
                verified_recognition["har"][idpName] = har
                verified_recognition["idp_url"][idpName] = idp_url

        verified_recognition["duration_verification"] = (datetime.now() - start2).seconds

        if comprehensive_search:
            if not (verified_recognition["google"] & verified_recognition["facebook"] & verified_recognition["apple"]):
                self.__init__(match_intensity=match_intesity_scale_screenshot)
                screenshot_filename = analysis_path + domain_url + "_recognition.png"
                recognition2nd = self.matchTemplate_scaleScreenshot(logos=logoLoader.logosFiles,
                                                                    image_path=screenshot_filename,
                                                                    result_path=result_image, website=domain_url,
                                                                    recognition=verified_recognition)

                for idpName in self.supported_idps:
                    if recognition2nd[idpName] and verified_recognition[idpName] == False:
                        idp_url, verificationStatus, har = seleniumController.verfyLoginButton(login_url=login_url,
                                                                                               xCoordinate=
                                                                                               recognition2nd[
                                                                                                   "logoCoordinates"][
                                                                                                   idpName][0],
                                                                                               yCoordinate=
                                                                                               recognition2nd[
                                                                                                   "logoCoordinates"][
                                                                                                   idpName][1],
                                                                                               idpName=idpName)

                        verified_recognition[idpName] = verificationStatus | verified_recognition[idpName]
                        verified_recognition['har'][idpName] = har
                        verified_recognition['idp_url'][idpName] = idp_url
                        verified_recognition["max_matching"] = recognition2nd["max_matching"]
                        verified_recognition["upper_bound"] = recognition2nd["upper_bound"]
                        verified_recognition["lower_bound"] = recognition2nd["lower_bound"]
                        verified_recognition["scale_upper_bound"] = recognition2nd["scale_upper_bound"]
                        verified_recognition["scale_lower_bound"] = recognition2nd["scale_lower_bound"]
                        verified_recognition["match_intensity"] = recognition2nd["match_intensity"]
                        verified_recognition["match_algorithm"] = recognition2nd["match_algorithm"]
                        verified_recognition["logo_match"] = recognition2nd["logo_match"]
                        verified_recognition["scale"] = recognition2nd["scale"]
                        verified_recognition["matching_score"] = recognition2nd["matching_score"]
                        verified_recognition["logoCoordinates"] = recognition2nd["logoCoordinates"]

        return verified_recognition


class LogoLoader():
    def __init__(self):
        self.logosFiles = {}
        for idpName in config.SocialLoginInformation.keys():
            cfg = os.path.dirname(os.path.realpath(__file__)) + "/" + config.SocialLoginInformation[idpName]["logos"]
            self.logosFiles[idpName] = self.readLogos(logos_path=cfg, idpName=idpName)

    def loadLogoImage(self, filepath):
        """Read logo image

        Args:
            filepath (str): Path to logo image

        Returns:
            byte: Processed image
        """
        template = cv2.imread(filepath)
        return cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    def readLogos(self, logos_path, idpName):
        """This function reads all logos for the specified IdP

        Args:
            logos_path (string): Path to the logos
            idpName (string): IdP name

        Returns:
            [array]: An array with the loaded image
        """
        filesArray = []

        for logo_filename in os.listdir(logos_path):
            if logo_filename.endswith(".jpg") or logo_filename.endswith(".png"):
                logger.debug("Reading Logo-file [" + idpName + "]: " + logo_filename)
                filesArray.append({"filename": logo_filename, "logo_raw": self.loadLogoImage(os.path.abspath(
                    os.path.join(logos_path, logo_filename)))})
        return filesArray
