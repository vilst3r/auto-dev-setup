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
from services import powerline, git, ssh, brew, dotfiles, pyp
from utils.decorators import measure_time, print_process_step
from utils.general import format_success_message

setup: SetupSingleton = SetupSingleton.get_instance()
GITHUB: GithubSingleton = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


@print_process_step(step_no=1, title='Configuring Git SSH...')
def configure_git_ssh():
    """
    Configure git ssh key to user ssh agent
    """
    if ssh.public_key_exists() and git.public_key_exists_on_github():
        LOGGER.info(format_success_message('Git SSH is already configured!'))
        return

    ssh.generate_rsa_keypair()
    ssh.start_ssh_agent()
    git.update_ssh_config()
    ssh.register_private_key_to_ssh_agent()

    current_public_key = ssh.get_public_key()

    payload = {'title': 'script-env-pub-key', 'key': current_public_key}
    GITHUB.create_public_key(payload)


@print_process_step(step_no=2, title='Installing Homebrew...')
def install_homebrew():
    """
    Install homebrew & cask if it doesn't exist in *nix environment & requires
    password input
    """
    if brew.brew_exists():
        LOGGER.info(format_success_message('Homebrew is already installed!'))
        return

    brew.install_brew()
    brew.tap_brew_cask()


@print_process_step(step_no=3, title='Installing brew packages...')
def install_brew_packages():
    """
    Install all brew binaries for Brew
    """
    brew.install_all_brew_packages()


@print_process_step(step_no=4, title='Installing cask packages...')
def install_cask_packages():
    """
    Installs all cask applications for Brew
    """
    brew.install_all_cask_packages()


@print_process_step(step_no=5, title='Installing PYP packages...')
def install_pyp_packages():
    """
    Installs all packages for PyP
    """
    pyp.install_all_pip_packages()


@print_process_step(step_no=6, title='Configuring dotfiles...')
def configure_dotfiles():
    """
    Configure user bash, vim & emacs settings
    """
    if not dotfiles.user_has_dotfiles_repo():
        LOGGER.info(format_success_message('User account doesn\'t have a '
                                           'dotfiles repository. Skipping '
                                           'this step...'))
        return

    dotfiles.pull_dotfile_settings()
    dotfiles.configure_vimrc()
    dotfiles.configure_bash_profile()
    dotfiles.configure_emacs()


@print_process_step(step_no=7, title='Installing powerline...')
def install_powerline():
    """
    Install powerline & configure it to bash & vim
    """
    powerline.install_powerline_at_user()
    powerline.write_bash_daemon()
    powerline.write_vim_config()
    powerline.configure_user_config_directory()
    powerline.install_fonts()

    powerline.install_gitstatus_at_user()
    powerline.config_git_colorscheme()
    powerline.config_git_shell()


if __name__ == '__main__':
    @measure_time
    def build_dev_environment():
        """
        Run the following installation processes in sequential order
        """
        configure_git_ssh()
        install_homebrew()
        install_brew_packages()
        install_cask_packages()
        install_pyp_packages()
        configure_dotfiles()
        install_powerline()

    build_dev_environment()
