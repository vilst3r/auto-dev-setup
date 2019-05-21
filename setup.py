#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

import subprocess

def process_realtime_output(process: subprocess.Popen) -> int:
    '''
    Output child stdout in root process call
    '''
    if not process:
        return 1

    while True:
        output = process.stdout.readline()

        if output:
            print(output.strip().decode('utf-8'))
        else:
            break
    return_code = process.poll()
    return return_code

#def config_vim() -> int:
#    return

def install_homebrew() -> int:
    '''
    Install homebrew if it doesn't exist in *nix environment
    '''

    command = '/usr/bin/ruby -e'.split()
    command.append("$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)")
    print(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return process_realtime_output(process)

def install_git() -> int:
    '''
    Install git if it doesn't exist in *nix environment
    '''

    command = 'brew install git'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return process_realtime_output(process)

def initialise_git_keychain() -> int:
    '''
    Initialise keychain for git in usr level
    '''
    return

def install_iterm2() -> int:
    '''
    Install iterm2 through cask
    '''

    command = 'brew cask install iterm2'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process_realtime_output(process)

def install_vim_configs() -> int:
    '''
    Configure vim settings including allocated theme
    '''

    # Check if credentials are configured
    with open('config/git-credentials.txt') as text_file:
        lines = text_file.readlines().split(':')
        print(lines)
    return

if __name__ == '__main__':
    install_vim_configs()
#    if install_git() != 0:
#        raise Exception('Failed to install git')
#    if install_homebrew() != 0:
#       raise Exception('Failed to install homebrew')
#    if install_iterm2() != 0:
#       raise Exception('Failed to install iterm2')
