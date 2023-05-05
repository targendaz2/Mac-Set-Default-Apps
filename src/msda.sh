#!/usr/bin/env zsh

function print_help() {
    local message="$1"
    [ ! -z "$message" ] && print "$message\n"
    print -rC1 --      \
        "msda.sh [-h|--help]" \
        "msda.sh [set]"
    exit
}

function set_command() {
    print command is set
    exit
}

# Parse keyword args
zparseopts -D -E -F -- \
    {h,-help}=help \
    || exit

# Get positional args
command=$1

# Parse positional args
case $command in
    set)
        set_command
        ;;
    *)
        print_help "\"$command\" is not a valid command"
        ;;
esac


if (( $#help )); then
    print_help
    return
fi
