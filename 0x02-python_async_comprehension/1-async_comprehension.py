#!/usr/bin/env python3
"""a module that contains the async_comprehension function"""

from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """returns a list of async generated numbers"""
    async_list = [n async for n in async_generator()]
    return async_list
