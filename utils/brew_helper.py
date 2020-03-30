"""
Module delegated to handling brew logic
"""

# Native Modules
import functools
import itertools
import logging
import sys
from subprocess import Popen, call, check_output, PIPE, DEVNULL

# Third Party Modules
import pexpect

# Custom Modules
from singletons.setup import SetupSingleton

SETUP: SetupSingleton = SetupSingleton.get_instance()
LOGGER = logging.getLogger()


def brew_exists() -> bool:
    """
    Check if the brew dependency management tool exists in the system
    """
    command = 'find /usr/local/Caskroom'
    directory_found = call(command.split(), stdout=DEVNULL, stderr=DEVNULL) == 0

    if directory_found:
        LOGGER.info('Brew has already been configured')
    else:
        LOGGER.info('Brew hasn\'t been configured - configuring now...')

    return directory_found


def install_brew():
    """
    Pulls brew from the web via git and installs it with local authentication
    """
    ruby_bin = '/usr/bin/ruby'
    brew_url = 'https://raw.githubusercontent.com/Homebrew/install/master/' \
               'install'

    command = f'{ruby_bin} -e \"$(curl -fsSL {brew_url})\"'
    child = pexpect.spawn('/bin/bash', ['-c', command])

    try:
        child.expect('Press RETURN', timeout=60*5)
    except pexpect.TIMEOUT:
        LOGGER.error('Request to install from brew url timed out')

    child.sendline('')

    try:
        child.expect('Password:', timeout=60*5)
    except pexpect.TIMEOUT:
        LOGGER.error('Child process timed out from installation')
        sys.exit()

    child.sendline(SETUP.password)

    try:
        expectations = ['Sorry, try again.', pexpect.EOF]
        index = child.expect(expectations, timeout=60*30)

        if index == 0:
            LOGGER.error('Incorrect user password given at start of setup')
            sys.exit()

        LOGGER.warning(f'Password provided for root access command - {command}')

        child_output = child.before

        LOGGER.debug(child_output)
        LOGGER.info('Homebrew has successfully been installed')
    except pexpect.TIMEOUT:
        LOGGER.error('Invalid expectation or process timed out')
        sys.exit()


def tap_brew_cask():
    """
    Self explanatory
    """
    command = 'brew tap homebrew/cask'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()
        tapped_successfully = process.returncode == 0

        if err and not tapped_successfully:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Brew failed to tap into cask')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Brew has successfully tapped into cask')


def install_all_brew_packages():
    """
    Downloads & installs every package config if it's valid
    """
    def process_package(package: str):
        """
        Installs the package if possible & logs correspondingly
        """
        command = f'brew info {package}'
        package_found = call(command.split(), stdout=DEVNULL) == 0

        if not package_found:
            LOGGER.warning(f'This package does not exist in registry - '
                           f'{package}')
            return

        command = f'brew install {package}'
        with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
            out, err = process.communicate()
            installed_successfully = process.returncode == 0

            if err and not installed_successfully:
                LOGGER.warning(err.decode('utf-8'))
                LOGGER.warning(f'{package} - issue during installation')
            else:
                LOGGER.debug(out.decode('utf-8'))
                LOGGER.info(f'{package} - successfully installed')

    command = 'brew list'
    output = check_output(command.split()).strip()
    brew_list = output.decode('utf-8').split('\n')

    with open(SETUP.brew_config_file) as text_file:
        configured_packages = map(lambda x: x.strip(), text_file.readlines())

    uninstalled_packages = filter(
        lambda x: x not in brew_list, configured_packages)

    uninstalled_packages, uninstalled_packages_copy = \
        itertools.tee(uninstalled_packages)

    if not next(uninstalled_packages_copy, None):
        LOGGER.info('No available brew packages to install')
    else:
        # list(map(lambda x: process_package(x), uninstalled_packages))
        # TODO remove below
        print('Stub completed')


def install_all_cask_packages():
    """
    Downloads & installs every package config if it's valid
    """
    def process_package(package: str):
        """
        Installs the package if possible & logs correspondingly
        """
        command = f'brew cask info {package}'
        package_found = call(command.split(), stdout=DEVNULL) == 0

        if not package_found:
            LOGGER.warning(f'This package does not exist in registry - '
                           f'{package}')
            return

        command = f'brew cask install {package}'
        with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
            out, err = process.communicate()
            installed_successfully = process.returncode == 0

            if err and not installed_successfully:
                LOGGER.warning(err.decode('utf-8'))
                LOGGER.warning(f'{package} - issue during installation')
            else:
                LOGGER.debug(out.decode('utf-8'))
                LOGGER.info(f'{package} - successfully installed')

    command = 'brew cask list'
    output = check_output(command.split()).strip()
    cask_list = output.decode('utf-8').split('\n')

    with open(SETUP.brew_cask_config_file) as text_file:
        configured_packages = map(lambda x: x.strip(), text_file.readlines())

    uninstalled_packages = filter(
        lambda x: x not in cask_list, configured_packages)

    uninstalled_packages, uninstalled_packages_copy = \
        itertools.tee(uninstalled_packages)

    if not uninstalled_packages:
        LOGGER.info('No available cask packages to install')
    else:
        # list(map(lambda x: process_package(x), uninstalled_packages))
        # TODO remove below
        print('Stub completed')


def uninstall_brew():
    """
    Uninstalls brew from the web via git
    """
    command = 'which brew'
    bin_exists = call(command.split(), stdout=DEVNULL) == 0

    if not bin_exists:
        LOGGER.info('Homebrew is already uninstalled')
        return

    ruby_bin = '/usr/bin/ruby'
    brew_url = 'https://raw.githubusercontent.com/Homebrew/install/master/' \
               'uninstall'

    command = f'{ruby_bin} -e \"$(curl -fsSL {brew_url})\"'
    child = pexpect.spawn('/bin/bash', ['-c', command])

    try:
        child.expect(r'\[y/N\]', timeout=60*10)
    except pexpect.TIMEOUT:
        LOGGER.error('Request to uninstall from brew url timed out')

    child.sendline('y')

    try:
        child.expect('Password:', timeout=60*10)
    except pexpect.TIMEOUT:
        LOGGER.error('Homebrew is cleaned locally but child process timed out '
                     'from cleanup')
        sys.exit()

    child.sendline(SETUP.password)

    try:
        expectations = ['Sorry, try again.', pexpect.EOF]
        index = child.expect(expectations)

        if index == 0:
            LOGGER.error('Incorrect user password given at start of setup')
            sys.exit()

        LOGGER.warning(f'Password provided for root access command - {command}')

        child_output = child.before

        LOGGER.debug(child_output)
        LOGGER.info('Homebrew has successfully been uninstalled')
    except pexpect.TIMEOUT:
        LOGGER.error('Invalid expectation or process timed out')
        sys.exit()
