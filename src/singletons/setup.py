"""
Singleton object for managing the setup script
"""

import collections
# Native Modules
import copy
import getpass
import logging
import pathlib
import pprint
import re
import sys
import traceback
from subprocess import DEVNULL, call, check_output

# Custom Modules
from utils.general import format_ansi_string, random_string
from utils.unicode import ForeGroundColor, Format, Symbols

LOGGER = logging.getLogger()

Directories = collections.namedtuple("Directories", ['home', 'brew', 'dotfiles',
                                                     'emacs', 'python_site',
                                                     'powerline', 'ssh'])

Files = collections.namedtuple('Files', ['brew', 'cask', 'pip', 'git', 'bash',
                                         'vim', 'emacs'])


class SetupSingleton:
    """
    Singleton object for managing the setup script
    """

    __instance = None

    def __init__(self):
        """ Virtually private constructor """
        if SetupSingleton.__instance:
            raise Exception('Class already instantiated')

        initialise_logger()

        self.username = getpass.getuser()
        self.ssh_passphrase = random_string(8)
        self.entry_point = get_entry_point()
        self.directories: Directories = retrieve_directories()
        self.files: Files = retrieve_files(
            self.directories.home, self.entry_point)

        LOGGER.info(format_ansi_string('Ensure you\'ve configured the '
                                       'following files before proceeding: ',
                                       ForeGroundColor.LIGHT_RED))
        LOGGER.info(format_ansi_string(
            f'- {self.files.brew} (optional)', Format.BOLD))
        LOGGER.info(format_ansi_string(
            f'- {self.files.cask} (optional)', Format.BOLD))
        LOGGER.info(format_ansi_string(
            f'- {self.files.pip} (optional)', Format.BOLD))
        LOGGER.info(format_ansi_string(f'- {self.files.git}\n', Format.BOLD))

        print()

        SetupSingleton.__instance = self

        LOGGER.debug(f'SetupSingleton:\n {self}')

    def __str__(self) -> str:
        """
        Stringifies the singleton object
        """
        object_copy = copy.deepcopy(self.__dict__)
        object_copy.pop('directories')
        object_copy.pop('files')
        object_copy['directories'] = self.directories._asdict()
        object_copy['files'] = self.files._asdict()
        return pprint.pformat(object_copy)

    @staticmethod
    def get_instance():
        """ Static access method """
        if not SetupSingleton.__instance:
            SetupSingleton()
        return SetupSingleton.__instance


def get_entry_point() -> str:
    """
    Determines the entry point of the python program based on the filename
    executed. There can only be two candidate values based on the project:
        - "run"
        - "rollback"
    """
    first_stack_message = traceback.format_stack()[0]

    pattern = re.compile(r'File ".*"')
    match_object = re.search(pattern, first_stack_message).group(0)

    # Expected match template -> "**/**/<file>.py"
    file = match_object.split()[1].replace('\"', '')
    file = file.split('/')[-1]
    file = file.split('.')[0]
    return file.lower()


def initialise_logger():
    """
    Set up logging for writing stdout & stderr to files based on the
    filename executed
    """
    LOGGER.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s - %(levelname)s - "
                                  "%(filename)s.%(funcName)s.%(lineno)d] : "
                                  "%(message)s")

    log_dir = f'logs/{get_entry_point()}'

    command = f'mkdir -p {log_dir}'
    call(command.split(), stdout=DEVNULL)

    out_path = f'{log_dir}/out.log'
    err_path = f'{log_dir}/err.log'

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    out_handler = logging.FileHandler(f'{out_path}', 'w+')
    out_handler.setLevel(logging.DEBUG)
    out_handler.setFormatter(formatter)

    err_handler = logging.FileHandler(f'{err_path}', 'w+')
    err_handler.setLevel(logging.WARNING)
    err_handler.setFormatter(formatter)

    LOGGER.addHandler(out_handler)
    LOGGER.addHandler(err_handler)
    LOGGER.addHandler(stream_handler)


def log_initial_message(entry_point):
    """
    Logs initial message based on the entry point of the program or the
    flag passed in
    """
    if entry_point == 'clean':
        LOGGER.info(format_ansi_string(' Executing cleanup against '
                                       'the development environment...\n',
                                       ForeGroundColor.LIGHT_RED,
                                       Symbols.RIGHT_ARROW,
                                       Format.BOLD, Format.UNDERLINE))
        return

    if '--test' in sys.argv:
        LOGGER.info(format_ansi_string(' Executing with minimal non-user '
                                       'configurations for testing...\n',
                                       ForeGroundColor.LIGHT_RED,
                                       Symbols.RIGHT_ARROW,
                                       Format.BOLD, Format.UNDERLINE))
    else:
        LOGGER.info(format_ansi_string(' Executing with your user '
                                       'configurations for your setup...'
                                       '\n', ForeGroundColor.LIGHT_RED,
                                       Symbols.RIGHT_ARROW, Format.BOLD,
                                       Format.UNDERLINE))


def retrieve_directories() -> Directories:
    """
    Retrieves directories required for setup
    """
    home = str(pathlib.Path.home())
    brew = '/usr/local/Caskroom'
    dotfiles = f'{home}/dotfiles'
    emacs = f'{home}/.emacs.d'

    command = 'python3 -m site --user-site'
    python_site = check_output(command.split()).decode('utf-8').strip()

    powerline = f'{home}/.config/powerline'
    ssh = f'{home}/.ssh'

    return Directories(home, brew, dotfiles, emacs, python_site, powerline, ssh)


def retrieve_files(home: str, entry_point: str) -> Files:
    """
    Retrieves files required for setup
    """
    log_initial_message(entry_point)

    if '--test' in sys.argv:
        brew = 'config/brew/leaves-test'
        cask = 'config/brew/casks-test'
        pip = 'config/pip/leaves-test'
    else:
        brew = 'config/brew/leaves'
        cask = 'config/brew/casks'
        pip = 'config/pip/leaves'

    git = 'config/git-credentials.txt'
    bash = f'{home}/.bash_profile'
    vim = f'{home}/.vimrc'
    emacs = f'{home}/.emacs.d/init.el'

    return Files(brew, cask, pip, git, bash, vim, emacs)
