from enum import Flag, auto
from util.apollon_request import ApollonRequest

MAX_HINT_LEVEL_NOTIFICATION = "Maximale Anzahl an Hinweisen erreicht. "


class TaskType(Flag):
    EULERIAN = auto()
    PLANARITY = auto()
    BIPARTITE = auto()


class FormAnswer(Flag):
    YES = auto()
    NO = auto()


class AssessmentResult(Flag):
    PASS = auto()
    FAIL = auto()
    HINT = auto()
    MAX_HINT_LEVEL_NOTIFICATION = auto()
    ERROR = auto()


## Util
def assertion_failed(message):
    return AssessmentResult.FAIL, message


def assertion_passed(message):
    return AssessmentResult.PASS, message


def provide_hint(message):
    return AssessmentResult.HINT, message


def notify_max_hint_level_reached(message):
    return AssessmentResult.MAX_HINT_LEVEL_NOTIFICATION, message


# Eulerian Graphs
# A graph is *eulerian* if there exists a walk that uses every edge exactly once.
# Equivalent: A graph is eulerian if and only if every node has even degree.
def assess_eulerian(request: ApollonRequest):
    if request.solution is None:
        if request.hint_level == 0:
            return provide_hint(
                'Definition: Ein Graph G ist eulersch,wenn es einen Kantenzug gibt, in dem jede Kante von G genau '
                'einmal auftaucht.')
        if request.hint_level == 1:
            return provide_hint(
                'Charakterisierung: Ein Graph ist genau dann eulersch, wenn jeder Knoten eine gerade Anzahl von '
                'Nachbarn hat.')
        if request.hint_level >= 2:  ##encode maximum hint_level -> when this is reached, print solution
            if request.graph.is_eulerian():
                return notify_max_hint_level_reached(MAX_HINT_LEVEL_NOTIFICATION + 'Der Graph ist eulersch.')
            else:
                number_nodes_uneven_degree = str(len([v for v in request.graph if request.graph.degree(v) % 2 == 1]))
                return notify_max_hint_level_reached(MAX_HINT_LEVEL_NOTIFICATION + 'Der Graph ist nicht eulersch.  Es '
                                                                                   'gibt '
                                                     + number_nodes_uneven_degree + ' Knoten mit ungeradem Grad.')
    else:
        is_graph_eulerian = request.graph.is_eulerian()
        participant_solution = None
        if request.solution == "yes":
            participant_solution = True
        if request.solution == "no":
            participant_solution = False

        if is_graph_eulerian == participant_solution:
            return assertion_passed("Your answer is correct.")
        else:
            return assertion_failed("Your answer is incorrect.")


# Planar Graphs
# A graph is *planar* if it can be drawn in the plane without any two edges crossing.
# Equivalent: A graph is planar if it does not have a a subgraph isomorphic to a subdivision of K_3,3 or K_5.
# Hint: A planar graph with n>2 vertices has at most 3n-6 edges.
def assess_planar(request: ApollonRequest):
    hint_level = request.hint_level
    G = request.graph
    if request.solution is None:
        if hint_level == 0:
            return provide_hint('Definition: Ein Graph ist planar wenn er so in der Ebene gezeichnet werden kann, '
                                'dass sich keine zwei Kanten überkreuzen.')
        if hint_level == 1:
            return provide_hint(
                'Charakterisierung: Ein Graph ist genau dann planar, wenn er keinen Teilgraphen enthält, der isomorph '
                'zu einer Unterteilung des K_5 bzw. K_3,3 ist.')
        if hint_level == 2:
            return provide_hint('Hinweis: Für n>2 gilt: ein planarer Graph mit n Knoten hat höchstens 3n-6 Kanten.')
        if hint_level >= 3:
            cert = G.is_planar(kuratowski=True)
            if cert[0]:  # the graph is planar
                return notify_max_hint_level_reached(MAX_HINT_LEVEL_NOTIFICATION + 'Der Graph ist planar.')
            else:
                n = len(G.vertices())
                e = len(G.edges())
                if n > 2 and e > 3 * n - 6:
                    return notify_max_hint_level_reached(MAX_HINT_LEVEL_NOTIFICATION +
                                                         'Der Graph hat ' + str(n) + ' Knoten und ' + str(e) + 'Kanten.'
                                                                                                               'Da ' + str(
                        e) + ' > 3*' + str(
                        n) + '-6  = ' + str(3 * n - 6) + ' gilt, ist der Graph nicht planar.')
                else:
                    vertex_colmap = dict()
                    vertex_colmap['r'] = cert[1].vertices()
                    vertex_colmap['w'] = [v for v in G if v not in cert[1]]
                    edge_colmap = dict()
                    edge_colmap['red'] = cert[1].edges()
                    G.show(method='matplotlib', vertex_colors=vertex_colmap, edge_colors=edge_colmap)
                    try:  ##this might take a while
                        cert[1].minor(graphs.CompleteGraph(5))
                        return notify_max_hint_level_reached(MAX_HINT_LEVEL_NOTIFICATION + 'Der Graph ist nicht '
                                                                                           'planar.  Die Knoten ' + str(
                            cert[1].vertices()) + ' bilden eine Unterteilung des K_5.')
                    except ValueError as veK5:
                        try:
                            cert[1].minor(graphs.CompleteBipartiteGraph(3, 3))
                            return notify_max_hint_level_reached(MAX_HINT_LEVEL_NOTIFICATION + 'Der Graph ist nicht '
                                                                                               'planar.  Die Knoten '
                                                                 + str(cert[1].vertices()) + 'bilden eine '
                                                                                             'Unterteilung des K_3,3.')
                        except ValueError as veK33:
                            return notify_max_hint_level_reached(MAX_HINT_LEVEL_NOTIFICATION + 'Hmm, das sollte nicht '
                                                                                               'passieren. Interner '
                                                                                               'Fehler.')
    else:
        is_graph_planar = request.graph.is_planar()
        participant_solution = None
        if request.solution == "yes":
            participant_solution = True
        if request.solution == "no":
            participant_solution = False

        if is_graph_planar == participant_solution:
            return assertion_passed("Your answer is correct.")
        else:
            return assertion_failed("Your answer is incorrect")


