#!/usr/bin/env bash
# Sets LLM_API_KEY for the CURRENT shell session — nothing is written to disk.
# MUST be sourced (a plain execution runs in a subshell and changes nothing):
#   source set-key.sh
# Every python/poetry command started from this shell inherits the key.

if [ "${BASH_SOURCE[0]:-}" = "$0" ]; then
    echo "Please source this script instead of executing it:  source set-key.sh" >&2
    exit 1
fi

read -rs -p "LLM API key (input hidden): " LLM_API_KEY
echo
if [ -n "$LLM_API_KEY" ]; then
    export LLM_API_KEY
    echo "LLM_API_KEY set for this session. It vanishes when the shell closes."
else
    echo "Empty input - LLM_API_KEY not set." >&2
fi
