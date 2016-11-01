#!/usr/bin/env python


from templite import Templite

from build_warning import BuildWarning
from build_log import BuildLog
import compiler
import collectors
from config import Config
from override import Override
from suppression import Suppression

def collect_values(build, ref, collectors=collectors.collectors):
    vals = {}

    for collector in collectors:
        vals.update(collector(build, ref))
    return vals

def render(vals, template):
    t = Templite(template)
    return t.render(**vals)

def populate(buildlog, reflog, compiler, confpaths):
    build = BuildLog.from_file(buildlog, compiler)
    if reflog is not None:
        ref = BuildLog.from_file(reflog, compiler)
    else:
        ref = BuildLog()

    for confpath in confpaths:
        config = Config.from_file(confpath)
        build.apply_config(config)
        ref.apply_config(config)

    return (build, ref)
