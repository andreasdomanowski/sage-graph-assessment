from enum import Flag, auto
from typing import List
import json


# Task types
class FormInputType(Flag):
    CHECKBOX = auto()
    RADIO = auto()


class FormUserInterfaceComponent:
    def __init__(self, form_input_type: FormInputType, question: str,
                 form_input_answers: List[str], form_input_correct_answers: List[str]):
        if not set(form_input_correct_answers).issubset(form_input_answers):
            raise ValueError("Set of correct answers is not a subset of the set of all possible answers")
        self.form_input_type = form_input_type
        self.question = question
        self.form_input_answers = form_input_answers
        self.form_input_correct_answer = form_input_correct_answers


a = FormUserInterfaceComponent(form_input_type=FormInputType.RADIO,
                               question="question?",
                               form_input_answers=["yes", "no"],
                               form_input_correct_answers=["yes"])


def serialize_format_user_interface_component(obj):
    if isinstance(obj, FormInputType):
        return obj.name
    else:
        return obj.__dict__


