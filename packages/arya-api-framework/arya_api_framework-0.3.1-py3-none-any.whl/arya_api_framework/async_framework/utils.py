"""
Author: Arya Mayfield
Date: June 2022
Description: Utility functions for general use within the async branch.
"""

# Stdlib modules
from collections import OrderedDict
from pathlib import Path
from typing import (
    AsyncIterator,
    Dict,
    List,
    Mapping,
    Optional,
    Union,
)

# Local modules
from ..errors import AsyncClientError

# Async modules
is_async: bool
try:
    import aiofiles

    is_async = True
except ImportError:
    is_async = False

# Define exposed objects
__all__ = [
    'chunk_file_reader',
]


# ======================
#       Methods
# ======================
async def chunk_file_reader(file: Union[str, Path]) -> AsyncIterator[bytes]:
    """|coro|

    Reads a file from a path in chunks, to allow to large file uploads.

    Arguments
    ---------
        file: Union[:py:class:`str`, :py:class:`pathlib.Path`]
            The filepath to read from.

    Returns
    -------
        AsyncGenerator[:py:class:`bytes`]
            The bytes read from the file, in chunked increments.
    """

    if not is_async:
        raise AsyncClientError("The async context is unavailable. Try installing with `python -m pip install arya-api-framework[async]`.")

    async with aiofiles.open(file, 'rb') as f:
        chunk = await f.read(64 * 1024)

        while chunk:
            yield chunk
            chunk = await f.read(64 * 1024)
