'''
Wrapper object for setup script
'''

# System/Third-Party modules
from subprocess import check_output
import logging
import pathlib
import pprint

LOGGER = logging.getLogger()

class SetupWrapper():
    '''
    Wrapper object to track state of setup
    '''
    def __init__(self):
        self.step = 1

        home = str(pathlib.Path.home())

        self.dir = {}
        self.dir['home'] = home

        command = 'python3 -m site --user-site'
        python_site = check_output(command.split()).decode('utf-8').strip()

        self.dir['python_site'] = python_site
        self.dir['powerline_config'] = f'{home}/.config/powerline'

    def __str__(self):
        str_vals = {**self.dir, 'step': self.step}
        pretty_str = pprint.pformat(str_vals)
        return pretty_str

    def print_process_step_start(self, message: str):
        '''
        Prints each step of the setup in a pretty format
        '''
        step_str = f'| {self.step}. {message} |'
        row_len = len(step_str)

        top = ''.join(['-' for _ in range(row_len)])
        bottom = ''.join(['-' for _ in range(row_len)])

        LOGGER.info(f'{top}')
        LOGGER.info(step_str)
        LOGGER.info(f'{bottom}')

    def print_process_step_finish(self, message: str):
        '''
        Prints each step of the setup in a pretty format
        '''
        step_str = f'| {self.step}. {message} |'
        row_len = len(step_str)

        top = ''.join(['-' for _ in range(row_len)])
        bottom = ''.join(['-' for _ in range(row_len)])

        LOGGER.info(f'{top}')
        LOGGER.info(step_str)
        LOGGER.info(f'{bottom}')

        self.step += 1

# Singleton
SETUP = SetupWrapper()
