#!/usr/bin/env bash

if [ $(basename $PWD) != "osx-dev-bootstrap" ]; then
    echo "Cannot execute script in this directory, must be in \"osx-dev-bootstrap\""
    exit 1
fi


if test ! $(find config/git-credentials.txt); then
    echo "username: <INSERT OWN VALUE>" >> config/git-credentials.txt
    echo "email: <INSERT OWN VALUE>" >> config/git-credentials.txt
    echo "token: <INSERT OWN VALUE>" >> config/git-credentials.txt
    echo "Please configure ./config/git-credentials.txt"
    exit 1
fi

# Install homebrew
if test ! $(which brew); then
    echo "Installing homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    brew install python
fi

# Install requirements for the script
if test ! $(which pip3); then
    echo "pip3 is not installed..."
    exit 1
else
    pip3 install --user -r src/requirements.txt
fi

# Run main script that bootstraps the development environment
python3 src/run.py
