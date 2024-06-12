#!/usr/bin/env python3
""" auth.py """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """ returns bytes """
    utf = password.encode()
    return bcrypt.hashpw(utf, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, psw: str) -> User:
        """ register user """
        try:
            hashed = _hash_password(psw)
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            return self._db.add_user(email, hashed)
        if user:
            raise ValueError(f'User {email} already exists')
        return
