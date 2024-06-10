#!/usr/bin/env python3
""" user.py """
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    """ user table """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False, unique=True)
    session_id = Column(String(250), nullable=False)
    reset_token = Column(String(250), nullable=False)

    def __repr__(self):
        s = f"<User(id={self.id}, username='{self.username}',"
        return s + " email='{self.email}')>"
