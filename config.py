#!/usr/bin/env python
class Config:
    def __init__(self):
        self._conf = None

    def load(self, confpath):
        with open(confpath, 'r') as f:
            self._conf = yaml.load(f)
        return self._conf
