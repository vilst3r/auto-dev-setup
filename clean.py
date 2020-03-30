#!/usr/bin/env python3

"""
Script to automate setup of unix environment with personal configurations and
tools
"""

# Native Modules
import logging
import time

# Custom Modules
from singletons.setup import SetupSingleton
from singletons.github import GithubSingleton
from utils import powerline_helper, git_helper, ssh_helper, \
    brew_helper, vim_helper, bash_helper
from utils.decorators import measure_time, print_process_step

SETUP: SetupSingleton = SetupSingleton.get_instance()
GITHUB: GithubSingleton = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


@print_process_step(step_no=1,
                    begin_message='Uninstalling powerline...',
                    end_message='Powerline uninstalled!')
def uninstall_powerline():
    """
    Remove existing powerline configurations
    """
    # powerline_helper.uninstall_gitstatus()
    # powerline_helper.delete_fonts()
    # powerline_helper.delete_config()
    # powerline_helper.remove_bash_daemon()
    # powerline_helper.remove_vim_config()
    # powerline_helper.uninstall_powerline_status()


@print_process_step(step_no=2,
                    begin_message='Uninstalling bash...',
                    end_message='Bash uninstalled!')
def uninstall_bash():
    """
    Remove existing bash configurations
    """
    # bash_helper.remove_bash_settings()


@print_process_step(step_no=3,
                    begin_message='Uninstalling vim...',
                    end_message='Vim uninstalled!')
def uninstall_vim():
    """
    Remove existing vim configurations
    """
    # vim_helper.remove_color_themes()
    # vim_helper.remove_vim_settings()


@print_process_step(step_no=4,
                    begin_message='Uninstalling homebrew...',
                    end_message='Homebrew uninstalled!')
def uninstall_brew():
    """
    Uninstall brew and cask together
    """
    # brew_helper.uninstall_brew()


@print_process_step(step_no=5,
                    begin_message='Uninstalling Git SSH...',
                    end_message='Git SSH uninstalled!')
def uninstall_git_ssh():
    """
    Remove existing git ssh configurations locally and on github
    """
    # if not ssh_helper.public_key_exists():
    #     LOGGER.info('Git SSH already uninstalled!')
    #     return
    #
    # current_public_key = ssh_helper.get_public_key()
    # public_keys = GITHUB.get_public_keys().json()
    #
    # git_helper.delete_github_pub_key(current_public_key, public_keys)
    # ssh_helper.delete_ssh_rsa_keypair()
    # ssh_helper.stop_ssh_agent()
    # git_helper.remove_ssh_config()
    # git_helper.remove_ssh_github_host()


if __name__ == '__main__':
    @measure_time
    def clean_dev_environment():
        """
        Cleans up the development environment that was automated
        TODO - Add multithreading for idle-dependencies, chart dependency graph
        """
        uninstall_powerline()
        uninstall_bash()
        uninstall_vim()
        uninstall_brew()
        uninstall_git_ssh()

    clean_dev_environment()
