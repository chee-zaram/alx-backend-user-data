#!/usr/bin/env python3
"""
Module `session_exp_auth` for creating expiration for sessions.
"""

from os import getenv
from datetime import datetime, timedelta

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth inherits from SessionAuth and sets an expiration time."""

    def __init__(self):
        """Initialize the class."""
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION", "0"))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ create a session for a user_id."""
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }

        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        `user_id_for_session_id` returns a user id associated with the
        given session id.
        """
        if session_id not in self.user_id_by_session_id:
            return

        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict["user_id"]

        if "created_at" not in session_dict:
            return

        current_time = datetime.now()
        duration = timedelta(seconds=self.session_duration)
        exp_time = session_dict["created_at"] + duration
        if exp_time < current_time:
            return
        return session_dict["user_id"]
