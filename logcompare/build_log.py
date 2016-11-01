#!/usr/bin/env python

import os
import compiler
from build_warning import BuildWarning
import logging

logger = logging.getLogger(__name__)

class BuildLog(object):
    NORMAL = 0
    SUPPRESSED = 1
    OVERRIDDEN = 2

    def __init__(self):
        self._name = None
        self._compiler = None
        self._warnings = {}

    @property
    def name(self):
        return self._name

    @property
    def compiler(self):
        if self._compiler is not None:
            return self._compiler.name
        return None

    @property
    def warnings(self):
        return [k for k, v in self._warnings.items() if not v & self.SUPPRESSED]

    @property
    def suppressed(self):
        return [k for k, v in self._warnings.items() if v & self.SUPPRESSED]

    @property
    def overridden(self):
        return [k for k, v in self._warnings.items() if v & self.OVERRIDDEN]

    def warning_count(self):
        return len(self.warnings)

    def has_warning(self, warning):
        return warning in self.warnings

    def __contains__(self, item):
        return self.has_warning(item)

    def count_of_warning(self, warning):
        count = 0
        for my_warning in self.warnings:
            if my_warning == warning:
                count += 1
        return count

    def suppress(self, suppression):
        for warning in self.warnings:
            if suppression.suppresses(warning):
                self._warnings[warning] |= self.SUPPRESSED

    def override(self, override):
        for warning in self.warnings:
            if override.overrides(warning):
                self._warnings[warning] |= self.OVERRIDDEN
                override.override(warning)

    def apply_config(self, config):
        for suppression in config.suppressions:
            self.suppress(suppression)

        for override in config.overrides:
            self.override(override)

    @classmethod
    def from_file(cls, logfile, comp):
        with open(logfile) as f:
            self = cls.from_string(f.read(), comp)
        self._name = os.path.basename(logfile)
        return self

    @classmethod
    def from_string(cls, string, comp):
        pattern = comp.warn
        warnings = []
        for match in pattern.finditer(string):
            # Handle the match
            warnings.append(BuildWarning.from_match(match))
        self = cls.from_warnings(warnings)
        self._compiler = comp
        return self

    @classmethod
    def from_warnings(cls, warnings):
        self = cls()
        self._warnings = {warning: self.NORMAL for warning in warnings}
        return self
