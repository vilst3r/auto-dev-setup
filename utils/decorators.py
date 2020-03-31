"""
Module holding all decorators for use
"""

# Native Modules
import logging
from time import time
from typing import Callable

# Custom Modules
from utils.unicode import *
from utils.general import format_ansi_string, get_green_check, get_green_right_arrow

LOGGER = logging.getLogger()


def measure_time(wrapped_function: Callable) -> Callable:
    """
    Times how long the method takes to complete in seconds

    :param wrapped_function: function to record the time elapsed
    :return: decorator function wrapped over the one passed in
    """
    def decorator(*args, **kwargs):
        start_time = time()
        wrapped_function(*args, **kwargs)
        finish_time = time()

        time_elapsed = finish_time - start_time
        message = f'{wrapped_function.__name__}() execution time: ' \
                  f'{time_elapsed} seconds'

        LOGGER.info(format_ansi_string(message, ForeGroundColor.LIGHT_RED,
                                       Format.UNDERLINE, Format.BOLD))
    return decorator


def print_process_step(step_no: int, begin_message: str,
                       end_message: str) -> Callable:
    def format_template(message: str):
        """
        Prints each step of the installation process in a pretty format
        """
        return format_ansi_string(message, ForeGroundColor.LIGHT_BLUE,
                                  Format.UNDERLINE, Format.BOLD)

    def decorator(wrapped_function: Callable):
        def wrapper(*args, **kwargs):
            begin_string = format_template(f'{step_no}. {begin_message}')
            LOGGER.info(f'{begin_string} {get_green_right_arrow()}')

            wrapped_function(*args, **kwargs)

            final_string = format_template(f'{step_no}. {end_message}')
            LOGGER.info(f'{final_string} {get_green_check()}')

            # Add empty line in between steps in stdout
            print()
        return wrapper
    return decorator
