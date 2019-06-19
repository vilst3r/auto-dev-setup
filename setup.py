#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

# System/Third-Party modules
import subprocess
from subprocess import PIPE, DEVNULL
import time
import re

# Custom modules
from utils.setup_wrapper import SetupWrapper
from utils.github_wrapper import GithubWrapper
import utils.powerline_helper as powerline_helper
import utils.git_helper as git_helper

SETUP = SetupWrapper()
GITHUB = GithubWrapper()

def install_brew_packages():
    '''
    Install brew packages and uses brew python over system by replacing symlink
    '''
    buff = []
    with open('config/brew.txt') as text_file:
        buff = [line.strip() for line in text_file.readlines()]

    command = 'brew list'
    brew_list = subprocess.check_output(command.split()).decode('utf-8').split('\n')

    for package in buff:
        if package in brew_list:
            continue

        # Check that package is valid and exists in brew registry
        command = f'brew info {package}'
        check_rc = subprocess.call(command.split())

        if check_rc != 0:
            print(f'This package does not exist in registry - {package}')

        command = f'brew install {package}'
        subprocess.call(command.split())

    ## Use brew python over system
    subprocess.call('brew link --overwrite python'.split())
    SETUP.print_process_step('Installation of brew packages are complete!')

def install_cask_packages():
    '''
    Reads brew-cask.txt file in child config directory to install all software applications
    '''
    buff = []
    with open('config/brew-cask.txt') as text_file:
        buff = [line.strip() for line in text_file.readlines()]

    command = 'brew cask list'
    cask_list = subprocess.check_output(command.split()).decode('utf-8').split('\n')

    for package in buff:
        if package in cask_list:
            continue

        # Check that package is valid and exists in brew registry
        command = f'brew cask info {package}'
        check_rc = subprocess.call(command.split())

        if check_rc != 0:
            print(f'This package does not exist in registry - {package}')

        command = f'brew cask install {package}'
        subprocess.call(command.split())

def install_homebrew():
    '''
    Install homebrew & cask if it doesn't exist in *nix environment and requires password input
    '''
    # Brew is installed if and only if cask is installed
    command = 'find /usr/local/Caskroom'
    return_code = subprocess.call(command.split(), stdout=DEVNULL, stderr=DEVNULL)

    if return_code == 0:
        SETUP.print_process_step('Homebrew is already installed!')
        return

    ruby_bin = '/usr/bin/ruby'
    brew_url = 'https://raw.githubusercontent.com/Homebrew/install/master/install'

    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'{ruby_bin} -e \"$(curl -fsSL {brew_url})\"')
    subprocess.call(command_list, stdin=PIPE)

    command = 'brew tap caskroom/cask'
    subprocess.call(command.split())

    SETUP.print_process_step('Installation of homebrew is complete')

def configure_git_ssh():
    '''
    Configure git ssh key to user ssh agent
    '''
    home_dir = SETUP.dir['home']
    git_email = GITHUB.email

    command = f'find {home_dir}/.ssh/id_rsa.pub'
    return_code = subprocess.call(command.split(), stdout=DEVNULL, stderr=DEVNULL)

    if return_code == 0:
        SETUP.print_process_step('Git SSH is already configured')
        return

    # Generate ssh key and overwrite if exists
    command = f'ssh-keygen -t rsa -b 4096 -C \"{git_email}\" -N foobar'
    with subprocess.Popen(command.split(), stdin=PIPE) as proc:
        proc.communicate(input=b'\ny\n')

    # Start ssh-agent
    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'eval \"$(ssh-agent -s)\"')
    subprocess.call(command_list)

    git_helper.update_ssh_config()

    # Add ssh private key to ssh-agent
    command = f'ssh-add -K {home_dir}/.ssh/id_rsa'
    subprocess.call(command.split())

    # Need to pbcopy and send this to GitAPI
    command = f'cat {home_dir}/.ssh/id_rsa.pub'
    key_type, curr_pub_key = subprocess.check_output(command.split()).decode('utf-8').split()[:2]
    curr_pub_key = f'{key_type} {curr_pub_key}'

    public_keys = GITHUB.get_public_keys().json()

    # Search if key already exists
    pattern = re.compile(re.escape(curr_pub_key))
    for key in public_keys:
        if re.match(pattern, key['key']):
            SETUP.print_process_step('Git SSH is already configured')
            return

    # Add new public key to Git API
    payload = {}
    payload['title'] = 'script-env-pub-key'
    payload['key'] = curr_pub_key
    GITHUB.create_public_key(payload)

    SETUP.print_process_step('SSH key for Git is configured')

def configure_vim():
    '''
    Configure vim settings
    '''
    home_dir = SETUP.dir['home']
    git_username = GITHUB.username

    # Pull vim settings remotely
    command = 'find config/vim-settings'
    return_code = subprocess.call(command.split(), stdout=DEVNULL)

    if return_code == 0:
        print('Vim settings already pulled from git')
    else:
        command = f'git clone git@github.com:{git_username}/vim-settings.git config/vim-settings'
        subprocess.check_call(command.split())

    command = f'cp config/vim-settings/.vimrc {home_dir}/.vimrc'
    subprocess.check_call(command.split())

    # Configure vim color themes in directory
    vim_color_dir = f'{home_dir}/.vim/colors'
    command = f'mkdir {vim_color_dir}'
    subprocess.call(command.split())

    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'cp config/vim-settings/color_themes/*.vim {vim_color_dir}')
    copy_rc = subprocess.call(command_list)

    if copy_rc == 0:
        print('Vim color themes copied to ~/.vim/colors')
    else:
        raise Exception('Error copying vim color themes in config')

    SETUP.print_process_step('Vim is now configured')

def configure_bash():
    '''
    Configure bash settings
    '''
    home_dir = SETUP.dir['home']
    git_username = GITHUB.username

    # Pull bash settings remotely
    command = 'find config/bash-settings'
    return_code = subprocess.call(command.split(), stdout=DEVNULL)

    if return_code == 0:
        print('Bash settings already pulled from git')
    else:
        command = f'git clone git@github.com:{git_username}/bash-settings.git config/bash-settings'
        subprocess.check_call(command.split())

    command = f'cp config/bash-settings/.bash_profile {home_dir}/.bash_profile'
    subprocess.call(command.split())

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
