from flask import Blueprint, request, jsonify, make_response
from bson import ObjectId
from globals import courses
from decorators import jwt_required

reviews_bp = Blueprint("reviews_bp", __name__)


def _serialise_review(r):
    if "_id" in r:
        r["_id"] = str(r["_id"])
    return r


@reviews_bp.get("/courses/<string:course_id>/reviews")
def get_course_reviews(course_id):
    if not ObjectId.is_valid(course_id):
        return make_response(jsonify({"error": "Invalid course ID"}), 404)

    course = courses.find_one({"_id": ObjectId(course_id)}, {"reviews": 1})
    if course is None:
        return make_response(jsonify({"error": "Course not found"}), 404)

    reviews = course.get("reviews", [])
    return make_response(jsonify([_serialise_review(r) for r in reviews]), 200)


@reviews_bp.post("/courses/<string:course_id>/reviews")
@jwt_required
def add_course_review(course_id):
    if not ObjectId.is_valid(course_id):
        return make_response(jsonify({"error": "Invalid course ID"}), 404)

    if not request.is_json:
        return make_response(jsonify({"error": "Expected JSON body"}), 400)

    body = request.get_json()
    required = ("username", "comment", "stars")
    if not all(k in body for k in required):
        return make_response(jsonify({"error": "Missing review fields"}), 404)

    new_review = {
        "_id": ObjectId(),
        "username": body["username"],
        "comment": body["comment"],
        "stars": body["stars"],
    }

    result = courses.update_one(
        {"_id": ObjectId(course_id)},
        {"$push": {"reviews": new_review}},
    )

    if result.matched_count != 1:
        return make_response(jsonify({"error": "Course not found"}), 404)

    return make_response(jsonify(_serialise_review(new_review)), 201)
