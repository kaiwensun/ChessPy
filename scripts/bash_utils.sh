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

build_translations() {
    if [ -f "app/translations/messages.pot" ]; then
        echo "A translations messages.pot file is found. Please make sure messages.mo and messages.po files are in good state."
    else
        declare -a locales=("zh_Hans_CN" "zh_Hant_TW")
        pybabel extract -F config/babel.cfg -k lazy_gettext -o app/translations/messages.pot --input-dirs=.
        for locale in "${locales[@]}"
        do
            pybabel init -i app/translations/messages.pot -d app/translations -l ${locale}
        done
        echo "Don't forget to edit these messages.po file(s) and run 'paybabel compile'"
        for locale in "${locales[@]}"
        do
            echo "   - app/translations/${locales[@]}/LC_MESSAGES/messages.po"
        done
    fi
    pybabel compile -d app/translations
}
