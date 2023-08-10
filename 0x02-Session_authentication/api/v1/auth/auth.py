#!/usr/bin/env python3
"""
Module `auth` contains the class `Auth`.
"""

from typing import List, TypeVar, Union
from flask import request
import re
from os import getenv


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

        for excluded_path in map(lambda x: x.strip(), excluded_paths):
            pattern = ''
            if excluded_path[-1] == '*':
                pattern = '{}.*'.format(excluded_path[0:-1])
            elif excluded_path[-1] == '/':
                pattern = '{}/*'.format(excluded_path[0:-1])
            else:
                pattern = '{}/*'.format(excluded_path)
            if re.match(pattern, path):
                return False
        return True

    def authorization_header(
            self, request: request = None) -> Union[str, None]:
        """
        `authorization_header` returns None.
        """
        if request is None or request.headers.get("Authorization") is None:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request: request = None) -> TypeVar('User'):
        """
        `current_user` returns None.
        """
        return None

    def session_cookie(self, request: request = None) -> Union[str, None]:
        """
        `session_cookie` gets a cookie value from a request.

        Returns:
            str: Value of cookie named `_my_session_id` from request. Name of
                cookie is defined by env var `SESSION_NAME`.
            None: If request is None or not a flask.request object.
        """
        if request is None:
            return

        return request.cookies.get(getenv("SESSION_NAME"))
