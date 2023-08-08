#!/usr/bin/env python3
"""a module that defines the measure_time function"""

import asyncio
import time

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """measures the time taken for a fuction to be completed"""
    start_time = asyncio.get_event_loop.time()
    asyncio.run(wait_n(n, max_delay))
    end_time = asyncio.get_event_loop.time()
    total_time = end_time - start_time
    return total_time / n
