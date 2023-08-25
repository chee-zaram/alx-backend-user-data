#!/usr/bin/env python3
"""
Module `auth` defines functions for authentication.
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes `password` using bcrypt algorithm."""
    if type(password) != str:
        raise TypeError("password must be a string")

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
