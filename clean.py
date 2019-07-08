#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

# System/Third-Party modules
import logging
import time

# Custom modules
from utils.setup_wrapper import SETUP
from utils.github_wrapper import GITHUB
import utils.powerline_helper as powerline_helper
import utils.git_helper as git_helper
import utils.ssh_helper as ssh_helper
import utils.brew_helper as brew_helper
import utils.vim_helper as vim_helper
import utils.bash_helper as bash_helper

LOGGER = logging.getLogger()

def uninstall_powerline():
    '''
    Remove existing powerline configurations
    '''
    powerline_helper.uninstall_gitstatus()
    powerline_helper.delete_fonts()
    powerline_helper.delete_config()
    powerline_helper.remove_bash_daemon()
    powerline_helper.remove_vim_config()
    powerline_helper.uninstall_powerline()

def uninstall_bash():
    '''
    Remove existing bash configurations
    '''
    bash_helper.remove_bash_settings()

def uninstall_vim():
    '''
    Remove existing vim configurations
    '''
    vim_helper.remove_color_themes()
    vim_helper.remove_vim_settings()

def uninstall_brew():
    '''
    Uninstall brew and cask together
    '''
    brew_helper.uninstall_brew()

def uninstall_git_ssh():
    '''
    Remove existing git ssh configurations locally and on github
    '''
    current_public_key = ssh_helper.get_public_key()
    public_keys = GITHUB.get_public_keys().json()

    git_helper.delete_github_pub_key(current_public_key, public_keys)
    ssh_helper.delete_ssh_rsa_keypair()
    ssh_helper.stop_ssh_agent()
    git_helper.remove_ssh_config()
    git_helper.remove_ssh_github_host()

def pretty_print_wrapper(wrapper: object, title: str):
    '''
    Function to pretty print wrapper in beginning of cleanup
    '''
    LOGGER.info(f'###### {title} #####')
    LOGGER.info(f'{wrapper}')

def initialise_logger():
    '''
    Set up logging for writing stdout & stderr to files
    '''
    LOGGER.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    out_path = 'logs/cleanup_out.log'
    err_path = 'logs/cleanup_err.log'

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    out_handler = logging.FileHandler(f'{out_path}', 'w+')
    out_handler.setLevel(logging.INFO)
    out_handler.setFormatter(formatter)

    err_handler = logging.FileHandler(f'{err_path}', 'w+')
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(formatter)

    LOGGER.addHandler(out_handler)
    LOGGER.addHandler(err_handler)
    LOGGER.addHandler(stream_handler)

if __name__ == '__main__':
    START = time.time()
    pretty_print_wrapper(SETUP, 'SetupWrapper')
    pretty_print_wrapper(GITHUB, 'GithubWrapper')

    uninstall_powerline()
    uninstall_bash()
    uninstall_vim()
    uninstall_brew()
    uninstall_git_ssh()

    END = time.time()
    LOGGER.info(f'Cleanup time: {END - START} seconds')
