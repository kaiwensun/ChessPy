#!/bin/bash
set -e
pushd $( dirname "${BASH_SOURCE[0]}" ) > /dev/null
source "./scripts/bash_utils.sh"
activate_venv
python run.py
deactivate
popd > /dev/null
