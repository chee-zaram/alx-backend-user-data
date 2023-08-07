#!/usr/bin/env python3
"""
Module `auth` contains the class `Auth`.
"""

from typing import List, TypeVar


class Auth:
    """
    `Auth` is the template for all authentication systems that will be
    implemented.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        `require_auth` returns false.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        `authorization_header` returns None.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        `current_user` returns None.
        """
        return None
