#!/usr/bin/env python3
"""
Module of a type-annotated function element_length
"""
from typing import Iterable, List, Tuple, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Function element_length
    """ 
    return [(i, len(i)) for i in lst]
