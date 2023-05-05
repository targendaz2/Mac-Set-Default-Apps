#!/usr/bin/env bash

is_running() {
    # Set variables from args
    local APP="$1"

    # Ensure an app name is provided
    if [ -z "$APP" ]; then
        echo 'You must provide an application name.' >&2
        exit 1
    fi

    # Check app running state
    pgrep -l ^$APP$ > /dev/null
    local result=$?

    # Return the appropriate exit code
    return $result
}
