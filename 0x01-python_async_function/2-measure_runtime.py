#!/usr/bin/env python3
'''
Module for measurimg time for execution
'''

import time
import asyncio
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    '''
    Measure_time function with integers n and max_delay as arguments
    '''
    startTime = time.time()
    asyncio.run(wait_n(n, max_delay))
    timeUsed = time.time() - startTime

    return timeUsed / n
