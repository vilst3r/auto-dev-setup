'''
Module delegated to handling git logic
'''

# System/Third-Party modules
import re

# Custom modules
from utils.setup_wrapper import SetupWrapper

SETUP = SetupWrapper()

def read_git_credentials() -> dict:
    '''
    Read credentials from file into wrapper object from project directory
    '''
    res = {}
    valid_properties = ['username', 'email', 'token']

    buff = None
    with open('config/git-credentials.txt') as text_file:
        buff = [line for line in text_file.readlines()]

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
    '''
    Update config file in .ssh directory
    '''
    home_dir = SETUP.dir['home']

    buff = []
    config = None

    with open(f'{home_dir}/.ssh/config') as text_file:
        config = [line for line in text_file.readlines()]

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

    with open(f'{home_dir}/.ssh/config', 'w+') as text_file:
        for line in buff:
            text_file.write(line)

def github_public_key_exists(current_key: str, public_keys: list) -> bool:
    '''
    Check if current public key passed in exists on github
    '''
    pattern = re.compile(re.escape(current_key))

    for key in public_keys:
        if re.match(pattern, key['key']):
            return True
    return False
