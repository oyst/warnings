#!/usr/bin/env python
from warning import RegexWarning

class Override(RegexWarning):
    def __init__(self, new=""):
        super(self.__class__, self).__init__()
        self.new = new

    def overrides(self, warning):
        return self >= warning

    def override(self, warning):
        warning.message = self.new
        return warning
