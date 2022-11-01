import json
import logging
from collections import defaultdict
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
    skills = TeacherResource.get_skills_by_ids([id])
    skills = [e[1] for e in skills]  # squeeze the last dimension
    if db_result:
        db_result = db_result[0]
        result = {'id': db_result[0], 'name': db_result[1], 'price': db_result[2], 'introduction': db_result[3],
                  'skills': skills}
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
        result, teacher_ids = [], []

        # get skills for each teacher
        for r in db_result:
            teacher_ids.append(r[0])
        # example of id_and_skills: ((1, 'Java'), (1, 'Python'), (1, 'Go'), (2, 'Python'), (2, 'C'))
        id_and_skills = TeacherResource.get_skills_by_ids(teacher_ids)
        id_to_skills = defaultdict(list)
        for t in id_and_skills:
            id_to_skills[t[0]].append(t[1])

        for r in db_result:
            result.append({'id': r[0], 'name': r[1], 'price': r[2], 'introduction': r[3], 'skills': id_to_skills[r[0]]})
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/teacher", methods=["POST"])
def add_new_teacher():
    # request.args contains duplicate keys
    # we need to convert them to a dict with 1 single key and a list of values
    arg_dict = dict(request.args.lists())

    # add a row in teacher_info table
    new_teacher_id = TeacherResource.add_teacher_info(name=request.args['name'], price=request.args['price'],
                                                      introduction=request.args['introduction'])

    # add rows in skills table
    for skill in arg_dict['skills']:
        TeacherResource.add_skill(new_teacher_id, skill)

    # return the id in response
    rsp = Response(json.dumps(new_teacher_id), status=200, content_type="application.json")
    return rsp


@app.route("/teacher/<id>/available_time/<date>", methods=["GET"])
def get_available_time_by_id_and_date(id, date):
    db_result = TeacherResource.get_available_time_by_id_and_date(id, date)
    result = {'hour': []}
    if db_result:
        for hour in db_result:
            result['hour'].append(hour[0])
    rsp = Response(json.dumps(result), status=200, content_type="application.json")

    return rsp


@app.route("/teacher/<id>/available_time/<date>", methods=["PUT"])
def update_available_time_by_id_and_date(id, date):
    hour, occupied = request.args['hour'], request.args['occupied']
    TeacherResource.update_available_time_by_id_and_date(teacher_id=id, date=date, hour=hour,
                                                         occupied=occupied)

    # return the id in response
    rsp = Response("SUCCEED", status=200, content_type="text/plain")
    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
