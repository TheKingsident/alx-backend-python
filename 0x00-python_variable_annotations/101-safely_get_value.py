#!/usr/bin/env python3
"""
Module of a typed annotated function safely_get_value
"""
from typing import Any, Mapping, Union, TypeVar

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """
    Function safely_get_value
    """
    if key in dct:
        return dct[key]
    else:
        return default
