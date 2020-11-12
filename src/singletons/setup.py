"""
Singleton object for managing the setup script
"""

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
from utils.general import format_ansi_string
from utils.unicode import ForeGroundColor, Format, Symbols

LOGGER = logging.getLogger()


class SetupSingleton:
    """
    Singleton object for managing the setup script
    """

    __instance = None

    def _initialize_singleton(self):
        """ Initialise the singleton"""
        initialise_logger()

        self.brew_dir = '/usr/local/Caskroom'
        self.entry_point = get_entry_point()

        home = str(pathlib.Path.home())
        self.home_dir = home

        self.dotfiles_dir = f'{home}/dotfiles'
        self.emacs_dir = f'{home}/.emacs.d'

        command = 'python3 -m site --user-site'
        python_site = check_output(command.split()).decode('utf-8').strip()

        self.python_site_dir = python_site

        self.powerline_local_config_dir = f'{home}/.config/powerline'
        self.powerline_system_config_dir = f'{python_site}/' \
                                           f'powerline/config_files'

        self.ssh_dir = f'{home}/.ssh'

        if '--test' in sys.argv:
            self.log_initial_message()
            self.brew_config_file = 'config/test/brew-leaves'
            self.brew_cask_config_file = 'config/test/casks'
            self.pyp_config_file = 'config/test/pyp-leaves'
        else:
            self.log_initial_message()
            self.brew_config_file = 'config/brew/leaves'
            self.brew_cask_config_file = 'config/brew/casks'
            self.pyp_config_file = 'config/pyp-leaves'

        self.git_credentials_file = 'config/git-credentials.txt'
        self.bash_profile_file = f'{home}/.bash_profile'
        self.vimrc_file = f'{home}/.vimrc'
        self.emacs_file = f'{home}/.emacs.d/init.el'

        LOGGER.info(format_ansi_string('Ensure you\'ve configured the '
                                       'following files before proceeding: ',
                                       ForeGroundColor.LIGHT_RED))
        LOGGER.info(format_ansi_string(f'- {self.brew_config_file}',
                                       Format.BOLD))
        LOGGER.info(format_ansi_string(f'- {self.brew_cask_config_file}',
                                       Format.BOLD))
        LOGGER.info(format_ansi_string(f'- {self.git_credentials_file}\n',
                                       Format.BOLD))

        self.username = getpass.getuser()
        self.password = getpass.getpass()
        print()

    def __init__(self):
        """ Virtually private constructor """
        if SetupSingleton.__instance:
            raise Exception('Class already instantiated')

        self._initialize_singleton()
        SetupSingleton.__instance = self

        LOGGER.debug(f'SetupSingleton:\n {self}')

    def __str__(self):
        """
        Stringifies the singleton object except for the username & password
        """
        object_copy = copy.deepcopy(self.__dict__)
        object_copy.pop('username')
        object_copy.pop('password')
        subset_string = pprint.pformat(object_copy)
        return subset_string

    @staticmethod
    def get_instance():
        """ Static access method """
        if not SetupSingleton.__instance:
            SetupSingleton()
        return SetupSingleton.__instance

    def log_initial_message(self):
        """
        Logs initial message based on the entry point of the program or the
        flag passed in
        """
        if self.entry_point == 'clean':
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
