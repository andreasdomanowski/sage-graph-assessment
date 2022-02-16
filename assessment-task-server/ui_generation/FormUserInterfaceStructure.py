from enum import Flag, auto



class FormUserInterfaceComponent:
    def __init__(self, form_input_type, form_input_answers):
        self.form_input_type = form_input_type;
        self.form_input_answers = form_input_answers;





# Task types
class FormInputType(Flag):
    TEXT = auto()
    CHECKBOX = auto()