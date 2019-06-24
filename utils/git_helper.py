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
        key, val = key.strip(), val.strip()

        if not key or not val:
            raise Exception('Git credentials are not configured properly')
        if key not in valid_properties:
            raise Exception('Git property is invalid')

        res[key] = val
    return res

def update_ssh_config():
    '''
    Update config file in .ssh directory
    '''
    home_dir = SETUP.dir['home']
    ssh_config = f'{home_dir}/.ssh/config'

    buff = []
    config = None

    with open(ssh_config) as text_file:
        config = [line for line in text_file.readlines()]

    content = ''.join(config)

    pattern = re.compile(r'IdentityFile .*')
    key_match = re.search(pattern, content)

    identity_val = f'IdentityFile {home_dir}/.ssh/id_rsa'

    if not key_match:
        with open(ssh_config, 'a') as text_file:
            text_file.write(identity_val)
        print('IdentityFile key value appended to ssh config file')
        return

    start, end = key_match.span()
    current_config = content[start:end]

    if current_config == identity_val:
        print('IdentityFile key value already configured in ssh config file')
        return

    content = content[:start] + identity_val + content[end:]
    with open(ssh_config, 'w') as text_file:
        text_file.write(content)

    print('IdentityFile key value updated in ssh config file')

def github_public_key_exists(current_key: str, public_keys: list) -> bool:
    '''
    Check if current public key passed in exists on github
    '''
    pattern = re.compile(re.escape(current_key))

    for key in public_keys:
        if re.match(pattern, key['key']):
            return True
    return False
