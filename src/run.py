"""
Script to automate setup of development environment with personally configured
tools & software by mainly using the subprocess interface
"""

# Native Modules
import logging

# Custom Modules
from lib import brew, dotfiles, git, pip, powerline, ssh
from utils.decorators import measure_time, print_process_step
from utils.general import format_success_message

LOGGER = logging.getLogger()


@print_process_step(step_no=1, title='Installing Homebrew...')
def configure_brew():
    """
    Installs all configured system & application packages
    """
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
    Configure the user's SSH key to their own Github account
    """
    if git.public_key_exists_on_github():
        LOGGER.info(format_success_message('Github SSH connection is already'
                                           ' configured!'))
        return

    git.upload_ssh_key_to_github()


@print_process_step(step_no=4, title='Configuring dotfiles from GitHub...')
def configure_dotfiles():
    """
    Configure user's bash, vim & emacs settings from their Github account
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


@print_process_step(step_no=5, title='Configuring powerline for terminal...')
def configure_powerline():
    """
    Installs pip & all configured packages
    """
    powerline.install_powerline_at_user()
    powerline.configure_user_config()
    powerline.install_fonts()
    powerline.install_gitstatus_at_user()
    powerline.config_git_colorscheme()
    powerline.config_git_shell()


@print_process_step(step_no=6, title='Configuring other PIP packages...')
def configure_pip():
    """
    Installs pip & all configured packages
    """
    pip.install_all_pip_packages()


if __name__ == '__main__':
    @measure_time
    def build_dev_environment():
        """
        Runs the following installation processes in sequential order
        """
        configure_brew()
        configure_ssh_keys()
        configure_github_connection()
        configure_dotfiles()
        configure_powerline()
        # configure_pip()
    build_dev_environment()
