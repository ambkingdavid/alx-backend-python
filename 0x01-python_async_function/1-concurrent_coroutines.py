#!/usr/bin/env python3
"""a module that contains the wait_n func"""

import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> list:
    tasks = [wait_random(max_delay) for _ in range(n)]
    results = await asyncio.gather(*tasks)

    # Sort the results as they are gathered
    delays = []
    for delay in results:
        inserted = False
        for i, d in enumerate(delays):
            if delay < d:
                delays.insert(i, delay)
                inserted = True
                break
        if not inserted:
            delays.append(delay)

    return delays
