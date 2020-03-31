#!/usr/bin/env python3

"""
Script to automate setup of development environment with personally configured
tools & software by mainyl using the subprocess interface
"""

# Native Modules
import logging

# Custom Modules
from singletons.setup import SetupSingleton
from singletons.github import GithubSingleton
from services import powerline, git, ssh, brew, dotfiles
from utils.decorators import measure_time, print_process_step

SETUP: SetupSingleton = SetupSingleton.get_instance()
GITHUB: GithubSingleton = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


@print_process_step(step_no=1,
                    begin_message='Configuring Git SSH...',
                    end_message='SSH key for Git is now configured!')
def configure_git_ssh():
    """
    Configure git ssh key to user ssh agent
    """
    if ssh.public_key_exists() and git.public_key_exists_on_github():
        LOGGER.info('Git SSH is already configured!')
        return

    ssh.generate_rsa_keypair()
    ssh.start_ssh_agent()
    git.update_ssh_config()
    ssh.register_private_key_to_ssh_agent()

    current_public_key = ssh.get_public_key()

    payload = {'title': 'script-env-pub-key', 'key': current_public_key}
    GITHUB.create_public_key(payload)


@print_process_step(step_no=2,
                    begin_message='Installing homebrew...',
                    end_message='Installation of homebrew is complete!')
def install_homebrew():
    """
    Install homebrew & cask if it doesn't exist in *nix environment and requires
    password input
    """
    if brew.brew_exists():
        LOGGER.info('Homebrew is already installed!')
        return

    brew.install_brew()
    brew.tap_brew_cask()


@print_process_step(step_no=3,
                    begin_message='Installing brew packages...',
                    end_message='Installation of brew packages are complete!')
def install_brew_packages():
    """
    Install brew packages
    """
    brew.install_all_brew_packages()


@print_process_step(step_no=4,
                    begin_message='Installing cask packages...',
                    end_message='Installation of cask packages are complete!')
def install_cask_packages():
    """
    Reads brew-cask.txt file in child config directory to install all software
    applications
    """
    brew.install_all_cask_packages()


@print_process_step(step_no=5,
                    begin_message='Configuring dotfiles...',
                    end_message='Dotfiles are now configured!')
def configure_dotfiles():
    """
    Configure user bash, vim & emacs settings
    """

    dotfiles.pull_dotfile_settings()
    # dotfiles.configure_vimrc()
    # dotfiles.configure_vim_color_themes()
    # dotfiles.configure_bash_profile()
    # dotfiles.configure_emacs()


@print_process_step(step_no=6,
                    begin_message='Installing powerline...',
                    end_message='Powerline is installed & configured!')
def install_powerline():
    """
    Install powerline & configure it to bash & vim
    """
    # powerline.install_powerline_at_user()
    # powerline.write_bash_daemon()
    # powerline.write_vim_config()
    # powerline.configure_user_config_directory()
    # powerline.install_fonts()
    #
    # powerline.install_gitstatus_at_user()
    # powerline.config_git_colorscheme()
    # powerline.config_git_shell()


if __name__ == '__main__':
    @measure_time
    def build_dev_environment():
        """
        Run the following installation processes in sequential order with a
        single thread for now
        TODO - Add multithreading for idle-dependencies, chart dependency graph
        """
        # configure_git_ssh()
        # install_homebrew()
        # install_brew_packages()
        # install_cask_packages()
        # configure_dotfiles()
        # install_powerline()

    build_dev_environment()

