#!/usr/bin/env python
from build_warning import RegexBuildWarning
import re

class Suppression(RegexBuildWarning):
    def suppresses(self, warning):
        return self >= warning
