"""
Author: Arya Mayfield
Date: June 2022
Description: Utility functions for general use within the sync branch.
"""

# Stdlib modules
from typing import (
    Generator,
    Union,
)
from functools import wraps
import time
import logging
from pathlib import Path

# 3rd party modules
from pydantic import validate_arguments

# Sync modules
try:
    from ratelimit import RateLimitException
except ImportError:
    pass

# Define exposed objects
__all__ = [
    "chunk_file_reader",
    "sleep_and_retry",
]

# ======================
#     Logging Setup
# ======================
_log = logging.getLogger('arya_api_framework.Sync')


# ======================
#       Methods
# ======================
@validate_arguments
def chunk_file_reader(file: Union[str, Path]) -> Generator[bytes, None, None]:
    """Reads a file from a path in chunks, to allow to large file uploads.

    Arguments
    ---------
        file: Union[:py:class:`str`, :py:class:`pathlib.Path`]
            The filepath to read from.

    Returns
    -------
        Generator[:py:class:`bytes`]
            The bytes read from the file, in chunked increments.
    """
    with open(file, 'rb') as f:
        chunk = f.read(64 * 1024)

        while chunk:
            yield chunk
            chunk = f.read(64 * 1024)


# ======================
#      Decorators
# ======================
def sleep_and_retry(func):
    """|deco|

    This decorator wraps a :resource:`ratelimited <ratelimit>` function, causing it to sleep until the rate limit resets,
    then reruns the failed function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except RateLimitException as exception:
                _log.info(f"Applying rate limit: Sleeping for {exception.period_remaining}s")
                time.sleep(exception.period_remaining)
    return wrapper
