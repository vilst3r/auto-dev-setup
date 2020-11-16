"""
Module delegated to handling powerline status logic
"""

import json
# Native Modules
import logging
import re
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


def install_powerline_at_user():
    """
    Installs the powerline tool at the user level of the system
    """
    command = 'pip3 install --user powerline-status'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to install powerline from '
                                            'pip3', ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Powerline now installed from pip3 '
                                           'at the user level',
                                           ForeGroundColor.GREEN))


def configure_user_config():
    """
    Checks & creates proper directory for the powerline configs to go
    """
    command = f'mkdir -p {SETUP.directories.powerline}'
    call(command.split(), stdout=DEVNULL)

    LOGGER.info(format_ansi_string(f'{SETUP.directories.powerline} - has '
                                   f'been created', ForeGroundColor.GREEN))

    command = f'cp -r {SETUP.directories.python_site}/powerline/config_files/ ' \
              f'{SETUP.directories.powerline}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to copy powerline config '
                                            'from system to user directory',
                                            ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Successfully copied powerline '
                                           'config from system to user '
                                           'directory', ForeGroundColor.GREEN))


def install_fonts():
    """
    Downloads & installs all font files to proper location
    """

    destination = f'{SETUP.directories.powerline}/fonts'

    command = f'find {destination}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if directory_found:
        LOGGER.info(format_ansi_string('Powerline fonts are already installed',
                                       ForeGroundColor.LIGHT_GREEN))
        return

    source = f'git@github.com:powerline/fonts.git'
    command = f'git clone {source} {destination}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()
        cloned_successfully = process.returncode == 0

        if err and not cloned_successfully:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to clone powerline fonts'
                                            ' from github',
                                            ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Successfully cloned powerline '
                                           'fonts from github',
                                           ForeGroundColor.GREEN))

    command = f'/bin/bash {destination}/install.sh'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to install powerline '
                                            'fonts', ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Successfully installed powerline '
                                           'fonts', ForeGroundColor.GREEN))


def install_gitstatus_at_user():
    """
    Installs powerline-gitstatus at user level of system
    """
    command = 'pip3 install --user powerline-gitstatus'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to install '
                                            'powerline-gitstatus through pip3',
                                            ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Powerline-gitstatus successfully '
                                           'installed through pip3',
                                           ForeGroundColor.GREEN))


def config_git_colorscheme():
    """
    Configures color scheme for git status in powerline
    """
    default_block = f'{SETUP.directories.powerline}/' \
                    f'colorschemes/default.json'
    config_block = 'config/powerline/powerline_git_color.json'

    with open(default_block) as default_json, open(config_block) \
            as config_json:
        default_data = json.load(default_json)
        config_data = json.load(config_json)
        default_group = default_data['groups']
        config_group = config_data['groups']

        if all([group in default_group for group in config_group]):
            LOGGER.info(format_ansi_string('Color scheme for git status for '
                                           'powerline is already configured',
                                           ForeGroundColor.LIGHT_GREEN))
            return

        data = default_data
        data['groups'] = {**default_group, **config_group}

    with open(default_block, 'w+', encoding='utf-8') as default_json:
        json.dump(data, default_json, ensure_ascii=False, indent=4)

    LOGGER.info(format_ansi_string('Finish configuring color scheme for git '
                                   'status in powerline!',
                                   ForeGroundColor.GREEN))


def config_git_shell():
    """
    Configure shell to display git status
    """
    default_block = f'{SETUP.directories.powerline}/' \
                    f'themes/shell/default.json'
    config_block = 'config/powerline/powerline_git_shell.json'

    with open(default_block) as default_json, open(config_block)\
            as config_json:
        default_data = json.load(default_json)
        config_data = json.load(config_json)
        function_list = default_data['segments']['left']

        for function in function_list:
            if function == config_data:
                LOGGER.info(format_ansi_string('Shell for git stats for '
                                               'powerline is already '
                                               'configured',
                                               ForeGroundColor.LIGHT_GREEN))
                return

        function_list.append(config_data)
        data = default_data
        data['segments']['left'] = function_list

    with open(default_block, 'w+', encoding='utf-8') as default_json:
        json.dump(data, default_json, ensure_ascii=False, indent=4)

    LOGGER.info(format_ansi_string('Finish configuring shell for git status '
                                   'in powerline!', ForeGroundColor.GREEN))


def delete_powerline_fonts():
    """
    Deletes all font files associated with the powerline package from
    installation
    """
    uninstall_font_script = f'{SETUP.directories.powerline}' \
                            f'/fonts/uninstall.sh'

    command = f'find {uninstall_font_script}'
    script_exists = call(command.split(), stdout=DEVNULL) == 0

    if not script_exists:
        LOGGER.info(format_ansi_string('Powerline fonts are already '
                                       'uninstalled',
                                       ForeGroundColor.LIGHT_GREEN))
        return

    command = f'/bin/bash {uninstall_font_script}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to uninstall powerline '
                                            'fonts in the system level',
                                            ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Powerline fonts has successfully '
                                           'been uninstalled in the system '
                                           'level', ForeGroundColor.GREEN))

    command = f'rm -rf {SETUP.directories.powerline}/fonts'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to remove powerline fonts '
                                            'in the user level',
                                            ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Powerline fonts in the user level '
                                           'has successfully been removed',
                                           ForeGroundColor.GREEN))


def delete_powerline_config_folder():
    """
    Deletes the entire powerline folder in user config
    """
    command = f'find {SETUP.directories.powerline}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if not directory_found:
        LOGGER.info(format_ansi_string('Powerline config at the user config '
                                       'directory has already been removed',
                                       ForeGroundColor.LIGHT_GREEN))
        return

    command = f'rm -rf {SETUP.directories.powerline}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to remove the powerline '
                                            'config at the user config '
                                            'directory', ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('Powerline config has successfully'
                                           ' been removed at the user config '
                                           'directory', ForeGroundColor.GREEN))
