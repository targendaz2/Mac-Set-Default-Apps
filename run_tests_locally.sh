#!/bin/bash

mkdir -p ./.test_results

results_filename="$(date '+results_%Y%m%d%H%M%S.txt')"

cirrus run --artifacts-dir .test_results --environment RESULTS_FILENAME=$results_filename

exit 0
