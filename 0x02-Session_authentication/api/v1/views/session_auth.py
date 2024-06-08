#!/usr/bin/env python3
""" Module of session views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """ session route """
    email = request.form.get("email")
    pswd = request.form.get("password")
    user = None
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if pswd is None:
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(user) == 0 or not user[0]:
        return jsonify({"error": "no user found for this email"}), 404
    else:
        user = user[0]
    if user and not user.is_valid_password(pswd):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    s_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    res.set_cookie(os.getenv('SESSION_NAME'), s_id)
    return res

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_delete():
    """ delete session """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
