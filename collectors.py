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

# == Counts ==
# build_warn_count
# ref_warn_count
# total_warn_count
# introduced_warn_count
# removed_warn_count
# shared_warn_count
def collect_counts(build, ref):
    build_warnings = build.warnings()
    ref_warnings = ref.warnings()
    all_warnings = []
    introduced_warnings = []
    removed_warnings = []
    shared_warnings = []

    for warning in build.warnings():
        build_count = build.count_of_warning(warning)
        ref_count = ref.count_of_warning(warning)
        if ref_count == build_count:
            all_warnings.append(warning)
        elif build_count > ref_count:
            all_warnings.append(warning)

    # Don't add the warning if there are equal amounts in both since we have already done it above
    for warning in ref.warnings():
        build_count = build.count_of_warning(warning)
        ref_count = ref.count_of_warning(warning)
        if ref_count > build_count:
            all_warnings.append(warning)

    for warning in all_warnings:
        build_count = build.count_of_warning(warning)
        ref_count = ref.count_of_warning(warning)
        # None in the reference, so it must be introduced
        if ref_count == 0:
            introduced_warnings.append(warning)
        # None in the build, so it must have been removed
        elif build_count == 0:
            removed_warnings.append(warning)
        # Equal reference and build, so it must be shared
        elif ref_count == build_count:
            shared_warnings.append(warning)
        # More in the build than reference, so if the difference is already in the introduced
        #  then the rest are shared
        elif ref_count < build_count:
            diff = build_count - ref_count
            if diff > introduced_warnings.count(warning):
                introduced_warnings.append(warning)
            else:
                shared_warnings.append(warning)
        # More in the reference than build, so if the difference is already in the removed
        #  then the rest are shared
        elif ref_count > build_count:
            diff = ref_count - build_count
            if diff > removed_warnings.count(warning):
                removed_warnings.append(warning)
            else:
                shared_warnings.append(warning)

    counts['build_warn_count'] = len(build_warnings)
    counts['ref_warn_count'] = len(ref_warnings)
    counts['total_warn_count'] = len(all_warnings)
    counts['introduced_warn_count'] = len(introduced_warnings)
    counts['removed_warn_count'] = len(removed_warnings)
    counts['shared_warn_count'] = len(shared_warnings)

    return counts
