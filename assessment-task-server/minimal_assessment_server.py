import json
import logging
from time import sleep

import bottle
from bottle import response

from graph_assessment import parse_graph_from_json, TaskType, assess_connectivity, assess_planarity, \
    parse_selected_vertices_from_json, assess_cut_vertex, AssessmentResult

# Setup
logging.getLogger().setLevel(logging.INFO)


# from https://stackoverflow.com/questions/17262170/bottle-py-enabling-cors-for-jquery-ajax-requests
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors


@bottle.route('/graphAssessment', method='POST')
@enable_cors
def graph_assessment_endpoint():
    sleep(1.5);
    payload_as_json = json.load(bottle.request.body)
    logging.info(payload_as_json)

    input_task_type = payload_as_json["taskType"]
    logging.info("Task type: " + input_task_type)

    graph = parse_graph_from_json(payload_as_json)
    selected_vertices = parse_selected_vertices_from_json(payload_as_json)

    assessment = None

    if input_task_type == TaskType.CONNECTIVITY.name:
        assessment = assess_connectivity(graph)

    if input_task_type == TaskType.PLANARITY.name:
        assessment = assess_planarity(graph)

    if input_task_type == TaskType.CUT_VERTEX.name:
        assessment = assess_cut_vertex(graph, selected_vertices)

    # not yet implemented in the frontend
    # if input_task_type == TaskType.CUT_EDGE.name:
    # assess_cut_edge(graph, selected_edge)

    if assessment is not None:
        # build response
        assessment_result_key = "assessmentResponse"
        assessment_result_message_key = "message"

        assessment_response = {
            assessment_result_key: assessment[0].name,
            assessment_result_message_key: assessment[1]
        }

        return json.dumps(assessment_response)

    else:
        bottle.response.status = 422
        return None


bottle.run(host='0.0.0.0', port=8889, debug=True)
