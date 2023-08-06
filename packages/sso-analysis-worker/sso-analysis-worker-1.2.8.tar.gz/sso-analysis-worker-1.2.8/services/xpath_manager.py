class XPathManager:
    @staticmethod
    def get_xpath_for_input_type(user_input_step_description):
        split_input = user_input_step_description.split(":")
        if len(split_input) > 2 or len(split_input) < 1:
            raise Exception("Invalid user input")

        if len(split_input) == 1 or split_input[0] == "text":
            return "//*[contains(text(), '" + (user_input_step_description.split(":")[1] if user_input_step_description.
                                               __contains__(":") else user_input_step_description) + "')]"
        else:
            return "//*[@" + split_input[0] + "=\"" + split_input[1] + "\"]"

    @staticmethod
    def get_xpath_find_search_term_in_text_and_attributes(attributes_with_explicit_info, search_terms,
                                                          text_exact_match=False):
        first = True
        xpath = "//*["
        for text in search_terms:
            if not first:
                xpath += " or "
            if text_exact_match:
                xpath += "translate(normalize-space(text()), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', " \
                         "'abcdefghijklmnopqrstuvwxyz')='" + text.lower() + "'"
            else:
                xpath += "contains(translate(normalize-space(text()), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', " \
                         "'abcdefghijklmnopqrstuvwxyz'), '" + text.lower() + "')"
            for attribute_with_explicit_info in attributes_with_explicit_info:
                if attribute_with_explicit_info[1]:
                    xpath += " or translate(@" + attribute_with_explicit_info[0] + \
                             ", 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='" + text.lower() + "'"
                else:
                    xpath += " or contains(translate(@" + attribute_with_explicit_info[0] + \
                             ", 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '" + text.lower() + "')"
            first = False
        xpath += "]"
        return xpath

    @staticmethod
    def get_xpath_find_elment_with_text_and_attributes(element_tag, attributes_with_explicit_info, search_terms,
                                                       text_exact_match=False):
        first = True
        xpath = "//" + element_tag + "["
        for text in search_terms:
            if not first:
                xpath += " or "
            if text_exact_match:
                xpath += "translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='" + text.lower() + "'"
            else:
                xpath += "contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'" + text.lower() + "')"
            for attribute_with_explicit_info in attributes_with_explicit_info:
                if attribute_with_explicit_info[1]:
                    xpath += " or translate(@" + attribute_with_explicit_info[0] + \
                             ", 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='" + text.lower() + "'"
                else:
                    xpath += " or contains(translate(@" + attribute_with_explicit_info[0] + \
                             ", 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '" + text.lower() + "')"
            first = False
        xpath += "]"
        return xpath
