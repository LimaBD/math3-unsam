#! /usr/bin/env python
#
# Tests for function.py module
#
# by Bruno Daniel Lima


"""Tests for function.py module"""


# Standard packages
import unittest


# Local packages
import function as func


class TestFunction(unittest.TestCase):
    """Class for testcase definition"""
    maxDiff = None


    def test_function(self):
        """Test set_function() and get_function() methods"""
        polynomial = func.Function()
        polynomial.set_function('2x^2+3x+6')
        self.assertEqual(polynomial.get_function(), '2x^2+3x+6')
        another_polynomial = func.Function('5x^2+8x+56')
        self.assertEqual(another_polynomial.get_function(), '5x^2+8x+56')


    def test_get_formated_function(self):
        """Test formatting of functions to executable strings"""
        function = func.Function('5x+8x^2+3')
        self.assertEqual(function.get_formated_function(), '5*x+8*(x**2)+3')


    def test_calc(self):
        """Test calc() method"""
        function = func.Function('5x+8x^2+3')
        self.assertEqual(function.calc(2), 45)
        self.assertEqual(function.calc(-5), 178)


    def test_bolsano_signs_condition(self):
        """Test bolsano_signs_condition()"""
        lineal = func.Function('2x+4')
        self.assertTrue(lineal.bolsano_signs_condition([-3, -1]))
        self.assertFalse(lineal.bolsano_signs_condition([3, 5]))


    def test_calc_bolsano_steps(self):
        """Test for calc_bolsano_steps()"""
        # NOTE: this calculation does not depend on the function
        function = func.Function()
        self.assertEqual(function.calc_bolsano_steps([0, 100], 1, 2), 7)
        self.assertEqual(function.calc_bolsano_steps([-7, 23], 0.01, 5), 5)


    def test_nsection(self):
        """Test nsection(), bisection() and trisection() methods to find roots"""
        ## TODO: test max steps param.
        ## TODO: test split.
        polynomial = func.Function('5x^3+9x^2+2x-4')
        self.assertEqual(polynomial.bisection([-2, 2], 0.01), (0.507, 0.0078))
        self.assertEqual(polynomial.trisection([0, 3.5], 0.0001), (0.508403, 5.9e-05))
        big_lineal = func.Function('x+200')
        self.assertEqual(big_lineal.nsection([-300, 50], 5, splits=2), (-202.5, 2.7))


    def test_get_correlative(self):
        """Test get_correlative()"""
        test_list = [3, 45, 6]
        self.assertEqual(func.get_correlative(test_list, 11), 6)
        self.assertEqual(func.get_correlative(test_list, 9), 3)


if __name__ == '__main__':
    unittest.main()
