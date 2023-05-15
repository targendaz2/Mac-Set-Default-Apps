#!/usr/bin/env zsh
# shellcheck shell=bash

# App Settings
CACHE='/Library/Caches/msda'

# Aliases
lsregister='/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister'
PlistBuddy='/usr/libexec/PlistBuddy'

# Initializes the app
function _init() {
    mkdir -p "$CACHE"
}

# Role definitions
function _get_role_definition() {
    local role_name="$1"

    case $role_name in
        browser)
            role_url_schemes=(
                http
                https
            )
            role_utis=(
                public.html:Viewer
                public.url:Viewer
                public.xhtml:Viewer
            )
            ;;
        calendar)
            role_url_schemes=(
                webcal
            )
            role_utis=(
                com.apple.ical.ics:All
                com.apple.ical.vcs:All
            )
            ;;
        mail)
            role_url_schemes=(
                mailto
            )
            ;;
        pdf)
            role_utis=(
                com.adobe.pdf:All
            )
            ;;
        *)
            return 1
            ;;
    esac

    return 0
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
    path="$(_app_id_to_path $bundle_id)"

    [ -z "$path" ] && return 1
    return 0
}

# Check if an app supports a role
function _app_supports_role() {
    local bundle_id="$1"
    local role_name="$2"

    _get_role_definition $role_name

    if [ ${#role_url_schemes[@]} = 0 ] && [ ${#role_utis[@]} = 0 ]; then
        return 1
    fi

    if [ ${#role_url_schemes[@]} -gt 0 ]; then
        for url_scheme in ${role_url_schemes[@]}; do
            _app_supports_url_scheme $bundle_id $url_scheme
            result=$?
            [ $result = 1 ] && return 1
        done
    fi

    if [ ${#role_utis[@]} -gt 0 ]; then
        for uti in ${role_utis[@]}; do
            _app_supports_uti $bundle_id $uti
            result=$?
            [ $result = 1 ] && return 1
        done
    fi

    return 0
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
    local uti_and_role="$2"
    local uti=$(echo $uti_and_role | cut -d ":" -f 1)
    local uti_role=$(echo $uti_and_role | cut -d ":" -f 2)

    local supported_mime_types="$(_get_supported_mime_types $bundle_id)"
    local supported_extensions="$(_get_supported_extensions $bundle_id)"

    local tags="$(_convert_uti $uti)"
    tags=( $(echo ${tags}) )

    for tag in ${tags[@]}; do
        if [ "$tag" = *'/'* ]; then
            [[ "$supported_mime_types" == *"$tag:$uti_role"* ]] && return 0
        else
            [[ "$supported_extensions" == *"$tag"* ]] && return 0
        fi
    done
    
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

            local role=$($PlistBuddy $info_plist -c "print :CFBundle${type_name}Types:$i:CFBundleTypeRole" 2>/dev/null)

            [ ! -z $role ] && item+=":$role"

            type_array+="$item "
        done
    done

    echo "$type_array" | xargs
    return 0
}

# Gets file extensions and MIME types assciated with a UTI
function _convert_uti() {
    local uti="$1"
    local tags=$($lsregister -gc -dump Type | \
        awk -F ':' "{ \
            if (\$1 == \"type id\" && \$2 ~ \"$uti\") { \
                check=\"yes\" \
            } else if (\$1 == \"type id\") { \
                check=\"no\" \
            } else if (\$1 == \"tags\" && check == \"yes\") { \
                print \$2 \
            } \
        }" \
    )

    [ -z "$tags" ] && return 1

    tags="$(echo "$tags" | sed -r "s/('[A-Z]*')|(\"[A-z ]*\")|(['\.\,])//g" | tr -s ' ' | xargs)"

    echo "$tags"
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
    [ $? = 1 ] && return 1
    return 0
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
