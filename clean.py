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
from utils.general import format_ansi_string
from utils.unicode import *

SETUP: SetupSingleton = SetupSingleton.get_instance()
GITHUB: GithubSingleton = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


@print_process_step(step_no=1, title='Uninstalling powerline...')
def uninstall_powerline():
    """
    Remove existing powerline configurations
    """
    # powerline.uninstall_gitstatus()
    # powerline.delete_fonts()
    # powerline.delete_powerline_config_folder()
    # powerline.remove_bash_daemon()
    # powerline.remove_vim_config()
    # powerline.uninstall_powerline_status()


@print_process_step(step_no=2, title='Uninstalling bash...')
def uninstall_bash():
    """
    Remove existing bash configurations
    """
    # bash.remove_bash_settings()


@print_process_step(step_no=3, title='Uninstalling vim...')
def uninstall_vim():
    """
    Remove existing vim configurations
    """
    # vim.remove_color_themes()
    # vim.remove_vim_settings()


@print_process_step(step_no=4, title='Uninstalling homebrew...')
def uninstall_brew():
    """
    Uninstall brew and cask together
    """
    # brew.uninstall_brew()


@print_process_step(step_no=5, title='Uninstalling Git SSH...')
def uninstall_git_ssh():
    """
    Remove existing git ssh configurations locally and on github
    """
    # if not ssh.public_key_exists() and not git.public_key_exists_on_github():
    #     LOGGER.info(format_ansi_string('Git SSH already uninstalled!',
    #                                    ForeGroundColor.LIGHT_GREEN))
    #     return
    #
    # current_public_key = ssh.get_public_key()
    # public_keys = GITHUB.get_public_keys().json()
    #
    # git.delete_github_pub_key(current_public_key, public_keys)
    # ssh.delete_ssh_rsa_keypair()
    # ssh.stop_ssh_agent()
    # git.remove_ssh_config()
    # git.remove_ssh_github_host()


if __name__ == '__main__':
    @measure_time
    def clean_dev_environment():
        """
        Cleans up the development environment that was automated
        TODO - Add multithreading for idle-dependencies, chart dependency graph
        """
        uninstall_powerline()
        uninstall_bash()
        # TODO - add uninstall for dotfiles later
        uninstall_vim()
        uninstall_brew()
        uninstall_git_ssh()

    clean_dev_environment()
