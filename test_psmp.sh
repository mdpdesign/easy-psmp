#!/usr/bin/env bash

set -euo pipefail

# set -x

declare -ra questions=(
    "Password:"
    "Multi-factor authentication is required."
    "Provide a reason for this operation:"
)

declare -a passed=()
declare -a failed=()

for question in "${questions[@]}"; do
    echo "${question}"

    case "${question}" in
        Pass*) match='^vagrant$' ;;
        Multi*) match='[[:digit:]]{6}' ;;
        *reason*) match='^BAU$' ;;
        * ) echo "Did not match question!.."; exit 1 ;;
    esac

    read -rs line < /dev/stdin

    if grep -qE "${match}" <<< "${line}"; then
        passed+=("PASSED: ${question}")
    else
        failed+=("FAILED: ${question}, expected: '${match}', got: '${line}'")
    fi

done

echo
echo "TESTS SUMMARY:"
printf '%s\n' "${passed[@]}"
printf '%s\n' "${failed[@]}"

[[ "${#failed[@]}" -gt 0 ]] && exit 1
