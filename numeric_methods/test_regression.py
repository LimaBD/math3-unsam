#!/usr/bin/env python3
#
# Tests for regression.py module
#
# by Bruno Daniel Lima


"""Tests for regression.py module"""


# Standard packages
import unittest


# Local packages
from regression import LinearRegression, Point


class TestUtils(unittest.TestCase):
    """Class for testcase definition"""
    maxDiff = None

    points = [Point(2, 5),
              Point(3, 8),
              Point(4, 7),
              Point(5, 9)]
    linear = LinearRegression(points)

    def test_slope(self):
        """Test for calc_slope() and get_slope()"""
        self.assertTrue( 1.05 < self.linear.get_slope() < 1.15 )

    def test_y_interception(self):
        """
        Test for calc_y_interception() and
        get_y_interception()
        """
        self.assertTrue( 3.35 < self.linear.get_y_interception() < 3.45 )

    def test_get_function(self):
        """Test for get_function()"""
        ## TODO: WORK-IN-PROGRESS

    def test_calc(self):
        """Test for calc(x_value)"""
        ## TODO: WORK-IN-PROGRESS

    def test_get_square_error(self):
        """Test for get_square_error()"""
        self.assertTrue( 2.65 < self.linear.get_square_error() < 2.75 )

    def test_get_domain(self):
        """Test for get_domain()"""
        self.assertEqual(self.linear.get_domain(), [2, 5])


if __name__ == '__main__':
    unittest.main()
