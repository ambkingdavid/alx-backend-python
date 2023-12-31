#!/usr/bin/env python3
"""a module that  contains the wait_random async function"""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """an async function that waits for a random delay btw 0-max_delay"""
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
