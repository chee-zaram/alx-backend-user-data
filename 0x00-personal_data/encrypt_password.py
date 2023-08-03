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

    Raises:
        TypeError: If `password` is not a string.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a string type")

    return bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    `is_valid` checks if the given password matches the hashed password.

    Returns:
        bool: True if the password matches the hash, False otherwise.

    Raises:
        TypeError: If `password` is not a string or `hashed_password` is
            not bytes.
    """
    if not isinstance(hashed_password, bytes):
        raise TypeError("hashed_password must be a bytes type")
    if not isinstance(password, str):
        raise TypeError("password must be a string type")

    return bcrypt.checkpw(password.encode('UTF-8'), hashed_password)
