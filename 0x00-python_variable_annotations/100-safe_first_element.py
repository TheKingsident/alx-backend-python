#!/usr/bin/env python3
"""
Module of a duck-typed annotated function safe_first_element
"""
from typing import Sequence, Union, Any, NoneType

def safe_first_element(lst: Sequence[Any]) -> Union[Any, NoneType]:
    """
    Function safe_first_element
    """
    if lst:
        return lst[0]
    else:
        return None
