#!/usr/bin/env python3
"""
Module `basic_auth` contains the `BasicAuth` class.
This class inherits from the `Auth` class.
"""

from base64 import b64decode
from typing import Optional, Tuple, TypeVar
import binascii
import re

from api.v1.auth.auth import Auth
from models.user import User


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

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> Optional[str]:
        """
        `decode_base64_authorization_header` gets the decoded value of
        `base64_authorization_header`.

        Returns:
            str: The decoded value of `base64_authorization_header` as utf-8.
            None:
                If base64_authorization_header is None.
                If base64_authorization_header is not a string.
                If base64_authorization_header is not valid base64.
        """
        if not base64_authorization_header or not isinstance(
                base64_authorization_header, str):
            return

        try:
            decoded = b64decode(base64_authorization_header,
                                validate=True).decode("UTF-8")
        except (UnicodeEncodeError, binascii.Error, UnicodeDecodeError):
            return

        return decoded

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        `extract_user_credentials` gets the user credentials from the decoded
        base64 token in the authorization header.

        Returns:
            (str, str): User email and password separated by `:` in the header.
            (None, None):
                If `decoded_base64_authorization_header` is None.
                If `decoded_base64_authorization_header` is not a string.
                If `decoded_base64_authorization_header` does not contain `:`.
        """

        if not decoded_base64_authorization_header:
            return (None, None)

        if type(decoded_base64_authorization_header) != str:
            return (None, None)

        p = r'(?P<username>[^:]+):(?P<pwd>[^:]+)'
        match = re.fullmatch(p, decoded_base64_authorization_header.strip())
        if not match:
            return (None, None)

        return (match.group("username"), match.group("pwd"))

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """
        `user_object_from_credentials` gets a user instance based on the email
        and password.

        Returns:
            User: An instance of the User class.
            None:
                If `user_email` is None or not a string.
                If `user_pwd` is None or not a string.
                If the database has no record of user with given email.
                If `user_pwd` is not the password of the User instance found.
        """
        if not user_email or type(user_email) != str:
            return

        if not user_pwd or type(user_pwd) != str:
            return

        try:
            users = User.search({"email": user_email})
        except Exception:
            return

        if len(users) < 1:
            return

        for u in users:
            if not u.is_valid_password(user_pwd):
                continue
            return u

        return None
