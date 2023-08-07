import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """defines a function that returns a asyncio object"""
    task = asyncio.create_task(wait_random(max_delay))
    return task
