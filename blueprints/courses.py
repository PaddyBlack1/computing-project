from flask import Blueprint, request, jsonify, make_response
from bson import ObjectId
from globals import courses

courses_bp = Blueprint("courses_bp", __name__)


def _serialise_course(doc):
    doc["_id"] = str(doc["_id"])
    if "reviews" in doc:
        for r in doc["reviews"]:
            if "_id" in r:
                r["_id"] = str(r["_id"])
    return doc


@courses_bp.get("/courses")
def get_all_courses():
    pn = int(request.args.get("pn", 1))
    ps = int(request.args.get("ps", 10))
    page_start = ps * (pn - 1)

    data = []
    for c in courses.find().skip(page_start).limit(ps):
        data.append(_serialise_course(c))

    return make_response(jsonify(data), 200)


@courses_bp.get("/courses/<string:course_id>")
def get_one_course(course_id):
    if not ObjectId.is_valid(course_id):
        return make_response(jsonify({"error": "Invalid course ID"}), 404)

    course = courses.find_one({"_id": ObjectId(course_id)})
    if course is None:
        return make_response(jsonify({"error": "Course not found"}), 404)

    return make_response(jsonify(_serialise_course(course)), 200)
