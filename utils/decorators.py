"""
Module holding all decorators for use
"""

# Native Modules
import logging
from time import time
from typing import Callable

LOGGER = logging.getLogger()


def measure_time(wrapped_function: Callable) -> None:
    """
    Times how long the method takes to complete in seconds

    :param wrapped_function: function to record the time elapsed
    :return: None
    """
    start_time = time()
    wrapped_function()
    finish_time = time()

    time_elapsed = finish_time - start_time
    LOGGER.info(f"{wrapped_function.__name__}() execution time:"
                f" {time_elapsed} seconds")
