#!/usr/bin/env python3
"""
Test for the `basic_auth` module.
"""

import unittest
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.auth import Auth


class TestBasicAuth(unittest.TestCase):
    """Test for the `basic_auth` module."""

    def setUp(self):
        self.ba = BasicAuth()

    def test_inheritance(self):
        """Tests that BasicAuth inherits from Auth."""
        parent_class = BasicAuth.__bases__[0].__name__
        self.assertTrue(parent_class == Auth.__name__)

    def test_extract_base64_authorization_header_with_None(self):
        """Tests for `extract_base64_authorization_header` with None header."""
        self.assertIsNone(self.ba.extract_base64_authorization_header(None))

    def test_extract_base64_authorization_header_with_non_str(self):
        """Test extract_base64_authorization_header with non-str as header."""
        self.assertIsNone(self.ba.extract_base64_authorization_header(100))

    def test_extract_base64_authorization_header_with_invalid_scheme(self):
        """Test extract_base64_authorization_header with invalid scheme."""
        self.assertIsNone(self.ba.extract_base64_authorization_header(
            "Okeke Chee-zaram"))

    def test_extract_base64_authorization_header_with_invalid_format(self):
        """Test extract_base64_authorization_header with invalid format."""
        self.assertIsNone(self.ba.extract_base64_authorization_header(
            "BasicChee"))

    def test_extract_base64_authorization_header(self):
        """Test extract_base64_authorization_header."""
        header = "Basic SG9sYmVydG9uIFNjaG9vbA=="
        token = header.split(" ")[1]
        reval = self.ba.extract_base64_authorization_header(header)
        self.assertIsNotNone(reval)
        self.assertTrue(type(reval) == str)
        self.assertTrue(token == reval)


if __name__ == "__main__":
    unittest.main()
