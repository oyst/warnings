#!/usr/bin/env python
from collections import defaultdict

class Config(object):
    SUPPRESS = 'suppress'
    OVERRIDE = 'override'

    def __init__(self):
        self._conf = None
        self._overrides = []
        self._suppressions = []

    def suppressions(self):
        return self._suppressions

    def overrides(self):
        return self._overrides

    @classmethod
    def load(cls, confpath):
        conf = cls()
        with open(confpath, 'r') as f:
            loaded = defaultdict([], yaml.load(f))

        for supp in loaded[cls.SUPPRESS]:
            conf._suppressions.append(Suppression.from_dict(supp))

        for over in loaded[cls.OVERRIDE]:
            conf._overrides.append(Override.from_dict(over))

        return conf
