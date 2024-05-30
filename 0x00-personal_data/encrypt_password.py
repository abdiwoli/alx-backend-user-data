#!/usr/bin/env python3
""" incrypt password """
import bcrypt


def hash_password(password: str) -> bytes:
    """ secure your password """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def is_valid(hashed_password: bytes, password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
