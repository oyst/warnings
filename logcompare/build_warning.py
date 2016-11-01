#!/usr/bin/env python
import logging
import re

logger = logging.getLogger(__name__)

MatchType = type(re.match("", ""))

# Container for a single warning
class BuildWarning(object):
    # Each warning is made up of these fields
    # The boolean for each field is whether the field contributes to equality
    _parts = {'fullpath': True,
              'filepath': True,
              'filename': True,
              'function': True,
              'code': True,
              'message': True,
              'linenum': False,}

    def _eq_parts(self):
        return [k for k, v in self._parts.items() if v]

    def __init__(self):
        for part in self._parts:
            self.__dict__[part] = None

    def __eq__(self, other):
        """ Two warnings are equal if their parts are equal. """
        for part in self._eq_parts():
            other_part = getattr(other, part, None)
            self_part = getattr(self, part, None)
            if other_part != self_part:
                return False
        return True

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        """ everything in self is in other """
        for part in self._eq_parts():
            other_part = getattr(other, part, None)
            self_part = getattr(self, part, None)
            if self_part is None:
                continue
            if other_part != self_part:
                return False
        return True

    def __le__(self, other):
        """ everything in other is in self """
        for part in self._eq_parts():
            other_part = getattr(other, part, None)
            self_part = getattr(self, part, None)
            if other_part is None:
                continue
            if other_part != self_part:
                return False
        return True

    def __lt__(self, other):
        return self != other and self <= other

    def __gt__(self, other):
        return self != other and self >= other

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

class RegexBuildWarning(BuildWarning):
    class RegexPart:
        def __init__(self, val):
            self._val = val
        def __eq__(self, other):
            return re.match(self._val, other)
        def __str__(self):
            return "/" + self._val + "/"
        def __repr__(self):
            return "/" + self._val + "/"

    def register_part(self, name, equality=False):
        self._parts[name] = equality

    @classmethod
    def from_dict(cls, d):
        warning = super(RegexBuildWarning, cls).from_dict(d)
        for part in warning._parts:
            val = getattr(warning, part)
            try:
                if val.startswith("/") and val.endswith("/"):
                    setattr(warning, part, RegexBuildWarning.RegexPart(val[1:-1]))
            except AttributeError:
                pass
        return warning
