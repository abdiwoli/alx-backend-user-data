#!/usr/bin/env python3
""" api/v1/auth/auth.py """
from flask import request
from typing import List, TypeVar


class Auth:
    """ class Auth """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns Bool """
        return False

    def authorization_header(self, request=None) -> str:
        """ returns str """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ return None str """
        return None
