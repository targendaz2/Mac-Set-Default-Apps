#!/usr/bin/env zsh

FIRST_RUN_FILE=/tmp/bats-tutorial-project-ran

if [[ ! -e "$FIRST_RUN_FILE" ]]; then
    echo "Welcome to our project!"
    touch "$FIRST_RUN_FILE"
fi

echo "NOT IMPLEMENTED!" >&2
exit 1
