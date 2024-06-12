#!/usr/bin/env python3
""" auth.py """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ returns bytes """
    utf = password.encode()
    return bcrypt.hashpw(utf, bcrypt.gensalt())
