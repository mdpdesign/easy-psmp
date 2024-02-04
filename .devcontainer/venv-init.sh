#!/usr/bin/env bash

set -euo pipefail

VENV_DIR=".venv"

if [ ! -d "${VENV_DIR}" ]; then
  virtualenv "${VENV_DIR}"
fi

# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate" 2>/dev/null && pip install -r requirements.txt && pip list

exit 0
