#!/usr/bin/env python3

"""
Script to automate setup of unix environment with personal configurations and tools
"""

# Native Modules
import time

# Custom Modules
from utils.logger import LOGGER, initialise_logger
from utils.setup_wrapper import SETUP
from utils.github_wrapper import GITHUB
import utils.powerline_helper as powerline_helper
import utils.git_helper as git_helper
import utils.ssh_helper as ssh_helper
import utils.brew_helper as brew_helper
import utils.vim_helper as vim_helper
import utils.bash_helper as bash_helper


def install_brew_packages():
    """
	Install brew packages
	"""
    SETUP.print_process_step_start("Installing brew packages...")

    brew_helper.install_all_brew_packages()

    SETUP.print_process_step_finish("Installation of brew packages are complete!")


def install_cask_packages():
    """
	Reads brew-cask.txt file in child config directory to install all software applications
	"""
    SETUP.print_process_step_start("Installing cask packages...")

    brew_helper.install_all_cask_packages()

    SETUP.print_process_step_finish("Installation of cask packages are complete!")


def install_homebrew():
    """
	Install homebrew & cask if it doesn't exist in *nix environment and requires password input
	"""
    SETUP.print_process_step_start("Installing homebrew...")

    # if brew_helper.brew_exists():
    # 	SETUP.print_process_step_finish("Homebrew is already installed!")
    # 	return

    brew_helper.install_brew()
    brew_helper.tap_brew_cask()

    SETUP.print_process_step_finish("Installation of homebrew is complete!")


def configure_git_ssh():
    """
	Configure git ssh key to user ssh agent
	"""
    SETUP.print_process_step_start("Configuring Git SSH...")

    # if ssh_helper.public_key_exists() and git_helper.public_key_exists_on_github():
    # 	SETUP.print_process_step_finish("Git SSH is already configured!")
    # 	return

    ssh_helper.generate_rsa_keypair()
    ssh_helper.start_ssh_agent()
    git_helper.update_ssh_config()
    ssh_helper.register_private_key_to_ssh_agent()

    current_public_key = ssh_helper.get_public_key()

    payload = {}
    payload["title"] = "script-env-pub-key"
    payload["key"] = current_public_key
    GITHUB.create_public_key(payload)

    SETUP.print_process_step_finish("SSH key for Git is now configured!")


def configure_vim():
    """
	Configure vim settings
	"""
    SETUP.print_process_step_start("Configuring vim...")

    vim_helper.pull_vim_settings()
    vim_helper.configure_vimrc()
    vim_helper.configure_color_themes()

    SETUP.print_process_step_finish("Vim is now configured!")


def configure_bash():
    """
	Configure bash settings
	"""
    SETUP.print_process_step_start("Configuring bash...")

    bash_helper.pull_bash_settings()
    bash_helper.configure_bash_profile()

    SETUP.print_process_step_finish("Bash is now configured!")


def install_powerline():
    """
	Install powerline & configure it to bash & vim
	"""
    SETUP.print_process_step_start("Installing powerline...")

    powerline_helper.install_powerline_at_user()
    powerline_helper.write_bash_daemon()
    powerline_helper.write_vim_config()
    powerline_helper.configure_user_config_directory()
    powerline_helper.install_fonts()

    powerline_helper.install_gitstatus_at_user()
    powerline_helper.config_git_colorscheme()
    powerline_helper.config_git_shell()

    SETUP.print_process_step_finish("Powerline is installed & configured!")


if __name__ == "__main__":
    initialise_logger()

    LOGGER.debug("###### SetupWrapper #####")
    LOGGER.debug(SETUP)
    LOGGER.debug("###### GithubWrapper #####")
    LOGGER.debug(GITHUB)

    START = time.time()

    # configure_git_ssh()
    # install_homebrew()
    # install_brew_packages()
    # install_cask_packages()
    # configure_vim()
    # configure_bash()
    # install_powerline()

    END = time.time()
    TIME_ELAPSED = END - START
    LOGGER.info(f"Setup time: {TIME_ELAPSED} seconds")
