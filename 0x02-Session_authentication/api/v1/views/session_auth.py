#!/usr/bin/env python3
"""
Module `session_auth` handles all routes for the Session Authentication.
"""

from flask import request, jsonify, make_response, abort
from typing import List
import os

from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """login route"""
    email = request.form.get("email")
    pwd = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not pwd:
        return jsonify({"error": "password missing"}), 400

    email = email.strip()
    pwd = pwd.strip()
    try:
        users: List[User] = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    for u in users:
        if not u.is_valid_password(pwd):
            continue
        return response(create_session_id(u.id), u)

    return jsonify({"error": "wrong password"}), 401


def create_session_id(user_id: str) -> str:
    """ create_session_id creates a session ID for the user. """
    from api.v1.app import auth
    return auth.create_session(user_id)


def response(session_id: str, u: User):
    """gets the response object"""
    res = make_response(jsonify(u.to_json()), 200)
    res.set_cookie(os.getenv("SESSION_NAME"), session_id)
    return res


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def logout():
    """logout a user."""
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404, description="Could not logout user using session")

    return jsonify({}), 200
