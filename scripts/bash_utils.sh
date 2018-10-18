activate_venv() {
    if [ ! -d .venv ]; then
        if ! hash py 2>/dev/null ; then
            python3.7 -m venv .venv
        else
            py -3.7 -m venv .venv
        fi
    fi
    WIN_VENV_PATH="./.venv/Scripts/activate"
    LINUX_VENV_PATH="./.venv/bin/activate"
    if [ -f $WIN_VENV_PATH ]; then
        source "${WIN_VENV_PATH}"
    else
        source "${LINUX_VENV_PATH}"
    fi
}

install_redis() {
    unameOut="$(uname -s)"
    case "${unameOut}" in
        Linux*|Darwin*)    install_linux_redis;;
        CYGWIN*|MINGW*)    install_windows_redis;;
        *)                 echo "UNKNOWN:${unameOut}"
                        exit 1
    esac
}

install_windows_redis() {
    if [ ! -f ./redis/win/redis-server.exe ]; then
        mkdir -p redis/win
        pushd redis/win
        rm -rf *
        curl 'https://github.com/MicrosoftArchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.zip' -O -J -L
        unzip *.zip
        rm *.zip *.docx
        popd
    fi
}

install_linux_redis() {
    if [ ! hash python3.7 2>/dev/null ]; then
        mkdir -p redis/linux
        pushd redis/linux
        rm -rf *
        wget http://download.redis.io/redis-stable.tar.gz
        tar xvzf redis-stable.tar.gz
        rm redis-stable.tar.gz
        mv redis-stable/* .
        rm -r redis-stable
        make
        pop
        pop
    fi
}

run_redis() {
    unameOut="$(uname -s)"
    case "${unameOut}" in
        Linux*|Darwin*)    ./redis/linux/src/redis-server;;
        CYGWIN*|MINGW*)    ./redis/win/redis-server.exe ./redis/win/redis.windows.conf;;
        *)                 echo "UNKNOWN:${unameOut}"
                           exit 1
    esac
}

stop_redis() {
    unameOut="$(uname -s)"
    case "${unameOut}" in
        Linux*|Darwin*)    ./redis/linux/src/redis-cli shutdown;;
        CYGWIN*|MINGW*)    ./redis/win/redis-cli.exe shutdown;;
        *)                 echo "UNKNOWN:${unameOut}"
                           exit 1
    esac
}
