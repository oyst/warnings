#!/usr/bin/env python

# == Log info ==
# build_name
# build_path
# build_compiler
# ref_name
# ref_path
# ref_name
def collect_log_details(build, ref):
    details = {'build_name': build.logname(),
               'build_path': build.logpath(),
               'build_compiler': build.compiler(),
               'ref_name': ref.logname(),
               'ref_path': ref.logpath(),
               'ref_compiler': ref.compiler(),}
    return details
