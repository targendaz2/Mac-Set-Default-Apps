setup() {
    load '../../node_modules/bats-support/load'
    load '../../node_modules/bats-assert/load'
    load '../../node_modules/bats-zsh/load'

    load '../utils/utils'
}

teardown() {
    :
}

@test "_convert_uti returns associated file extensions and MIME types for known UTI's" {
    # Given a known UTI
    uti='public.html'

    # When that UTI is submitted submitted
    zsource src/msda.sh
    zrun _convert_uti $uti
    
    # Then the associated file extensions and MIME types should be returned
    assert_output 'html htm shtml shtm text/html'
}

@test "_convert_uti fails for unknown UTI's" {
    # Given an unknown UTI
    uti='dgrdev.fake'

    # When that UTI is submitted submitted
    zsource src/msda.sh
    zrun _convert_uti $uti
    
    # Then the function should fail
    assert_failure
}
