#!/usr/bin/env python3
""" api/v1/auth/session_auth.py """
from flask import request
from typing import List, TypeVar
from api.v1.auth.basic_auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """ session auth that extends Auth """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ instance method """
        if user_id is None or not isinstance(user_id, str):
            return None
        self.id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[self.id] = user_id
        return self.id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ return session id"""
        return SessionAuth.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> TypeVar('User'):
        '''return user '''
        session_id = self.session_cookie(request)
        return User.get(self.user_id_for_session_id(session_id))

    def destroy_session(self, request=None) -> bool:
        """ delete user session """
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if not cookie:
            return False
        user_id = self.user_id_for_session_id(cookie)
        if not user_id:
            return False
        del self.user_id_by_session_id[cookie]
        return True
