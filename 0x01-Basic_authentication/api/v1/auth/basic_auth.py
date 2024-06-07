#!/usr/bin/env python3
"""api/v1/auth/basic_auth.py """
from api.v1.auth.auth import Auth
import base64
from models.base import Base
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ class Bacic """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extract base64 text """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if authorization_header.startswith("Basic "):
            return authorization_header.split(" ")[1]
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization: str) -> str:
        """ decode value """
        if base64_authorization is None:
            return None
        if not (isinstance(base64_authorization, str)):
            return None
        try:
            valu = base64.b64decode(base64_authorization, validate=True)
            return valu.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(self, auth_header: str) -> (str, str):
        """ returns user and password """
        if auth_header is None:
            return (None, None)
        if not isinstance(auth_header, str):
            return (None, None)
        if ":" not in auth_header:
            return (None, None)
        value = auth_header.split(":")
        return (value[0], ":".join(value[1:]))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ user object """
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({"email": user_email})
        except Exception:
            return None
        if not user or len(user) == 0:
            return None
        if len(user) == 1:
            user = user[0]
            if user.is_valid_password(user_pwd):
                return user
            else:
                return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ The last task to get the user
        """
        header = self.authorization_header(request)
        token = self.extract_base64_authorization_header(header)
        auth_token = self.decode_base64_authorization_header(token)
        email, pswd = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, pswd)
