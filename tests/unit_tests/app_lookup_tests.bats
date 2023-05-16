setup() {
    load '../../node_modules/bats-support/load'
    load '../../node_modules/bats-assert/load'
    load '../../node_modules/bats-zsh/load'

    load '../utils/utils'
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
