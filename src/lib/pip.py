"""
Module delegated to handling PIP logic
"""

# Native Modules
import logging
import sys
from itertools import tee
from subprocess import DEVNULL, PIPE, Popen, call, check_output

# Custom Modules
from singletons.setup import SetupSingleton
from utils.general import (consume, format_ansi_string, format_success_message,
                           partition)
from utils.unicode import ForeGroundColor

# Third Party Modules
# import pexpect


SETUP = SetupSingleton.get_instance()
LOGGER = logging.getLogger()


def install_all_pip_packages():
    pass


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
    return []
    # with open(SETUP.files.pip) as text_file:


def install_packages():
    """
    Downloads & installs every package config if it's valid
    """
    return


# def install_powerline_at_user():
#     """
#     Installs the powerline tool at the user level of the system
#     """
#     command = 'pip3 install --user powerline-status'
#     with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
#         out, err = process.communicate()

#         if err:
#             LOGGER.error(err.decode('utf-8'))
#             LOGGER.error(format_ansi_string('Failed to install powerline from '
#                                             'pip3', ForeGroundColor.RED))
#             sys.exit()
#         else:
#             LOGGER.debug(out.decode('utf-8'))
#             LOGGER.info(format_ansi_string('Powerline now installed from pip3 '
#                                            'at the user level',
#                                            ForeGroundColor.GREEN))
