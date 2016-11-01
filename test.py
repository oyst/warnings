#! /usr/bin/env python
import unittest
import sys, re, os

from logcompare import *

test_dir = os.path.join("tests")
testlog_dir = os.path.join("tests", "test_logs")

class SimpleCompiler(object):
    name = "simpleCompiler"
    warn = re.compile(r'''^
                      (?P<fullpath>
                       (?P<filepath>.+/)?                   # <filepath>
                       (?P<filename>.+)                     # <filename>
                      )\s*
                      \(                                     # (
                       (?P<linenum>\d+)                      # <linenum>
                      \)\s*                                  # )
                      (?P<code>C\d+?)                        # <code>
                      :\s*                                   # :
                      (?P<message>.+)                        # <message>
                      $''', re.MULTILINE|re.VERBOSE)

def warn_to_str(warning):
    return "{w.fullpath}({w.linenum}){w.code}:{w.message}".format(w=warning)

def str_to_warn(string):
    return BuildWarning.from_match(re.match(SimpleCompiler.warn, string))

test_warnings = [
    str_to_warn("file1.c(10)C123:warning1"),
    str_to_warn("path/to/file2.c(20)C45:warning2"),
]

compare_test_warnings = [
    str_to_warn("file3.c(30)C55:warning3"),
    str_to_warn("file3.c(30)C55:warning3"),
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
        """ Test the population of build logs from a list of BuildWarnings """
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

class TestBuildWarningComparison(unittest.TestCase):
    def test_eq(self):
        """ Test equality and gt, lt of two warnings """
        w1 = compare_test_warnings[0]
        w2 = compare_test_warnings[1]

        self.assertTrue(w1 == w2)
        self.assertFalse(w1 != w2)
        self.assertTrue(w1 >= w2)
        self.assertTrue(w1 <= w2)
        self.assertFalse(w1 < w2)
        self.assertFalse(w1 > w2)

    def test_ne(self):
        """ Test the inequality and gt, lt comparison of two warnings """
        w1 = compare_test_warnings[0]
        w2 = compare_test_warnings[1]

        # BuildWarning 2 is the most specific, so BuildWarning 1 is greater
        w1.filename = None
        self.assertFalse(w1 == w2)
        self.assertTrue(w1 != w2)
        self.assertTrue(w1 >= w2)
        self.assertFalse(w1 <= w2)
        self.assertTrue(w1 > w2)
        self.assertFalse(w1 < w2)

        # Both BuildWarning 1 and BuildWarning 2 are missing parts from each other, so neither
        # are greater
        w2.code = None
        self.assertFalse(w1 == w2)
        self.assertTrue(w1 != w2)
        self.assertFalse(w1 >= w2)
        self.assertFalse(w1 <= w2)
        self.assertFalse(w1 > w2)
        self.assertFalse(w1 < w2)

class TestCompare(unittest.TestCase):
    class TestCase(object):
        def __init__(self, name, buildlog=None, reflog=None, template=None, output=None, configs=None):
            self.buildlog = os.path.join(testlog_dir, "empty.log") if buildlog is None else buildlog
            self.reflog = os.path.join(testlog_dir, "empty.log") if reflog is None else reflog
            self.configs = [] if configs is None else configs
            self.template = os.path.join(testlog_dir, "empty.log") if template is None else template
            self.output = os.path.join(testlog_dir, "empty.log") if output is None else output
            self.name = name

    testcases = [
    ]

    def test_end_to_end(self):
        for testcase in self.testcases:
            build, ref = populate(testcase.buildlog, testcase.reflog, SimpleCompiler, testcase.configs)
            vals = collect_values(build, ref)
            template = open(testcase.template, "r").read()
            actual = render(vals, template)
            expected = open(testcase.output, "r").read()
            self.assertEqual(expected, actual, "TestCase {0} failed to match the expected output".format(testcase.name))

if __name__ == "__main__":
    unittest.main()
