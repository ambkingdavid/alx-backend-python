#!/usr/bin/env python3
"""
This module tests client.py
"""
import unittest
from unittest.mock import patch
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
        expected_url = GithubOrgClient.ORG_URL.format(org_name)
        mock_get_json.return_value = output
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.get_called_once_with(expected_url)
        self.assertEqual(result, output)


if __name__ == "__main__":
    unittest.main()
