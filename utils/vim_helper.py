'''
Module delegated to handling vim logic
'''

# System/Third-Party modules
from subprocess import call, check_call, DEVNULL

# Custom modules
from utils.setup_wrapper import SETUP
from utils.github_wrapper import GITHUB

def pull_vim_settings():
    '''
    Pull vim setting repository from github account
    '''
    git_username = GITHUB.username

    command = 'find config/vim/vim-settings'
    directory_found = call(command.split(), stdout=DEVNULL)

    if directory_found == 0:
        print('Vim settings already pulled from git')
        return

    source = f'git@github.com:{git_username}/vim-settings.git'
    destination = f'config/vim/vim-settings'
    command = f'git clone {source} {destination}'
    check_call(command.split())

def configure_vimrc():
    '''
    Copies vimrc from local project vim settings to user settings
    '''
    home_dir = SETUP.dir['home']

    command = f'cp config/vim/vim-settings/.vimrc {home_dir}/.vimrc'
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
    command_list.append(f'cp config/vim/vim-settings/color_themes/*.vim {vim_color_dir}')
    copy_result = call(command_list)

    if copy_result == 0:
        print('Vim color themes copied to ~/.vim/colors')
    else:
        raise Exception('Error copying vim color themes in config')

def remove_color_themes():
    '''
    Remove all color themes in the vim config folder of user
    '''
    home_dir = SETUP.dir['home']
    vim_color_dir = f'{home_dir}/.vim/colors'

    command =f'rm {vim_color_dir}/*.vim')
    call(command.split())

def remove_vim_settings():
    '''
    Remove vim setting repository cloned from github
    '''
    command = 'find config/vim/vim-settings'
    directory_found = call(command.split(), stdout=DEVNULL)

    if directory_found != 0:
        print('Vim settings already removed')
        return

    command = 'rm -rf config/vim/vim-settings'
    check_call(command.split())
