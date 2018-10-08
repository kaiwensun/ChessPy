activate_venv() {
    if [ ! -d .venv ]; then
        py -3 -m venv .venv
    fi
    WIN_VENV_PATH="./.venv/Scripts/activate"
    LINUX_VENV_PATH="./.venv/bin/activate"
    if [ -f $WIN_VENV_PATH ]; then
        source "${WIN_VENV_PATH}"
    else
        source "${LINUX_VENV_PATH}"
    fi
}
