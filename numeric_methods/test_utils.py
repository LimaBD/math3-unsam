#! /usr/bin/env python
#
# Tests for utils.py module
#
# by Bruno Daniel Lima


"""Tests for utils.py module"""


# Standard packages
import sys
import unittest


# Local packages
import utils


class TestUtils(unittest.TestCase):
    """Class for testcase definition"""
    maxDiff = None


    def test_get_argument(self):
        """Test get_simple_argument() and get_multiple_argument()"""
        sys.argv = ['--url', 'google.com', 'yahoo.com', '--path', '/home/test/urls.txt']
        self.assertEqual(utils.get_simple_argument('path'), '/home/test/urls.txt')
        self.assertEqual(utils.get_multiple_argument('url'), ['google.com', 'yahoo.com'])
        self.assertEqual(utils.get_multiple_argument('extension', '.com'), '.com')


if __name__ == '__main__':
    unittest.main()
