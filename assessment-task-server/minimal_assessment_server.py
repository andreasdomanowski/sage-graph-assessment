import json
import logging
import random

import bottle
from bottle import response

# Setup
from graph_assessment.graph_assessment import TaskType, assess_planar, assess_eulerian, assess_bipartite
from util.apollon_request import ApollonRequest

ASSESSMENT_RESULT_MESSAGE_KEY = "message"
ASSESSMENT_RESULT_KEY = "assessmentResponse"

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


@bottle.route('/requestTask', method='GET')
@enable_cors
def request_task_endpoint():
    param_dict = bottle.request.query.decode()
    question = "No question in response. Query does not contain a task type."
    if "taskType" in param_dict:
        task_type = param_dict["taskType"]
        if task_type == "BIPARTITE":
            question = "Is the displayed graph bipartite?"
        if task_type == "PLANARITY":
            question = "Is the displayed graph planar?"
        if task_type == "EULERIAN":
            question = "Is the displayed graph eulerian?"
    with open('resources/graph.json') as json_file:
        data = random.choice(json.load(json_file))
    return json.dumps({
        "model": data,
        "question": question
    })


@bottle.route('/graphAssessment', method='POST')
@enable_cors
def graph_assessment_endpoint():
    apollon_request = ApollonRequest(request_body=bottle.request.body)

    assessment = None

    if apollon_request.task_type == TaskType.PLANARITY.name:
        assessment = assess_planar(apollon_request)

    if apollon_request.task_type == TaskType.EULERIAN.name:
        assessment = assess_eulerian(apollon_request)

    if apollon_request.task_type == TaskType.BIPARTITE.name:
        assessment = assess_bipartite(apollon_request)

    if assessment is not None:
        # build response
        assessment_result_key = "%s" % ASSESSMENT_RESULT_KEY
        assessment_result_message_key = "%s" % ASSESSMENT_RESULT_MESSAGE_KEY

        assessment_response = {
            assessment_result_key: assessment[0].name,
            assessment_result_message_key: assessment[1]
        }

        return json.dumps(assessment_response)

    else:
        bottle.response.status = 422
        return None


bottle.run(host='0.0.0.0', port=8889, debug=True)


