#!/usr/bin/env python3
"""Test module"""

import unittest
from utils import access_nested_map as access
from parameterized import parameterized


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
        ({}, ("a",), "Key 'a' not found in nested_map"),
        ({"a": 1}, ("a", "b"), "Key 'b' not found in nested_map"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_error_message):
        with self.assertRaises(KeyError) as context:
            access(nested_map, path)
        
        self.assertEqual(str(context.exception), expected_error_message)


if __name__ == '__main__':
    unittest.main()
