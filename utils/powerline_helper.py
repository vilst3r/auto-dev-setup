'''
Module delegated to handling powerline status logic
'''

# System/Third-Party modules
import re
import json
from subprocess import call, check_call

# Custom modules
from utils.setup_wrapper import SETUP
from utils.github_wrapper import GITHUB

def install_powerline_at_user():
    '''
    Installs the powerline tool at the user level of the system
    '''
    command = 'pip3 install --user powerline-status'
    check_call(command.split())

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
    pattern.append('source [\w(\-)/.]+.sh')

    daemon_config = '\n'.join(daemon_config)
    pattern = '\n'.join(pattern)

    content = None
    with open(bash_profile) as text_file:
        content = ''.join([line for line in text_file.readlines()])

    pattern = re.compile(pattern)
    config_match = re.search(pattern, content)

    if not config_match:
        print('Appended powerline configuration in bash profile')
        with open(bash_profile, 'a') as text_file:
            text_file.write(f'\n{daemon_config}\n')
        return

    current_config = config_match[0]

    if current_config == daemon_config:
        print('Powerline already configured in bash profile')
        return

    start, end = config_match.span() 
    content = content[:start] + daemon_config + content[end:]

    with open(bash_profile, 'w') as text_file:
        text_file.write(content)
    print('Powerline configuration updated in bash profile')

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
    pattern[1] = 'set rtp\+\=[\w(\-)/.]+/vim'
    
    config = '\n'.join(config)
    pattern = '\n'.join(pattern)

    content = None
    with open(vimrc) as text_file:
        content = ''.join([line for line in text_file.readlines()])

    pattern = re.compile(pattern)
    config_match = re.search(pattern, content)

    if not config_match:
        print('Appended powerline configuration in vimrc')
        with open(vimrc, 'a') as text_file:
            text_file.write(f'\n{config}\n')
        return

    current_config = config_match[0]

    if current_config == config:
        print('Powerline already configured in vimrc')
        return

    start, end = config_match.span()
    content = content[:start] + config + content[end:]

    with open(vimrc, 'w') as text_file:
        text_file.write(content)
    print('Powerline configuration updated in vimrc')

def configure_user_config_directory() -> bool:
    '''
    Checks & creates proper directory for the powerline configs to go
    '''
    home_dir = SETUP.dir['home']
    user_config_dir = SETUP.dir['powerline_config']
    system_config_dir = f'{SETUP.dir["python_site"]}/powerline/config_files/'

    command = f'find {home_dir}/.config'
    directory_found = call(command.split())

    if directory_found != 0:
        command = f'mkdir {home_dir}/.config'
        call(command.split())

    command = f'mkdir {user_config_dir}'
    call(command.split())

    command = f'cp -r {system_config_dir} {user_config_dir}'
    call(command.split())

def install_fonts():
    '''
    Downloads & installs all font files to proper location
    '''
    git_username = GITHUB.username
    user_config_dir = SETUP.dir['powerline_config']

    # Download & install fonts
    source = f'git@github.com:{git_username}/fonts.git'
    command = f'git clone {source}'
    call(command.split(), cwd=f'{user_config_dir}')

    command = '/bin/bash ./install.sh'
    call(command.split(), cwd=f'{user_config_dir}/fonts')

def install_gitstatus_at_user():
    '''
    Installs powerline-gitstatus at user level of system
    '''
    command = 'pip3 install --user powerline-gitstatus'
    check_call(command.split())

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
            print('Color scheme for git status for powerline is already configured')
            return

        data = default_data
        data['groups'] = {**default_group, **config_group}

    with open(default_block, 'w+', encoding='utf-8') as default_json:
        json.dump(data, default_json, ensure_ascii=False, indent=4)
    print('Finish configuring color scheme for git status in powerline!')

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
                print('Shell for git stats for powerline is already configured')
                return

        function_list.append(config_data)
        data = default_data
        data['segments']['left'] = function_list

    with open(default_block, 'w+', encoding='utf-8') as default_json:
        json.dump(data, default_json, ensure_ascii=False, indent=4)
    print('Finish configuring shell for git status in powerline!')

def uninstall_gitstatus():
    '''
    Uninstalls git powerline status at user level of system
    '''
    command = 'pip3 uninstall powerline-gitstatus'
    check_call(command.split())
    return

def delete_fonts():
    '''
    Deletes all font files assosciated with powerline from installation
    '''
    user_config_dir = SETUP.dir['powerline_config']

    command = '/bin/bash ./uninstall.sh'
    call(command.split(), cwd=f'{user_config_dir}/fonts')

    command = f'rm -r -f /fonts')
    call(command.split(), cwd=f'{user_config_dir}')

def delete_config():
    '''
    Deletes the entire powerline folder in user config
    '''
    user_config_dir = SETUP.dir['powerline_config']

    command = f'rm -r -f {user_config_dir}')
    call(command.split())

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
    pattern.append('source [\w(\-)/.]+.sh')

    pattern = '\n'.join(pattern)

    content = None
    with open(bash_profile) as text_file:
        content = ''.join([line for line in text_file.readlines()])

    pattern = re.compile(pattern)
    config_match = re.search(pattern, content)

    if not config_match:
        print('Powerline configuration in bash profile already removed')
        return

    start, end = config_match.span()
    content = content[:start] + content[end:]

    with open(bash_profile, 'w') as text_file:
        text_file.write(content)
    print('Powerline configuration removed in bash profile')

def remove_vim_config():
    '''
    Remove powerline config block in vimrc
    '''
    home_dir = SETUP.dir['home']
    vimrc = f'{home_dir}/.vimrc'

    pattern = []
    pattern.append('\" Powerline')
    pattern.append('set rtp\+\=[\w(\-)/.]+/vim')
    pattern.append('set laststatus=2')
    pattern.append('set t_Co=256')

    pattern = '\n'.join(pattern)

    content = None
    with open(vimrc) as text_file:
        content = ''.join([line for line in text_file.readlines()])

    pattern = re.compile(pattern)
    config_match = re.search(pattern, content)

    if not config_match:
        print('Powerline configuration in vimrc already removed')
        return

    start, end = config_match.span()
    content = content[:start] + content[end:]

    with open(vimrc, 'w') as text_file:
        text_file.write(content)
    print('Powerline configuration removed  in vimrc')

def uninstall_powerline():
    '''
    Uninstalls the powerline tool
    '''
    command = 'pip3 uninstall powerline-status'
    check_call(command.split())

