#!/usr/bin/env python3
""" api/v1/auth/auth.py """
from flask import request
from typing import List, TypeVar
import os
import fnmatch as fn


class Auth:
    """ class Auth """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns Bool """
        if path is None:
            return True
        if not excluded_paths:
            return True
        if any(fn.fnmatch(path, s) for s in excluded_paths):
            return False
        if path in excluded_paths:
            return False
        if path + '/' in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ check reuaest validity"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ return None str """
        return None

    def session_cookie(self, request=None):
        """ return cookie """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        if not session_name:
            return None
        return request.cookies.get(session_name, None)
