#!/usr/bin/env python
import re

class Compiler:
    def __init__(self, name, warn_pattern=None):
        self._name = name
        self.warning_pattern = warn_pattern

class VC9(Compiler):
    def __init__(self):
        name = 'vc9'
        warn = re.compile(r'''^
                          (?:\d+>)?                              # part id
                          (?P<fullpath>
                           (?P<filepath>.+\\)?                   # <filepath>
                           (?P<filename>.+)                      # <filename>
                          )
                          \(                                     # (
                           (?P<linenum>\d+)                      # <linenum>
                          \)\s:\s                                # ) :
                          warning\s                              # warning
                          (?P<code>.+?)                          # <code>
                          :\s                                    # :
                          (?P<message>[^\(].+)                   # <message>
                          \s*$''', re.MULTILINE|re.VERBOSE)
        Compiler.__init__(self, name, warn, err)

class VC14(Compiler):
    def __init__(self):
        name = 'vc14'
        warn = re.compile(r'''^
                          (?:\d+>)?                              # part id
                          (?P<fullpath>
                           (?P<filepath>.+\\)?                   # <filepath>
                           (?P<filename>.+?)                     # <filename>
                          )
                          \(                                     # (
                           (?P<linenum>\d+)                      # <linenum>
                          \):\s                                  # ):
                          warning\s                              # warning
                          (?P<code>.+?)                          # <code>
                          :\s                                    # :
                          (?P<message>[^\(].+)                   # <message>
                          \s*$''', re.MULTILINE|re.VERBOSE)
        Compiler.__init__(self, name, warn, err)

class GCC4(Compiler):
    def __init__(self):
        name = 'gcc4'
        warn = re.compile(r'''^
                          (?P<fullpath>
                           (?P<filepath>.+/)?                                 # <filepath>
                           (?P<filename>.+?)                                  # <filename>
                          )
                          :                                                   # :
                          (?P<linenum>\d+)                                    # <linenum>
                          :(\d+:)?\s                                          # :column:
                          warning:\s                                          # warning:
                          (?P<message>[^\(].+?)                               # <message>
                          \s*                                                 #
                          (?P<code>(\[(-W\S+|enabled \s by \s default)\])?)   # <code>
                          \s*$''', re.MULTILINE|re.VERBOSE)
        Compiler.__init__(self, name, warn, err)

class Clang(Compiler):
    def __init__(self):
        name = 'clang'
        warn = re.compile(r'''^
                          (?P<fullpath>
                           (?P<filepath>.+/)?                                 # <filepath>
                           (?P<filename>.+?)                                  # <filename>
                          )
                          :                                                   # :
                          (?P<linenum>\d+)                                    # <linenum>
                          :(\d+:)?\s                                          # :column:
                          warning:\s                                          # warning:
                          (?P<message>[^\(].+?)                               # <message>
                          \s*                                                 #
                          (?P<code>(\[(-W\S+|enabled \s by \s default)\])?)   # <code>
                          \s*$''', re.MULTILINE|re.VERBOSE)
        return Compiler.__init__(self, name, warn, err)

class XLC(Compiler):
    def __init__(self):
        name = 'xlc'
        warn = re.compile(r'''^
                          "                                                   # "
                          (?P<fullpath>
                           (?P<filepath>.+/)?                                 # <filepath>
                           (?P<filename>.+)                                   # <filename>
                          )
                          ", \s line \s                                       # ", line
                          (?P<linenum>\d+)                                    # <linenum>
                          \.\d+:\s                                            # .column:
                          (?P<code>\d+-\d+)                                   # <code>
                          \s \(W\) \s                                         # (W)
                          (?P<message>[^\(].+?)                               # <message>
                          \.                                                  # .
                          \s*$''', re.MULTILINE|re.VERBOSE)
        Compiler.__init__(self, name, warn, err)
