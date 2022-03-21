#! /usr/bin/env python
#
# Utils module
#
# by Bruno Daniel Lima


"""Utils module"""


# Standard packages
import sys
import re


def get_multiple_argument(arg, default=['']):
    """Extract n arg values and returns a list"""
    result = []
    is_arg_value = False
    for item in sys.argv:
        if item.startswith('-'):
            is_arg_value = False
        if f'-{arg}' in item:
            is_arg_value = True
            continue
        if is_arg_value:
            result.append(item)
    return result if result else default


def get_simple_argument(arg, default=''):
    """Extract arg value and return string"""
    args = get_multiple_argument(arg)
    return args[0] if args else default
