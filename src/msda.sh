#!/usr/bin/env zsh

# Aliases
lsregister='/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister'
PlistBuddy='/usr/libexec/PlistBuddy'

# Gets an app's path from its ID
function _app_id_to_path() {
    local bundle_id="$1"
    local app_path=$(mdfind kMDItemCFBundleIdentifier = $bundle_id)
    [ -z "$app_path" ] && return 1
    echo "$app_path"
    return 0
}

# Checks if an app with the specified ID is installed
function _app_is_installed() {
    local bundle_id="$1"
    _app_id_to_path $bundle_id
    return $?
}

# Check if an app supports a UTI
function _app_supports_uti() {
    local bundle_id="$1"
    local uti="$2"

    local app_path=$(_app_id_to_path $bundle_id)
}

# Gets the path to an app's Info.plist
function _get_app_info_plist() {
    local bundle_id="$1"
    local app_path=$(_app_id_to_path $bundle_id)
    local info_plist_path=$app_path/Contents/Info.plist

    [ ! -f "$info_plist_path" ] && return 1

    echo "$info_plist_path"
    return 0
}

# Converts a UTI to a MIME type
function _uti_to_mime() {
    local uti="$1"
    local mime_type="$($lsregister -gc -dump MIMEBinding | awk -F ':' "/$uti/ {print \$1}")"

    [ -z "$mime_type" ] && return 1
    
    echo "$mime_type"
    return 0
}

function print_help() {
    local message="$1"
    [ ! -z "$message" ] && print "$message\n"
    print -rC1 --      \
        "msda.sh [-h|--help]" \
        "msda.sh [set]"
    return 0
}

function set_command() {
    local bundle_id="$1"
    _app_is_installed $bundle_id
    return $?
}

if [[ "$ZSH_EVAL_CONTEXT" == 'toplevel' ]]; then
    # Parse keyword args
    zparseopts -D -E -F -- \
        {h,-help}=help \
        -browser=browser \
        || return

    # Get positional args
    command=$1

    # Parse positional args
    case $command in
        set)
            set_command
            ;;
        '')
            print_help
            ;;
        *)
            print_help "\"$command\" is not a valid command"
            ;;
    esac


    if (( $#help )); then
        print_help
        return
    fi
    exit 0
fi
