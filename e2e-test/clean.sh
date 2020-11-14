!/usr/bin/env bash

# Test cleanup is same as regular script but no need for sudo prompt

if test $(which brew); then
    echo "Uninstalling homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall.sh)"
fi

python3 rollback.py
