#!/usr/bin/env bash

set -euo pipefail

source ~/.easy-psmp/.venv/bin/activate \
    && python ~/.easy-psmp/epsmp.py scp "$@"
