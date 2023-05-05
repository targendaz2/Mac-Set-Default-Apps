#!/usr/bin/env zsh

source src/msda.sh

output=$(eval "$@")
exit_code=$?

echo "$output"

exit $exit_code
