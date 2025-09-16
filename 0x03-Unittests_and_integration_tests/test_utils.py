#!/usr/bin/env python3

"""
This module tests the utils.access_nested_map, utils.memoize function
"""

import unittest
from typing import Any, Dict, Mapping, Sequence
from unittest.mock import Mock, patch

from parameterized import parameterized # type: ignore
from utils import access_nested_map, get_json, memoize # type: ignore


class TestAccessNestedMap(unittest.TestCase):
    """
    test class
    """

    @parameterized.expand([ # type: ignore
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ]) 
    def test_access_nested_map(self, nested_map: Mapping[str, Any], path: Sequence[str],
                               output: Any) -> None:
        """TestCase for AccessNestedMap method"""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, output)

    @parameterized.expand([ # type: ignore
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping[str, Any], path:
                                         Sequence[str], output: Any) -> None:
        """
        TestCase for AccessNestedMap keyError
        """
        with self.assertRaises(output):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """"Test class"""
    @parameterized.expand([  # type: ignore
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])  # type: ignore
    def test_get_json(self, url: str, payload: Dict[str, Any]):
        """
        TestCase
        for get_json method
        """
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = payload
            mock_get.return_value = mock_response
            result: Dict[str, Any] = get_json(url) # type: ignore
            mock_get.assert_called_once_with(url)
            self.assertEqual(result, payload)


class TestMemoize(unittest.TestCase):
    """
    Test memoize
    """
    def test_memoize(self):
        """
        TestCase for utils.memoize
        """
        class TestClass:
            def a_method(self) -> int:
                return 42

            @memoize
            def a_property(self) -> int:
                return self.a_method()
        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_a_method:
            test_obj = TestClass()

            # Call a_property twice
            result1 = test_obj.a_property # type: ignore
            result2 = test_obj.a_property # type: ignore

            # Assert that a_method is called only once
            mock_a_method.assert_called_once()

            # Assert that the results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)


if __name__ == "__main__":
    unittest.main()
