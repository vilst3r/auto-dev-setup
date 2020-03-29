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
from utils import powerline_helper, git_helper, ssh_helper, \
                    brew_helper, vim_helper, bash_helper
from utils.decorators import measure_time, print_process_step

SETUP = SetupSingleton.get_instance()
GITHUB = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


@print_process_step(step_no=1,
                    begin_message='Configuring Git SSH...',
                    end_message='SSH key for Git is now configured!')
def configure_git_ssh():
    """
    Configure git ssh key to user ssh agent
    """
    # if (ssh_helper.public_key_exists() and
    #         git_helper.public_key_exists_on_github()):
    #     LOGGER.info("Git SSH is already configured!")
    #     return
    #
    # ssh_helper.generate_rsa_keypair()
    # ssh_helper.start_ssh_agent()
    # git_helper.update_ssh_config()
    # ssh_helper.register_private_key_to_ssh_agent()
    #
    # current_public_key = ssh_helper.get_public_key()
    #
    # payload = {"title": "script-env-pub-key", "key": current_public_key}
    # GITHUB.create_public_key(payload)


@print_process_step(step_no=2,
                    begin_message='Installing homebrew...',
                    end_message='Installation of homebrew is complete!')
def install_homebrew():
    """
    Install homebrew & cask if it doesn't exist in *nix environment and requires
    password input
    """
    # if brew_helper.brew_exists():
    #     LOGGER.info("Homebrew is already installed!")
    #     return
    #
    # brew_helper.install_brew()
    # brew_helper.tap_brew_cask()


@print_process_step(step_no=3,
                    begin_message='Installing brew packages...',
                    end_message='Installation of brew packages are complete!')
def install_brew_packages():
    """
    Install brew packages
    """
    # brew_helper.install_all_brew_packages()


@print_process_step(step_no=4,
                    begin_message='Installing cask packages...',
                    end_message='Installation of cask packages are complete!')
def install_cask_packages():
    """
    Reads brew-cask.txt file in child config directory to install all software
    applications
    """
    # brew_helper.install_all_cask_packages()


@print_process_step(step_no=5,
                    begin_message='Configuring vim...',
                    end_message='Vim is now configured!')
def configure_vim():
    """
    Configure vim settings
    """
    # vim_helper.pull_vim_settings()
    # vim_helper.configure_vimrc()
    # vim_helper.configure_color_themes()


@print_process_step(step_no=6,
                    begin_message='Configuring bash...',
                    end_message='Bash is now configured!')
def configure_bash():
    """
    Configure bash settings
    """
    # bash_helper.pull_bash_settings()
    # bash_helper.configure_bash_profile()


@print_process_step(step_no=7,
                    begin_message='Installing powerline...',
                    end_message='Powerline is installed & configured!')
def install_powerline():
    """
    Install powerline & configure it to bash & vim
    """
    # powerline_helper.install_powerline_at_user()
    # powerline_helper.write_bash_daemon()
    # powerline_helper.write_vim_config()
    # powerline_helper.configure_user_config_directory()
    # powerline_helper.install_fonts()
    #
    # powerline_helper.install_gitstatus_at_user()
    # powerline_helper.config_git_colorscheme()
    # powerline_helper.config_git_shell()


if __name__ == "__main__":
    @measure_time
    def build_dev_environment():
        """
        Run the following installation processes in sequential order with a
        single thread for now
        TODO - Add multithreading for idle-dependencies, chart dependency graph
        """
        configure_git_ssh()
        install_homebrew()
        install_brew_packages()
        install_cask_packages()
        configure_vim()
        configure_bash()
        install_powerline()

    build_dev_environment()

