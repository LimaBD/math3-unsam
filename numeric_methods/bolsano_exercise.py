#! /usr/bin/env python
#
# Numeric methods exercise - Bolsano exercise
#
# Exercise requirements:
# - with a iterator, approximate a root using bisection
#   and trisection when i is odd or even.
# - use at least two stop conditions.
# - output lines with iteration value, intervals,
#   approximated root and finally, the root with error.
#
# by Bruno Daniel Lima


"""
Numeric methods - Bolsano exercise\n
usage:\n
$ python bolsano_exercise.py --interval [-1, 3] --error 0.001\n
"""


# Standard packages
import re


# Local packages
from function import Function
import utils


# Global constants
FUNCTION = 'function'
INTERVAL = 'interval'
ERROR    = 'error'


def main():
    """Main function"""

    # Process args
    function = '5x^2+8x-2' # to input function use: utils.get_simple_argument(FUNCTION, '')
    interval = utils.get_multiple_argument(INTERVAL, [0, 0])
    error    = float(utils.get_simple_argument(ERROR, 0.0))

    # Sanitize interval
    interval = ''.join(interval)
    interval = [float(x) for x in re.findall(r'-?\d+\.?\d*', interval)]

    # Find and print root
    function = Function(function, verbose=True)
    function.nsection(interval, error, splits=[3,2])


if __name__ == '__main__':
    main()
