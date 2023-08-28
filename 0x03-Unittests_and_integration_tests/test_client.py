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
    def test_org(self, org_name, output):
        """Test the GithubOrgClient.org method"""
        expected_url = f"{GithubOrgClient.ORG_URL.format(org=org_name)}"
        with patch('client.get_json', return_value=output) as mock_get_json:
            client = GithubOrgClient(org_name)
            result = client.org
            mock_get_json.assert_called_once_with(expected_url)
            self.assertEqual(result, output)


if __name__ == "__main__":
    unittest.main()