#!/usr/bin/env python3
"""a module that defines a sum_mixed_list function"""

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Returns the sum of the list"""
    return float(sum(mxd_lst))
