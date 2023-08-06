"""
Author: Arya Mayfield
Date: June 2022
Description: A RESTful API framework for both synchronous and asynchronous applications.
"""

__title__ = 'arya-api-framework'
__project__ = "Arya's API Framework"
__author__ = 'Aryathel'
__license__ = 'MIT'
__copyright__ = '2022, Aryathel'
__version__ = '0.3.0'

# Local modules
from .async_framework import AsyncClient
from .models import Response, PaginatedResponse, BaseModel
from .sync_framework import SyncClient
from .framework import SubClient

# Define exposed objects
__all__ = [
    "AsyncClient",
    "BaseModel",
    "PaginatedResponse",
    "Response",
    "SubClient",
    "SyncClient",
]
