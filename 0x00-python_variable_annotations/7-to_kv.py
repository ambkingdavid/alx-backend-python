#!/usr/bin/python3
"""a module that defines to_kv function"""

from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    return k, float(v ** 2)
