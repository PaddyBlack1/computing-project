import jwt
from functools import wraps
from flask import request, jsonify, make_response, current_app
from globals import blacklist


def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return make_response(jsonify({"message": "Token is missing"}), 401)

        if blacklist.find_one({"token": token}) is not None:
            return make_response(jsonify({"message": "Token has been cancelled"}), 401)

        try:
            jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except Exception:
            return make_response(jsonify({"message": "Token is invalid"}), 401)

        return func(*args, **kwargs)

    return jwt_required_wrapper
