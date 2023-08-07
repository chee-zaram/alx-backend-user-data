#!/usr/bin/env python3
"""
Tests the `api.v1.auth.auth` module.
"""
import unittest
from api.v1.auth.auth import Auth


class TestAuth(unittest.TestCase):
    """Tests the `api.v1.auth.auth` module."""

    def test_auth(self):
        """Test the `auth` module."""
        a = Auth()
        reval = a.require_auth("/api/v1/status/", ["/api/v1/status/"])
        self.assertFalse(reval)
        reval = a.current_user()
        self.assertIsNone(reval)
        reval = a.authorization_header()
        self.assertIsNone(reval)


if __name__ == "__main__":
    unittest.main()
