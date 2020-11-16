!/usr/bin/env bash

if [ $(basename $PWD) == "e2e-test" ]; then
    cd ..
fi

if [ $(basename $PWD) != "osx-dev-bootstrap" ]; then
    echo
    "Cannot execute script in this directory, must be in \"osx-dev-bootstrap\"
    or \"e2e-test\""
    exit 1
fi

if test $(which brew); then
    echo "Uninstalling homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall.sh)"
fi

python3 src/rollback.py
