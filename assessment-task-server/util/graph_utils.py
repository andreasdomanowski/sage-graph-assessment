from sage.all import *


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