#!/usr/bin/env python

import os
import compiler
from warning import Warning
import logging

logger = logging.getLogger(__name__)

class BuildLog(object):
    NORMAL = 0
    SUPPRESSED = 1
    OVERRIDEN = 2

    def __init__(self):
        self._compiler = None
        self._logpath = None
        self._warning_pattern = None
        self._warnings = {}

    def logpath(self):
        return self._logpath

    def logname(self):
        if self._logpath is not None:
            return os.path.dirname(self._logpath)
        return self._logpath

    def compiler(self):
        if self._compiler is not None:
            return self._compiler.name
        return None

    def warnings(self):
        return [k for k, v in self._warnings.items() if not v & self.SUPPRESSED]

    def suppressed(self):
        return [k for k, v in self._warnings.items() if v & self.SUPPRESSED]

    def overridden(self):
        return [k for k, v in self._warnings.items() if v & self.OVERRIDEN]

    def warning_count(self):
        return len(self.warnings())

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

    def suppress(self, suppression):
        for warning in self.warnings():
            if suppression.suppresses(warning):
                self._warnings[warning] &= self.SUPPRESSED

    def override(self, override):
        for warning in self.warnings():
            if override.overrides(warning):
                self._warnings[warning] &= self.OVERRIDDEN
                self._warning = override.replace(warning)

    def apply_config(self, config):
        for suppression in config.suppressions():
            self.suppress(suppression)

        for override in config.overrides():
            self.override(override)

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
        self._warning_pattern = comp.warn
        self._warnings = {}

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
                self._warnings[warning] = self.NORMAL

        return 0
