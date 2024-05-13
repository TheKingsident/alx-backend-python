#!/usr/bin/env python3
"""Client test module
"""

import unittest
from unittest.mock import PropertyMock, patch
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
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

    def test_public_repos_url(self):
        """ Test _public_repos_url method
        """

        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock,
                   return_value={
                       'repos_url': 'https://api.github.com/orgs/google/repos'}
                   ) as patched:
            client = GithubOrgClient("Google")
            result = client._public_repos_url
            self.assertEqual(result, patched.return_value['repos_url'])

    @patch('client.get_json')
    @patch.object(GithubOrgClient, '_public_repos_url',
                  new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """ Test _public_repos method
        """
        url = 'https://api.github.com/orgs/google/repos'
        mock_public_repos_url.return_value = url
        # Mock the get_json function
        mock_get_json.return_value = [
            {'name': 'repo1', 'license': {'key': 'MIT'}},
            {'name': 'repo2', 'license': None},
            {'name': 'repo3', 'license': {'key': 'GPL'}}
        ]

        client = GithubOrgClient("Google")

        result = client.public_repos(license='MIT')

        self.assertEqual(result, ['repo1'])

        mock_public_repos_url.assert_called_once()

        mock_get_json.assert_called_once_with(url)

    @parameterized.expand([
        # Test case 1: repo has the expected license
        [{'license': {'key': 'my_license'}}, 'my_license', True],
        # Test case 2: repo has a different license
        [{'license': {'key': 'other_license'}}, 'my_license', False],
        # Test case 3: repo does not have a license
        [{}, 'my_license', False],
        # Test case 4: repo has no license key
        [{'license': {}}, 'my_license', False],
    ])
    def test_has_license(self, repo, license_key, expected_result):
        # Create an instance of GithubOrgClient
        client = GithubOrgClient("Google")
        # Call the has_license method
        result = client.has_license(repo, license_key)
        # Assert that the result is what we expect
        self.assertEqual(result, expected_result)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ TestIntegrationGithubOrgClient class
    """
    @classmethod
    def setUpClass(cls):
        """ testing patcher setup """
        cls.get_patcher = patch('requests.get')
        cls.mock = cls.get_patcher.start()
        cls.mock.return_value.json.side_effect = [
            cls.org_payload, cls.repos_payload,
            cls.org_payload, cls.repos_payload,
        ]

    @classmethod
    def tearDownClass(cls):
        """ tearDown class
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ Test _public_repos method
        """
        client = GithubOrgClient("Google")
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("random"), [])

    def test_public_repos_with_license(self):
        """ Test _public_repos_with_license method
        """
        client = GithubOrgClient("Google")
        self.assertEqual(client.public_repos(license="apache-2.0"),
                         self.apache2_repos)