# Bipartite Graphs A graph is *bipartite* if its vertex set can be partitioned into two sets A and B such that no two
# vertices in A (resp. B) are connected by an edge. Equivalent: A graph is bipartite if and only if its vertices can
# be colored with two colors so that no two adjacend vertices have the same color. Equivalent: A graph is bipartite
# if and only if it does not have any cycles of odd length.
def assess_bipartite(request: ApollonRequest):
    hint_level = request.hint_level
    G = request.graph
    if request.solution is None:
        if hint_level == 0:
            return provide_hint(
                'Definition: Ein Graph G ist bipartitwenn man die Knotenmenge V(G) so in zwei disjunkte '
                'Teilmengen A und B zerlegen kann, dass es keine Kante '
                '{u,v} gibt mit u,v in A bzw. u,v in B.')
        if hint_level == 1:
            return provide_hint('Charakterisierung: Ein Graph ist genau dann bipartit, wenn er 2-färbbar ist.')
        if hint_level == 2:
            return provide_hint(
                'Charakterisierung: Ein Graph ist genau dann bipartit, wenn es keinen Kreis ungerader Länge gibt.')
        if hint_level >= 3:
            cert = G.is_bipartite(certificate=True)
            if cert[0]:  # the graph is bipartite
                A = [v for v in G if cert[1][v] == 0]
                B = [v for v in G if cert[1][v] == 1]
                return assertion_failed(MAX_HINT_LEVEL_NOTIFICATION + 'Der Graph ist bipartit.  Eine '
                                        'mögliche Zerlegung der Knotenmenge ist A = ' + str(
                    A) + ' und B = ' + str(B) + '.')  # perhaps color vertices in the drawing
                vertex_colmap = dict()
                vertex_colmap['b'] = A
                vertex_colmap['r'] = B
                G.show(method='matplotlib', vertex_colors=vertex_colmap)
            else:
                return assertion_failed(
                    MAX_HINT_LEVEL_NOTIFICATION + 'Der Graph ist nicht bipartit.  Die Knoten ' + str(
                        cert[1]) + ' bilden einen Kreis der Länge ' + str(
                        len(cert[1])) + '.')  # perhaps highlight this cycle in the drawing?!
                vertex_colmap = dict()
                vertex_colmap['r'] = cert[1]
                vertex_colmap['w'] = [v for v in G if v not in cert[1]]
                edge_colmap = dict()
                edge_colmap['red'] = [(cert[1][i], cert[1][i + 1], None) for i in range(len(cert[1]) - 1)] + [
                    (cert[1][-1], cert[1][0], None)]
                G.show(method='matplotlib', vertex_colors=vertex_colmap, edge_colors=edge_colmap)
    else:
        is_graph_bipartite = request.graph.is_bipartite()
        participant_solution = None
        if request.solution == "yes":
            participant_solution = True
        if request.solution == "no":
            participant_solution = False

        if is_graph_bipartite == participant_solution:
            return assertion_passed("Your answer is correct.")
        else:
            return assertion_failed("Your answer is incorrect")

##Prüfer Code

##Connectivity
