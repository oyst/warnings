#!/usr/bin/env python

from build_log import BuildLog
import compiler
import sys, os
import argparse
from collections import defaultdict
import importlib

COMPILERS = defaultdict(None, {comp.name: comp for comp in compiler.compilers})

def import_collectors(import_path):
    module = importlib.import_module(import_path)
    collectors = filter(lambda f: f.startswith("collect_"), dir(module))
    return collectors

DEFAULT_COLLECTORS = import_collectors("collectors")

def collect_values(build, ref, collectors):
    vals = {}

    for collector in DEFAULT_COLLECTORS + collectors:
        vals.update(collector(build, ref))
    return vals

def display(vals, template, outstream):
    template.format(**vals)

def populate(newlog, reflog, compiler_name, confpaths):
    compiler = COMPILERS[compiler_name]

    build = BuildLog()
    build.populate(buildlog, compiler)

    ref = BuildLog()
    if reflog is not None:
        ref.populate(goldenlog, compiler)

    return (build, ref)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compare two build logs for differences in warnings")
    parser.add_argument("--build_log", "-b", dest="buildlog", required=True, help="The build log to check")
    parser.add_argument("--ref_log", "-r", dest="reflog", required=False, help="The build log to compare against. If missing, a report of just the build log will be produced")
    parser.add_argument("--compiler", "-c", dest="compiler", required=True, choices=[COMPILERS.keys()], help="The (closest) compiler which created the logs")
    parser.add_argument("--config", "-f", dest="config", required=False, nargs="*", help="Optional paths to config files containing overrides and suppressions")
    parser.add_argument("--template", "-t", dest="template", required=True, help="The output template")
    parser.add_argument("--collector", "-r", dest="collector", required=False, nargs="*", help="Optional paths to collector python scripts containing a list `collectors` of methods")
    parser.add_argument("--output", "-o", dest="output", required=False, default=None, help="The file to output to. Default to stdout")

    args = parser.parse_args()

    build, ref = main(args.buildlog, args.reflog, args.compiler, args.config)

    collectors = []
    for path in args.collector:
        collectors += import_collectors(path)

    vals = collect_values(build, ref, collectors)

    if args.output is None:
        outstream = sys.stdout
    else:
        outstream = open(outstream, "w")
    display(vals, args.template, outstream)
