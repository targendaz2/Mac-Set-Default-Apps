setup() {
    load '../../node_modules/bats-support/load'
    load '../../node_modules/bats-assert/load'
    load '../../node_modules/bats-zsh/load'

    load '../utils/utils'
}

teardown() {
    :
}

@test "_cache_supported_utis caches an installed app's supported UTI's" {
    # Given an installed app
    bundle_id='com.apple.Safari'

    # When the app's bundle ID is submitted
    zsource src/msda.sh
    zrun _cache_supported_utis $bundle_id
    
    # Then the app's supported UTI's should be cached
    cache=/Library/Caches/msda/com.apple.Safari.txt
    assert [ ! -z "$(cat "$cache" | grep 'text/html:Viewer')" ]
    assert [ ! -z "$(cat "$cache" | grep 'application/xhtml+xml:Viewer')" ]
    assert [ ! -z "$(cat "$cache" | grep 'url:Viewer')" ]
}

@test "_cache_supported_utis doesn't write duplicates to cache" {
    # Given an installed app
    bundle_id='com.apple.Safari'

    # When the app's bundle ID is submitted
    zsource src/msda.sh
    zrun _cache_supported_utis $bundle_id
    
    # Then the app's supported UTI's should be cached
    cache=/Library/Caches/msda/com.apple.Safari.txt
    html_count=$(cat "$cache" | grep 'text/html:Viewer' | wc -l | xargs)
    assert_equal $html_count 1
}
