#!/usr/bin/env zsh
# shellcheck shell=bash

# Settings
CACHE='/Library/Caches/msda'

# Aliases
lsregister='/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister'
PlistBuddy='/usr/libexec/PlistBuddy'

# Initializes the app
function _init() {
    mkdir -p "$CACHE"
}

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

# Check if an app supports a URL scheme
function _app_supports_url_scheme() {
    local bundle_id="$1"
    local url_scheme="$2"

    local supported_url_schemes="$(_get_supported_url_schemes $bundle_id)"

    [[ "$supported_url_schemes" == *"$url_scheme"* ]] && return 0
    return 1
}

# Check if an app supports a UTI
function _app_supports_uti() {
    local bundle_id="$1"
    local uti="$2"

    local supported_mime_types="$(_get_supported_mime_types $bundle_id)"
    local mime_type="$(_uti_to_mime_type $uti)"
    [ -z "$mime_type" ] && return 1

    [[ "$supported_mime_types" == *"$mime_type"* ]] && return 0
    return 1
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

# Gets all file extensions supported by an app
function _get_supported_extensions() {
    local bundle_id="$1"

    local result="$(_parse_supported_types $bundle_id Document TypeExtensions)"

    [ -z "$result" ] && return 1

    echo "$result"
    return 0
}

# Gets all MIME types supported by an app
function _get_supported_mime_types() {
    local bundle_id="$1"
    
    local result="$(_parse_supported_types $bundle_id Document TypeMIMETypes)"

    [ -z "$result" ] && return 1

    echo "$result"
    return 0
}

function _get_supported_url_schemes() {
    local bundle_id="$1"
    
    local result="$(_parse_supported_types $bundle_id URL URLSchemes)"

    [ -z "$result" ] && return 1

    echo "$result"
    return 0
}

# Returns a list of types supported by the specified app
function _parse_supported_types() {
    local bundle_id="$1"
    local info_plist=$(_get_app_info_plist "$bundle_id")
    local type_name="$2"
    local subtype_name="$3"
    local file_line_count=$(wc -l < $info_plist | xargs)
    local type_array=''

    for (( i=0; i<$file_line_count; i++ )); do
        local supported_type=$($PlistBuddy $info_plist -c "print :CFBundle${type_name}Types:$i:CFBundle${subtype_name}" 2>/dev/null)
        local result=$?

        [ $result = 1 ] && continue

        local array_line_count=$(echo $supported_type | wc -l | xargs)

        for (( n=0; n<(($array_line_count-2)); n++ )); do
            local item=$($PlistBuddy $info_plist -c "print :CFBundle${type_name}Types:$i:CFBundle${subtype_name}:$n")

            type_array+="$item "
        done
    done

    echo "$type_array" | xargs
    return 0
}

# Converts a UTI to a MIME type
function _uti_to_mime_type() {
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
