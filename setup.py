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
from utils.decorators import measure_time

import utils.powerline_helper as powerline_helper
import utils.git_helper as git_helper
import utils.ssh_helper as ssh_helper
import utils.brew_helper as brew_helper
import utils.vim_helper as vim_helper
import utils.bash_helper as bash_helper

SETUP = SetupSingleton.get_instance()
GITHUB = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


def install_brew_packages():
    """
    Install brew packages
    """
    SETUP.print_process_step("Installing brew packages...")

    # brew_helper.install_all_brew_packages()

    SETUP.print_process_step(
        "Installation of brew packages are complete!", True
    )


def install_cask_packages():
    """
    Reads brew-cask.txt file in child config directory to install all software
    applications
    """
    SETUP.print_process_step("Installing cask packages...")

    # brew_helper.install_all_cask_packages()

    SETUP.print_process_step(
        "Installation of cask packages are complete!", True
    )


def install_homebrew():
    """
    Install homebrew & cask if it doesn't exist in *nix environment and requires
    password input
    """
    SETUP.print_process_step("Installing homebrew...")

    # if brew_helper.brew_exists():
    # 	SETUP.print_process_step("Homebrew is already installed!")
    # 	return

    # brew_helper.install_brew()
    # brew_helper.tap_brew_cask()

    SETUP.print_process_step("Installation of homebrew is complete!", True)


def configure_git_ssh():
    """
    Configure git ssh key to user ssh agent
    """
    SETUP.print_process_step("Configuring Git SSH...")

    # if ssh_helper.public_key_exists() and git_helper.public_key_exists_on_github():
    # 	SETUP.print_process_step("Git SSH is already configured!")
    # 	return

    # ssh_helper.generate_rsa_keypair()
    # ssh_helper.start_ssh_agent()
    # git_helper.update_ssh_config()
    # ssh_helper.register_private_key_to_ssh_agent()

    # current_public_key = ssh_helper.get_public_key()

    # payload = {}
    # payload["title"] = "script-env-pub-key"
    # payload["key"] = current_public_key
    # GITHUB.create_public_key(payload)

    SETUP.print_process_step("SSH key for Git is now configured!", True)


def configure_vim():
    """
    Configure vim settings
    """
    SETUP.print_process_step("Configuring vim...")

    # vim_helper.pull_vim_settings()
    # vim_helper.configure_vimrc()
    # vim_helper.configure_color_themes()

    SETUP.print_process_step("Vim is now configured!", True)


def configure_bash():
    """
    Configure bash settings
    """
    SETUP.print_process_step("Configuring bash...")

    # bash_helper.pull_bash_settings()
    # bash_helper.configure_bash_profile()

    SETUP.print_process_step("Bash is now configured!", True)


def install_powerline():
    """
    Install powerline & configure it to bash & vim
    """
    SETUP.print_process_step("Installing powerline...")

    # powerline_helper.install_powerline_at_user()
    # powerline_helper.write_bash_daemon()
    # powerline_helper.write_vim_config()
    # powerline_helper.configure_user_config_directory()
    # powerline_helper.install_fonts()

    # powerline_helper.install_gitstatus_at_user()
    # powerline_helper.config_git_colorscheme()
    # powerline_helper.config_git_shell()

    SETUP.print_process_step("Powerline is installed & configured!", True)


if __name__ == "__main__":
    @measure_time
    def main():
        """
        Run the following installations in sequence
        """
        configure_git_ssh()
        # install_homebrew()
        # install_brew_packages()
        # install_cask_packages()
        # configure_vim()
        # configure_bash()
        # install_powerline()
