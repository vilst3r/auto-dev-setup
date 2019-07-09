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
    directory_found = call(command.split(), stdout=DEVNULL, stderr=DEVNULL)

    if directory_found != 0:
        LOGGER.info('Brew hasn\'t been configured - configuring now...')

    return directory_found == 0

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

def get_uninstalled_brew_packages() -> list:
    '''
    Scans config list of brew packages to install what's missing
    '''
    command = 'brew list'
    output = check_output(command.split())
    brew_list = output.decode('utf-8').split('\n')

    buff = []
    with open('config/brew/test-brew.txt') as text_file:
        for line in text_file.readlines():
            package = line.strip()

            if package not in brew_list:
                buff.append(package)
    return buff

def install_that_brew(package: str):
    '''
    Downloads & Installs the single package if it's valid
    '''
    command = f'brew info {package}'
    package_found = call(command.split())

    if package_found != 0:
        LOGGER.warn(f'This package does not exist in registry - {package}')
        return

    command = f'brew install {package}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(f'Error installing the package - {package}')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('{package} - successfully installed')

def use_brew_python():
    '''
    Replaces system binary path with symlink to brew python
    '''
    command = 'brew link --overwrite python'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to overwrite current python symlink with brew python')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Brew python has successfully been symlinked')

def get_uninstalled_cask_packages() -> list:
    '''
    Scans config list of cask packages to install what's missing
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

    buff = []
    with open('config/brew/test-brew-cask.txt') as text_file:
        for line in text_file.readlines():
            package = line.strip()

            if package not in cask_list:
                buff.append(package)
    return buff

def install_that_cask(package: str):
    '''
    Downloads & Installs the single package if it's valid
    '''
    command = f'brew cask info {package}'
    package_found = call(command.split())

    if package_found != 0:
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
            LOGGER.info('{package} - successfully installed')

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
            sys.exit()
        else:
            LOGGER.info(out.decode('utf-8'))
