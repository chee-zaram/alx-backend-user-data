#!/usr/bin/env python3
"""
Module `session_db_auth` handles database transactions for session-based
authentication with IDs in the database.
"""

from datetime import datetime, timedelta
from typing import Optional

from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """`Session` inherits from `SessionExpAuth` and give storage support.
    """

    def create_session(self, user_id: str = None) -> Optional[str]:
        """Creates and stores a session id for the user.
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return

        kwargs = {
            "user_id": user_id,
            "session_id": session_id,
        }
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> Optional[str]:
        """
        `user_id_for_session_id` returns a user id associated with the
        given session id.
        """
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return

        if len(sessions) < 1:
            return

        current_time = datetime.now()
        duration = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + duration
        if exp_time < current_time:
            return

        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """
        `destroy_session` deletes the user session and logs out.

        Returns:
            True: If the session ID for the user is deleted successfully.
            False:
                - If `request` is None.
                - If the session cookie is not set, or its value is not a valid
                  session ID.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return False

        if len(sessions) < 1:
            return False

        sessions[0].remove()
        return True
