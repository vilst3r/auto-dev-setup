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
from subprocess import check_output, call, DEVNULL

# Custom Modules
from utils.general import format_ansi_string
from utils.unicode import *

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

        home = str(pathlib.Path.home())
        self.home_dir = home

        self.dotfiles_dir = f'{home}/dotfiles'

        command = 'python3 -m site --user-site'
        python_site = check_output(
            command.split()).decode('utf-8').strip()
        self.python_site_dir = python_site

        self.powerline_local_config_dir = f'{home}/.config/powerline'
        self.powerline_system_config_dir = f'{python_site}/' \
                                           f'powerline/config_files'

        self.ssh_dir = f'{home}/.ssh'
        self.vim_color_dir = f'{home}/.vim/colors'

        if '--test' in sys.argv:
            LOGGER.info(format_ansi_string(' Executing with minimal non-user '
                                           'configurations for testing...\n',
                                           ForeGroundColor.LIGHT_RED,
                                           Symbols.RIGHT_ARROW,
                                           Format.BOLD, Format.UNDERLINE))
            self.brew_config_file = 'config/brew/test-brew.txt'
            self.brew_cask_config_file = 'config/brew/test-brew-cask.txt'
        else:
            LOGGER.info(format_ansi_string(' Executing with your user '
                                           'configurations for your setup...\n',
                                           ForeGroundColor.LIGHT_RED,
                                           Symbols.RIGHT_ARROW,
                                           Format.BOLD, Format.UNDERLINE))
            self.brew_config_file = 'config/brew/brew.txt'
            self.brew_cask_config_file = 'config/brew/brew-cask.txt'

        self.git_credentials_file = 'config/git-credentials.txt'
        self.bash_profile_file = f'{home}/.bash_profile'
        self.vimrc_file = f'{home}/.vimrc'

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


def initialise_logger():
    """
    Set up logging for writing stdout & stderr to files based on the
    filename executed
    """
    def determine_log_output() -> str:
        """
        Determines where to log the output by reading the first stack frame
        :return: root file that executed the containing process
        """
        first_stack_message = traceback.format_stack()[0]

        pattern = re.compile(r'File ".*"')
        match_object = re.search(pattern, first_stack_message).group(0)

        # Expected match template -> "**/**/<file>.py"
        file = match_object.split()[1].replace('\"', '')
        file = file.split('/')[-1]
        file = file.split('.')[0]

        return f'logs/{file.lower()}'

    LOGGER.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s - %(levelname)s - "
                                  "%(filename)s.%(funcName)s.%(lineno)d] : "
                                  "%(message)s")

    log_dir = determine_log_output()

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
