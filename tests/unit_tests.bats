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

@test "_app_supports_role succeeds if the app supports the role" {
    skip
    # Given an app's bundle ID and a role it supports
    bundle_id='com.apple.Safari'
    role_name='browser'

    # When that bundle ID and role are submitted
    zsource src/msda.sh
    zrun _app_supports_role $bundle_id $role_name
    
    # Then the function should succeed
    assert_success
}

@test "_app_supports_role fails if the app doesn't support the role" {
    skip
    # Given an app's bundle ID and a role it doesn't support
    bundle_id='com.apple.Safari'
    role_name='calendar'

    # When that bundle ID and role are submitted
    zsource src/msda.sh
    zrun _app_supports_role $bundle_id $role_name
    
    # Then the function should fail
    assert_failure
}

@test "_app_supports_uti succeeds if the app supports the UTI" {
    skip
    # Given an app's bundle ID and a UTI it supports
    bundle_id='com.apple.Safari'
    uti='public.url:Viewer'

    # When that bundle ID and UTI are submitted
    zsource src/msda.sh
    zrun _app_supports_uti $bundle_id $uti
    
    # Then the function should succeed
    assert_success
}

@test "_app_supports_uti fails if the app doesn't support the UTI" {
    # Given an app's bundle ID and a UTI it doesn't support
    bundle_id='com.apple.Safari'
    uti='dgrdev.fake:Viewer'

    # When that bundle ID and UTI are submitted
    zsource src/msda.sh
    zrun _app_supports_uti $bundle_id $uti
    
    # Then the function should fail
    assert_failure
}

@test "_app_supports_url_scheme succeeds if the app supports the URL scheme" {
    # Given an app's bundle ID and a URL scheme it supports
    bundle_id='com.apple.Safari'
    url_scheme='https'

    # When that bundle ID and URL scheme are submitted
    zsource src/msda.sh
    zrun _app_supports_url_scheme $bundle_id $url_scheme
    
    # Then the function should succeed
    assert_success
}

@test "_app_supports_url_scheme fails if the app doesn't support the URL scheme" {
    # Given an app's bundle ID and a URL scheme it doesn't support
    bundle_id='com.apple.Safari'
    url_scheme='fakeappscheme'

    # When that bundle ID and URL scheme are submitted
    zsource src/msda.sh
    zrun _app_supports_url_scheme $bundle_id $url_scheme
    
    # Then the function should fail
    assert_failure
}

@test "_expand_uti returns associated file extensions and MIME types for known UTI's" {
    # Given a known UTI
    uti='public.html'

    # When that UTI is submitted submitted
    zsource src/msda.sh
    zrun _expand_uti $uti
    
    # Then the associated file extensions and MIME types should be returned
    assert_output 'html htm shtml shtm text/html'
}

@test "_expand_uti fails for unknown UTI's" {
    # Given an unknown UTI
    uti='dgrdev.fake'

    # When that UTI is submitted submitted
    zsource src/msda.sh
    zrun _expand_uti $uti
    
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
    assert_output 'css:Viewer pdf:Viewer webarchive:Viewer webbookmark:Viewer webhistory:Viewer webloc:Viewer download:Editor safariextz:Viewer gif:Viewer html:Viewer htm:Viewer shtml:Viewer jhtml:Viewer js:Viewer jpg:Viewer jpeg:Viewer jp2:Viewer txt:Viewer text:Viewer png:Viewer tiff:Viewer tif:Viewer url:Viewer ico:Viewer xhtml:Viewer xht:Viewer xhtm:Viewer xht:Viewer xml:Viewer xbl:Viewer xsl:Viewer xslt:Viewer svg:Viewer avif:Viewer webp:Viewer'
}

@test "_get_supported_mime_types returns an array of supported UTI's for an installed app" {
    # Given an installed app's bundle ID
    bundle_id='com.apple.Safari'

    # When that bundle ID is submitted
    zsource src/msda.sh
    zrun _get_supported_mime_types $bundle_id
    
    # Then an array of supported UTI's should be returned
    assert_output 'text/css:Viewer application/pdf:Viewer application/x-webarchive:Viewer application/x-safari-extension:Viewer image/gif:Viewer text/html:Viewer application/x-javascript:Viewer image/jpeg:Viewer image/jp2:Viewer text/plain:Viewer image/png:Viewer image/tiff:Viewer image/x-icon:Viewer application/xhtml+xml:Viewer application/xml:Viewer text/xml:Viewer image/svg+xml:Viewer image/avif:Viewer image/webp:Viewer'
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

@test "_get_supported_url_schemes returns an array of supported URL schemes for an installed app" {
    # Given an installed app's bundle ID
    bundle_id='com.apple.Safari'

    # When that bundle ID is submitted
    zsource src/msda.sh
    zrun _get_supported_url_schemes $bundle_id
    
    # Then an array of supported file extensions should be returned
    assert_output 'http https file x-safari-https prefs x-webkit-app-launch'
}

@test "_get_supported_url_schemes fails for unknown apps" {
    # Given an unknown app's bundle ID
    bundle_id='com.dgrdev.FakeBrowser'

    # When that bundle ID is submitted
    zsource src/msda.sh
    zrun _get_supported_url_schemes $bundle_id
    
    # Then an array of supported file extensions should be returned
    assert_failure
}

@test "_uti_to_mime_type converts an existing UTI to its MIME type" {
    # Given a known UTI
    uti='public.html'

    # When that UTI is submitted
    zsource src/msda.sh
    zrun _uti_to_mime_type $uti

    # Then the function should succeed and return the MIME type
    assert_success
    assert_equal "$output" "text/html"
}

@test "_uti_to_mime_type fails for nonexistent UTIs" {
    # Given a nonexistent UTI
    uti='dgrdev.fake'

    # When that UTI is submitted
    zsource src/msda.sh
    zrun _uti_to_mime_type $uti

    # Then the function should fail
    assert_failure
}
