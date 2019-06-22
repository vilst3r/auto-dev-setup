'''
Wrapper object for setup script
'''

# System/Third-Party modules
from subprocess import check_output
import pathlib
import pprint

class SetupWrapper():
    '''
    Wrapper object to track state of setup
    '''
    def __init__(self):
        self.step = 0

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
