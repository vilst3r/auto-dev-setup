#!/usr/bin/env python3

"""
Script to automate setup of unix environment with personal configurations and
tools
"""

# Native Modules
import logging

# Custom Modules
from singletons.setup import SetupSingleton
from singletons.github import GithubSingleton
from services import powerline, git, ssh, brew, dotfiles
from utils.decorators import measure_time, print_process_step
from utils.general import format_ansi_string, format_success_message
from utils.unicode import *

SETUP: SetupSingleton = SetupSingleton.get_instance()
GITHUB: GithubSingleton = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


@print_process_step(step_no=1, title='Uninstalling Powerline...')
def uninstall_powerline():
    """
    Remove existing powerline configurations
    """
    # powerline.uninstall_powerline_gitstatus()
    # powerline.delete_powerline_fonts()
    # powerline.delete_powerline_config_folder()
    # powerline.remove_powerline_daemon_in_bash_profile()
    # powerline.remove_powerline_config_in_vimrc()
    # powerline.uninstall_powerline_status()


@print_process_step(step_no=2, title='Uninstalling dotfiles...')
def uninstall_dotfiles():
    """
    Remove existing dotfile configurations
    """
    # dotfiles.remove_color_themes()
    # dotfiles.remove_dotfiles_settings()


@print_process_step(step_no=3, title='Uninstalling Homebrew...')
def uninstall_brew():
    """
    Uninstall brew and cask together
    """
    # brew.uninstall_brew()


@print_process_step(step_no=4, title='Uninstalling Git SSH...')
def uninstall_git_ssh():
    """
    Remove existing git ssh configurations locally & on github
    """
    if not ssh.public_key_exists() and not git.public_key_exists_on_github():
        LOGGER.info(format_success_message('Git SSH already uninstalled!'))
        return

    current_public_key = ssh.get_public_key()
    public_keys = GITHUB.get_public_keys().json()

    git.delete_github_pub_key(current_public_key, public_keys)
    ssh.delete_ssh_rsa_keypair()
    ssh.stop_ssh_agent()
    git.remove_ssh_config()
    git.remove_ssh_github_host()


if __name__ == '__main__':
    @measure_time
    def clean_dev_environment():
        """
        Cleans up the development environment that was automatically setup
        previously
        """
        uninstall_powerline()
        uninstall_dotfiles()
        uninstall_brew()
        uninstall_git_ssh()

    clean_dev_environment()
