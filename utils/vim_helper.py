'''
Module delegated to handling vim logic
'''

# System/Third-Party modules
import logging
import sys
from subprocess import Popen, call, DEVNULL, PIPE

# Custom modules
from utils.setup_wrapper import SETUP
from utils.github_wrapper import GITHUB

LOGGER = logging.getLogger()

def pull_vim_settings():
    '''
    Pull vim setting repository from github account
    '''
    git_username = GITHUB.username

    source = f'git@github.com:{git_username}/vim-settings.git'
    destination = f'config/vim/vim-settings'

    command = f'find {destination}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if directory_found:
        LOGGER.info('Vim settings already pulled from git')
        return

    command = f'git clone {source} {destination}'

    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()
        cloned_successfully = process.returncode == 0

        if err and not cloned_successfully:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to clone vim settings from github')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Vim settings has successfully been cloned from github')

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
            LOGGER.error('Failed to configure vimrc from git repository')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Vimrc now configured from git repository')

def configure_color_themes():
    '''
    Moves color theme vim scripts to correct location
    '''
    home_dir = SETUP.dir['home']
    vim_color_dir = f'{home_dir}/.vim/colors'

    command = f'mkdir -p {vim_color_dir}'
    call(command.split(), stdout=DEVNULL)
    LOGGER.info(f'{vim_color_dir} - has been created')

    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'cp config/vim/vim-settings/color_themes/*.vim {vim_color_dir}')

    files_copied = call(command_list, stdout=DEVNULL) == 0

    if files_copied:
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

    command = f'find {vim_color_dir}'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if not directory_found:
        LOGGER.info('Vim color themes already removed')
        return

    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'rm {vim_color_dir}/*.vim')
    with Popen(command_list, stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.debug(err.decode('utf-8'))
            LOGGER.info('Vim color themes has already been removed')
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Vim color themes has successfully been removed')

def remove_vim_settings():
    '''
    Remove vim setting repository cloned from github
    '''
    command = 'find config/vim/vim-settings'
    directory_found = call(command.split(), stdout=DEVNULL) == 0

    if not directory_found:
        LOGGER.info('Vim settings already removed')
        return

    command = 'rm -rf config/vim/vim-settings'

    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to remove vim settings cloned from github')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('Vim settings cloned from github has successfully been removed')
