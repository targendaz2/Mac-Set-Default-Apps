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

# Gets all UTI's supported by an app
function _get_supported_mime_types() {
    local bundle_id="$1"
    local info_plist=$(_get_app_info_plist "$bundle_id")
    local file_line_count=$(wc -l < $info_plist | xargs)

    local mime_type_array=''
    for (( i=0; i<$file_line_count; i++ )); do
        local document_type=$($PlistBuddy $info_plist -c "print :CFBundleDocumentTypes:$i:CFBundleTypeMIMETypes" 2>/dev/null)
        local result=$?
        
        [ $result = 1 ] && continue

        local array_line_count=$(($(echo $document_type | wc -l | xargs) - 2))

        for (( n=0; n<$array_line_count; n++ )); do
            local mime_type=$($PlistBuddy $info_plist -c "print :CFBundleDocumentTypes:$i:CFBundleTypeMIMETypes:$n")

            mime_type_array+="$mime_type "
        done
    done

    [ -z "$mime_type_array" ] && return 1

    mime_type_array=$(echo "$mime_type_array" | xargs)
    echo "$mime_type_array"
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
