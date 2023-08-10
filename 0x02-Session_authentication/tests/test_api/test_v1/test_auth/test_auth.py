#!/usr/bin/env python3
"""
Tests the `api.v1.auth.auth` module.
"""
import unittest
from api.v1.auth.auth import Auth
from unittest.mock import Mock
from base64 import b64encode
import os


class TestAuth(unittest.TestCase):
    """Tests the `api.v1.auth.auth` module."""

    def setUp(self):
        """Runs before every test case."""
        self.a = Auth()

    def test_require_auth(self):
        """Tests the `require_auth` method."""
        self.assertTrue(self.a.require_auth(None, None))
        self.assertTrue(self.a.require_auth(None, []))
        self.assertTrue(self.a.require_auth("/api/v1/status/", []))
        self.assertFalse(self.a.require_auth(
            "/api/v1/status/", ["/api/v1/status/"]))
        self.assertFalse(self.a.require_auth(
            "/api/v1/status", ["/api/v1/status/"]))
        self.assertTrue(self.a.require_auth(
            "/api/v1/users", ["/api/v1/status/"]))
        self.assertTrue(self.a.require_auth(
            "/api/v1/users",
            ["/api/v1/status/", "/api/v1/stats"]))

    def test_current_user(self):
        """Tests the `current_user` method."""
        self.assertIsNone(self.a.current_user())

    def test_authorization_header_no_request(self):
        """Tests the `authorization_header` method with no request argument."""
        self.assertIsNone(self.a.authorization_header())

    def test_authorization_header_no_header(self):
        """Tests the `authorization_header` method with no auth header."""
        r = Mock()
        r.headers = {}
        self.assertIsNone(self.a.authorization_header(r))

    def test_authorization_header(self):
        """Tests the `authorization_header` method with valid request."""
        r = Mock()
        token = b64encode("user:password".encode()).decode()
        r.headers = {"Authorization": "Basic {}".format(token)}
        self.assertEqual(
            self.a.authorization_header(r), r.headers["Authorization"])

    def test_session_cookie_with_invalid_key(self):
        """Tests session_cookie with invalid key request."""
        mock_request = Mock(cookies={"session_id": "123"})
        self.assertIsNone(self.a.session_cookie(mock_request))

    def test_session_cookie_with_valid_key_but_no_env_var(self):
        """Tests session_cookie with valid key but no env var."""
        mock_request = Mock(cookies={"_my_session_id": "123"})
        self.assertIsNone(self.a.session_cookie(mock_request))

    def test_session_cookie_with_valid_key_and_env_var(self):
        """Tests session_cookie with valid key and env var."""
        session_id = "123"
        mock_request = Mock(cookies={"_my_session_id": session_id})
        os.environ["SESSION_NAME"] = "_my_session_id"
        self.assertEqual(self.a.session_cookie(mock_request), session_id)
        if os.environ["SESSION_NAME"]:
            del os.environ["SESSION_NAME"]


if __name__ == "__main__":
    unittest.main()
