#!/usr/bin/env python3
"""a module that contains the measure_runtime function"""

import asyncio

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """measures the time taken to execute a function"""
    start_time = asyncio.get_event_loop().time()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    end_time = asyncio.get_event_loop().time()
    exec_time = end_time - start_time

    return exec_time
