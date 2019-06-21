#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

# System/Third-Party modules
import subprocess
import time

# Custom modules
from utils.setup_wrapper import SetupWrapper
from utils.github_wrapper import GithubWrapper
import utils.powerline_helper as powerline_helper
import utils.git_helper as git_helper
import utils.ssh_helper as ssh_helper
import utils.brew_helper as brew_helper
import utils.vim_helper as vim_helper
import utils.bash_helper as bash_helper

SETUP = SetupWrapper()
GITHUB = GithubWrapper()

def install_brew_packages():
    '''
    Install brew packages and uses brew python over system by replacing symlink
    '''
    packages = brew_helper.get_uninstalled_brew_packages()

    for package in packages:
        brew_helper.install_that_brew(package)

    brew_helper.use_brew_python()

    SETUP.print_process_step('Installation of brew packages are complete!')

def install_cask_packages():
    '''
    Reads brew-cask.txt file in child config directory to install all software applications
    '''
    packages = brew_helper.get_uninstalled_cask_packages()

    for package in packages:
        brew_helper.install_that_cask(package)

def install_homebrew():
    '''
    Install homebrew & cask if it doesn't exist in *nix environment and requires password input
    '''
    if brew_helper.brew_exists():
        SETUP.print_process_step('Homebrew is already installed!')
        return

    brew_helper.install_brew()
    brew_helper.tap_brew_cask()

    SETUP.print_process_step('Installation of homebrew is complete')

def configure_git_ssh():
    '''
    Configure git ssh key to user ssh agent
    '''
    if ssh_helper.ssh_public_key_exists():
        SETUP.print_process_step('Git SSH is already configured')
        return

    ssh_helper.generate_rsa_ssh_keypair()
    ssh_helper.start_ssh_agent()
    git_helper.update_ssh_config()
    ssh_helper.register_private_key_to_ssh_agent()

    current_public_key = ssh_helper.get_ssh_public_key()
    public_keys = GITHUB.get_public_keys().json()

    if git_helper.github_public_key_exists(current_public_key, public_keys):
        SETUP.print_process_step('Git SSH is already configured')
        return

    payload = {}
    payload['title'] = 'script-env-pub-key'
    payload['key'] = current_public_key
    GITHUB.create_public_key(payload)

    SETUP.print_process_step('SSH key for Git is configured')

def configure_vim():
    '''
    Configure vim settings
    '''
    vim_helper.pull_vim_settings()
    vim_helper.configure_vimrc()
    vim_helper.configure_color_themes()

    SETUP.print_process_step('Vim is now configured')

def configure_bash():
    '''
    Configure bash settings
    '''
    bash_helper.pull_bash_settings()
    bash_helper.configure_bash_profile()

    SETUP.print_process_step('Bash is now configured')

def install_powerline():
    '''
    Install powerline & configure it to bash & vim
    '''
    git_username = GITHUB.username
    home_dir = SETUP.dir['home']
    python_site = SETUP.dir['python_site']
    powerline_config = SETUP.dir['powerline_config']

    # Install powerline from pip
    command = 'pip3 install --user powerline-status'
    subprocess.check_call(command.split())

    powerline_helper.write_bash_daemon()

    command = f'find {home_dir}/.config'
    find_rc = subprocess.call(command.split())

    if find_rc != 0:
        command = f'mkdir {home_dir}/.config'
        subprocess.call(command.split())

    # Copy powerline system config to user config
    command = f'mkdir {powerline_config}'
    subprocess.call(command.split())

    system_config_dir = f'{python_site}/powerline/config_files/'
    command = f'cp -r {system_config_dir} {powerline_config}'
    subprocess.call(command.split())

    # Download & install fonts
    command = f'git clone git@github.com:{git_username}/fonts.git'
    subprocess.call(command.split(), cwd=f'{powerline_config}')

    command = '/bin/bash ./install.sh'
    subprocess.call(command.split(), cwd=f'{powerline_config}/fonts')

    # Install forked powerline-gitstatus & configure it
    command = 'pip3 install --user powerline-gitstatus'
    subprocess.check_call(command.split())

    powerline_helper.config_git_colorscheme()
    powerline_helper.config_git_shell()

    SETUP.print_process_step('Powerline is installed & configured')

def pretty_print_wrapper(wrapper: object, title: str):
    '''
    Function to pretty print wrapper in beginning of setup
    '''
    print(f'###### {title} #####')
    print(f'\n{wrapper}\n')

if __name__ == '__main__':
    START = time.time()
    pretty_print_wrapper(SETUP, 'SetupWrapper')
    pretty_print_wrapper(GITHUB, 'GithubWrapper')

#    configure_git_ssh()
#    install_homebrew()
#    install_brew_packages()
#    install_cask_packages()
#    configure_vim()
#    configure_bash()
    install_powerline()

    END = time.time()
    print(f'\nSetup time: {END - START} seconds\n')
