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
        `require_auth` tells if the given `path` requires authentication.

        This method is slash tolerant i.e:
        `path=/api/v1/status` and `path=/api/v1/status/` return False if
        `excluded_paths` contains `/api/v1/status/`.

        Returns:
            True: If `path` is None. If `excluded_paths` is None or empty.
            False: If `path` is in `excluded_paths`

        Raises:
            TypeError: If `path` is not a string.
                If `excluded_paths` is not a List of strings.
        """
        if not path or not excluded_paths:
            return True

        if not isinstance(path, str):
            raise TypeError("path must be a string")

        try:
            excluded_paths = list(excluded_paths)
        except Exception:
            raise TypeError("excluded_paths must be a list")

        if not all(isinstance(p, str) for p in excluded_paths):
            raise TypeError("excluded_paths must be a list of strings")

        # We need to make the method slash-tolerant.
        # We standardize all paths to have a trailing slash.
        excluded_paths_copy = excluded_paths.copy()
        if path[-1] != "/":
            path = path + "/"

        for i, p in enumerate(excluded_paths_copy):
            if path == p:
                return False
            if p[-1] == "/":
                continue
            excluded_paths_copy[i] = p + "/"
            if path == excluded_paths_copy[i]:
                return False

        return True

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
