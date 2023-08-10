#!/usr/bin/env python3
"""Test `session_auth` module."""

import unittest
from os import path, remove, rename

from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth


class TestSessionAuth(unittest.TestCase):
    """Test for the `session_auth` module."""

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
        self.sa = SessionAuth()
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
        parent_class = SessionAuth.__bases__[0].__name__
        self.assertTrue(parent_class == Auth.__name__)

    def test_create_session_with_None_user_id(self):
        """Test create_session with None argument."""
        self.assertIsNone(self.sa.create_session(None))

    def test_create_session_with_non_str_user_id(self):
        """Test create_session with non str argument."""
        self.assertIsNone(self.sa.create_session(100))

    def test_create_session_with_empty_str_user_id(self):
        """Test create_session with empty str argument."""
        self.assertIsNone(self.sa.create_session(""))

    def test_create_session_with_valid_user_id(self):
        """Test create_session with valid user_id."""
        user_id = "user_id"
        s_id = self.sa.create_session(user_id)
        self.assertTrue(type(s_id) == str)
        self.assertTrue(s_id in self.sa.user_id_by_session_id)
        self.assertEqual(user_id, self.sa.user_id_by_session_id.get(s_id))

    def test_create_session_with_valid_user_id_multiple(self):
        """Test create_session with valid user id multiple."""
        user_id = "one"
        s_id_1 = self.sa.create_session(user_id)
        self.assertTrue(type(self.sa.create_session(s_id_1)) == str)
        s_id_2 = self.sa.create_session(user_id)
        self.assertTrue(type(self.sa.create_session(s_id_2)) == str)

        self.assertTrue(self.sa.user_id_by_session_id.get(s_id_1) == user_id)
        self.assertTrue(self.sa.user_id_by_session_id.get(s_id_2) == user_id)

    def test_user_id_for_session_id_with_None_user_id(self):
        """Test user_id_for_session_id."""
        self.assertIsNone(self.sa.user_id_for_session_id(None))

    def test_user_id_for_session_id_with_non_str_user_id(self):
        """Test user_id_for_session_id."""
        self.assertIsNone(self.sa.user_id_for_session_id(100))

    def test_user_id_for_session_id_with_empty_str_user_id(self):
        """Test user_id_for_session_id."""
        self.assertIsNone(self.sa.user_id_for_session_id(""))

    def test_user_id_for_session_id_with_valid_user_id(self):
        """Test user_id_for_session_id."""
        user_id = "user_id"
        s_id = self.sa.create_session(user_id)
        u_id = self.sa.user_id_for_session_id(s_id)
        self.assertTrue(type(u_id) == str)
        self.assertTrue(user_id == u_id)


if __name__ == "__main__":
    unittest.main()
