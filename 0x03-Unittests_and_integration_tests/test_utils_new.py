#!/usr/bin/env python3
""" 0 - 1. Parameterize a unit test
"""

from utils import access_nested_map, get_json, memoize
from unittest import TestCase, main
from unittest.mock import patch, MagicMock
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

class TestGetJson(TestCase):
    """ TestGetJson class
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        mock_response = MagicMock()
        mock_response.json.return_value = test_payload
        with patch('requests.get', return_value=mock_response) as mock_get:
            result = get_json(test_url)

            self.assertEqual(result, test_payload)
            mock_get.assert_called_once_with(test_url)


if __name__ == "__main__":
    main()