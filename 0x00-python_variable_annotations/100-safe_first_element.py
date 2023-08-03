#!/usr/bin/env python3
"""a module that defines safe_first_element function"""

from typing import Sequence, Any, Union, Optional


def safe_first_element(lst: Sequence[Any]) -> Union[Any, Optional[None]]:
    """returns a list if true or None if false"""
    if lst:
        return lst[0]
    else:
        return None
