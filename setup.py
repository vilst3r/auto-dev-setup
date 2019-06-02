#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

import subprocess
import pathlib
import pprint

class SetupWrapper():
    '''
    Wrapper object to track state of counter
    '''
    def __init__(self):
        self.step = 0
        self.git = {}

        # Read from config for git credentials
        with open('./config/git-credentials.txt') as text_file:
            lines = text_file.readlines()

            for line in lines:
                key, val = line.split(':')

                if not key or not val:
                    raise Exception('Git credentials are not configured properly')

                key, val = key.strip(), val.strip()
                self.git[key] = val

        # Configure directory map
        self.dir = {}
        self.dir['home'] = str(pathlib.Path.home())
        self.dir['user_powerline_config'] = '.config/powerline'
        self.dir['system_powerline_config'] = '/usr/local/lib/python3.7/site-packages/powerline/config_files/'

    def __str__(self):
        str_vals = {**self.git, **self.dir, 'step': self.step}
        pretty_str = pprint.pformat(str_vals)
        return pretty_str

    def increment_step(self):
        '''
        Increment counter
        '''
        self.step += 1

SETUP = SetupWrapper()

def print_process_step(message: str):
    '''
    Prints each step of the setup in a pretty format
    '''
    SETUP.increment_step()
    step_str = f'| {SETUP.step}. {message} |'
    row_len = len(step_str)

    top = ''.join(['-' for _ in range(row_len)])
    bottom = ''.join(['-' for _ in range(row_len)] + ['\n'])

    print(top)
    print(step_str)
    print(bottom)

def install_brew_packages():
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
        print_process_step('Installation of brew packages are complete!')

def install_cask_packages():
    '''
    Reads brew-cask.txt file in child config directory to install all software applications
    '''
    with open('config/brew-cask.txt') as text_file:
        lines = text_file.readlines()

        for line in lines:
            command = 'brew cask install ' + line
            install_rc = subprocess.call(command.split())

            # Try updating if package is not up to date
            if install_rc != 0:
                command = 'brew upgrade ' + line
                upgrade_rc = subprocess.call(command.split())

                if upgrade_rc != 0:
                    print(f'Error with this package in brew.txt - {line}')

        # Use brew python over system
        subprocess.call('brew link --overwrite python'.split())
        print_process_step('Installation of brew cask packages are complete!')

def install_homebrew():
    '''
    Install homebrew if it doesn't exist in *nix environment and requires password input
    '''
    # Check if homebrew is installed already curl command
    command = 'ls /usr/local/Cellar'
    ls_rc = subprocess.call(command.split(), stdout=subprocess.DEVNULL)
    if ls_rc == 0:
        print_process_step('Homebrew is already installed!')
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
    print_process_step('Installation of homebrew is complete')

def configure_git_ssh():
    '''
    Configure git ssh key to user ssh agent
    '''
    home_dir = SETUP.dir['home']
    command = f'ssh-keygen -t rsa -b 4096 -C \"{SETUP.git["email"]}\"'
    print(command)

def configure_vim_and_bash():
    '''
    Configure vim & bash settings
    '''
    home_dir = SETUP.dir['home']

    command = 'cp .vimrc {home_dir}/.vimrc'
    subprocess.call(command.split(), cwd=home_dir)

    command = 'cp .bashrc {home_dir}/.bashrc'
    subprocess.call(command.split(), cwd=home_dir)

    # Configure vim color themes in directory
    vim_color_dir = f'{SETUP.dir["home"]}/.vim/colors'
    command = f'mkdir {vim_color_dir}'
    subprocess.call(command.split())

    command_list = []
    command_list.append('sh')
    command_list.append('-c')
    command_list.append(f'cp config/color_themes/*.vim {vim_color_dir}')
    copy_rc = subprocess.call(command_list)

    if copy_rc == 0:
        print('Vim color themes copied to ~/.vim/colors')
    else:
        raise Exception('Error copying vim color themes in config')

def install_powerline():
    '''
    Install powerline & configure it to bash & vim
    '''
    home_dir = SETUP.dir['home']
    user_config_dir = SETUP.dir['user_powerline_config']
    system_config_dir = SETUP.dir['system_powerline_config']
    git_username = SETUP.git['username']
#
    command = 'pip3 install powerline-status'
    subprocess.check_call(command.split())

    # Copy powerline system config to user config
    command = f'mkdir {home_dir}/{user_config_dir}'
    subprocess.call(command.split())
    command = f'cp -r {system_config_dir} {home_dir}/{user_config_dir}'
    subprocess.call(command.split())

    # Download & install fonts
    command = f'git clone git@github.com:{git_username}/fonts.git'
    subprocess.call(command.split(), cwd=f'{home_dir}/{user_config_dir}')
    command = '/bin/bash ./install.sh'
    subprocess.call(command.split(), cwd=f'{home_dir}/{user_config_dir}/fonts')

    # Install forked powerline-gitstatus & configure it
    command = 'pip3 install --user powerline-gitstatus'
    subprocess.check_call(command.split())

if __name__ == '__main__':
#    install_homebrew()
#    install_brew_packages()
#    install_cask_packages()
    configure_vim_and_bash()
#    configure_git_ssh()
#    install_powerline()
