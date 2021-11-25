import logging

from enum import Flag, auto

from sage.all import *
from sage.graphs.planarity import is_planar
from sage.graphs.connectivity import is_connected
from sage.graphs.connectivity import is_cut_edge
from sage.graphs.connectivity import is_cut_vertex

import argparse
import json

# Setup
logging.getLogger().setLevel(logging.INFO)


# Task types
class TaskType(Flag):
    PLANARITY = auto()
    CONNECTIVITY = auto()
    CUT_VERTEX = auto()
    CUT_EDGE = auto()


# Assessment results
class AssessmentResult(Flag):
    PASS = auto()
    FAIL = auto()
    ERROR = auto()


def main():
    # Initialize help message for script arguments
    task_type_help = "must be one of the following: "
    first = True
    for input_task_type in TaskType:
        if first:
            first = False
            task_type_help += input_task_type.name
        else:
            task_type_help += "," + input_task_type.name

    parser = argparse.ArgumentParser()
    parser.add_argument("-task", help=task_type_help, required=True)
    parser.add_argument("-file", help="path to the json-file containing the graph data", required=True)
    args = parser.parse_args()
    # validate task type
    input_task_type = args.task
    if input_task_type not in [t.name for t in TaskType]:
        raise argparse.ArgumentError("The specified task type does not match the available task types."
                                     "Execute this script with the flag \"--help\" to see the available task types.")

    logging.info("Task: " + args.task)
    logging.info("Path to file containing the graph (JSON): " + args.file)

    # Get file contents and parse them
    parsed_json = json.load(open(args.file))

    # Read graph and selections from JSON
    graph = parse_graph_from_json(parsed_json)
    selected_vertex = parsed_json["selectedVertex"]
    selected_edge = parsed_json["selectedEdge"]

    if input_task_type == TaskType.CONNECTIVIY.name:
        assess_connectivity(graph)

    if input_task_type == TaskType.PLANARITY.name:
        assess_planarity(graph)

    if input_task_type == TaskType.CUT_VERTEX.name:
        assess_cut_vertex(graph, selected_vertex)


#    if input_task_type == TaskType.CUT_EDGE.name:
#        assess_cut_edge(graph, selected_edge)


# def assess_cut_edge(graph, selected_edges):
#    if is_cut_edge(graph, (selected_edges["source"], selected_edges["destination"])):
#        return assertion_passed("The selected edge is a cut edge")
#    else:
#        return assertion_failed("The selected edge is not a cut edge")


def assess_cut_vertex(graph, selected_vertices):
    if is_cut_vertex(graph, selected_vertices):
        return assertion_passed("The selected veritces are all cut certices")
    else:
        return assertion_failed("The selected vertex is not a cut vertex")


def assess_planarity(graph):
    if is_planar(graph):
        return assertion_passed("The graph is planar.")
    else:
        return assertion_failed("The graph is not planar.")


def assess_connectivity(graph):
    if is_connected(graph):
        return assertion_passed("The graph is connected")
    else:
        return assertion_failed("The graph is not connected.")


def parse_graph_from_json(json_data):
    graph = Graph()

    for vertex in json_data["elements"]:
        graph.add_vertex(name=vertex["id"])

    for edge in json_data["relationships"]:
        source = edge["source"]["element"]
        target = edge["target"]["element"]
        graph.add_edge(source, target)

    return graph


def parse_selected_vertices_from_json(json_data):
    selected_vertices = []

    for vertex in json_data["elements"]:
        if vertex["marking"]:
            selected_vertices.append(vertex["id"])

    return selected_vertices


def assertion_failed(message):
    return AssessmentResult.FAIL, message


def assertion_passed(message):
    return AssessmentResult.PASS, message


if __name__ == "__main__":
    main()
