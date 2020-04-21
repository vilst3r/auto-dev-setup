"""
Module delegated to handling brew logic
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


def brew_exists() -> bool:
    """
    Checks if the brew dependency management tool exists in the system
    """
    command = f'find {SETUP.brew_dir}'
    directory_found = call(
        command.split(), stdout=DEVNULL, stderr=DEVNULL) == 0

    if not directory_found:
        LOGGER.info(format_ansi_string('Brew hasn\'t been configured',
                                       ForeGroundColor.LIGHT_RED))

    return directory_found


def install_brew():
    """
    Pulls brew from the web & installs it with local authentication
    """
    ruby_bin = '/usr/bin/ruby'
    brew_url = 'https://raw.githubusercontent.com/Homebrew/install/master/' \
               'install'

    command = f'{ruby_bin} -e \"$(curl -fsSL {brew_url})\"'
    child = pexpect.spawn('/bin/bash', ['-c', command])

    try:
        child.expect('Press RETURN', timeout=60*5)
    except pexpect.TIMEOUT:
        LOGGER.error(format_ansi_string('Request to install from brew url '
                                        'timed out', ForeGroundColor.RED))
        sys.exit()

    child.sendline('')

    try:
        child.expect('Password:', timeout=60*5)
    except pexpect.TIMEOUT:
        LOGGER.error(format_ansi_string('Child process timed out from '
                                        'installation', ForeGroundColor.RED))
        sys.exit()

    child.sendline(SETUP.password)

    try:
        expectations = ['Sorry, try again.', pexpect.EOF]
        index = child.expect(expectations, timeout=60*30)

        if index == 0:
            LOGGER.error(format_ansi_string('Incorrect user password given at '
                                            'start of setup',
                                            ForeGroundColor.RED))
            sys.exit()

        LOGGER.warning(format_ansi_string(f'Password provided for root access'
                                          f' command - {command}',
                                          ForeGroundColor.YELLOW))

        child_output = child.before

        LOGGER.debug(child_output)
        LOGGER.info(format_ansi_string('Homebrew has successfully been '
                                       'installed', ForeGroundColor.GREEN))
    except pexpect.TIMEOUT:
        LOGGER.error(format_ansi_string('Invalid expectation or process '
                                        'timed out', ForeGroundColor.RED))
        sys.exit()


def tap_brew_cask():
    """
    Registers cask packages for installation through brew
    """
    command = 'brew tap homebrew/cask'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()
        tapped_successfully = process.returncode == 0

        if err and not tapped_successfully:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Brew failed to tap into cask',
                                            ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_success_message(
                'Brew has successfully tapped into cask'))


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

    command = 'brew list'
    output = check_output(command.split()).strip()
    brew_list = output.decode('utf-8').split('\n')

    with open(SETUP.brew_config_file) as text_file:
        configured_packages = map(lambda x: x.strip(), text_file.readlines())

    installed_packages, uninstalled_packages = partition(
        lambda x: x in brew_list, configured_packages)

    consume(map(lambda x: LOGGER.info(
        format_ansi_string(f'{x} - already installed',
                           ForeGroundColor.LIGHT_GREEN)), installed_packages))

    uninstalled_packages, uninstalled_packages_copy = tee(uninstalled_packages)

    if not next(uninstalled_packages_copy, None):
        LOGGER.info(format_success_message(
            'No available brew packages to install'))
    else:
        # TODO - remove below when project is in final stages
        # consume(map(lambda x: process_package(x), uninstalled_packages))
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

    command = 'brew cask list'
    output = check_output(command.split()).strip()
    cask_list = output.decode('utf-8').split('\n')

    with open(SETUP.brew_cask_config_file) as text_file:
        configured_packages = map(lambda x: x.strip(), text_file.readlines())

    installed_packages, uninstalled_packages = partition(
        lambda x: x in cask_list, configured_packages)

    consume(map(lambda x: LOGGER.info(
        format_ansi_string(f'{x} - already installed',
                           ForeGroundColor.LIGHT_GREEN)), installed_packages))

    uninstalled_packages, uninstalled_packages_copy = tee(uninstalled_packages)

    if not next(uninstalled_packages_copy, None):
        LOGGER.info(format_success_message(
            'No available cask packages to install'))
    else:
        # TODO - remove below when project is in final stages
        # consume(map(lambda x: process_package(x), uninstalled_packages))
        LOGGER.info(format_success_message(
            'All configured brew cask packages are now install'))


def uninstall_brew():
    """
    Uninstalls brew from the web via git
    """
    command = 'which brew'
    brew_installed = call(command.split(), stdout=DEVNULL) == 0

    if not brew_installed:
        LOGGER.info(format_success_message('Homebrew is already uninstalled'))
        return

    ruby_bin = '/usr/bin/ruby'
    brew_url = 'https://raw.githubusercontent.com/Homebrew/install/master/' \
               'uninstall'

    command = f'{ruby_bin} -e \"$(curl -fsSL {brew_url})\"'
    child = pexpect.spawn('/bin/bash', ['-c', command])

    try:
        child.expect(r'\[y/N\]', timeout=60*10)
    except pexpect.TIMEOUT:
        LOGGER.error(format_ansi_string('Request to uninstall from brew url '
                                        'timed out', ForeGroundColor.RED))
        sys.exit()

    child.sendline('y')

    try:
        child.expect('Password:', timeout=60*10)
    except pexpect.TIMEOUT:
        LOGGER.error(format_ansi_string('Homebrew is cleaned locally but '
                                        'child process timed out from cleanup',
                                        ForeGroundColor.RED))
        sys.exit()

    child.sendline(SETUP.password)

    try:
        expectations = ['Sorry, try again.', pexpect.EOF]
        index = child.expect(expectations)

        if index == 0:
            LOGGER.error(format_ansi_string('Incorrect user password given at '
                                            'start of setup',
                                            ForeGroundColor.RED))
            sys.exit()

        LOGGER.warning(format_ansi_string(f'Password provided for root access'
                                          f' command - {command}',
                                          ForeGroundColor.YELLOW))

        child_output = child.before

        LOGGER.debug(child_output)
        LOGGER.info(format_success_message(
            'Homebrew has successfully been uninstalled'))
    except pexpect.TIMEOUT:
        LOGGER.error(format_ansi_string('Invalid expectation or process timed '
                                        'out', ForeGroundColor.RED))
        sys.exit()
