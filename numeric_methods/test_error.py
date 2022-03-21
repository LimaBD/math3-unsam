#! /usr/bin/env python
#
# Tests for error.py module
#
# by Bruno Daniel Lima


"""Tests for error.py module"""


# Standard packages
import unittest


# Local packages
import error as err


class TestError(unittest.TestCase):
    """Class for testcase definition"""
    maxDiff = None


    def test_absolute_error(self):
        """Test absolute_error()"""
        self.assertEqual(err.absolute_error([-3, 2]), 5)


    def test_remove_inaccuracy(self):
        """Test remove_inaccuracy()"""
        self.assertEqual(err.remove_inaccuracy(0.3290955281676, 0.01), 0.32)
        self.assertEqual(err.remove_inaccuracy(364674, 2), 364674)
        self.assertEqual(err.remove_inaccuracy(2.5083955281676, 0.00001), 2.50839)


if __name__ == '__main__':
    unittest.main()
