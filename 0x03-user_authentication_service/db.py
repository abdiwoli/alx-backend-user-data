#!/usr/bin/env python3
""" db.py """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError, MultipleResultsFound
from user import User


Base = declarative_base()


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add to the database"""
        try:
            user = User(email=email, hashed_password=hashed_password)
        except Exception as e:
            print(f"Error adding user to database: {e}")
            self._session.rollback()
            raise
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find user by arbitrary keyword arguments"""
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound(f"No user found with criteria: {kwargs}")
        except MultipleResultsFound as e:
            raise InvalidRequestError()
        except InvalidRequestError:
            raise InvalidRequestError()
