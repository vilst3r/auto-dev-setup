'''
Module delegated to handling vim logic
'''

# System/Third-Party modules
from subprocess import call, check_call, DEVNULL

# Custom modules
from utils.setup_wrapper import SetupWrapper
from utils.github_wrapper import GithubWrapper

SETUP = SetupWrapper()
GITHUB = GithubWrapper()

def pull_vim_settings():
    '''
    Pull vim setting repository from github account
    '''
    git_username = GITHUB.username

    command = 'find config/vim-settings'
    directory_exists = call(command.split(), stdout=DEVNULL)

    if directory_exists == 0:
        print('Vim settings already pulled from git')
        return

    source = f'git@github.com:{git_username}/vim-settings.git'
    destination = f'config/vim-settings'
    command = f'git clone {source} {destination}'
    check_call(command.split())

def configure_vimrc():
    '''
    Copies vimrc from local project vim settings to user settings
    '''
    home_dir = SETUP.dir['home']

    command = f'cp config/vim-settings/.vimrc {home_dir}/.vimrc'
    check_call(command.split())

def configure_color_themes():
    '''
    Moves color theme vim scripts to correct location
    '''
    home_dir = SETUP.dir['home']
    vim_color_dir = f'{home_dir}/.vim/colors'

    command = f'mkdir {vim_color_dir}'
    call(command.split())

    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'cp config/vim-settings/color_themes/*.vim {vim_color_dir}')
    copy_result = call(command_list)

    if copy_result == 0:
        print('Vim color themes copied to ~/.vim/colors')
    else:
        raise Exception('Error copying vim color themes in config')
