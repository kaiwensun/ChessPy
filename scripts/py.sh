#!/bin/bash
set -e
version=$1
if [ $version == "-3.7" ] && [ hash python3.7 2>/dev/null ]; then
    python3.7 "${@:2}"
elif [ hash python3 2>/dev/null ]; then
    echo "Warning: python3 is depreciated. Please use python3.7"
    python3 "${@:2}"
else
    echo "Can't find python3.7"
    exit 127
fi
