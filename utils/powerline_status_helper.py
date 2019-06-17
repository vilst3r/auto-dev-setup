'''
Module delegated to handling powerline status logic
'''

# System/Third-Party modules
import re

# Custom modules
from utils.setup_wrapper import SetupWrapper
from utils.io_helper import read_file

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
    content = ''.join(read_file(bash_profile))

    if re.search(daemon_config, content):
        print('Powerline already configured in bash profile')
        return

    with open(bash_profile, 'a') as text_file:
        text_file.write(f'\n{daemon_config}\n')
