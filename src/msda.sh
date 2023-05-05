#!/usr/bin/env zsh

function app_is_installed() {
    local app_id="$1"
    app_path=$(mdfind kMDItemCFBundleIdentifier = $app_id)
    [ -z "$app_path" ] && return 1
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
    :
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
