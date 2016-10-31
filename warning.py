#!/usr/bin/env python
import logging
import re

logger = logging.getLogger(__name__)

MatchType = type(re.match("", ""))

# Container for a single warning
class Warning(object):
    # Each warning is made up of these fields
    # The boolean for each field is whether the field contributes to equality
    _parts = {'fullpath': True,
               'filepath': True,
               'filename': True,
               'function': True,
               'code': True,
               'message': True,
               'linenum': False,}

    def __init__(self):
        for part in self._parts:
            self.__dict__[part] = None

    def __eq__(self, other):
        if isinstance(other, dict):
            other = self.__class__.from_dict(other)
        if isinstance(other, MatchType):
            other = self.__class__.from_match(other)
        if not isinstance(other, self.__class__):
            return False

        for part, include in self._parts.items():
            if not include:
                continue
            other_part = getattr(other, part)
            self_part = getattr(self, part)
            if other_part != self_part:
                return False
        return True

    def __str__(self):
        output = []
        for part in self._parts:
            value = getattr(self, part)
            if value is not None:
                output.append("{0}: {1}".format(part, repr(value)))
        return "\n".join(output)

    @classmethod
    def from_match(cls, match):
        return cls.from_dict(match.groupdict())

    @classmethod
    def from_dict(cls, d):
        warning = cls()
        for key in d:
            if not isinstance(key, str):
                logger.warning("Invalid part {0}".format(key))
                continue
            if key not in cls._parts:
                logger.warning("Unknown part {0}".format(key))
                continue

            setattr(warning, key, d[key])
        return warning

class RegexWarning(Warning):
    class RegexPart:
        def __init__(self, val):
            self._val = val
        def __eq__(self, other):
            return re.match(self._val, other)
        def __str__(self):
            return "/" + self._val + "/"
        def __repr__(self):
            return "/" + self._val + "/"

    @classmethod
    def from_dict(cls, d):
        warning = super(RegexWarning, cls).from_dict(d)
        for part in warning._parts:
            val = getattr(warning, part)
            try:
                if val.startswith("/") and val.endswith("/"):
                    setattr(warning, part, RegexWarning.RegexPart(val[1:-1]))
            except AttributeError:
                pass
        return warning
