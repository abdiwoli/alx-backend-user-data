#!/usr/bin/env python3
""" api/v1/auth/session_auth.py """
from flask import request
from typing import List, TypeVar
from api.v1.auth.basic_auth import Auth
import uuid


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
        return SessionAuth.get(session_id, None)
