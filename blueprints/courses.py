
from flask import Blueprint, request, jsonify, make_response
from bson import ObjectId
from globals import courses

courses_bp = Blueprint("courses_bp", __name__)

def _serialise_course(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@courses_bp.route("/courses", methods=["GET"])
def get_all_courses():
    pn = int(request.args.get("pn", 1))
    ps = int(request.args.get("ps", 10))
    page_start = ps * (pn - 1)

    data = []
    for c in courses.find().skip(page_start).limit(ps):
        data.append(_serialise_course(c))

    return make_response(jsonify(data), 200)

@courses_bp.route("/courses/<string:course_id>", methods=["GET"])
def get_one_course(course_id):
    course = courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        return make_response(jsonify({"error": "Course not found"}), 404)
    return make_response(jsonify(_serialise_course(course)), 200)
