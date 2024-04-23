#!/usr/bin/env python3
""" Module of an async coroutine """

import asyncio
import random
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator[float, None]:
    """ The coroutine called async_generator that takes no arguments """
    for _ in range(10):
        yield random.uniform(0, 10)
        await asyncio.sleep(1)
