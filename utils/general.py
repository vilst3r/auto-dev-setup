"""
Module holding helper methods for functional tasks
"""

# Native Modules
import collections
from itertools import islice
from typing import Iterable
import random
import string


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




