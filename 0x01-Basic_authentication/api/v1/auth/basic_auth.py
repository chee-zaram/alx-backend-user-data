#!/usr/bin/env python3
"""
Module `basic_auth` contains the `BasicAuth` class.
This class inherits from the `Auth` class.
"""

from api.v1.auth.auth import Auth
from typing import Optional


class BasicAuth(Auth):
    """ BasicAuth class """

    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> Optional[str]:
        """
        `extract_base64_authorization_header` gets the base64 part of the
        `authorization_header` for a Basic Authentication.

        Returns:
            str: The base64 part of the `authorization_header`.
            None:
                If `authorization_header` is empty.
                If the `authorization_header` is not an instance of `str`.
                If the header value does not start with `Basic`.
        """
        exp_scheme = "Basic"
        if not authorization_header or not isinstance(
                authorization_header, str):
            return

        got_scheme_and_token = authorization_header.split(" ", 1)
        if got_scheme_and_token[0] != exp_scheme:
            return

        return got_scheme_and_token[1]
