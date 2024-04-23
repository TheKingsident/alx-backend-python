#!/usr/bin/env python3
""" Module of an async coroutine """

import asyncio
import random


async def async_generator():
    """ The coroutine called async_generator that takes no arguments """
    for _ in range(10):
        yield random.uniform(1, 10)
        await asyncio.sleep(1)
        