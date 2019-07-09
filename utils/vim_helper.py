'''
Module delegated to handling vim logic
'''

# System/Third-Party modules
import logging
import sys
from subprocess import Popen, call, check_call, DEVNULL, PIPE

# Custom modules
from utils.setup_wrapper import SETUP
from utils.github_wrapper import GITHUB

LOGGER = logging.getLogger()

def pull_vim_settings():
    '''
    Pull vim setting repository from github account
    '''
    git_username = GITHUB.username

    command = 'find config/vim/vim-settings'
    directory_found = call(command.split(), stdout=DEVNULL)

    if directory_found == 0:
        LOGGER.info('Vim settings already pulled from git')
        return

    source = f'git@github.com:{git_username}/vim-settings.git'
    destination = f'config/vim/vim-settings'
    command = f'git clone {source} {destination}'

    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            sys.exit()
        else:
            LOGGER.info(out.decode('utf-8'))

def configure_vimrc():
    '''
    Copies vimrc from local project vim settings to user settings
    '''
    home_dir = SETUP.dir['home']

    command = f'cp config/vim/vim-settings/.vimrc {home_dir}/.vimrc'

    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            sys.exit()
        else:
            LOGGER.info(out.decode('utf-8'))

def configure_color_themes():
    '''
    Moves color theme vim scripts to correct location
    '''
    home_dir = SETUP.dir['home']
    vim_color_dir = f'{home_dir}/.vim/colors'

    command = f'mkdir {vim_color_dir}'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.info(err.decode('utf-8'))
        else:
            LOGGER.info(out.decode('utf-8'))

    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'cp config/vim/vim-settings/color_themes/*.vim {vim_color_dir}')

    copy_result = call(command_list, stdout=DEVNULL)

    if copy_result == 0:
        LOGGER.info('Vim color themes copied to ~/.vim/colors')
    else:
        LOGGER.error('Error copying vim color themes in config')
        sys.exit()

def remove_color_themes():
    '''
    Remove all color themes in the vim config folder of user
    '''
    home_dir = SETUP.dir['home']
    vim_color_dir = f'{home_dir}/.vim/colors'

    command = f'rm {vim_color_dir}/*.vim'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.info(err.decode('utf-8'))
        else:
            LOGGER.info(out.decode('utf-8'))

def remove_vim_settings():
    '''
    Remove vim setting repository cloned from github
    '''
    command = 'find config/vim/vim-settings'
    directory_found = call(command.split(), stdout=DEVNULL)

    if directory_found != 0:
        LOGGER.info('Vim settings already removed')
        return

    command = 'rm -rf config/vim/vim-settings'

    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.info(err.decode('utf-8'))
        else:
            LOGGER.info(out.decode('utf-8'))

