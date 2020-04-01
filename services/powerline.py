"""
Module delegated to handling powerline status logic
"""

# Native Modules
import logging
import sys
import re
import json
from subprocess import Popen, call, PIPE, DEVNULL

# Custom Modules
from singletons.setup import SetupSingleton
from singletons.github import GithubSingleton
from utils.general import format_ansi_string, format_success_message
from utils.unicode import *

SETUP: SetupSingleton = SetupSingleton.get_instance()
GITHUB: GithubSingleton = GithubSingleton.get_instance()
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


def write_bash_daemon():
    """
    Append daemon configuration lines to bash profile
    TODO - refactor later
    """
    source_version = f'source ' \
                     f'{SETUP.python_site_dir}/powerline/bindings' \
                     f'/bash/powerline.sh'

    daemon_config = []
    daemon_config.append('# Powerline user config')
    daemon_config.append('powerline-daemon -q')
    daemon_config.append('POWERLINE_BASH_CONTINUATION=1')
    daemon_config.append('POWERLINE_BASH_SELECT=1')
    daemon_config.append(source_version)

    pattern = daemon_config[:-1]
    pattern.append(r'source [\w(\-)/.]+.sh')

    daemon_config = '\n'.join(daemon_config)
    pattern = '\n'.join(pattern)

    with open(SETUP.bash_profile_file) as text_file:
        content = ''.join(text_file.readlines())

    pattern = re.compile(pattern)
    config_match = re.search(pattern, content)

    if not config_match:
        with open(SETUP.bash_profile_file, 'a') as text_file:
            text_file.write(f"\n{daemon_config}\n")
        LOGGER.info(format_ansi_string('Appended powerline configuration in '
                                       'bash profile', ForeGroundColor.GREEN))
        return

    current_config = config_match[0]

    if current_config == daemon_config:
        LOGGER.info(format_ansi_string('Powerline already configured in '
                                       'bash profile',
                                       ForeGroundColor.LIGHT_GREEN))
        return

    start, end = config_match.span()
    content = content[:start] + daemon_config + content[end:]

    with open(SETUP.bash_profile_file, 'w') as text_file:
        text_file.write(content)

    LOGGER.info(format_ansi_string('Powerline configuration updated in '
                                   'bash profile', ForeGroundColor.GREEN))


def write_vim_config():
    """
    Append powerline configuration to vimrc
    """
    rtp_version = f'set rtp+={SETUP.python_site_dir}/powerline/bindings/vim'

    config = []
    config.append('" Powerline')
    config.append(rtp_version)
    config.append("set laststatus=2")
    config.append("set t_Co=256")

    pattern = config[::]
    pattern[1] = r"set rtp\+\=[\w(\-)/.]+/vim"

    config = "\n".join(config)
    pattern = "\n".join(pattern)

    with open(SETUP.vimrc_file) as text_file:
        content = "".join(text_file.readlines())

    pattern = re.compile(pattern)
    config_match = re.search(pattern, content)

    if not config_match:
        LOGGER.info(format_ansi_string('Appended powerline configuration in '
                                       'vimrc', ForeGroundColor.GREEN))

        with open(SETUP.vimrc_file, 'a') as text_file:
            text_file.write(f"\n{config}\n")
        return

    current_config = config_match[0]

    if current_config == config:
        LOGGER.info(format_ansi_string('Powerline already configured in '
                                       'vimrc', ForeGroundColor.LIGHT_GREEN))
        return

    start, end = config_match.span()
    content = content[:start] + config + content[end:]

    with open(SETUP.vimrc_file, 'w') as text_file:
        text_file.write(content)

    LOGGER.info(format_ansi_string('Powerline configuration updated in '
                                   'vimrc', ForeGroundColor.GREEN))


def configure_user_config_directory():
    """
    Checks & creates proper directory for the powerline configs to go
    """
    command = f'mkdir -p {SETUP.powerline_local_config_dir}'
    call(command.split(), stdout=DEVNULL)

    LOGGER.info(format_ansi_string(f'{SETUP.powerline_local_config_dir} - has '
                                   f'been created', ForeGroundColor.GREEN))

    command = f'cp -r {SETUP.powerline_system_config_dir}/ ' \
              f'{SETUP.powerline_local_config_dir}'
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
    source = f"git@github.com:{GITHUB.username}/fonts.git"
    destination = f'{SETUP.powerline_local_config_dir}/fonts'

    command = f'find {destination}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if directory_found:
        LOGGER.info(format_ansi_string('Powerline fonts are already installed',
                                       ForeGroundColor.LIGHT_GREEN))
        return

    # Check if repository is forked in configured account
    command = f'git ls-remote {source}'
    fork_exists = call(command.split(), stdout=DEVNULL) == 0

    if not fork_exists:
        source = "git@github.com:powerline/powerline.git"

    command = f'git clone {source} {destination}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()
        cloned_successfully = process.returncode == 0

        if err and not cloned_successfully:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to clone powerline fonts '
                                            'from github', ForeGroundColor.RED))
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
            LOGGER.error(format_ansi_string('Failed to install powerline fonts',
                                            ForeGroundColor.RED))
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
    # TODO Double check these two lines again
    default_block = f'{SETUP.powerline_local_config_dir}/' \
                    f'colorschemes/default.json'
    config_block = 'config/powerline/powerline_git_color.json'

    with open(default_block) as default_json, open(config_block) as config_json:
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
    default_block = f'{SETUP.powerline_local_config_dir}/' \
                    f'themes/shell/default.json'
    config_block = 'config/powerline/powerline_git_shell.json'

    with open(default_block) as default_json, open(config_block) as config_json:
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


