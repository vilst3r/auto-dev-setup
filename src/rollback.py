"""
Script to automate  cleanup of developement environment
"""

# Native Modules
import logging

from lib import dotfiles, git, pip, powerline, ssh
from singletons.github import GithubSingleton
# Custom Modules
from singletons.setup import SetupSingleton
from utils.decorators import measure_time, print_process_step
from utils.general import format_success_message

SETUP = SetupSingleton.get_instance()
GITHUB = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


@print_process_step(step_no=1, title='Uninstalling PIP...')
def uninstall_pip():
    """
    Remove all packages installed on PIP
    """
    pip.delete_all_user_packages()


@print_process_step(step_no=2, title='Uninstalling Powerline...')
def uninstall_powerline():
    """
    Remove existing powerline configurations
    """
    powerline.delete_powerline_fonts()
    powerline.delete_powerline_config_folder()


@print_process_step(step_no=3, title='Uninstalling dotfiles...')
def uninstall_dotfiles():
    """
    Remove dotfiles configurations
    """
    dotfiles.remove_dotfiles_repository()
    dotfiles.remove_user_dotfiles()


@print_process_step(step_no=4, title='Uninstalling Git SSH...')
def uninstall_git_ssh():
    """
    Remove existing git ssh configurations locally & on github.
    We only need to verify that the SSH public key is removed from GitHub
    """
    if not git.public_key_exists_on_github():
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
        uninstall_pip()
        uninstall_powerline()
        uninstall_dotfiles()
        uninstall_git_ssh()

    clean_dev_environment()
