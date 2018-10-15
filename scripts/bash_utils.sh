activate_venv() {
    if [ ! -d .venv ]; then
        if ! hash pyddd 2>/dev/null ; then
            py="./scripts/py.sh"
        else
            py="py"
        fi
        ${py} -3.7 -m venv .venv
    fi
    WIN_VENV_PATH="./.venv/Scripts/activate"
    LINUX_VENV_PATH="./.venv/bin/activate"
    if [ -f $WIN_VENV_PATH ]; then
        source "${WIN_VENV_PATH}"
    else
        source "${LINUX_VENV_PATH}"
    fi
}
