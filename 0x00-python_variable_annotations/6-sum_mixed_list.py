#!/usr/bin/env python3
"""
Module of a type-annotated function sum_mixed_list
"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[float, int]]) -> float:
    """
    Function sum_mixed_list which takes a list mxd_lst
    """
    return sum(mxd_lst)
