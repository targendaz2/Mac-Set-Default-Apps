is_running() {
    # Set variables from args
    local APP="$1"

    # Ensure an app name is provided
    if [ -z "$APP" ]; then
        echo 'You must provide an application name.' >&2
        return
    fi

    # Check app running state
    pgrep -l ^$APP$ > /dev/null
    local result=$?

    # Return the appropriate exit code
    return $result
}

close() {
    # Set variables from args
    local APP="$1"

    # Ensure an app name is provided
    if [ -z "$APP" ]; then
        echo 'You must provide an application name.' >&2
        return
    fi

    # Check app running state
    pkill -l ^$APP$ > /dev/null
    local result=$?

    # Return the appropriate exit code
    return $result
}
