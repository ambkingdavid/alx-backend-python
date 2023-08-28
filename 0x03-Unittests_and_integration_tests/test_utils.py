#!/usr/bin/env python3
"""Test module"""

import unittest
from utils import access_nested_map as access
from utils import get_json, memoize
from parameterized import parameterized
from unittest.mock import Mock, patch
from typing import Dict


class TestAccessNestedMap(unittest.TestCase):
    """
    Test utils methods
    """
    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2),
    ])
    def test_access_nested_map(self, data, path, expected_result):
        """Test access_nested_map method"""
        result = access(data, path)
        self.assertEqual(result, expected_result)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path, output):
        """
        test_access_nested_map exception
        """
        with self.assertRaises(output):
            result = access(nested_map, path)


class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, url: str, payload: Dict):
        """
        TestCase for get_json method
        """
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = payload
            mock_get.return_value = mock_response
            result = get_json(url)
            mock_get.assert_called_once_with(url)
            self.assertEqual(result, payload)


# Define TestClass
class TestClass:
    def a_method(self):
        return 42

    @memoize
    def a_property(self):
        return self.a_method()


# Define the test class
class TestMemoize(unittest.TestCase):

    def test_memoize(self):
        # Mock a_method
        with patch.object(TestClass, 'a_method') as mock_a_method:
            # Create an instance of TestClass
            test_obj = TestClass()

            # Call a_property twice
            result1 = test_obj.a_property()
            result2 = test_obj.a_property()

            # Assert that a_method is called only once
            mock_a_method.assert_called_once()

            # Assert that the results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)


if __name__ == '__main__':
    unittest.main()
