#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

import subprocess
import pathlib
import time

def print_title(message: str):
    '''
    Prints each step of the setup in a pretty format
    '''
    n = len(message)
    top = ''.join(['-' for _ in range(n + 4)])
    middle = ''.join(list(f'| {message} |'))
    bottom = ''.join(['-' for _ in range(n + 4)] + ['\n'])

    print(top)
    print(middle)
    print(bottom)

def install_homebrew_packages():
    '''
    Reads brew.txt file in child config directory to install all brew packages
    '''
    with open('config/brew.txt') as text_file:
        lines = text_file.readlines()

        for line in lines:
            command = 'brew install ' + line
            install_rc = subprocess.call(command.split())

            # Try updating if package is not up to date
            if install_rc != 0:
                command = 'brew upgrade ' + line
                upgrade_rc = subprocess.call(command.split())
                
                if upgrade_rc != 0:
                    print(f'Error with this package in brew.txt - {line}')

        # Use brew python over system
        subprocess.call('brew link --overwrite python'.split())
        print_title('Installation of brew packages are complete!')

#def config_vim() -> int:
#    return

def install_homebrew():
    '''
    Install homebrew if it doesn't exist in *nix environment and requires password input
    '''
    # Check if homebrew is installed already curl command
    command = 'ls /usr/local/Cellar'
    ls_rc = subprocess.call(command.split(), stdout=subprocess.DEVNULL)
    if ls_rc == 0:
        print_title('Homebrew is already installed!')
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
    print_title('Installation of homebrew is complete')
     
def initialise_git_keychain() -> int:
    '''
    Initialise keychain for git in usr level
    '''
    return 0

def install_vim_configs():
    '''
    Configure vim settings including allocated theme
    '''

    # Check if credentials are configured
    with open('config/git-credentials.txt') as text_file:
        lines = text_file.readlines()

        for line in lines:
            key, val = line.split(':')

            if not val or val == '\n':
                raise Exception('Credentials are not initialised')

def install_powerline():
    '''
    Install powerline & configure it to bash & vim
    '''
    home_dir = str(pathlib.Path.home())
    config_dir = '.config/powerline'
    git_username = 'vilst3r'

    command = 'pip3 install powerline-status'
    subprocess.check_call(command.split())

    # Copy powerline build to user config
    command = f'mkdir {home_dir}/{config_dir}'
    subprocess.call(command.split())
    command = f'cp -r /usr/local/lib/python3.7/site-packages/powerline/config_files/ {home_dir}/{config_dir}'
    subprocess.call(command.split())

    # Download & install fonts
    command = f'git clone git@github.com:{git_username}/fonts.git'
    subprocess.call(command.split(), cwd=f'{home_dir}/{config_dir}')
    command = '/bin/bash ./install.sh'
    subprocess.call(command.split(), cwd=f'{home_dir}/{config_dir}/fonts')

    # Install forked powerline-gitstatus & configure it
    command = 'pip3 install --user powerline-gitstatus'
    subprocess.check_call(command.split())

if __name__ == '__main__':
    install_homebrew()
    install_homebrew_packages()
#    install_vim_configs()
#    install_powerline()
