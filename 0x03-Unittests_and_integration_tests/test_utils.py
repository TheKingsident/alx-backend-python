#!/usr/bin/env python3
""" 0 - 1. Parameterize a unit test
"""

import unittest
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, MagicMock
from parameterized import parameterized
import requests


class TestAccessNestedMap(unittest.TestCase):
    """TestAccessNestedMap class
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ method to test that the method returns what it is supposed to
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """ Uses the assertRaises context manager to test for KeyError(s)
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """ TestGetJson class
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """ method to test that utils.get_json returns the expected result
        """
        expected_json = test_payload
        mock_response = MagicMock()
        mock_response.json.return_value = expected_json
        mock_get.return_value = mock_response

        result = get_json(test_url)

        self.assertEqual(result, expected_json)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """ TestMemoize class
    """
    def test_memoize(self):
        """ test_memoize method
        """
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_a_method:
            mock_a_method.return_value = 42
            instance = TestClass()

            call1 = instance.a_property
            call2 = instance.a_property

            mock_a_method.assert_called_once()

            self.assertEqual(call1, 42)
            self.assertEqual(call2, 42)


if __name__ == "__main__":
    unittest.main()
