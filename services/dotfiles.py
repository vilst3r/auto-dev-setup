"""
Module delegated to handling vim logic
"""

# Native Modules
import logging
import sys
from subprocess import Popen, call, DEVNULL, PIPE

# Custom Modules
from singletons.setup import SetupSingleton
from singletons.github import GithubSingleton
from utils.general import format_ansi_string
from utils.unicode import *

SETUP: SetupSingleton = SetupSingleton.get_instance()
GITHUB: GithubSingleton = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


def pull_dotfile_settings():
    """
    Pull dotfiles repository from github account
    """
    command = f'find {SETUP.dotfiles_dir}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if directory_found:
        LOGGER.info(format_ansi_string('Dotfile settings already pulled from '
                                       'git', ForeGroundColor.LIGHT_GREEN))
        return

    # Check if repository is forked in configured account
    source = f'git@github.com:{GITHUB.username}/dotfiles.git'
    command = f'git ls-remote {source}'
    fork_exists = call(command.split(), stdout=DEVNULL) == 0

    if not fork_exists:
        LOGGER.warning(format_ansi_string(f'This step is optional but it '
                                          f'requires - {source} to proceed',
                                          ForeGroundColor.YELLOW, Format.BOLD))
        return

    command = f'git clone {source} {SETUP.dotfiles_dir}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()
        cloned_successfully = process.returncode == 0

        if err and not cloned_successfully:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to clone dotfile settings '
                                            'from github', ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Dotfile settings has successfully '
                                           'been cloned from github',
                                           ForeGroundColor.GREEN))


def configure_vimrc():
    """
    Copies vimrc from dotfile settings to user settings
    """
    command = f'cp {SETUP.dotfiles_dir}/.vimrc {SETUP.vimrc_file}'
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


def configure_vim_color_themes():
    """
    Moves the vim color theme scripts from the dotfiles settings repository to
    the correct location
    """
    command = f'mkdir -p {SETUP.vim_color_dir}'
    call(command.split(), stdout=DEVNULL)
    LOGGER.info(format_ansi_string(f'{SETUP.vim_color_dir} - has been '
                                   f'created', ForeGroundColor.GREEN))

    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'cp {SETUP.dotfiles_dir}/vim_color_themes/*.vim '
                        f'{SETUP.vim_color_dir}')

    files_copied = call(command_list, stdout=DEVNULL) == 0

    if files_copied:
        LOGGER.info(format_ansi_string('Vim color themes copied to '
                                       '~/.vim/colors', ForeGroundColor.GREEN))
    else:
        LOGGER.error(format_ansi_string('Error copying vim color themes in '
                                        'user config', ForeGroundColor.RED))
        sys.exit()


def configure_bash_profile():
    """
    Copies bash profile from dotfile settings to user settings
    """
    command = f'cp {SETUP.dotfiles_dir}/.bash_profile ' \
              f'{SETUP.bash_profile_file}'
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
    Maps `.emacs` from dotfile settings to `init.el` in user settings
    """
    command = f'cp {SETUP.dotfiles_dir}/.emacs ' \
              f'{SETUP.home_dir}/.emacs'
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
            LOGGER.info(format_ansi_string('Emacs settings are now configured'
                                           ' from the dotfiles repository',
                                           ForeGroundColor.GREEN))


def remove_color_themes():
    """
    Remove all color themes in the vim config folder of user
    """
    command = f'find {SETUP.vim_color_dir}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if not directory_found:
        LOGGER.info(format_ansi_string('Vim color themes already removed',
                                       ForeGroundColor.LIGHT_GREEN))
        return

    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'rm {SETUP.vim_color_dir}/*.vim')
    with Popen(command_list, stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.debug(err.decode('utf-8'))
            LOGGER.info(format_ansi_string('Vim color themes has already been '
                                           'removed',
                                           ForeGroundColor.LIGHT_GREEN))
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Vim color themes has successfully '
                                           'been removed',
                                           ForeGroundColor.GREEN))


def remove_dotfiles_settings():
    """
    Remove dotfile setting repository cloned from github
    """
    command = f'find {SETUP.dotfiles_dir}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if not directory_found:
        LOGGER.info(format_ansi_string('Dotfile settings has been already '
                                       'removed', ForeGroundColor.LIGHT_GREEN))
        return

    command = f'rm -rf {SETUP.dotfiles_dir}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to remove the dotfiles '
                                            'settings respository cloned from '
                                            'github', ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Dotfiles settings repository '
                                           'cloned from github has '
                                           'successfully been removed',
                                           ForeGroundColor.GREEN))


