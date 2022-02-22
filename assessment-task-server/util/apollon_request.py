import json
import logging

from util.graph_utils import parse_graph_from_json, parse_selected_vertices_from_json


class ApollonRequest:
    def __init__(self, request_body):
        self.payload = json.load(request_body)

        if "taskType" in self.payload:
            self.task_type = self.payload["taskType"]
        else:
            self.task_type = None

        if "hintLevel" in self.payload:
            self.hint_level = self.payload["hintLevel"]
        else:
            self.hint_level = None

        if "taskDescription" in self.payload:
            self.task_description = self.payload["taskDescription"]
        else:
            self.task_description = None

        if "solution" in self.payload:
            self.solution = self.payload["solution"]
        else:
            self.solution = None

        self.graph = parse_graph_from_json(self.payload)
        #  selected_vertices = parse_selected_vertices_from_json(self.payload)
