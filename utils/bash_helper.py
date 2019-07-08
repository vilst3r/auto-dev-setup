'''
Module delegated to handling bash logic
'''

# System/Third-Party modules
import logging
from subprocess import call, check_call, DEVNULL

# Custom modules
from utils.setup_wrapper import SETUP
from utils.github_wrapper import GITHUB

LOGGER = logging.getLogger()

def pull_bash_settings():
    '''
    Pull bash setting repository from github account
    '''
    git_username = GITHUB.username

    command = 'find config/bash/bash-settings'
    directory_found = call(command.split(), stdout=DEVNULL)

    if directory_found == 0:
        LOGGER.info('Bash settings already pulled from git')
        return

    source = f'git@github.com:{git_username}/bash-settings.git'
    destination = f'config/bash/bash-settings'
    command = f'git clone {source} {destination}'
    check_call(command.split())

def configure_bash_profile():
    '''
    Copies bash profile from local project bash settings to user settings
    '''
    home_dir = SETUP.dir['home']

    command = f'cp config/bash/bash-settings/.bash_profile {home_dir}/.bash_profile'
    call(command.split())

def remove_bash_settings():
    '''
    Remove bash setting repository cloned from github
    '''
    command = 'find config/bash/bash-settings'
    directory_found = call(command.split(), stdout=DEVNULL)

    if directory_found != 0:
        LOGGER.info('Bash settings already removed')
        return

    command = 'rm -rf config/bash/bash-settings'
    check_call(command.split())
