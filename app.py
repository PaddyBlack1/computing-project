import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from blueprints.auth import auth_bp
from blueprints.courses import courses_bp
from blueprints.reviews import reviews_bp
from blueprints.statistics import stats_bp

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "secret-key")
    CORS(app)

    @app.get("/api/v1.0/health")
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
