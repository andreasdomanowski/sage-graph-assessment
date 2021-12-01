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
    if len(selected_vertices) == 0:
        return assertion_failed("No vertex is selected.")

    if len(selected_vertices) > 1:
        return assertion_failed("You may select only one vertex for this task.")

    selected_vertex = selected_vertices[0]

    if is_cut_vertex(graph, selected_vertex):
        return assertion_passed("The selected vertex is a cut vertex.")
    else:
        return assertion_failed("The selected vertex is not a cut vertex.")


def assess_planarity(graph):
    if is_planar(graph):
        return assertion_passed("The graph is planar.")
    else:
        return assertion_failed("The graph is not planar.")


def assess_connectivity(graph):
    print(len(graph.get_vertices()))
    print(len(graph.edges()))
    if len(graph.get_vertices()) != 7 or len(graph.edges()) < 6:
        return assertion_failed("There must be exactly 7 vertices and 6 edges. "
                                "You may need to reset the task to restore the original graph.")

    if len(graph.edges()) > 7:
        return assertion_failed("Do not add any new edges.")

    if not is_connected(graph):
        return assertion_passed("You removed the correct edge. The graph is disconnected now.")
    else:
        return assertion_failed("The graph is still connected.")


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
