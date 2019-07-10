'''
Module delegated to handling powerline status logic
'''

# System/Third-Party modules
import logging
import sys
import re
import json
from subprocess import Popen, call, PIPE, DEVNULL

# Custom modules
from utils.setup_wrapper import SETUP
from utils.github_wrapper import GITHUB

LOGGER = logging.getLogger()

def install_powerline_at_user():
    '''
    Installs the powerline tool at the user level of the system
    '''
    command = 'pip3 install --user powerline-status'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to install powerline from pip3')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Powerline now installed from pip3 at the user level')

def write_bash_daemon():
    '''
    Append daemon configuration lines to bash profile
    '''
    home_dir = SETUP.dir['home']
    python_site = SETUP.dir['python_site']
    bash_profile = f'{home_dir}/.bash_profile'

    source_version = f'source {python_site}/powerline/bindings/bash/powerline.sh'

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

    content = None
    with open(bash_profile) as text_file:
        content = ''.join([line for line in text_file.readlines()])

    pattern = re.compile(pattern)
    config_match = re.search(pattern, content)

    if not config_match:
        LOGGER.info('Appended powerline configuration in bash profile')

        with open(bash_profile, 'a') as text_file:
            text_file.write(f'\n{daemon_config}\n')
        return

    current_config = config_match[0]

    if current_config == daemon_config:
        LOGGER.info('Powerline already configured in bash profile')
        return

    start, end = config_match.span()
    content = content[:start] + daemon_config + content[end:]

    with open(bash_profile, 'w') as text_file:
        text_file.write(content)

    LOGGER.info('Powerline configuration updated in bash profile')

def write_vim_config():
    '''
    Append powerline configuration to vimrc
    '''
    home_dir = SETUP.dir['home']
    python_site = SETUP.dir['python_site']
    vimrc = f'{home_dir}/.vimrc'

    rtp_version = f'set rtp+={python_site}/powerline/bindings/vim'

    config = []
    config.append('\" Powerline')
    config.append(rtp_version)
    config.append('set laststatus=2')
    config.append('set t_Co=256')

    pattern = config[::]
    pattern[1] = r'set rtp\+\=[\w(\-)/.]+/vim'

    config = '\n'.join(config)
    pattern = '\n'.join(pattern)

    content = None
    with open(vimrc) as text_file:
        content = ''.join([line for line in text_file.readlines()])

    pattern = re.compile(pattern)
    config_match = re.search(pattern, content)

    if not config_match:
        LOGGER.info('Appended powerline configuration in vimrc')

        with open(vimrc, 'a') as text_file:
            text_file.write(f'\n{config}\n')
        return

    current_config = config_match[0]

    if current_config == config:
        LOGGER.info('Powerline already configured in vimrc')
        return

    start, end = config_match.span()
    content = content[:start] + config + content[end:]

    with open(vimrc, 'w') as text_file:
        text_file.write(content)

    LOGGER.info('Powerline configuration updated in vimrc')

def configure_user_config_directory() -> bool:
    '''
    Checks & creates proper directory for the powerline configs to go
    '''
    user_config_dir = SETUP.dir['powerline_config']
    system_config_dir = f'{SETUP.dir["python_site"]}/powerline/config_files/'

    command = f'mkdir -p {user_config_dir}'
    call(command.split(), stdout=DEVNULL)
    LOGGER.info(f'{user_config_dir} - has been created')

    command = f'cp -r {system_config_dir} {user_config_dir}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to copy powerline config from system to user directory')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Successfully copied powerline config from system to user directory')

def install_fonts():
    '''
    Downloads & installs all font files to proper location
    '''
    git_username = GITHUB.username
    user_config_dir = SETUP.dir['powerline_config']

    source = f'git@github.com:{git_username}/fonts.git'
    destination = f'{user_config_dir}/fonts'

    command = f'find {destination}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if directory_found:
        LOGGER.info('Powerline fonts are already installed')
        return

    command = f'git clone {source} {destination}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()
        cloned_successfully = process.returncode == 0

        if err and not cloned_successfully:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to clone powerline fonts from github')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Successfully cloned powerline fonts from github')

    command = f'/bin/bash {destination}/install.sh'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to install powerline fonts')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Successfully installed powerline fonts')

def install_gitstatus_at_user():
    '''
    Installs powerline-gitstatus at user level of system
    '''
    command = 'pip3 install --user powerline-gitstatus'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to install powerline-gitstatus through pip3')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Powerline-gitstatus successfully installed through pip3')

def config_git_colorscheme():
    '''
    Configures color scheme for git status in powerline
    '''
    powerline_config = SETUP.dir['powerline_config']
    default_block = f'{powerline_config}/colorschemes/default.json'
    config_block = 'config/powerline/powerline_git_color.json'

    data = None
    with open(default_block) as default_json, open(config_block) as config_json:
        default_data, config_data = json.load(default_json), json.load(config_json)
        default_group, config_group = default_data['groups'], config_data['groups']

        if all([group in default_group for group in config_group]):
            LOGGER.info('Color scheme for git status for powerline is already configured')
            return

        data = default_data
        data['groups'] = {**default_group, **config_group}

    with open(default_block, 'w+', encoding='utf-8') as default_json:
        json.dump(data, default_json, ensure_ascii=False, indent=4)

    LOGGER.info('Finish configuring color scheme for git status in powerline!')

