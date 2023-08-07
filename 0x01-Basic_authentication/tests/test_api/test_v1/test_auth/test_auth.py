#!/usr/bin/env python3
"""
Tests the `api.v1.auth.auth` module.
"""
import unittest
from api.v1.auth.auth import Auth


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
        self.assertTrue(self.a.require_auth("/api/v1/users",
                                            ["/api/v1/status/", "/api/v1/stats"]))

    def test_current_user(self):
        """Tests the `current_user` method."""
        self.assertIsNone(self.a.current_user())

    def test_authorization_header(self):
        """Tests the `authorization_header` method."""
        self.assertIsNone(self.a.authorization_header())


if __name__ == "__main__":
    unittest.main()
