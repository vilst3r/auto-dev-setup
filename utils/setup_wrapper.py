'''
Wrapper object for setup script
'''

# System/Third-Party modules
import pathlib
import pprint

# Custom modules
from utils.io_helper import *

class SetupWrapper():
    '''
    Wrapper object to track state of counter
    '''
    def __init__(self):
        self.step = 0
        self.git = read_git_credentials()

        python = '/usr/local/lib/python3.7'
        home = str(pathlib.Path.home())

        self.dir = {}
        self.dir['home'] = home
        self.dir['user_powerline_config'] = f'{home}/.config/powerline'
        self.dir['system_powerline_config'] = f'{python}/site-packages/powerline/config_files'

    def __str__(self):
        str_vals = {**self.git, **self.dir, 'step': self.step}
        pretty_str = pprint.pformat(str_vals)
        return pretty_str

    def print_process_step(self, message: str):
        '''
        Prints each step of the setup in a pretty format
        '''
        self.step += 1
        step_str = f'| {self.step}. {message} |'
        row_len = len(step_str)

        top = ''.join(['-' for _ in range(row_len)])
        bottom = ''.join(['-' for _ in range(row_len)])

        print()
        print(top)
        print(step_str)
        print(bottom)
        print()

def read_git_credentials() -> dict:
    '''
    Read credentials from file into wrapper object from project directory
    '''
    res = {}

    buff = read_file('config/git-credentials.txt')
    for line in buff:
        key, val = line.split(':')

        if not key or not val:
            raise Exception('Git credentials are not configured properly')

        key, val = key.strip(), val.strip()
        res[key] = val
    return res
