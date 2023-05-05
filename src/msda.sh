#!/usr/bin/env zsh

# Aliases
lsregister='/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister'

function _app_is_installed() {
    local app_id="$1"
    local app_path=$(mdfind kMDItemCFBundleIdentifier = $app_id)
    [ -z "$app_path" ] && return 1
    return 0
}

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
    local app_id="$1"
    app_path=$(mdfind kMDItemCFBundleIdentifier = $app_id)
    [ -z "$app_path" ] && return 1
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
