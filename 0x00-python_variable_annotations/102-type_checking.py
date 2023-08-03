#!/usr/bin/env python3
"""a module that defines """

from typing import List, Tuple


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """returns a list"""
    zoomed_in = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array = (12, 72, 91)

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)
