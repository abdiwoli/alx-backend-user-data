#!/usr/bin/env python3
"""api/v1/auth/basic_auth.py """
from api.v1.auth.auth import Auth


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
