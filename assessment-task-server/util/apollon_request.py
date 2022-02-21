import json
import logging

from util.graph_utils import parse_graph_from_json, parse_selected_vertices_from_json


class ApollonRequest:
    def __init__(self, request_body):
        self.payload = json.load(request_body)
        logging.info("Received: ", self.payload)

        if "taskType" in self.payload:
            self.task_type = self.payload["taskType"]
            logging.info("Task type: ", self.task_type)
        else:
            self.task_type = None

        if "hintLevel" in self.payload:
            self.hint_level = self.payload["hintLevel"]
            logging.info("Hint level: ", self.hint_level)
        else:
            self.hint_level = None

        if "taskDescription" in self.payload:
            self.task_description = self.payload["taskDescription"]
            logging.info("Hint level: ", self.task_description)
        else:
            self.task_description = None

        if "solution" in self.payload:
            self.solution = self.payload["solution"]
            logging.info("Hint level: ", self.solution)
        else:
            self.solution = None

        self.graph = parse_graph_from_json(self.payload)
        #  selected_vertices = parse_selected_vertices_from_json(self.payload)
