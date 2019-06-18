'''
Module delegated to handling git logic
'''

# System/Third-Party modules
import re
import json

# Custom modules
from utils.setup_wrapper import SetupWrapper
from utils.io_helper import read_file, write_file

def read_git_credentials() -> dict:
    '''
    Read credentials from file into wrapper object from project directory
    '''
    res = {}
    valid_properties = ['username', 'email', 'token']

    buff = read_file('config/git-credentials.txt')
    for line in buff:
        key, val = line.split(':')

        if not key or not val:
            raise Exception('Git credentials are not configured properly')
        if key not in valid_properties:
            raise Exception('Git property is invalid')

        key, val = key.strip(), val.strip()
        res[key] = val
    return res

def update_ssh_config():
    home_dir = SETUP.dir['home']
    
    buff = []
    config = read_file(f'{home_dir}/.ssh/config')
    for line in config:
        key, val = line.strip().split()
        buff.append(f'{key} {val}\n')

    identity_key_exists = False
    identity_val = f'{home_dir}/.ssh/id_rsa'
    for i, line in enumerate(buff):
        key, val = line.split()

        if key == 'IdentityFile':
            identity_key_exists = True
            buff[i] = f'{key} {identity_val}'
            break

    if not identity_key_exists:
        buff.append(f'IdentityFile {identity_val}')

    write_file(f'{home_dir}/.ssh/config', buff)
