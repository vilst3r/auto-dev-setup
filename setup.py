#!/usr/bin/env python3

"""
Script to automate setup of development environment with personally configured
tools & software by mainyl using the subprocess interface
"""

# Native Modules
import logging

# Custom Modules
from singletons.github import GithubSingleton
from services import powerline, git, ssh, brew, dotfiles, pyp
from utils.decorators import measure_time, print_process_step
from utils.general import format_success_message

GITHUB: GithubSingleton = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


@print_process_step(step_no=1, title='Installing Homebrew...')
def install_homebrew():
    """
    Installs homebrew & all configured system & application packages
    """
    if brew.brew_exists():
        LOGGER.info(format_success_message('Homebrew is already installed!'))
        return

    brew.install_brew()
    brew.tap_brew_cask()
    brew.install_all_brew_packages()
    brew.install_all_cask_packages()


@print_process_step(step_no=2, title='Configuring SSH keys...')
def configure_ssh_keys():
    """
    Configure a new ssh key for the user
    """
    if ssh.public_key_exists():
        LOGGER.info(format_success_message('SSH keys are already configured!'))
        return

    ssh.generate_rsa_keypair()
    ssh.start_ssh_agent()
    ssh.update_config_identity()
    ssh.register_private_key_to_ssh_agent()


@print_process_step(step_no=3, title='Configuring Github SSH connection...')
def configure_github_connection():
    """
    Configure git ssh key to user ssh agent
    """
    if git.public_key_exists_on_github():
        LOGGER.info(format_success_message('Github SSH connection is already'
                                           ' configured!'))
        return

    current_public_key = ssh.get_public_key()
    payload = {'title': 'script-env-pub-key', 'key': current_public_key}
    GITHUB.create_public_key(payload)


@print_process_step(step_no=4, title='Configuring dotfiles from GitHub...')
def configure_dotfiles():
    """
    Configure user bash, vim & emacs settings from their Github account
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


@print_process_step(step_no=5, title='Installing PYP packages...')
def install_pyp():
    """
    Installs PyP & all configured packages
    """
    pyp.install_all_pip_packages()
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
        install_homebrew()
        configure_ssh_keys()
        configure_github_connection()
        configure_dotfiles()
        install_pyp()
    build_dev_environment()
