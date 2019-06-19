'''
Module delegated to handling powerline status logic
'''

# System/Third-Party modules
import re
import json

# Custom modules
from utils.setup_wrapper import SetupWrapper

SETUP = SetupWrapper()

def write_bash_daemon():
    '''
    Append daemon configuration lines to bash profile
    '''
    home_dir = SETUP.dir['home']
    python_site = SETUP.dir['python_site']
    bash_profile = f'{home_dir}/.bash_profile'

    daemon_config = []
    daemon_config.append('powerline-daemon -q')
    daemon_config.append('POWERLINE_BASH_CONTINUATION=1')
    daemon_config.append('POWERLINE_BASH_SELECT=1')
    daemon_config.append(f'source {python_site}/powerline/bindings/bash/powerline.sh')

    daemon_config = '\n'.join(daemon_config)
    content = None
    with open(bash_profile) as text_file:
        content = ''.join([line for line in text_file.readlines()]

    if re.search(daemon_config, content):
        print('Powerline already configured in bash profile')
        return

    with open(bash_profile, 'a') as text_file:
        text_file.write(f'\n{daemon_config}\n')

def config_git_colorscheme():
    '''
    Configures color scheme for git status in powerline
    '''
    powerline_config = SETUP.dir['powerline_config']
    default_block = f'{powerline_config}/colorschemes/default.json'
    config_block = 'config/powerline_git_color.json'

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
    config_block = 'config/powerline_git_shell.json'

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
