import unittest
import sys, re, os
sys.path.append("..")

from warning import Warning
from setup_test import *

test_warnings = [
    str_to_warn("file1.c(10)C123:warning1"),
    str_to_warn("file1.c(10)C123:warning1"),
]

class TestWarningComparison(unittest.TestCase):
    def test_eq(self):
        """ Test equality and gt, lt of two warnings """
        w1 = test_warnings[0]
        w2 = test_warnings[1]

        self.assertTrue(w1 == w2)
        self.assertFalse(w1 != w2)
        self.assertTrue(w1 >= w2)
        self.assertTrue(w1 <= w2)
        self.assertFalse(w1 < w2)
        self.assertFalse(w1 > w2)

    def test_ne(self):
        """ Test the inequality and gt, lt comparison of two warnings """
        w1 = test_warnings[0]
        w2 = test_warnings[1]

        # Warning 2 is the most specific, so Warning 1 is greater
        w1.filename = None
        self.assertFalse(w1 == w2)
        self.assertTrue(w1 != w2)
        self.assertTrue(w1 >= w2)
        self.assertFalse(w1 <= w2)
        self.assertTrue(w1 > w2)
        self.assertFalse(w1 < w2)

        # Both Warning 1 and Warning 2 are missing parts from each other, so neither
        # are greater
        w2.code = None
        self.assertFalse(w1 == w2)
        self.assertTrue(w1 != w2)
        self.assertFalse(w1 >= w2)
        self.assertFalse(w1 <= w2)
        self.assertFalse(w1 > w2)
        self.assertFalse(w1 < w2)

if __name__ == "__main__":
    unittest.main()
