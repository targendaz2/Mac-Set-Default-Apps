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

@test "Succeeds if the submitted app is installed" {
    # Given the bundle ID of an app that is installed
    bundle_id='com.apple.Safari'

    # When that bundle ID is submitted
    run $PROJECT_ROOT/tests/utils/zsh_wrapper.sh _app_is_installed $bundle_id

    # The function should succeed
    assert_success
}

@test "Fails if the submitted app is not installed" {
    # Given the bundle ID of an app that isn't installed
    bundle_id='com.dgrdev.FakeBrowser'

    # When that bundle ID is submitted
    run $PROJECT_ROOT/tests/utils/zsh_wrapper.sh _app_is_installed $bundle_id

    # The function should fail
    assert_failure
}

@test "Converts existing UTI to its MIME type" {
    # Given a known UTI
    uti='public.html'

    # When that UTI is submitted
    run $PROJECT_ROOT/tests/utils/zsh_wrapper.sh _uti_to_mime $uti

    # The function should succeed and return the MIME type
    assert_success
    assert_equal "$output" "text/html"
}
