#!/usr/bin/env python3
""" auth.py """
import bcrypt


def _hash_password(password):
    """ returns bytes """
    utf = password.encode("utf-8")
    return bcrypt.hashpw(utf, bcrypt.gensalt())
