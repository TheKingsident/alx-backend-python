#!/usr/bin/env python3
""" 0 - 1. Parameterize a unit test
"""

from utils import access_nested_map, get_json, memoize
from unittest import TestCase, main
from parameterized import parameterized


class TestAccessNestedMap(TestCase):
    """TestAccessNestedMap class
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Method to test that the method returns what it is supposed to
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),	
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Uses the assertRaises context manager to test for KeyError(s)
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


if __name__ == "__main__":
    main()