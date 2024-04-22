#!/usr/bin/env python3
"""
Module of an async coroutine
"""

wait_random = __import__('0-basic_async_syntax').wait_random
import asyncio


async def wait_n(n: int, max_delay: int) -> list[float]:
    """
    Async routine called wait_n that takes in 2 int arguments
    """
    wait_times = []
    delays = []
    for _ in range(n):
        wait_times.append(wait_random(max_delay))

    for wait_time in asyncio.as_completed(wait_times):
        delay = await wait_time
        delays.append(delay)
    return delays
