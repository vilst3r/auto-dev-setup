"""
Singleton object for managing the setup script
"""

# Native Modules
import copy
import getpass
import logging
import pathlib
import pprint
from subprocess import check_output, call, DEVNULL

LOGGER = logging.getLogger()


class SetupSingleton:
    """
    Singleton object for managing the setup script
    """

    __instance = None

    def _initialize_singleton(self):
        """ Initialise the singleton"""
        self.step = 1
        initialise_logger()

        home = str(pathlib.Path.home())

        self.dir = {"home": home}

        command = "python3 -m site --user-site"
        python_site = check_output(command.split()).decode("utf-8").strip()

        self.dir["python_site"] = python_site
        self.dir["powerline_config"] = f"{home}/.config/powerline"

        self.username = getpass.getuser()
        self.password = getpass.getpass()

    def __init__(self):
        """ Virtually private constructor """
        if SetupSingleton.__instance:
            raise Exception("Class already instantiated")

        self._initialize_singleton()
        SetupSingleton.__instance = self

        LOGGER.debug(f'SetupSingleton:\n {self}')

    def __str__(self):
        """
        Stringifies the singleton object except for the username & password
        """
        object_copy = copy.deepcopy(self.__dict__)
        object_copy.pop("username")
        object_copy.pop("password")
        subset_string = pprint.pformat(object_copy)
        return subset_string

    def print_process_step(self, message: str, step_has_finish: bool = False):
        """
        Prints each step of the setup in a pretty format
        """
        template = f"| {self.step}. {message} |"

        horizontal_bars = f"+{('-' * (len(template) - 2))}+"

        LOGGER.info(horizontal_bars)
        LOGGER.info(template)
        LOGGER.info(horizontal_bars)

        if step_has_finish:
            self.step += 1

    @staticmethod
    def get_instance():
        """ Static access method """
        if not SetupSingleton.__instance:
            SetupSingleton()
        return SetupSingleton.__instance


def initialise_logger():
    """
    Set up logging for writing stdout & stderr to files
    """
    LOGGER.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s - %(levelname)s - "
                                  "%(filename)s.%(funcName)s.%(lineno)d] : "
                                  "%(message)s")

    log_dir = 'logs/setup'
    command = f"mkdir -p {log_dir}"
    call(command.split(), stdout=DEVNULL)

    out_path = f"{log_dir}/out.log"
    err_path = f"{log_dir}/err.log"

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    out_handler = logging.FileHandler(f"{out_path}", "w+")
    out_handler.setLevel(logging.DEBUG)
    out_handler.setFormatter(formatter)

    err_handler = logging.FileHandler(f"{err_path}", "w+")
    err_handler.setLevel(logging.WARNING)
    err_handler.setFormatter(formatter)

    LOGGER.addHandler(out_handler)
    LOGGER.addHandler(err_handler)
    LOGGER.addHandler(stream_handler)


