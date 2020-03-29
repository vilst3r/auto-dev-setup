"""
Module holding all decorators for use
"""

# Native Modules
import logging
from time import time
from typing import Callable

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
        LOGGER.info(f"{wrapped_function.__name__}() execution time:"
                    f" {time_elapsed} seconds")
    return decorator


def print_process_step(step_no: int, begin_message: str,
                       end_message: str) -> Callable:
    def log_message(message: str):
        """
        Prints each step of the installation process in a pretty format
        """
        template = f"| {step_no}. {message} |"

        horizontal_bars = f"+{('-' * (len(template) - 2))}+"

        LOGGER.info(horizontal_bars)
        LOGGER.info(template)
        LOGGER.info(horizontal_bars)

    def decorator(wrapped_function: Callable):
        def wrapper(*args, **kwargs):
            log_message(begin_message)
            wrapped_function(*args, **kwargs)
            log_message(end_message)
        return wrapper
    return decorator
