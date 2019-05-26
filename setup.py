#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

import subprocess
import pathlib

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

def install_homebrew_packages():
    '''
    Reads brew.txt file in child config directory to install all brew packages
    '''
    
    with open('config/brew.txt') as text_file:
        lines = text_file.readlines()
        
        for line in lines:
            command = 'brew install ' + line
            with subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
                process_realtime_output(process)
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

   return process_realtime_output(process)

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

def install_powerline_status():
    '''
    Install powerline through git interface
    '''
    
    command = 'pip3 install powerline-status'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process_realtime_output(process)

def install_powerline_fonts():
    '''
    Install powerline through git interface
    '''
    home_dir = str(pathlib.Path.home())
    
    command = 'git clone git@github.com:vilst3r/fonts.git ' + home_dir + '/.config/powerline/fonts'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process_realtime_output(process)

def install_powerline_gitstatus():
    '''
    Install powerline through git interface
    '''
    command = 'pip3 install --user powerline-gitstatus'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process_realtime_output(process)

if __name__ == '__main__':
    install_homebrew_packages()
#    install_powerline_status()
#    install_powerline_fonts()
#    install_powerline_gitstatus()
#    install_vim_configs()
#    install_homebrew()
