#!/bin/bash
set -e
pushd $( dirname "${BASH_SOURCE[0]}" )/.. > /dev/null
source "./scripts/bash_utils.sh"
activate_venv

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*|Darwin*)    machine="linux";;
    CYGWIN*|MINGW*)    machine="win";;
    *)                 echo "UNKNOWN:${unameOut}"
                       exit 1
esac
python wsgi_server.py -${machine}

deactivate
popd > /dev/null
