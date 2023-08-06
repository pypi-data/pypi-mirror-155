from time import sleep


class InputManager:

    @staticmethod
    def get_input_with_specific_answer_values(prompt_text, specific_values, case_sensitive=True):
        valid_input = []
        if not case_sensitive:
            for val in specific_values:
                valid_input.append(val.lower())
        else:
            valid_input = specific_values
        additional_text = " ("
        for t in specific_values:
            additional_text += t + "/"
        additional_text = InputManager.remove_suffix(additional_text, "/").__add__(")")
        additional_text.__add__(")")
        inp = input(prompt_text + additional_text)
        while not valid_input.__contains__(inp if case_sensitive else inp.lower()):
            inp = input("Invalid input! " + prompt_text + additional_text)
        if case_sensitive:
            return inp
        else:
            for specific_value in specific_values:
                if inp.lower() == specific_value.lower():
                    return specific_value

    @staticmethod
    def get_input_from_gui_with_specific_answer_values(prompt_text, specific_values, case_sensitive=True):
        from tkinter import Tk, Label, Button
        from functools import partial
        chosen = {"selection": None}
        root = Tk()
        root.geometry('350x300+0+0')

        def listener(clicked):
            root.withdraw()
            root.destroy()

            chosen['selection'] = clicked

        mylabel = Label(root, text=prompt_text)
        mylabel.grid(row=0, column=0)
        element = 2
        for val in specific_values:
            b = Button(root, text=val, command=partial(listener, val))
            b.grid(row=int(element / 2), column=element % 2)
            element += 1
        while chosen['selection'] is None:
            root.mainloop()
            sleep(1)
        return chosen['selection']

    @staticmethod
    def remove_suffix(input_string, suffix):
        if suffix and input_string.endswith(suffix):
            return input_string[:-len(suffix)]
        return input_string

    @staticmethod
    def input_valid_additional_step_type(user_input):
        if user_input.startswith("@cookie") and len(user_input.split(" ")) == 3:
            return True
        elif user_input.startswith("@wait") and len(user_input.split(" ")) == 2:
            return True
        return len(user_input.split(":")) == 1 or len(user_input.split(":")) == 2

    @staticmethod
    def get_additional_step_type_from_user_input(user_input):
        if user_input.startswith("@cookie"):
            return "@cookie"
        if user_input.startswith("@wait"):
            return "@wait"
        if len(user_input.split(":")) == 1:
            return "text"
        else:
            return user_input.split(":")[0]

    @staticmethod
    def get_additional_step_value_from_user_input(user_input):
        if user_input.startswith("@cookie "):
            return user_input.replace("@cookie ", "")
        if user_input.startswith("@wait "):
            return user_input.replace("@wait ", "")
        if len(user_input.split(":")) == 1:
            return user_input
        else:
            return user_input.split(":")[1]

    @staticmethod
    def create_supported_sso_user_inputs(known_sso):
        inputs = []
        for sso in known_sso:
            subStringLength = 0
            count = 0
            while count != 1:
                count = 0
                subStringLength += 1
                for sso_check in known_sso:
                    if sso_check[1].startswith(sso[1][0:subStringLength]):
                        count += 1
            inputs.append([sso[1][0:subStringLength], sso[1]])
        return inputs
