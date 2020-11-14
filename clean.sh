!/usr/bin/env bash

# Require root user to execute
if [ "$(whoami)" != "root" ]; then
    echo "Please run the script as the root user"
    exit 1
fi

if test $(which brew); then
    echo "Uninstalling homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall.sh)"
fi

python3 rollback.py
