#!/usr/bin/env python3
"""
Module of a type-annotated function to_kv
"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Function to_kv  that takes a string k and an int OR float v as arguments
    """
    return (k, float(v ** 2))
