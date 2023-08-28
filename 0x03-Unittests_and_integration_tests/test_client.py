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


if __name__ == "__main__":
    unittest.main()
