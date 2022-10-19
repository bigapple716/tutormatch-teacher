import json
import logging
from datetime import datetime

from flask import Flask, Response, request

from teacher_resource import TeacherResource

logging.basicConfig(level=logging.INFO)

# Create the Flask application object.
app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return 'You have reached the index page!'


@app.route("/health", methods=["GET"])
def get_health():
    msg = {
        "name": "Teacher Service",
        "health": "Good",
        "at time": str(datetime.now())
    }
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/teacher/<id>", methods=["GET"])
def get_teacher_by_id(id):
    db_result = TeacherResource.get_teachers_by_id(id)
    if db_result:
        db_result = db_result[0]
        result = {'id': db_result[0], 'name': db_result[1], 'price': db_result[2], 'introduction': db_result[3]}
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/teacher", methods=["GET"])
def get_teacher():
    if not request.args:
        # get all teachers
        logging.info('request.args is empty')
        db_result = TeacherResource.get_all_teachers()
    else:
        # request.args contains duplicate keys of 'skills', e.g., /teacher?skills=Python&skills=Java
        # we need to convert them to a dict with 1 single 'skills' key and a list of skills
        arg_dict = dict(request.args.lists())
        db_result = TeacherResource.get_teachers_by_skills_and_price(skills=arg_dict['skills'],
                                                                     price_min=request.args['price_min'],
                                                                     price_max=request.args['price_max'])
    if db_result:
        result = []
        for r in db_result:
            result.append({'id': r[0], 'name': r[1], 'price': r[2], 'introduction': r[3]})
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
