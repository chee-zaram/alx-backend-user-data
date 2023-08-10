#!/usr/bin/env python3
"""
Module `session_auth` implements a session authentication mechanism using
the class `SessionAuth` that inherits from `Auth`.
"""

from typing import Optional
from uuid import uuid4

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    `SessionAuth` class implements a session authentication mechanism.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> Optional[str]:
        """
        `create_session` creates a session ID for the given `user_id`.

        Returns:
            str: A session ID as a string.
            None:
                If `user_id` is None.
                If `user_id` is not a string or an empty string.
        """
        if not user_id or type(user_id) != str:
            return

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> Optional[str]:
        """
        `user_id_for_session_id` returns the user_id with a given session_id.

        Returns:
            str: The `user_id` associated with the given `session_id`.
            None:
                If `session_id` is None or not a string.
                If `session_id` is an empty string.
        """

        if not session_id or type(session_id) != str:
            return

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        Returns the current user using the session ID stored in the request.
        """
        return User.get(
            self.user_id_for_session_id(self.session_cookie(request))
        )
