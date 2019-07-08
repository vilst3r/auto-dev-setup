'''
Module delegated to handling brew logic
'''

# System/Third-Party modules
import logging
from subprocess import call, check_output, PIPE, DEVNULL

# Custom modules

LOGGER = logging.getLogger()

def brew_exists() -> bool:
    '''
    Check if the brew dependency management tool exists in the system
    '''
    command = 'find /usr/local/Caskroom'
    directory_found = call(command.split(), stdout=DEVNULL, stderr=DEVNULL)

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
    call(command_list, stdin=PIPE)

def tap_brew_cask():
    '''
    Self explanatory
    '''
    command = 'brew tap caskroom/cask'
    call(command.split())

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
        LOGGER.info(f'This package does not exist in registry - {package}')
    else:
        command = f'brew install {package}'
        call(command.split())

def use_brew_python():
    '''
    Replaces system binary path with symlink to brew python
    '''
    command = 'brew link --overwrite python'
    call(command.split())

def get_uninstalled_cask_packages() -> list:
    '''
    Scans config list of cask packages to install what's missing
    '''
    command = 'brew cask list'
    output = check_output(command.split())
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
        LOGGER.info(f'This package does not exist in registry - {package}')
    else:
        command = f'brew cask install {package}'
        call(command.split())

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
    call(command_list, stdin=PIPE)
