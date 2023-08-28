#!/usr/bin/env python3
"""Test module"""

import unittest
from utils import access_nested_map as access
from parameterized import parameterized
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)


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



if __name__ == '__main__':
    unittest.main()