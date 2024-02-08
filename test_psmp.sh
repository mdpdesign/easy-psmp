#!/usr/bin/env bash

set -euo pipefail

# set -x

declare -ra questions=(
    "Provide password:"
    "Provide token. Multi-factor authentication is required."
    "Why are you logging in? Provide a reason for this operation:"
)

declare -a passed=()
declare -a failed=()

for question in "${questions[@]}"; do
    echo "${question}"

    case "${question}" in
        *[Pp]assword*) match='^vagrant$' ;;
        *[Mm]ulti*) match='[[:digit:]]{6}' ;;
        *reason*) match='^BAU$' ;;
        * ) echo "Did not match question!.."; exit 1 ;;
    esac

    read -rs line < /dev/stdin

    if grep -qE "${match}" <<< "${line}"; then
        passed+=("PASSED, expected: '${match}', got: '${line}'")
    else
        failed+=("FAILED, expected: '${match}', got: '${line}'")
    fi

done

echo
echo "TESTS SUMMARY:"
printf '%s\n' "${passed[@]}"
printf '%s\n' "${failed[@]}"

[[ "${#failed[@]}" -gt 0 ]] && exit 1

exit 0
