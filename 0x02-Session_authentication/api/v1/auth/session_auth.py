#!/usr/bin/env python3
"""
Module `session_auth` implements a session authentication mechanism using
the class `SessionAuth` that inherits from `Auth`.
"""

from typing import Optional
from uuid import uuid4

from api.v1.auth.auth import Auth


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
