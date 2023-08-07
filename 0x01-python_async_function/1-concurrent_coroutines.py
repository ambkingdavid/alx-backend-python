#!/usr/bin/env python3
"""a module that contains the wait_n func"""

import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> list[float]:
    """defines a wait_n function that returns a list of delays"""
    tasks = [wait_random(max_delay) for _ in range(n)]
    delays = []

    for task in asyncio.as_completed(tasks):
        delay = await task
        delays.append(delay)

    return delays
