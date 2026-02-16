# app.py
from flask import Flask, jsonify
from flask_cors import CORS

from blueprints.auth import auth_bp
from blueprints.courses import courses_bp
from blueprints.reviews import reviews_bp
from blueprints.statistics import stats_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "change_me_now"
    CORS(app)

    @app.route("/api/v1.0/health", methods=["GET"])
    def health():
        return jsonify({"ok": True})

    app.register_blueprint(auth_bp, url_prefix="/api/v1.0")
    app.register_blueprint(courses_bp, url_prefix="/api/v1.0")
    app.register_blueprint(reviews_bp, url_prefix="/api/v1.0")
    app.register_blueprint(stats_bp, url_prefix="/api/v1.0")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
