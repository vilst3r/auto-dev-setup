#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

import subprocess
import pathlib
import time

def install_homebrew_packages():
    '''
    Reads brew.txt file in child config directory to install all brew packages
    '''
    with open('config/brew.txt') as text_file:
        lines = text_file.readlines()

        for line in lines:
            command = 'brew install ' + line
            subprocess.check_call(command.split())
        print('Installation of brew packages are complete!')

#def config_vim() -> int:
#    return

def install_homebrew() -> int:
    '''
    Install homebrew if it doesn't exist in *nix environment
    '''
    command = '/usr/bin/ruby -e \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)\"'
    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(command)

    print(command_list)
    process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = process.communicate(input=b'one')[0]
    print(out.decode('utf-8'))

def initialise_git_keychain() -> int:
    '''
    Initialise keychain for git in usr level
    '''
    return 0

def install_vim_configs() -> int:
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
    return

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
#    install_homebrew()
#    install_vim_configs()
#    install_homebrew_packages()
#    install_powerline()
