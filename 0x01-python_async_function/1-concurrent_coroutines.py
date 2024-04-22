#!/usr/bin/env python3
""" Module of an async coroutine """

import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> list[float]:
    ''' spawn wait_random n times with the specified max_delay'''
    wait_times = []
    delays = []
    for _ in range(n):
        wait_times.append(wait_random(max_delay))

    for wait_time in asyncio.as_completed(wait_times):
        delay = await wait_time
        delays.append(delay)
    return delays
