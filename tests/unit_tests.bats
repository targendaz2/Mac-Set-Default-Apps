setup() {
    load '../node_modules/bats-support/load'
    load '../node_modules/bats-assert/load'
    load '../node_modules/bats-zsh/load'

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

@test "_app_id_to_path converts an installed app's ID to its path" {
    # Given the bundle ID of an app that is installed
    bundle_id='com.apple.Safari'

    # When that bundle ID is submitted
    zsource src/msda.sh
    zrun _app_id_to_path $bundle_id

    # Then the app's path should be returned
    assert_output '/Applications/Safari.app'
}

@test "_app_id_to_path fails for unknown app ID's" {
    # Given the bundle ID of an app that isn't installed
    bundle_id='com.dgrdev.FakeBrowser'

    # When that bundle ID is submitted
    zsource src/msda.sh
    zrun _app_id_to_path $bundle_id

    # Then the function should fail
    assert_failure
}

@test "_app_is_installed succeeds for installed apps" {
    # Given the bundle ID of an app that is installed
    bundle_id='com.apple.Safari'

    # When that bundle ID is submitted
    zsource src/msda.sh
    zrun _app_is_installed $bundle_id

    # Then the function should succeed
    assert_success
}

@test "_app_is_installed fails for apps that aren't installed" {
    # Given the bundle ID of an app that isn't installed
    bundle_id='com.dgrdev.FakeBrowser'

    # When that bundle ID is submitted
    zsource src/msda.sh
    zrun _app_is_installed $bundle_id

    # Then the function should fail
    assert_failure
}

@test "_app_supports_uti succeeds if the app supports the UTI" {
    # Given an app's bundle ID and a UTI it supports
    bundle_id='com.apple.Safari'
    uti='public.html'

    # When that bundle ID and UTI are submitted
    zsource src/msda.sh
    zrun _app_supports_uti $bundle_id $uti
    
    # Then the function should succeed
    assert_success
}

@test "_app_supports_uti fails if the app doesn't support the UTI" {
    # Given an app's bundle ID and a UTI it doesn't support
    bundle_id='com.apple.Safari'
    uti='dgrdev.fake'

    # When that bundle ID and UTI are submitted
    zsource src/msda.sh
    zrun _app_supports_uti $bundle_id $uti
    
    # Then the function should fail
    assert_failure
}

@test "_get_app_info_plist returns the path to an installed app's Info.plist" {
    # Given an installed app's bundle ID
    bundle_id='com.apple.Safari'

    # When that bundle ID is submitted
    zsource src/msda.sh
    zrun _get_app_info_plist $bundle_id
    
    # Then the path to the app's Info.plist should be returned
    assert_output '/Applications/Safari.app/Contents/Info.plist'
}

@test "_get_app_info_plist fails if the app's Info.plist doesn't exist" {
    # Given an unknown app's bundle ID
    bundle_id='com.dgrdev.FakeBrowser'

    # When that bundle ID is submitted
    zsource src/msda.sh
    zrun _get_app_info_plist $bundle_id
    
    # Then the function should fail
    assert_failure
}

@test "_get_supported_extensions returns an array of supported file extensions for an installed app" {
    # Given an installed app's bundle ID
    bundle_id='com.apple.Safari'

    # When that bundle ID is submitted
    zsource src/msda.sh
    zrun _get_supported_extensions $bundle_id
    
    # Then an array of supported file extensions should be returned
    assert_output 'css pdf webarchive webbookmark webhistory webloc download safariextz gif html htm shtml jhtml js jpg jpeg jp2 txt text png tiff tif url ico xhtml xht xhtm xht xml xbl xsl xslt svg avif webp'
}

@test "_get_supported_mime_types returns an array of supported UTI's for an installed app" {
    # Given an installed app's bundle ID
    bundle_id='com.apple.Safari'

    # When that bundle ID is submitted
    zsource src/msda.sh
    zrun _get_supported_mime_types $bundle_id
    
    # Then an array of supported UTI's should be returned
    assert_output 'text/css application/pdf application/x-webarchive application/x-safari-extension image/gif text/html application/x-javascript image/jpeg image/jp2 text/plain image/png image/tiff image/x-icon application/xhtml+xml application/xml text/xml image/svg+xml image/avif image/webp'
}

@test "_get_supported_mime_types fails for unknown apps" {
    # Given an unknown app's bundle ID
 bundle_id='com.dgrdev.FakeBrowser'

    # When that bundle ID is submitted
    zsource src/msda.sh
    zrun _get_supported_mime_types $bundle_id
    
    # Then the function should fail
    assert_failure
}

@test "_uti_to_mime converts an existing UTI to its MIME type" {
    # Given a known UTI
    uti='public.html'

    # When that UTI is submitted
    zsource src/msda.sh
    zrun _uti_to_mime $uti

    # Then the function should succeed and return the MIME type
    assert_success
    assert_equal "$output" "text/html"
}

@test "_uti_to_mime fails for nonexistent UTIs" {
    # Given a nonexistent UTI
    uti='dgrdev.fake'

    # When that UTI is submitted
    zsource src/msda.sh
    zrun _uti_to_mime $uti

    # Then the function should fail
    assert_failure
}
