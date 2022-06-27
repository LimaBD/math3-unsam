#! /usr/bin/env python
#
# Error module
#
# by Bruno Daniel Lima


"""Error module"""


def absolute_error(interval):
    """Calculate the absolute error of a interval"""
    return abs(interval[-1] - interval[0])


def remove_inaccuracy(value, error):
    """Remove imprecise decimals, removing remainder"""
    ## TODO: improve rounding
    result = (value // error) * error
    result = round(result, len(str(error)))
    return result
