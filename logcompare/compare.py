#!/usr/bin/env python

from build_log import BuildLog
import compiler
import sys, os
import argparse
from collections import defaultdict
import importlib
from collectors import collectors

from templite import Templite

COMPILERS = defaultdict(None, {comp.name: comp for comp in compiler.compilers})

def collect_values(build, ref, collectors=collectors):
    vals = {}

    for collector in collectors:
        vals.update(collector(build, ref))
    return vals

def render(vals, template):
    t = Templite(template)
    return t.render(**vals)

def populate(buildlog, reflog, compiler_name, confpaths):
    compiler = COMPILERS[compiler_name]

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compare two build logs for differences in warnings")
    parser.add_argument("--build_log", "-b", dest="buildlog", required=True, help="The build log to check")
    parser.add_argument("--ref_log", "-r", dest="reflog", required=False, help="The build log to compare against. If missing, a report of just the build log will be produced")
    parser.add_argument("--compiler", "-c", dest="compiler", required=True, choices=COMPILERS.keys(), help="The (closest) compiler which created the logs")
    parser.add_argument("--config", "-f", dest="config", required=False, nargs="*", default=[], help="Optional paths to config files containing overrides and suppressions")
    parser.add_argument("--template", "-t", dest="template", required=True, help="The output template")
    parser.add_argument("--output", "-o", dest="output", required=False, default=None, help="The file to output to. Default to stdout")

    args = parser.parse_args()

    build, ref = populate(args.buildlog, args.reflog, args.compiler, args.config)

    vals = collect_values(build, ref)

    if args.output is None:
        outstream = sys.stdout
    else:
        outstream = open(outstream, "w")

    with open(args.template) as template:
        output = render(vals, template.read())
    outstream.write(output)
