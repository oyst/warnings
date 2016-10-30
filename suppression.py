#!/usr/bin/env python
from warning import RegexWarning
import re

class Suppression(RegexWarning):
    def suppresses(self, warning):
        return self == warning
