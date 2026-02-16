import datetime
import jwt
from flask import Blueprint, request, jsonify, make_response, current_app
from globals import blacklist
from decorators import jwt_required

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.get("/login")
def login():
    auth = request.authorization
    if auth and auth.password == "password":
        token = jwt.encode(
            {
                "user": auth.username,
                "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return make_response(jsonify({"token": token}), 200)

    return make_response(
        "Could not verify",
        401,
        {"WWW-Authenticate": 'Basic realm="Login required"'},
    )


@auth_bp.get("/logout")
@jwt_required
def logout():
    token = request.headers["x-access-token"]
    blacklist.insert_one({"token": token})
    return make_response(jsonify({"message": "Logout successful"}), 200)
