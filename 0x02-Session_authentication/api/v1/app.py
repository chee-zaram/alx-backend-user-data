#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv("AUTH_TYPE") == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif getenv("AUTH_TYPE") == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif getenv("AUTH_TYPE") == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()

AUTH_EXCLUDED_PATHS = (
    "/api/v1/status/",
    "/api/v1/unauthorized/",
    "/api/v1/forbidden/",
)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def error_unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def error_forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def auth_filter() -> None:
    """ Filters which requests need authentication
    """
    if auth is None:
        return

    if not auth.require_auth(request.path, AUTH_EXCLUDED_PATHS):
        return

    if not auth.authorization_header(request):
        abort(401, description="User Unauthorized")

    if not auth.current_user(request):
        abort(403, description="User Forbidden")

    request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
