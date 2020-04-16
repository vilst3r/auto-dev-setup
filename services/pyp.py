"""
Module delegated to handling pyp logic
"""

# Native Modules
import logging
import sys
from itertools import tee
from subprocess import Popen, call, check_output, PIPE, DEVNULL

# Third Party Modules
import pexpect

# Custom Modules
from singletons.setup import SetupSingleton
from utils.general import consume, partition, format_ansi_string, \
    format_success_message
from utils.unicode import ForeGroundColor

SETUP: SetupSingleton = SetupSingleton.get_instance()
LOGGER = logging.getLogger()


def process_file() -> list:
    """
    Parses the config file generated from 'pip freeze > pip_leaves' located in
    the config directory

    The content of the file will look like this (excluding the (-|+) border):
    +-------------------------------+
    | Package             Version   |
    | ------------------- ----------|
    | autopep8            1.5       |
    | ...                           |
    | ...                           |
    +-------------------------------+
    We need to parse from the third line onwards & install the latest by
    reading the first column only of each line
    """
    return
    # with open(SETUP.pyp_config_file) as text_file:


def install_all_pip_packages():
    """
    Downloads & installs every package config if it's valid
    """
    return
