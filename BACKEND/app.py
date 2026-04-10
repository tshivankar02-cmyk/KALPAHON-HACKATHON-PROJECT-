import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from models import db
from routes.auth import auth_bp
from routes.users import users_bp
from routes.campaigns import campaigns_bp
from routes.applications import applications_bp


def create_app():
    app = Flask(__name__, static_folder="../frontend", static_url_path="")
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register API blueprints under /api prefix
    for bp in (auth_bp, users_bp, campaigns_bp, applications_bp):
        app.register_blueprint(bp, url_prefix="/api")

    @app.route("/api/healthz")
    def health():
        return {"status": "ok"}

    # Serve frontend for all non-API routes (SPA support)
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")

    @app.errorhandler(404)
    def not_found(e):
        return {"message": "Not found", "code": 404}, 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return {"message": "Method not allowed", "code": 405}, 405

    @app.errorhandler(500)
    def server_error(e):
        return {"message": "Internal server error", "code": 500}, 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
