#!/bin/bash

mkdir -p ./.test_results

results_filename="$(date '+results_%Y%m%d%H%M%S.html')"

cirrus run --artifacts-dir .test_results --environment RESULTS_FILENAME=$results_filename --output interactive

open ./.test_results/run_tests/results/$results_filename

exit 0
