setup() {
    load '../node_modules/bats-support/load'
    load '../node_modules/bats-assert/load'

    load '../tests/utils/utils'

    # get the containing directory of this file
    # use $BATS_TEST_FILENAME instead of ${BASH_SOURCE[0]} or $0,
    # as those will point to the bats executable's location or the preprocessed file respectively
    PROJECT_ROOT="$( cd "$( dirname "$BATS_TEST_FILENAME" )/.." >/dev/null 2>&1 && pwd )"
    # make executables in src/ visible to PATH
    PATH="$PROJECT_ROOT/src:$PATH"
}

teardown() {
    :
}

@test "Set Chrome as the default browser for the current user" {
    # Set testing variables
    TEST_URL='https://example.com'

    # Confirm expected initial OS state

    # - Safari is not running
    refute is_running 'Safari'

    # - Google Chrome is not running
    refute is_running 'Google Chrome'

    # - Opening a URL opens Safari
    open "$TEST_URL"
    assert is_running 'Safari'

    # Return to the initial OS state

    # - Close Safari
    assert close 'Safari'

    # Execute functional test

    # - User runs msda to set Google Chrome as the default browser
    msda.sh set --browser com.google.Chrome

    # Confirm resulting OS state

    # - Opening a URL opens Google Chrome
    open "$TEST_URL"
    assert is_running 'Google Chrome'

    # - Safari is still not running
    refute is_running 'Safari'
}
