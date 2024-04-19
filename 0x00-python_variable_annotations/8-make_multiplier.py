#!/usr/bin/env python3
"""
Module of a type-annotated function make_multiplier
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Function make_multiplier that takes a float multiplier as argument
    """
    def multiplier_func(x: float) -> float:
        return x * multiplier

    return multiplier_func
