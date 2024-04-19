#!/usr/bin/env python3
"""
Module of a type-annotated function sum_list
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """
    Function sum_list which takes a list input_list of floats as argument
    """
    return sum(input_list)
