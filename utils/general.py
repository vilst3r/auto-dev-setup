"""
Module holding helper methods for functional tasks
"""

# Native Modules
import collections
import random
import string
from itertools import islice
from typing import Iterable, Union, Callable

# Custom Modules
from utils.unicode import Symbols, Format, ForeGroundColor, BackgroundColor


def partition(predicate: Callable, iterable: Iterable[any]) -> tuple:
    """
    Partition a iterable into two lists, representing true & false values
    respectively, the iterable is partitioned by the predicate function
    passed in
    """
    true_values = []
    false_values = []

    for item in iterable:
        if predicate(item):
            true_values.append(item)
        else:
            false_values.append(item)
    return true_values, false_values


def consume(iterator: Iterable[any], n: int = None) -> None:
    """
    Fastest pythonic implementation of consuming iterables
        - 'Advance the iterator n-steps ahead. If n is None, consume entirely.'
    """
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


def random_string(n: int = 8) -> str:
    """
    Generate random string of length n
    """

    latin_letters = string.ascii_letters
    return ''.join(random.choice(latin_letters) for i in range(n))


def format_ansi_string(message: str,
                       *formats: Union[Symbols, Format, ForeGroundColor,
                                       BackgroundColor]) -> str:
    """
    Return ANSI formatted string with the following properties passed in from
    unicode.py. (Exclude Format.RESET if passed in)
    """
    valid_formats = filter(lambda x: x is not Format.RESET, formats)
    starting_format = ''.join(map(lambda x: x.value, valid_formats))

    return f'{starting_format}{message}{Format.RESET.value}'


def get_green_check() -> str:
    """
    Returns a ANSI formatted string representing a green tick
    """
    return format_ansi_string(f'{Symbols.TICK.value}', ForeGroundColor.GREEN)


def get_red_cross() -> str:
    """
    Returns a ANSI formatted string representing a red cross
    """
    return format_ansi_string(f'{Symbols.CROSS.value}', ForeGroundColor.RED)


def get_green_right_arrow() -> str:
    """
    Returns a ANSI formatted string representing a arrow
    """
    return format_ansi_string(f'{Symbols.RIGHT_ARROW.value}',
                              ForeGroundColor.GREEN)
