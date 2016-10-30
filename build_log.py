#!/usr/bin/env python

import os
import compiler
from warning import Warning
import logging

logger = logging.getLogger(__name__)

class BuildLog:
    def __init__(self):
        self._compiler = None
        self._logpath = None
        self._warning_pattern = None
        self._warnings = []

    def logpath(self):
        return self._logpath

    def logname(self):
        return os.path.dirname(self._logpath)

    def compiler(self):
        return self._compiler.name()

    def warnings(self):
        return self._warnings

    def warning_count(self):
        return len(self._warnings)

    def has_warning(self, warning):
        return warning in self.warnings()

    def __contains__(self, item):
        return self.has_warning(item)

    def count_of_warning(self, warning):
        count = 0
        for my_warning in self.warnings():
            if my_warning == warning:
                count += 1
        return count

    def populate(self, logpath, comp):
        """ Populate the BuildLog with all the warnings in a given log file

            Parameters
              logpath  : path to the build log to be parsed
              comp : compiler which best matches the one which produced the log

            Returns
              0 : successfully read and populated the BuildLog
              1 : failed to populate the BuildLog

            Raises
              TypeError, ValueError, IOError
        """
        # Reinitialise
        self._compiler = comp
        self._logpath = logpath
        self._warning_pattern = comp.warning_pattern()
        self._error_pattern = comp.error_pattern()
        self._warnings = []
        self._errors = []

        # Load in the log text
        with open(self._logpath, 'r') as logfile:
            logtext = logfile.read()
        if not logtext:
            logger.warning("Log {0} is empty".format(self._logpath))
            return 1

        if self._warning_pattern:
            for match in self._warning_pattern.finditer(logtext):
                # Handle the match
                warning = Warning.from_match(match)
                self._warnings.append(warning)

        return 0
