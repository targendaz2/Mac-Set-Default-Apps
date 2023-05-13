#!/usr/bin/env zsh

# mkdir -p test_reports

# results_filename="$(date '+results_%Y%m%d%H%M%S.txt')"

# cirrus run --artifacts-dir .test_results --environment RESULTS_FILENAME=$results_filename

zparseopts -F -K -- \
    -all=flag_all \
    -browsers=flag_browsers \
    -calendars=flag_calendars \
    -mail=flag_mail \
    -pdf=flag_pdf \
    || exit 1

[ ! -z $flag_browsers ] || [ ! -z $flag_all ] || [ $# = 0 ] && INC_BROWSERS=true
[ ! -z $flag_calendars ] || [ ! -z $flag_all ] || [ $# = 0 ] && INC_CALENDARS=true
[ ! -z $flag_mail ] || [ ! -z $flag_all ] || [ $# = 0 ] && INC_MAIL=true
[ ! -z $flag_pdf ] || [ ! -z $flag_all ] || [ $# = 0 ] && INC_PDF=true

cirrus run \
    --output github-actions \
    --environment INC_BROWSERS=$INC_BROWSERS \
    --environment INC_CALENDARS=$INC_CALENDARS \
    --environment INC_MAIL=$INC_MAIL \
    --environment INC_PDF=$INC_PDF

exit 0
