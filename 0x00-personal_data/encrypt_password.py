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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    `is_valid` checks if the given password matches the hashed password.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(password.encode('UTF-8'), hashed_password)
