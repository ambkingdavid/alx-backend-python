#!/usr/bin/env python3
"""a module that contains the async_generator function"""

import asyncio
import random
from types import NoneType
from typing import Generator


async def async_generator() -> Generator[float, NoneType, NoneType] :
    """an Async generator"""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
