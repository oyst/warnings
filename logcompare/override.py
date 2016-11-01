#!/usr/bin/env python
from build_warning import RegexBuildWarning

class Override(RegexBuildWarning):
    def __init__(self, new=""):
        self.register_part("new", equality=True)
        super(self.__class__, self).__init__()
        self.new = new

    def overrides(self, warning):
        return self >= warning

    def override(self, warning):
        warning.message = self.new
        return warning
