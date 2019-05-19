#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

import subprocess

def install_iterm2():
    command = 'ls -la'
    output = subprocess.check_output(command.split()).decode('utf-8')
    print(output)

if __name__ == '__main__':
    install_iterm2()
    print('hello')

