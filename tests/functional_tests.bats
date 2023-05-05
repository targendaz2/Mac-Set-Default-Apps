setup() {
    load '../includes/bats-support/load'
    load '../includes/bats-assert/load'

    # get the containing directory of this file
    # use $BATS_TEST_FILENAME instead of ${BASH_SOURCE[0]} or $0,
    # as those will point to the bats executable's location or the preprocessed file respectively
    PROJECT_ROOT="$( cd "$( dirname "$BATS_TEST_FILENAME" )/.." >/dev/null 2>&1 && pwd )"
    # make executables in src/ visible to PATH
    PATH="$DIR/../src:$PATH"
}

teardown() {
    :
}

@test "Set Chrome as the default browser for the current user" {
    # Confirm expected initial OS state

    # - Safari is not running

    # - Google Chrome is not running

    # - Opening a URL opens Safari

    # Return to the initial OS state

    # - Close Safari

    # Execute functional test

    # - User runs msda to set Google Chrome as the default browser

    # Confirm resulting OS state

    # - Opening a URL opens Google Chrome
}
