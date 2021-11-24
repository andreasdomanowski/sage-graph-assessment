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


# Task Types
class TaskType(Flag):
    PLANARITY = auto()
    CONNECTIVIY = auto()
    CUT_VERTEX = auto()
    CUT_EDGE = auto()


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


def main():
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

    if input_task_type == TaskType.CUT_EDGE.name:
        assess_cut_edge(graph, selected_edge)


def assess_cut_edge(graph, selected_edge):
    if is_cut_edge(graph, (selected_edge["source"], selected_edge["destination"])):
        logging.info("The selected edge is a cut edge")
        sys.exit(0)
    else:
        logging.info("The selected edge is not a cut edge")
        sys.exit(1)


def assess_cut_vertex(graph, selected_vertex):
    if is_cut_vertex(graph, selected_vertex):
        logging.info("The selected vertex is a cut vertex")
        sys.exit(0)
    else:
        sys.exit(1)
        logging.info("The selected vertex is not a cut vertex")


def assess_planarity(graph):
    if is_planar(graph):
        logging.info("Graph is planar")
        sys.exit(0)
    else:
        logging.info("Graph is not planar")
        sys.exit(1)


def assess_connectivity(graph):
    if is_connected(graph):
        logging.info("Graph is connected")
        sys.exit(0)
    else:
        logging.info("Graph is not connected")
        sys.exit(1)


def parse_graph_from_json(json_data):
    graph = Graph()

    for vertex in json_data["vertices"]:
        graph.add_vertex(vertex)

    for edge in json_data["edges"]:
        graph.add_edge(edge[0], edge[1])

    return graph


if __name__ == "__main__":
    main()
