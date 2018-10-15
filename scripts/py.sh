#!/bin/bash
version=$1
if [[ $version == "-2" ]]; then
    python2 "${@:2}"
elif [ $version == "-3.7" ] && [ hash python3.7 2>/dev/null ]; then
    python3.7 "${@:2}"
elif [ ${version:0:2} == "-3" ] && [ hash python3 2>/dev/null ]; then
    python3 "${@:2}"
else
    python "${@:2}"
fi
