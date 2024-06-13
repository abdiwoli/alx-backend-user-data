#!/usr/bin/env python3
""" auth.py """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid


def _hash_password(password: str) -> bytes:
    """ returns bytes """
    utf = password.encode()
    return bcrypt.hashpw(utf, bcrypt.gensalt())


def _generate_uuid() -> str:
    """ return new uuid """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ init class """
        self._db = DB()

    def register_user(self, email: str, psw: str) -> User:
        """ register user """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')
        except (NoResultFound, InvalidRequestError):
            hashed = _hash_password(psw)
            return self._db.add_user(email, hashed)
        return

    def valid_login(self, email: str, password: str) -> bool:
        """ validate login or user """
        try:
            user = self._db.find_user_by(email=email)
            if user and bcrypt.checkpw(password.encode(),
                                       user.hashed_password):
                return True
            else:
                return False
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """ return session id """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                user.session_id = _generate_uuid()
                self._db._session.commit()
                return user.session_id
        except (NoResultFound, InvalidRequestError):
            return None

    def get_user_from_session_id(Self, session_id: str) -> User:
        """ return user by session id """
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user and user.session_id is not None:
                return user
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: int) -> None:
        """ destroy user session """
        try:
            user = self._db.find_user_by(id=user_id)
            if user:
                user.session_id = None
                self._db._session.commit()
        except (NoResultFound, InvalidRequestError):
            return None
