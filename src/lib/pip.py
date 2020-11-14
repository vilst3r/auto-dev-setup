"""
Module delegated to handling PIP logic
"""

# Native Modules
import logging
import sys
from itertools import tee
from subprocess import PIPE, Popen, check_output
from typing import List

# Custom Modules
from singletons.setup import SetupSingleton
from utils.general import (consume, format_ansi_string, format_success_message,
                           partition)
from utils.unicode import ForeGroundColor

SETUP = SetupSingleton.get_instance()
LOGGER = logging.getLogger()


def retrieve_processed_packages(filename: str = None) -> List[str]:
    """
    Parses the output format generated from 'pip3 list --user' from either the
    the config directory for PIP or the user system

    The output will look like this (excluding the (-|+) border):
    +-------------------------------+
    | Package             Version   |
    | ------------------- ----------|
    | autopep8            1.5       |
    | ...                           |
    | ...                           |
    +-------------------------------+

    We need to parse from the third line onwards & install the latest by
    reading the first column only of each line based on this 'assumption'
    """
    if not filename:
        command = "pip3 list --user"
        output = check_output(command.split())
        pip_list = output.decode('utf-8').strip().split('\n')[2:]
        packages = [x.split()[0] for x in pip_list]
    else:
        with open(filename) as text_file:
            data = [x.strip() for x in text_file.readlines()[2:]]
            packages = [x.split()[0] for x in data]
    return packages


def install_all_pip_packages_at_user():
    """
    Downloads & installs every package config if it's valid
    """
    def process_package(package: str):
        """
        Installs the package if possible & logs correspondingly
        """
        command = f'pip3 install --user {package}'
        with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
            out, err = process.communicate()
            installed_successfully = process.returncode == 0

            if err and not installed_successfully:
                LOGGER.warning(err.decode('utf-8'))
                LOGGER.warning(format_ansi_string(f'{package} - issue during '
                                                  f'installation or it the '
                                                  f'package doesn\'t exist',
                                                  ForeGroundColor.YELLOW))
            else:
                LOGGER.debug(out.decode('utf-8'))
                LOGGER.info(format_ansi_string(f'{package} - successfully '
                                               f'installed',
                                               ForeGroundColor.GREEN))

    user_packages = retrieve_processed_packages()
    configured_packages = retrieve_processed_packages(SETUP.files.pip)

    installed_packages, uninstalled_packages = partition(
        lambda x: x in user_packages, configured_packages)

    consume(map(lambda x: LOGGER.info(
        format_ansi_string(f'{x} - already installed',
                           ForeGroundColor.LIGHT_GREEN)), installed_packages))

    uninstalled_packages, uninstalled_packages_copy = tee(uninstalled_packages)

    if not next(uninstalled_packages_copy, None):
        LOGGER.info(format_success_message(
            'No available pip packages to install'))
    else:
        consume(map(lambda x: process_package(x), uninstalled_packages))
        LOGGER.info(format_success_message(
            'All configured pip packages are now installed'))


def delete_all_user_packages():
    """
    Uninstalls all PIP packages at the user level
    """
    command = "pip3 freeze --user"
    pip_freeze_process = Popen(command.split(), stdout=PIPE)

    command = "xargs pip3 uninstall -y"
    with Popen(command.split(), stdin=pip_freeze_process.stdout, stdout=PIPE) \
            as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to delete PIP packages '
                                            'via piped shell process',
                                            ForeGroundColor.RED))
            sys.exit()

        parsed_output = out.decode('utf-8')

        LOGGER.debug(parsed_output)
        LOGGER.info(format_success_message(
            'All configured PIP packages are now deleted'))
