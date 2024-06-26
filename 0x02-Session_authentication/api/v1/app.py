#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = os.environ.get('AUTH_TYPE', None)
exclude = ['/api/v1/status/', '/api/v1/unauthorized/',
           '/api/v1/forbidden/', '/api/v1/auth_session/login/']
if auth:
    if auth == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif auth == "session_auth":
        auth = SessionAuth()
    elif auth == "session_exp_auth":
        auth = SessionExpAuth()
    elif auth == "session_db_auth":
        auth = SessionDBAuth()
    else:
        from api.v1.auth.basic_auth import Auth
        auth = Auth()


@app.before_request
def authenticate_user():
    """Authenticates a user before processing a request.
    """
    if auth:
        if auth.require_auth(request.path, exclude):
            auth_header = auth.authorization_header(request)
            user = auth.current_user(request)
            if auth.authorization_header(request) is None:
                if auth.session_cookie(request) is None:
                    abort(401)
            if user is None:
                abort(403)
        request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthrorized(error) -> str:
    """ un authorozed """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def handle_forbiden(error) -> str:
    """ un authorozed """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
