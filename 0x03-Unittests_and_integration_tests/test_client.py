#!/usr/bin/env python3
"""Client test module
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """ TestGithubOrgClient class
    """
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """ Test org method
        """
        # Mock the return value of get_json
        expected_result = {"org": org_name}
        mock_get_json.return_value = expected_result

        # Create GithubOrgClient instance
        client = GithubOrgClient(org_name)

        # Call the org method
        result = client.org

        # Assert that get_json was called once with the correct argument
        mock_get_json.assert_called_once_with(GithubOrgClient.ORG_URL.format(
            org=org_name))

        # Assert that the result is correct
        self.assertEqual(result, expected_result)
