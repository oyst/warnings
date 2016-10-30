#!/usr/bin/env python
import re

class VC9:
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

class VC14:
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

class GCC4:
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

class Clang:
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

class XLC:
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


compilers = [VC9, GCC4, VC14, Clang, XLC,]
