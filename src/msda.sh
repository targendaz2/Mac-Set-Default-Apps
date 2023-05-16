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

# App lookup functions

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

# Gets the path to an app's Info.plist
function _get_app_info_plist() {
    local bundle_id="$1"
    local app_path=$(_app_id_to_path $bundle_id)
    local info_plist_path=$app_path/Contents/Info.plist

    [ ! -f "$info_plist_path" ] && return 1

    echo "$info_plist_path"
    return 0
}

# Cache functions

# Caches an app's supported UTI's
function _cache_supported_utis() {
    local bundle_id="$1"

    local info_plist="$(_get_app_info_plist $bundle_id)"

    local cache_file="$CACHE/$bundle_id.txt"

    local document_type_count=$($PlistBuddy $info_plist -c "print :CFBundleDocumentTypes" | grep CFBundleTypeName | wc -l | xargs)

    echo '' > "$cache_file"

    for (( i=0; i<$document_type_count; i++ )); do
        local role="$($PlistBuddy $info_plist -c "print :CFBundleDocumentTypes:$i:CFBundleTypeRole")"

        local mime_type_count=$(($($PlistBuddy $info_plist -c "print :CFBundleDocumentTypes:$i:CFBundleTypeMIMETypes" 2>/dev/null | wc -l | xargs) - 2))

        if [ $mime_type_count -gt 0 ]; then
            for (( m=0; m<$mime_type_count; m++ )); do
                local mime_type="$($PlistBuddy $info_plist -c "print :CFBundleDocumentTypes:$i:CFBundleTypeMIMETypes:$m")"

                echo "$mime_type:$role" >> "$cache_file"
            done
            continue
        fi

        local extension_count=$(($($PlistBuddy $info_plist -c "print :CFBundleDocumentTypes:$i:CFBundleTypeExtensions" 2>/dev/null | wc -l | xargs) - 2))

        if [ $extension_count -gt 0 ]; then
            for (( e=0; e<$extension_count; e++ )); do
                local extension="$($PlistBuddy $info_plist -c "print :CFBundleDocumentTypes:$i:CFBundleTypeExtensions:$e")"

                echo "$extension:$role" >> "$cache_file"
            done
        else
            return 0
        fi
    done

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
    local role="$2"

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
