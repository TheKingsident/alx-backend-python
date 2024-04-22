#!/usr/bin/env python3
"""
Module on an asynchronous coroutine
"""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    Coroutine wait_random that takes in an integer argument
    (max_delay, with a default value of 10)
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
