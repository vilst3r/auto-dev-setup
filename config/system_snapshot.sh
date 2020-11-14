#!/usr/bin/env bash

if [ $(basename $PWD) != "config" ]; then
    echo "Cannot execute script in this directory, must run from ./config"
    exit 1
fi

# Require root user to execute
if [ "$(whoami)" == "root" ]; then
    echo "Running as root is disabled for this script"
    exit 1
fi


if test $(which brew); then
    brew leaves > brew/leaves
    brew list --cask > brew/casks
fi

if test $(which pip3); then
    pip3 list --user > pip/leaves
fi

echo "Snapshot generated for config files (brew & pip)"
