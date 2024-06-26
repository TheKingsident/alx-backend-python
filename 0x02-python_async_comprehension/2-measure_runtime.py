#!/usr/bin/env python3
""" Module of an async coroutine """

import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """measure_runtime coroutine that will execute async_comprehension
    four times in parallel using asyncio.gather.
    """
    startTime = time.time()
    await asyncio.gather(*[async_comprehension() for _ in range(4)])
    timeUsed = time.time() - startTime
    return timeUsed
