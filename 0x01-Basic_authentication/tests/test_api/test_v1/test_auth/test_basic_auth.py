#!/usr/bin/env python3
"""
Test for the `basic_auth` module.
"""

import unittest
from os import path, remove, rename

from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.auth import Auth
from models.user import User


class TestBasicAuth(unittest.TestCase):
    """Test for the `basic_auth` module."""

    @classmethod
    def setUpClass(cls):
        """Runs once, before any other method."""
        user_path = ".db_User.json"
        if not path.exists(user_path):
            return
        rename(user_path, user_path + ".bk")

    @classmethod
    def tearDownClass(cls):
        """Runs last, after every other method."""
        user_path = ".db_User.json"
        if not path.exists(user_path + ".bk"):
            return
        rename(user_path + ".bk", user_path)

    def setUp(self):
        """Runs before every test case."""
        self.ba = BasicAuth()
        user_path = ".db_User.json"
        if path.exists(user_path):
            remove(user_path)

    def tearDown(self):
        """Runs after every test case."""
        user_path = ".test_db_user.json"
        if path.exists(user_path):
            remove(user_path)

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

    def test_decode_base64_authorization_header_with_None(self):
        """Test decode_base64_authorization_header with None."""
        self.assertIsNone(self.ba.decode_base64_authorization_header(None))

    def test_decode_base64_authorization_header_with_non_str(self):
        """Test decode_base64_authorization_header with non-str."""
        self.assertIsNone(self.ba.decode_base64_authorization_header(100))

    def test_decode_base64_authorization_header_with_empty_str(self):
        """Test decode_base64_authorization_header with empty str."""
        self.assertIsNone(self.ba.decode_base64_authorization_header(""))

    def test_decode_base64_authorization_header_with_invalid_base64(self):
        """Test decode_base64_authorization_header with invalid base64 str."""
        invalid = "InvalidBase64$#%"
        self.assertIsNone(self.ba.decode_base64_authorization_header(invalid))

    def test_decode_base64_authorization_header(self):
        """Test decode_base64_authorization_header."""
        token = "SGVsbG8gV29ybGQ="  # Hello World
        decoded = self.ba.decode_base64_authorization_header(token)
        self.assertEqual("Hello World", decoded)

    def test_extract_user_credentials_with_None(self):
        """Test test_extract_user_credentials with None."""
        reval = self.ba.extract_user_credentials(None)
        self.assertTrue(type(reval) == tuple)
        self.assertEqual(len(reval), 2)
        for i in reval:
            self.assertIsNone(i)

    def test_extract_user_credentials_with_non_str(self):
        """Test test_extract_user_credentials with non-str."""
        reval = self.ba.extract_user_credentials(100)
        self.assertTrue(type(reval) == tuple)
        self.assertEqual(len(reval), 2)
        for i in reval:
            self.assertIsNone(i)

    def test_extract_user_credentials(self):
        """Test test_extract_user_credentials."""
        user_pwd = "cheezaram:okeke"
        user, pwd = (user_pwd.split(":"))
        reval = self.ba.extract_user_credentials(user_pwd)
        self.assertTrue(reval is not None)
        self.assertTrue(type(reval) == tuple)
        self.assertEqual(len(reval), 2)
        for i in reval:
            self.assertTrue(type(i) == str)
        got_user, got_pwd = reval
        self.assertEqual(got_user, user)
        self.assertEqual(got_pwd, pwd)

    def test_user_object_from_credentials_with_None_email(self):
        """Test user_object_from_credentials with None email."""
        self.assertIsNone(self.ba.user_object_from_credentials(None, "pwd"))

    def test_user_object_from_credentials_with_email_non_str(self):
        """Test user_object_from_credentials with email non-str."""
        self.assertIsNone(self.ba.user_object_from_credentials(100, "pwd"))

    def test_user_object_from_credentials_with_None_pwd(self):
        """Test user_object_from_credentials with None pwd."""
        self.assertIsNone(self.ba.user_object_from_credentials("a@b.c", None))

    def test_user_object_from_credentials_with_pwd_non_str(self):
        """Test user_object_from_credentials with pwd non-str."""
        self.assertIsNone(self.ba.user_object_from_credentials("a@b.c", 100))

    def test_user_object_from_credentials_with_invalid_email(self):
        """Test user_object_from_credentials with invalid email."""
        email = "cheeeee@zaram.com"
        pwd = "pwd"
        u = User()
        u.email = email
        u.password = pwd
        # We don't save so it shouldn't be in the DB.
        self.assertIsNone(self.ba.user_object_from_credentials(email, pwd))

    def test_user_object_from_credentials_with_invalid_pwd(self):
        """Test user_object_from_credentials with invalid password."""
        email = "chee@zaram.com"
        pwd = "pwd"
        u = User()
        u.email = email
        u.password = pwd
        u.save()
        self.assertIsNone(self.ba.user_object_from_credentials(email, "PWD"))

    def test_user_object_from_credentials(self):
        """Test user_object_from_credentials."""
        email = "chee@zaram.com"
        pwd = "pwd"
        u = User()
        u.email = email
        u.password = pwd
        u.save()
        got_u = self.ba.user_object_from_credentials(email, pwd)
        self.assertTrue(isinstance(got_u, User))
        self.assertEqual(got_u.email, u.email)


if __name__ == "__main__":
    unittest.main()
