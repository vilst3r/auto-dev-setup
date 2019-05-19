#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

import subprocess

def install_homebrew() -> int:
    command = '/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        output = process.stdout.readline()

        if output:
            print(output.strip().decode('utf-8'))
        else:
            break
    rc = process.poll()
    return rc

def install_iterm2() -> int:
    command = 'brew cask install iterm2'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        output = process.stdout.readline()

        if output:
            print(output.strip().decode('utf-8'))
        else:
            break
    rc = process.poll()
    return rc

if __name__ == '__main__':
    #if install_homebrew() != 0:
    #   raise Exception('Failed to install homebrew')
    if install_iterm2() != 0:
       raise Exception('Failed to install iterm2')

