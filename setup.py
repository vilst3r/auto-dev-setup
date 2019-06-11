#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

# System/Third-Party modules
import subprocess
import pathlib
import pprint
import time

# Custom modules
from utils.setup_wrapper import *
from utils.github_wrapper import *

SETUP = SetupWrapper()
GITHUB = GithubWrapper()

def install_brew_packages():
    '''
    Reads brew.txt file in child config directory to install all brew packages and uses brew python over system
    '''
    buff = [line.strip() for line in read_file('config/brew.txt')]

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
        install_rc = subprocess.call(command.split())

    ## Use brew python over system
    subprocess.call('brew link --overwrite python'.split())
    SETUP.print_process_step('Installation of brew packages are complete!')

def install_cask_packages():
    '''
    Reads brew-cask.txt file in child config directory to install all software applications
    '''
    buff = read_file('config/brew-cask.txt')
    for package in buff:
        command = f'brew cask install {package}'
        install_rc = subprocess.call(command.split())

        # Try updating if package is not up to date
        if install_rc != 0:
            command = f'brew upgrade {package}'
            upgrade_rc = subprocess.call(command.split())

            if upgrade_rc != 0:
                print(f'Error with this package in brew.txt - {package}')

    # Use brew python over system
    subprocess.call('brew link --overwrite python'.split())
    SETUP.print_process_step('Installation of brew cask packages are complete!')

def install_homebrew():
    '''
    Install homebrew & cask if it doesn't exist in *nix environment and requires password input
    '''
    # Brew is installed if and only if cask is installed
    command = 'find /usr/local/Caskroom'
    return_code = subprocess.call(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if return_code == 0:
        SETUP.print_process_step('Homebrew is already installed!')
        return 

    ruby_bin = '/usr/bin/ruby'
    brew_url = 'https://raw.githubusercontent.com/Homebrew/install/master/install'

    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'{ruby_bin} -e \"$(curl -fsSL {brew_url})\"')
    process = subprocess.Popen(command_list, stdin=subprocess.PIPE)
    process.communicate()

    command = 'brew tap caskroom/cask'
    subprocess.call(command.split())

    SETUP.print_process_step('Installation of homebrew is complete')

def configure_git_ssh():
    '''
    Configure git ssh key to user ssh agent
    '''
    command = f'find {SETUP.dir["home"]}/.ssh/id_rsa.pub'
    return_code = subprocess.call(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if return_code == 0:
        SETUP.print_process_step('Git SSH is already configured')
    else:
        home_dir = SETUP.dir['home']
        command = f'ssh-keygen -t rsa -b 4096 -C \"{GITHUB.email}\" -N foobar'

        # Generate ssh key and overwrite if exists
        with subprocess.Popen(command.split(), stdin=subprocess.PIPE) as proc:
            proc.communicate(input=b'\ny\n')

        # Start ssh-agent
        command_list = []
        command_list.append('sh')
        command_list.append('-c')
        command_list.append(f'eval \"$(ssh-agent -s)\"')
        subprocess.call(command_list)
        print(' '.join(command_list))

        # Modify config
        buff = []
        config = read_file(f'{SETUP.dir["home"]}/.ssh/config')
        for line in config:
            key, val = line.strip().split()
            buff.append(f'{key} {val}\n')

        identity_key_exists = False
        identity_val = f'{SETUP.dir["home"]}/.ssh/id_rsa'
        for i, line in enumerate(buff):
            key, val = line.split()

            if key == 'IdentityFile':
                identity_key_exists = True
                buff[i] = f'{key} {identity_val}'
                break

        if not identity_key_exists:
            buff.append(f'IdentityFile {identity_val}')

        # Rewrite config
        write_file(f'{SETUP.dir["home"]}/.ssh/config', buff)

        # Add ssh private key to ssh-agent
        command = f'ssh-add -K {home_dir}/.ssh/id_rsa'
        subprocess.call(command.split())

        SETUP.print_process_step('SSH key for Git is configured')

        # Need to pbcopy and send this to GitAPI

def configure_vim():
    '''
    Configure vim settings
    '''
    home_dir = SETUP.dir['home']
    git_username = GITHUB.username

    # Pull vim settings remotely
    command = 'find config/vim-settings'
    return_code = subprocess.call(command.split(), stdout=subprocess.DEVNULL)

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
    return_code = subprocess.call(command.split(), stdout=subprocess.DEVNULL)

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
    home_dir = SETUP.dir['home']
    git_username = GITHUB.username
    user_config_dir = SETUP.dir['user_powerline_config']
    system_config_dir = SETUP.dir['system_powerline_config']

    # Install powerline from pip
    command = 'pip3 install powerline-status'
    subprocess.check_call(command.split())

    # Copy powerline system config to user config
    command = f'mkdir {user_config_dir}'
    subprocess.call(command.split())

    command = f'cp -r {system_config_dir} {user_config_dir}'
    subprocess.call(command.split())

    # Download & install fonts
    command = f'git clone git@github.com:{git_username}/fonts.git'
    subprocess.call(command.split(), cwd=f'{user_config_dir}')

    command = '/bin/bash ./install.sh'
    subprocess.call(command.split(), cwd=f'{user_config_dir}/fonts')

    # Install forked powerline-gitstatus & configure it
    command = 'pip3 install --user powerline-gitstatus'
    subprocess.check_call(command.split())

    SETUP.print_process_step('Powerline is installed & configured')

def pretty_print_wrapper(wrapper: object, title: str):
    '''
    Function to pretty print wrapper in beginning of setup
    '''
    print(f'###### {title} #####')
    print(f'\n{wrapper}\n')

if __name__ == '__main__':
    start = time.time()
    pretty_print_wrapper(SETUP, 'SetupWrapper')
    pretty_print_wrapper(GITHUB, 'GithubWrapper')

    configure_git_ssh()
    install_homebrew()
    install_brew_packages()
#    install_cask_packages()
    configure_vim()
    configure_bash()
    install_powerline()

    end = time.time()
    print(f'\nSetup time - {end - start} seconds\n')
