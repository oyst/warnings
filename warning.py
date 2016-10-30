#!/usr/bin/env python
import logging

logger = logging.getLogger(__name__)

# Container for a single warning
class Warning:
    # Each warning is made up of these fields
    # The boolean for each field is whether the field contributes to equality
    __parts = {'fullpath': False,
               'filepath': False,
               'filename': True,
               'function': False,
               'code': False,
               'message': False,
               'linenum': False,}

    def __init__(self):
        for part in self.__parts:
            self.__dict__[part] = None

    def __eq__(self, other):
        if isinstance(other, dict):
            other = self.__class__.from_dict(other)
        if isinstance(other, MatchType):
            other = self.__class__.from_match(other)
        if not isinstance(self.__class__, other):
            return False

        for part, include in self.__parts:
            if not include:
                continue
            other_part = getattr(other, part)
            self_part = getattr(self, part)
            if other_part != self_part:
                return False
        return True

    def __str__(self):
        output = []
        for part in self.__parts:
            value = getattr(self, part)
            if value is not None:
                output.append("{0}: {1}".format(key, value))
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
            if key not in cls.__parts:
                logger.warning("Unknown part {0}".format(key))
                continue

            setattr(warning, key, d[key])
        return warning
