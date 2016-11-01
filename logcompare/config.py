#!/usr/bin/env python
import yaml
from collections import defaultdict
from suppression import Suppression
from override import Override

class Config(object):
    SUPPRESS = 'suppress'
    OVERRIDE = 'override'

    def __init__(self):
        self._conf = None
        self._overrides = []
        self._suppressions = []

    @property
    def suppressions(self):
        return self._suppressions

    @property
    def overrides(self):
        return self._overrides

    @classmethod
    def from_file(cls, confpath):
        with open(confpath, 'r') as f:
            loaded = defaultdict(list, yaml.load(f))
        return cls.from_dict(loaded)

    @classmethod
    def from_dict(cls, d):
        conf = cls()
        for supp in d[cls.SUPPRESS]:
            conf._suppressions.append(Suppression.from_dict(supp))

        for over in d[cls.OVERRIDE]:
            conf._overrides.append(Override.from_dict(over))

        return conf
