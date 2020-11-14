"""
Module delegated to handling logic related to dotfiles
"""

# Native Modules
import logging
import sys
from subprocess import DEVNULL, PIPE, Popen, call

from singletons.github import GithubSingleton
# Custom Modules
from singletons.setup import SetupSingleton
from utils.general import format_ansi_string, format_success_message
from utils.unicode import ForeGroundColor

SETUP = SetupSingleton.get_instance()
GITHUB = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


def user_has_dotfiles_repo() -> bool:
    """
    Check if the user has the `dotfiles` repository on Github to configure
    during the process
    """
    source = f'git@github.com:{GITHUB.username}/dotfiles.git'

    command = f'git ls-remote {source}'
    repo_exists = call(command.split(), stdout=DEVNULL) == 0

    if not repo_exists:
        LOGGER.warning(format_ansi_string(f'This step is optional but it'
                                          f' requires - {source} to proceed',
                                          ForeGroundColor.YELLOW))
    return repo_exists


def pull_dotfile_settings():
    """
    Pull the dotfiles repository from the github account assuming the user has
    this repository setup
    """
    command = f'find {SETUP.directories.dotfiles}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if directory_found:
        LOGGER.info(format_ansi_string('Dotfile settings already pulled from '
                                       'git', ForeGroundColor.LIGHT_GREEN))
        return

    # source = f'git@github.com:{GITHUB.username}/dotfiles.git'
    # command = f'git clone {source} {SETUP.directories.dotfiles}'
    # with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
    #     out, err = process.communicate()
    #     cloned_successfully = process.returncode == 0

    #     if err and not cloned_successfully:
    #         LOGGER.error(err.decode('utf-8'))
    #         LOGGER.error(format_ansi_string('Failed to clone dotfile settings '
    #                                         'from github',
    #                                         ForeGroundColor.RED))
    #         sys.exit()
    #     else:
    #         LOGGER.debug(out.decode('utf-8'))
    #         LOGGER.info(format_ansi_string('Dotfile settings has successfully '
    #                                        'been cloned from github',
    #                                        ForeGroundColor.GREEN))


def configure_vimrc():
    """
    Copies vimrc from dotfile settings to user settings
    """
    command = f'find {SETUP.directories.dotfiles}/.vimrc'
    dotfiles_vimrc_exists = call(command.split(), stdout=DEVNULL) == 0

    if not dotfiles_vimrc_exists:
        LOGGER.info(format_ansi_string('Missing the \'.vimrc\' file in the '
                                       'dotfiles repository',
                                       ForeGroundColor.YELLOW))
        return

    command = f'cp {SETUP.directories.dotfiles}/.vimrc {SETUP.files.vim}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to configure vimrc from '
                                            'the dotfiles repository',
                                            ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Vimrc now configured from the '
                                           'dotfiles repository',
                                           ForeGroundColor.GREEN))


def configure_bash_profile():
    """
    Copies bash profile from dotfile settings to user settings
    """
    command = f'find {SETUP.directories.dotfiles}/.bash_profile'
    dotfiles_bash_profile_exists = call(command.split(), stdout=DEVNULL) == 0

    if not dotfiles_bash_profile_exists:
        LOGGER.info(format_ansi_string('Missing the \'.bash_profile\' file in '
                                       'the dotfiles repository',
                                       ForeGroundColor.YELLOW))
        return

    command = f'cp {SETUP.directories.dotfiles}/.bash_profile ' \
              f'{SETUP.files.bash}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to configure bash_profile'
                                            ' from the dotfiles repository',
                                            ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Bash profile now configured from '
                                           'the dotfiles repository',
                                           ForeGroundColor.GREEN))


def configure_emacs():
    """
    Copies init.el file from dotfile settings to user settings
    """
    command = f'find {SETUP.directories.emacs}'
    emacs_exists = call(command.split(), stdout=DEVNULL) == 0

    if not emacs_exists:
        LOGGER.info(format_ansi_string('Missing emacs application in the user '
                                       'level config', ForeGroundColor.YELLOW))
        return

    command = f'find {SETUP.directories.dotfiles}/init.el'
    dotfiles_emacs_config_exists = call(command.split(), stdout=DEVNULL) == 0

    if not dotfiles_emacs_config_exists:
        LOGGER.info(format_ansi_string('Missing the \'init.el\' file in '
                                       'the dotfiles repository',
                                       ForeGroundColor.YELLOW))
        return

    command = f'cp {SETUP.directories.dotfiles}/init.el ' \
              f'{SETUP.files.emacs}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to configure emacs '
                                            'settings from the dotfiles '
                                            'repository', ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Emacs settings are now '
                                           'configured from the dotfiles '
                                           'repository', ForeGroundColor.GREEN))


def remove_dotfiles_repository():
    """
    Remove dotfiles setting repository cloned from github
    """
    command = f'find {SETUP.directories.dotfiles}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if not directory_found:
        LOGGER.info(format_success_message(
            'Dotfile settings has been already removed'))
        return

    command = f'rm -rf {SETUP.directories.dotfiles}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to remove the dotfiles '
                                            'settings repository cloned from '
                                            'github', ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_success_message('Dotfiles settings repository '
                                               'cloned from github has '
                                               'successfully been removed'))


def remove_user_dotfiles():
    """
    Remove dotfiles setting in $HOME, bash, vim & emacs if applicable
    """
    def remove_file(filename: str):
        """
        Helper method to remove individual user config files
        """
        command = f'find {filename}'
        file_found = call(command.split(), stdout=DEVNULL) == 0

        if not file_found:
            LOGGER.info(format_success_message(
                f'\"{filename}\" has been already removed'))
            return

        command = f'rm {filename}'
        with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
            out, err = process.communicate()

            if err:
                LOGGER.error(err.decode('utf-8'))
                LOGGER.error(format_ansi_string(
                    f'Failed to remove \"{filename}\"', ForeGroundColor.RED))
                sys.exit()
            else:
                LOGGER.debug(out.decode('utf-8'))
                LOGGER.info(format_ansi_string(
                    f'\"{filename}\" has successfully been removed', ForeGroundColor.GREEN))

    remove_file(SETUP.files.bash)
    remove_file(SETUP.files.vim)
    remove_file(SETUP.files.emacs)
