#!/usr/bin/env python3
"""a module that defines a safely_get_value function"""

from typing import Union, Mapping, Any, TypeVar, Optional

T = TypeVar('T')


def safely_get_value(dct: Mapping[Any, T], key: Any, default: Union
                     [T, Optional[None]] = None) -> Union[Any, T]:
    """returns a dict value"""
    if key in dct:
        return dct[key]
    else:
        return default
