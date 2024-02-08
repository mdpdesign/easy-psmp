#!/usr/bin/env bash

set -euo pipefail

declare -ra questions=(
    "Password:"
    "Multi-factor authentication is required."
    "Provide a reason for this operation:"
)

for question in "${questions[@]}"; do
    echo "${question}"

    case "${question}" in
        Pass*) match='vagrant' ;;
        Multi*) match='[[:digit:]]{6}' ;;
        *reason*) match='BAU' ;;
        * ) echo "Did not match question!.."; exit 1 ;;
    esac

    while read -s line; do
        grep -qE "${match}" <<< "${line}" || { echo "Incorrect answer";  exit 1; }
        echo "  Got ${line}, correct"
        break
    done < /dev/stdin
done

echo "Tests done" && exit 0
