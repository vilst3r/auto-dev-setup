"""
Module delegated to handling brew logic
"""

# Native Modules
import logging
from itertools import tee
from subprocess import DEVNULL, PIPE, Popen, call, check_output

# Custom Modules
from singletons.setup import SetupSingleton
from utils.general import (consume, format_ansi_string, format_success_message,
                           partition)
from utils.unicode import ForeGroundColor

SETUP = SetupSingleton.get_instance()
LOGGER = logging.getLogger()


def install_all_brew_packages():
    """
    Downloads & installs every package configured
    """
    def process_package(package: str):
        """
        Installs the package if possible & logs correspondingly
        """
        command = f'brew info {package}'
        package_found = call(command.split(), stdout=DEVNULL) == 0

        if not package_found:
            LOGGER.warning(format_ansi_string(f'This package does not exist '
                                              f'in registry - {package}',
                                              ForeGroundColor.YELLOW))
            return

        command = f'brew install {package}'
        with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
            out, err = process.communicate()
            installed_successfully = process.returncode == 0

            if err and not installed_successfully:
                LOGGER.warning(err.decode('utf-8'))
                LOGGER.warning(format_ansi_string(f'{package} - issue during '
                                                  f'installation',
                                                  ForeGroundColor.YELLOW))
            else:
                LOGGER.debug(out.decode('utf-8'))
                LOGGER.info(format_ansi_string(f'{package} - successfully '
                                               f'installed',
                                               ForeGroundColor.GREEN))

    command = 'brew list --formula'
    output = check_output(command.split())
    brew_list = output.decode('utf-8').strip().split('\n')

    with open(SETUP.files.brew) as text_file:
        configured_packages = map(lambda x: x.strip(), text_file.readlines())

        installed_packages, uninstalled_packages = partition(
            lambda x: x in brew_list, configured_packages)

        consume(map(lambda x: LOGGER.info(
            format_ansi_string(f'{x} - already installed',
                               ForeGroundColor.LIGHT_GREEN)), installed_packages))

        uninstalled_packages, uninstalled_packages_copy = tee(
            uninstalled_packages)

        if not next(uninstalled_packages_copy, None):
            LOGGER.info(format_success_message(
                'No available brew packages to install'))
        else:
            consume(map(lambda x: process_package(x), uninstalled_packages))
            LOGGER.info(format_success_message(
                'All configured brew packages are now install'))


def install_all_cask_packages():
    """
    Downloads & installs every package configured
    """
    def process_package(package: str):
        """
        Installs the package if possible & logs correspondingly
        """
        command = f'brew cask info {package}'
        package_found = call(command.split(), stdout=DEVNULL) == 0

        if not package_found:
            LOGGER.warning(format_ansi_string(f'This package does not exist '
                                              f'in registry - {package}',
                                              ForeGroundColor.YELLOW))
            return

        command = f'brew cask install {package}'
        with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
            out, err = process.communicate()
            installed_successfully = process.returncode == 0

            if err and not installed_successfully:
                LOGGER.warning(err.decode('utf-8'))
                LOGGER.warning(format_ansi_string(f'{package} - issue during '
                                                  f'installation',
                                                  ForeGroundColor.YELLOW))
            else:
                LOGGER.debug(out.decode('utf-8'))
                LOGGER.info(format_ansi_string(f'{package} - successfully '
                                               f'installed',
                                               ForeGroundColor.GREEN))

    command = 'brew list --cask'
    output = check_output(command.split())
    cask_list = output.decode('utf-8').strip().split('\n')

    with open(SETUP.files.cask) as text_file:
        configured_packages = map(lambda x: x.strip(), text_file.readlines())

        installed_packages, uninstalled_packages = partition(
            lambda x: x in cask_list, configured_packages)

        consume(map(lambda x: LOGGER.info(
            format_ansi_string(f'{x} - already installed',
                               ForeGroundColor.LIGHT_GREEN)), installed_packages))

        uninstalled_packages, uninstalled_packages_copy = tee(
            uninstalled_packages)

        if not next(uninstalled_packages_copy, None):
            LOGGER.info(format_success_message(
                'No available cask packages to install'))
        else:
            consume(map(lambda x: process_package(x), uninstalled_packages))
            LOGGER.info(format_success_message(
                'All configured brew cask packages are now install'))
