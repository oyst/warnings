import unittest
import sys, re, os
sys.path.append("..")

from warning import Warning
from build_log import BuildLog
from override import Override
from suppression import Suppression

from setup_test import *

test_warnings = [
    str_to_warn("file1.c(10)C123:warning1"),
    str_to_warn("path/to/file2.c(20)C45:warning2"),
]

override_test_warnings = test_warnings[:]

class TestBuildLog(unittest.TestCase):
    def test_init(self):
        """ Test the initalisation of build logs """
        log = BuildLog()

        # An unpopulated build log should be completely empty
        self.assertIsNone(log.name)
        self.assertIsNone(log.compiler)
        self.assertEqual(log.warnings, [])
        self.assertEqual(log.suppressed, [])
        self.assertEqual(log.overridden, [])
        self.assertEqual(log.warning_count(), 0)

    def test_populate_from_warnings(self):
        """ Test the population of build logs from a list of Warnings """
        log = BuildLog.from_warnings(test_warnings)
        self.assertIsNone(log.name)
        self.assertIsNone(log.compiler)
        for warning in log.warnings:
            self.assertIn(warning, test_warnings)
        self.assertEqual(log.suppressed, [])
        self.assertEqual(log.overridden, [])
        self.assertEqual(log.warning_count(), len(test_warnings))

    def test_populate_from_string(self):
        """ Test the population of build logs from a string of warning text """
        string = "\n".join(map(warn_to_str, test_warnings))
        log = BuildLog.from_string(string, SimpleCompiler)
        self.assertIsNone(log.name)
        self.assertEqual(log.compiler, SimpleCompiler.name)
        for warning in log.warnings:
            self.assertIn(warning, test_warnings)
        self.assertEqual(log.suppressed, [])
        self.assertEqual(log.overridden, [])
        self.assertEqual(log.warning_count(), len(test_warnings))

    def test_populate_from_file(self):
        """ Test the population of build logs from a log file """
        test_log_name = "_populate_test.log"

        f = open(test_log_name, "w")
        f.write("\n".join(map(warn_to_str, test_warnings)))
        f.close()

        log = BuildLog.from_file(test_log_name, SimpleCompiler)
        self.assertEqual(log.name, test_log_name)
        self.assertEqual(log.compiler, SimpleCompiler.name)
        for warning in log.warnings:
            self.assertIn(warning, test_warnings)
        self.assertEqual(log.suppressed, [])
        self.assertEqual(log.overridden, [])
        self.assertEqual(log.warning_count(), len(test_warnings))

        os.remove(test_log_name)

    def test_overridden_warnings(self):
        """ Test the build log correctly shows overridden warnings """
        log = BuildLog.from_warnings(override_test_warnings)

        self.assertNotEqual(log.warnings, [])

        override = Override(new="new")
        log.override(override)

        for warning in log.warnings:
            self.assertIn(warning, override_test_warnings)

        for warning in log.overridden:
            self.assertIn(warning, override_test_warnings)

        self.assertEqual(log.warning_count(), len(override_test_warnings))

    def test_suppressed_warnings(self):
        """ Test the build log correctly hides suppressed warnings """
        log = BuildLog.from_warnings(test_warnings)

        self.assertNotEqual(log.warnings, [])

        suppression = Suppression()
        log.suppress(suppression)

        self.assertEqual(log.warnings, [])

        for warning in log.suppressed:
            self.assertIn(warning, test_warnings)

        self.assertEqual(log.warning_count(), 0)

if __name__ == "__main__":
    unittest.main()
