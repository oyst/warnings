import re
from warning import Warning

class SimpleCompiler(object):
    name = "simpleCompiler"
    warn = re.compile(r'''^
                      (?P<fullpath>
                       (?P<filepath>.+/)?                   # <filepath>
                       (?P<filename>.+)                     # <filename>
                      )\s*
                      \(                                     # (
                       (?P<linenum>\d+)                      # <linenum>
                      \)\s*                                  # )
                      (?P<code>C\d+?)                        # <code>
                      :\s*                                   # :
                      (?P<message>.+)                        # <message>
                      $''', re.MULTILINE|re.VERBOSE)

def warn_to_str(warning):
    return "{w.fullpath}({w.linenum}){w.code}:{w.message}".format(w=warning)

def str_to_warn(string):
    return Warning.from_match(re.match(SimpleCompiler.warn, string))
