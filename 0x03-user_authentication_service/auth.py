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
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ return new uuid """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ init class """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register user """
        hashed = _hash_password(password)
        try:
            user: User = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')
        except (NoResultFound, InvalidRequestError):
            pass
        db = DB()
        return db.add_user(email, hashed)

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
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except (ValueError, NoResultFound, InvalidRequestError):
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ return user by session id """
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user and user.session_id is not None:
                return user
        except (NoResultFound, InvalidRequestError):
            return None

    def get_user(self, **kwargs: dict) -> User:
        """ get user by email """
        try:
            return self._db.find_user_by(**kwargs)
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

    def get_reset_password_token(self, email: str) -> str:
        """ reset password token """
        user = self.get_user(email=email)
        if user:
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        else:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ update password """
        user = self.get_user(reset_token=reset_token)
        if user:
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        else:
            raise ValueError
