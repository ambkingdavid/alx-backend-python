#!/usr/bin/env python3
"""
This module tests client.py
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


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



if __name__ == "__main__":
    unittest.main()
