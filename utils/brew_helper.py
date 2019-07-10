'''
Module delegated to handling brew logic
'''

# System/Third-Party modules
import logging
import sys
from subprocess import Popen, call, check_output, PIPE, DEVNULL

# Custom modules

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

    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'{ruby_bin} -e \"$(curl -fsSL {brew_url})\"')
    with Popen(command_list, stdin=PIPE, stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Homebrew failed to install')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Homebrew has successfully been installed')

def tap_brew_cask():
    '''
    Self explanatory
    '''
    command = 'brew tap caskroom/cask'

    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Brew cask failed to tap into')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Brew cask has successfully been tapped into')

def install_all_brew_packages():
    '''
    Downloads & installs every package config if it's valid
    '''
    command = 'brew list'
    output = check_output(command.split())
    brew_list = output.decode('utf-8').split('\n')

    uninstalled_packages = []
    with open('config/brew/test-brew.txt') as text_file:
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
            LOGGER.warn(f'This package does not exist in registry - {package}')
            continue

        command = f'brew install {package}'
        with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
            out, err = process.communicate()

            if err:
                LOGGER.error(err.decode('utf-8'))
                LOGGER.error(f'Error installing the package - {package}')
                sys.exit()
            else:
                LOGGER.debug(out.decode('utf-8'))
                LOGGER.info(f'{package} - successfully installed')

def install_all_cask_packages():
    '''
    Downloads & installs every package config if it's valid
    '''
    command = 'brew cask list'
    output = None
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            output = out

    cask_list = output.decode('utf-8').split('\n')

    uninstalled_packages = []
    with open('config/brew/test-brew-cask.txt') as text_file:
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
            LOGGER.warn(f'This package does not exist in registry - {package}')
            return

        command = f'brew cask install {package}'
        with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
            out, err = process.communicate()

            if err:
                LOGGER.error(err.decode('utf-8'))
                LOGGER.error(f'Error installing the package - {package}')
                sys.exit()
            else:
                LOGGER.debug(out.decode('utf-8'))
                LOGGER.info(f'{package} - successfully installed')

def uninstall_brew():
    '''
    Uninstalls brew from the web via git
    '''
    ruby_bin = '/usr/bin/ruby'
    brew_url = 'https://raw.githubusercontent.com/Homebrew/install/master/uninstall'

    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'{ruby_bin} -e \"$(curl -fsSL {brew_url})\"')
    with Popen(command_list, stdin=PIPE, stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to uninstall homebrew')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Homebrew has succesffully been uninstalled')
