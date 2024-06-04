#!/usr/bin/env python3
"""api/v1/auth/basic_auth.py """
from api.v1.auth.auth import Auth
import base64


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
                                           base64_authorization_header: str) -> str:
        """ decode value """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            return base64.b64decode(base64_authorization_header, validate=True)
        except Exception:
            return None
