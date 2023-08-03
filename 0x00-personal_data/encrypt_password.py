#!/usr/bin/env python3
"""
This is the `encrypt_password` module. It contains the function `hash_password`
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    `hash_password` hashes the given password with a salt.

    Returns:
        bytes: The hashed password.
    """
    if not isinstance(password, str):
        return bytes("")
    return bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
