#!/usr/bin/env python3
"""
Test `encrypt_password` module.
"""
import unittest
from encrypt_password import hash_password, is_valid


class TestEncryptPassword(unittest.TestCase):
    """Test `encrypt_password` module."""

    def test_hash_password(self) -> None:
        """Test hash_password function"""
        pwd = "test"
        hash = hash_password(pwd)
        self.assertTrue(type(hash) == bytes)
        self.assertTrue(len(hash) > 0)
        self.assertTrue(str(hash) != pwd)

    def test_is_valid(self) -> None:
        """Test is_valid function"""
        pwd = "test"
        hash = hash_password(pwd)
        self.assertTrue(is_valid(hash, pwd))
        self.assertTrue(not is_valid(hash, "test2"))


if __name__ == "__main__":
    unittest.main()
