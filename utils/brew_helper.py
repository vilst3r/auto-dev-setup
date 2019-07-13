'''
Module delegated to handling brew logic
'''

# Native Modules
import logging
import sys
from subprocess import Popen, call, check_output, PIPE, DEVNULL

# Third Party Modules
import pexpect

# Custom Modules
from utils.setup_wrapper import SETUP

LOGGER = logging.getLogger()

def brew_exists() -> bool:
    '''
    Check if the brew dependency management tool exists in the system
    '''
    command = 'find /usr/local/Caskroom'
    directory_found = call(command.split(), stdout=DEVNULL, stderr=DEVNULL) == 0

    if directory_found:
        LOGGER.info('Brew has already been configured')
    else:
        LOGGER.info('Brew hasn\'t been configured - configuring now...')

    return directory_found

def install_brew():
    '''
    Pulls brew from the web via git and installs it with local authentication
    '''
    ruby_bin = '/usr/bin/ruby'
    brew_url = 'https://raw.githubusercontent.com/Homebrew/install/master/install'

    command = f'{ruby_bin} -e \"$(curl -fsSL {brew_url})\"'
    child = pexpect.spawn('/bin/bash', ['-c', command])

    try:
        index = child.expect('Press RETURN', timeout=60*5)
    except pexpect.TIMEOUT:
        LOGGER.error('Request to install from brew url timed out')

    child.sendline('')

    try:
        index = child.expect('Password:', timeout=60*5)
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
    '''
    Self explanatory
    '''
    command = 'brew tap caskroom/cask'
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
    '''
    Downloads & installs every package config if it's valid
    '''
    command = 'brew list'
    output = check_output(command.split())
    brew_list = output.decode('utf-8').split('\n')

    uninstalled_packages = []
    with open('config/brew/brew.txt') as text_file:
        for line in text_file.readlines():
            package = line.strip()

            if package not in brew_list:
                uninstalled_packages.append(package)

    if not uninstalled_packages:
        LOGGER.info('No available brew packages to install')
        return

    for package in uninstalled_packages:
        command = f'brew info {package}'
        package_found = call(command.split(), stdout=DEVNULL) == 0

        if not package_found:
            LOGGER.warning(f'This package does not exist in registry - {package}')
            continue

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

def install_all_cask_packages():
    '''
    Downloads & installs every package config if it's valid
    '''
    output = None
    command = 'brew cask list'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.warning(err.decode('utf-8'))
        else:
            LOGGER.debug(out.decode('utf-8'))
            output = out

    cask_list = output.decode('utf-8').split('\n')

    uninstalled_packages = []
    with open('config/brew/brew-cask.txt') as text_file:
        for line in text_file.readlines():
            package = line.strip()

            if package not in cask_list:
                uninstalled_packages.append(package)

    if not uninstalled_packages:
        LOGGER.info('No available cask packages to install')
        return

    for package in uninstalled_packages:
        command = f'brew cask info {package}'
        package_found = call(command.split(), stdout=DEVNULL) == 0

        if not package_found:
            LOGGER.warning(f'This package does not exist in registry - {package}')
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

def uninstall_brew():
    '''
    Uninstalls brew from the web via git
    '''
    command = 'which brew'
    bin_exists = call(command.split(), stdout=DEVNULL) == 0

    if not bin_exists:
        LOGGER.info('Homebrew is already uninstalled')
        return

    ruby_bin = '/usr/bin/ruby'
    brew_url = 'https://raw.githubusercontent.com/Homebrew/install/master/uninstall'

    command = f'{ruby_bin} -e \"$(curl -fsSL {brew_url})\"'
    child = pexpect.spawn('/bin/bash', ['-c', command])

    try:
        index = child.expect(r'\[y/N\]', timeout=60*10)
    except pexpect.TIMEOUT:
        LOGGER.error('Request to uninstall from brew url timed out')

    child.sendline('y')

    try:
        index = child.expect('Password:', timeout=60*10)
    except pexpect.TIMEOUT:
        LOGGER.error('Homebrew is cleaned locally but child process timed out from cleanup')
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
