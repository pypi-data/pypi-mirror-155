"""
Collection of utility functions.
"""
from typing import Iterable


def enforce_str_on_dict(dictionary: dict, keys: Iterable[str]) -> dict:
    """
    Forces a dictionary to use string values instead of objects for the given keys.
    :param dictionary: which needs transformation
    :param keys: that values needed to be transformed
    :return: the above dictionary with values changes to string
    """
    for key in keys:
        if key in dictionary:
            dictionary[key] = str(dictionary[key]) if dictionary[key] else None
    return dictionary
