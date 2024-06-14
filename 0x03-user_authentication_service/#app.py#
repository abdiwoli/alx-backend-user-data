#!/usr/bin/env python3
""" basic flask app """
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


AUTH = Auth()


app = Flask(__name__)


@app.route("/")
def main():
    """ main """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=["POST"], strict_slashes=False)
def users():
    """ users endpoint """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or password is None:
        return jsonify({"error": "Invalid input"}), 400
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login():
    """ login function """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        out = jsonify({"email": email, "message": "logged in"})
        out.set_cookie("session_id", session_id)
        return out
    abort(401)


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """ logout function """
    session_id = request.cookies.get('session_id')
    if session_id:
        if AUTH.get_user_from_session_id(session_id):
            AUTH.destroy_session(session_id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ user profile """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """ get_reset_password_token """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=["PUT"], strict_slashes=False)
def update_password():
    ''' update pass word '''
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    password = request.form.get('new_password')
    if password:
        AUTH.update_password(reset_token, password)
        return jsonify({"email": email, "message": "Password updated"})
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
