"""
Module delegated to handling bash logic
"""

# Native Modules
import logging
import sys
from subprocess import Popen, call, DEVNULL, PIPE

# Custom Modules
from singletons.setup import SetupSingleton
from singletons.github import GithubSingleton

SETUP = SetupSingleton.get_instance()
GITHUB = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


def pull_bash_settings():
    """
    Pull bash setting repository from github account
    """
    git_username = GITHUB.username

    source = f'git@github.com:{git_username}/bash-settings.git'
    destination = 'config/bash/bash-settings'

    command = f'find {destination}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if directory_found:
        LOGGER.info('Bash settings already pulled from git')
        return

    # Check if repository is forked in configured account
    command = f'git ls-remote {source}'
    fork_exists = call(command.split(), stdout=DEVNULL) == 0

    if not fork_exists:
        LOGGER.info(f'This step is optional but it requires - {source}')
        return

    command = f'git clone {source} {destination}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()
        cloned_successfully = process.returncode == 0

        if err and not cloned_successfully:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to clone bash settings from github')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Bash settings has successfully been cloned from '
                        'github')


def configure_bash_profile():
    """
    Copies bash profile from local project bash settings to user settings
    """
    home_dir = SETUP.dir['home']

    command = f'cp config/bash/bash-settings/.bash_profile ' \
              f'{home_dir}/.bash_profile'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to configure bash_profile from git repository')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Bash profile now configured from git repository')


def remove_bash_settings():
    """
    Remove bash setting repository cloned from github
    """
    command = 'find config/bash/bash-settings'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if not directory_found:
        LOGGER.info('Bash settings already removed')
        return

    command = 'rm -rf config/bash/bash-settings'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to remove bash settings cloned from github')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Bash settings from github has successfully been '
                        'removed')
