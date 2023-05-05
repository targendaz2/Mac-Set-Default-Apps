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

@test "Fails if the submitted app is not installed" {
    # Given the bundle ID of an app that isn't installed
    bundle_id='com.dgrdev.FakeBrowser'

    # When that bundle ID is submitted to msda
    run $PROJECT_ROOT/tests/utils/zsh_wrapper.sh set_command

    # The app should fail
    assert_failure
}