def config_git_shell():
    '''
    Configure shell to display git status
    '''
    powerline_config = SETUP.dir['powerline_config']
    default_block = f'{powerline_config}/themes/shell/default.json'
    config_block = 'config/powerline/powerline_git_shell.json'

    data = None
    with open(default_block) as default_json, open(config_block) as config_json:
        default_data, config_data = json.load(default_json), json.load(config_json)
        function_list = default_data['segments']['left']

        for function in function_list:
            if function == config_data:
                LOGGER.info('Shell for git stats for powerline is already configured')
                return

        function_list.append(config_data)
        data = default_data
        data['segments']['left'] = function_list

    with open(default_block, 'w+', encoding='utf-8') as default_json:
        json.dump(data, default_json, ensure_ascii=False, indent=4)

    LOGGER.info('Finish configuring shell for git status in powerline!')

def uninstall_gitstatus():
    '''
    Uninstalls git powerline status at user level of system
    '''
    command = 'which pip3'
    bin_exists = call(command.split(), stdout=DEVNULL) == 0

    if not bin_exists:
        LOGGER.info('Powerline-gitstatus has already been uninstalled')
        return

    command = 'pip3 show powerline-gitstatus'
    package_found = call(command.split(), stdout=DEVNULL) == 0

    if not package_found:
        LOGGER.info('Powerline-gitstatus has already been uninstalled')
        return

    command = 'pip3 uninstall powerline-gitstatus'
    with Popen(command.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate(input=b'y\n')

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to uninstall powerline-gitstatus at the user level')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Powerline-gitstatus has successfully been uninstalled at the user level')

def delete_fonts():
    '''
    Deletes all font files assosciated with powerline from installation
    '''
    user_config_dir = SETUP.dir['powerline_config']
    uninstall_font_script = f'{user_config_dir}/fonts/uninstall.sh'

    command = f'find {uninstall_font_script}'
    script_exists = call(command.split(), stdout=DEVNULL) == 0

    if not script_exists:
        LOGGER.info('Powerline fonts are already uninstalled')
        return

    command = f'/bin/bash {uninstall_font_script}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to uninstall powerline fonts')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Powerline fonts has successfully been uninstalled')

    command = f'rm -rf {user_config_dir}/fonts'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to remove powerline fonts in the user config directory')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Powerline fonts in user config directory has successfully been removed')

def delete_config():
    '''
    Deletes the entire powerline folder in user config
    '''
    user_config_dir = SETUP.dir['powerline_config']

    command = f'find {user_config_dir}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if not directory_found:
        LOGGER.info('Powerline config has already been removed')
        return

    command = f'rm -rf {user_config_dir}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to remove powerline config at user config directory')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Powerline config has successfully been removed at user config directory')

def remove_bash_daemon():
    '''
    Remove powerline config block in bash profile
    '''
    home_dir = SETUP.dir['home']
    bash_profile = f'{home_dir}/.bash_profile'

    pattern = []
    pattern.append('# Powerline user config')
    pattern.append('powerline-daemon -q')
    pattern.append('POWERLINE_BASH_CONTINUATION=1')
    pattern.append('POWERLINE_BASH_SELECT=1')
    pattern.append(r'source [\w(\-)/.]+.sh')

    pattern = '\n'.join(pattern)

    content = None
    with open(bash_profile) as text_file:
        content = ''.join([line for line in text_file.readlines()])

    pattern = re.compile(pattern)
    config_match = re.search(pattern, content)

    if not config_match:
        LOGGER.info('Powerline configuration in bash profile already removed')
        return

    start, end = config_match.span()
    content = content[:start] + content[end:]

    with open(bash_profile, 'w') as text_file:
        text_file.write(content)

    LOGGER.info('Powerline configuration removed in bash profile')

def remove_vim_config():
    '''
    Remove powerline config block in vimrc
    '''
    home_dir = SETUP.dir['home']
    vimrc = f'{home_dir}/.vimrc'

    pattern = []
    pattern.append('\" Powerline')
    pattern.append(r'set rtp\+\=[\w(\-)/.]+/vim')
    pattern.append('set laststatus=2')
    pattern.append('set t_Co=256')

    pattern = '\n'.join(pattern)

    content = None
    with open(vimrc) as text_file:
        content = ''.join([line for line in text_file.readlines()])

    pattern = re.compile(pattern)
    config_match = re.search(pattern, content)

    if not config_match:
        LOGGER.info('Powerline configuration in vimrc already removed')
        return

    start, end = config_match.span()
    content = content[:start] + content[end:]

    with open(vimrc, 'w') as text_file:
        text_file.write(content)

    LOGGER.info('Powerline configuration removed in vimrc')

def uninstall_powerline_status():
    '''
    Uninstalls the powerline tool
    '''
    command = 'which pip3'
    bin_exists = call(command.split(), stdout=DEVNULL) == 0

    if not bin_exists:
        LOGGER.info('Powerline-gitstatus has already been uninstalled')
        return

    command = 'pip3 show powerline-status'
    package_found = call(command.split(), stdout=DEVNULL) == 0

    if not package_found:
        LOGGER.info('Powerline-status has already been uninstalled')
        return

    command = 'pip3 uninstall powerline-status'
    with Popen(command.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate(input=b'y\n')

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to uninstall powerline through pipe3')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Powerline has successfully been uninstalled through pip3')
