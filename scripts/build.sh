#!/bin/bash

set -e
pushd $( dirname "${BASH_SOURCE[0]}" )/.. > /dev/null
source "scripts/bash_utils.sh"
activate_venv

python -m pip install --upgrade pip
pip install -r config/requirements.txt
# install wsgi server
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*|Darwin*)    pip install -I gunicorn==19.9.0;;
    CYGWIN*|MINGW*)    pip install -I waitress==1.1.0;;
    *)                 echo "UNKNOWN:${unameOut}"
                       exit 1
esac

for arg in $@
do
case "$arg" in
    -d|-dev|--dev)
    pip install -r config/requirements_dev.txt
    ;;
esac
done

deactivate
popd > /dev/null