def uninstall_powerline_gitstatus():
    """
    Uninstalls the powerline git-status package from the system
    """
    command = 'which pip3'
    pip_installed = call(command.split(), stdout=DEVNULL) == 0

    command = 'pip3 show powerline-gitstatus'
    package_found = call(command.split(), stdout=DEVNULL) == 0

    if not pip_installed or not package_found:
        LOGGER.info(format_ansi_string('Powerline-gitstatus has already been '
                                       'uninstalled',
                                       ForeGroundColor.LIGHT_GREEN))
        return

    command = 'pip3 uninstall powerline-gitstatus'
    with Popen(command.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE) \
            as process:
        out, err = process.communicate(input=b"y\n")

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to uninstall the '
                                            'powerline-gitstatus package',
                                            ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_ansi_string('The powerline-gitstatus package '
                                           'has successfully been uninstalled',
                                           ForeGroundColor.GREEN))


def delete_powerline_fonts():
    """
    Deletes all font files associated with the powerline package from
    installation
    """
    uninstall_font_script = f'{SETUP.powerline_local_config_dir}' \
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

    command = f'rm -rf {SETUP.powerline_local_config_dir}/fonts'
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
    command = f'find {SETUP.powerline_local_config_dir}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if not directory_found:
        LOGGER.info(format_ansi_string('Powerline config at the user config '
                                       'directory has already been removed',
                                       ForeGroundColor.LIGHT_GREEN))
        return

    command = f'rm -rf {SETUP.powerline_local_config_dir}'
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


def remove_powerline_daemon_in_bash_profile():
    """
    Remove powerline config block in bash profile
    """
    pattern = []
    pattern.append("# Powerline user config")
    pattern.append('powerline-daemon -q')
    pattern.append("POWERLINE_BASH_CONTINUATION=1")
    pattern.append("POWERLINE_BASH_SELECT=1")
    pattern.append(r"source [\w(\-)/.]+.sh")

    pattern = "\n".join(pattern)

    with open(SETUP.bash_profile_file) as text_file:
        content = ''.join(text_file.readlines())

    pattern = re.compile(pattern)
    config_match = re.search(pattern, content)

    if not config_match:
        LOGGER.info(format_ansi_string('Powerline daemon in bash '
                                       'profile already removed',
                                       ForeGroundColor.LIGHT_GREEN))
        return

    start, end = config_match.span()
    content = content[:start] + content[end:]

    with open(SETUP.bash_profile_file, 'w') as text_file:
        text_file.write(content)

    LOGGER.info(format_ansi_string(
        'Powerline daemon removed in bash profile', ForeGroundColor.GREEN))


def remove_powerline_config_in_vimrc():
    """
    Remove the powerline config block in vimrc
    """
    pattern = []
    pattern.append('" Powerline')
    pattern.append(r"set rtp\+\=[\w(\-)/.]+/vim")
    pattern.append("set laststatus=2")
    pattern.append("set t_Co=256")

    pattern = "\n".join(pattern)

    with open(SETUP.vimrc_file) as text_file:
        content = ''.join(text_file.readlines())

    pattern = re.compile(pattern)
    config_match = re.search(pattern, content)

    if not config_match:
        LOGGER.info(format_ansi_string('Powerline configuration in vimrc '
                                       'already removed',
                                       ForeGroundColor.LIGHT_GREEN))
        return

    start, end = config_match.span()
    content = content[:start] + content[end:]

    with open(SETUP.vimrc_file, 'w') as text_file:
        text_file.write(content)

    LOGGER.info(format_ansi_string(
        'Powerline configuration removed in vimrc', ForeGroundColor.GREEN))


def uninstall_powerline_status():
    """
    Uninstalls the powerline tool
    """
    command = 'which pip3'
    pip_installed = call(command.split(), stdout=DEVNULL) == 0

    command = 'pip3 show powerline-status'
    package_found = call(command.split(), stdout=DEVNULL) == 0

    if not pip_installed or not package_found:
        LOGGER.info(format_success_message(
            'Powerline-status has already been uninstalled'))
        return

    command = 'pip3 uninstall powerline-status'
    with Popen(command.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE) \
            as process:
        out, err = process.communicate(input=b"y\n")

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error(format_ansi_string('Failed to uninstall the '
                                            'powerline-status package through '
                                            'pip3', ForeGroundColor.RED))
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info(format_success_message('The powerline-status package '
                                               'has successfully been '
                                               'uninstalled through pip3'))
