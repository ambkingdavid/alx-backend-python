#!/usr/bin/env python3
"""
This module tests client.py
"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized_class, parameterized

from client import GithubOrgClient

from utils import (
    get_json,
    access_nested_map,
    memoize,
)
from fixtures import TEST_PAYLOAD


@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    test class
    """
    @classmethod
    def setUpClass(cls):
        # Start a patcher to mock requests.get(url).json()
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        cls.mock_get.side_effect = [
            Mock(json=lambda: cls.org_payload),
            Mock(json=lambda: cls.repos_payload),
            Mock(json=lambda: cls.org_payload),
            Mock(json=lambda: cls.repos_payload),
        ]

    @classmethod
    def tearDownClass(cls):
        # Stop the patcher to clean up
        cls.get_patcher.stop()

    def test_public_repos(self):
        # Create an instance of GithubOrgClient with your organization name
        org_name = 'google'
        client = GithubOrgClient(org_name)

        # Call the method you want to test
        repos = client.public_repos()

        # Assert that the result matches your expected value
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self, license="apache-2.0"):
        # Create an instance of GithubOrgClient with your organization name
        org_name = 'google'
        client = GithubOrgClient(org_name)

        # Call the method you want to test
        repos = client.public_repos(license)

        # Assert that the result matches your expected value
        self.assertEqual(repos, self.apache2_repos)


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google", {"key": "value"}),
        ("abc", {"key": "value"})
    ])
    @patch("client.get_json")
    def test_org(self, org_name, output, mock_get_json):
        """Test the GithubOrgClient.org method"""
        expected_url = GithubOrgClient.ORG_URL.format(org=org_name)
        mock_get_json.return_value = output
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, output)

    @parameterized.expand([
        ("google", "https://api.github.com/orgs/adobe/repos"),
        ("abc", "https://api.github.com/orgs/abc/repos"),
        ('Netflix', "https://api.github.com/orgs/Netflix/repos")
    ])
    def test_public_repos_url(self, org_name, output):
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repo_url:
            mock_public_repo_url.return_value = output
            client = GithubOrgClient(org_name)
            result = client._public_repos_url
            self.assertEqual(result, output)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        test the public_repo function
        """
        payload = {
            "repos_url": "https://api.github.com/orgs/google/repos",
            "repos": [
                {
                    "id": 7697149,
                    "node_id": "MDEwOlJlcG9zaXRvcnk3Njk3MTQ5",
                    "name": "episodes.dart",
                    "full_name": "google/episodes.dart",
                    "private": False,
                    "owner": {
                            "login": "google",
                            "id": 1342004,
                            },
                    "forks": 22,
                    "open_issues": 0,
                    "watchers": 12,
                    "default_branch": "master",
                },
                {
                    "id": 7776515,
                    "node_id": "MDEwOlJlcG9zaXRvcnk3Nzc2NTE1",
                    "name": "cpp-netlib",
                    "full_name": "google/cpp-netlib",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                        },
                    "forks": 59,
                    "open_issues": 0,
                    "watchers": 292,
                    "default_branch": "master",
                },
            ]
        }
        mock_get_json.return_value = payload["repos"]
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = payload["repos_url"]
            client = GithubOrgClient("google")
            p_repos = client.public_repos()
            self.assertEqual(p_repos, ["episodes.dart", "cpp-netlib"])
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(payload["repos_url"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, license, key, output):
        """Tests the has_license static method"""
        repo_to_check = GithubOrgClient.has_license(license, key)
        self.assertEqual(repo_to_check, output)


if __name__ == "__main__":
    unittest.main()
