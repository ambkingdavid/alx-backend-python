#!/usr/bin/python3
"""a module that defines make_multiplier function"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Returns a function that takes a single float arg and returns a float"""
    def multiplier_function(x: float) -> float:
        return x * multiplier
    return multiplier_function
