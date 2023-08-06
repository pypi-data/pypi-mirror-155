"""
Author: Arya Mayfield
Date: June 2022
Description: Standalone functions created for general purpose use throughout the rest of the program.
"""

# Stdlib modules
from collections import OrderedDict
from enum import Enum
from functools import wraps
from json import JSONEncoder
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Type,
    Union,
)

# 3rd party modules
from pydantic import validate_arguments

# Local modules
from . import errors
from .constants import HTTPMethod
from .models import BaseModel

# Define exposed objects
__all__ = [
    "apiclient",
    "endpoint",
    "flatten_obj",
    "flatten_params",
    "merge_dicts",
    "validate_type",
]


# ======================
#        Typing
# ======================
MappingOrModel = Union[Dict[str, Union[str, int]], BaseModel]
HttpMapping = Dict[str, Union[str, int, List[Union[str, int]]]]
DictOrModel = Union[HttpMapping, BaseModel]


# ======================
#       Classes
# ======================
class FrameworkEncoder(JSONEncoder):
    def default(self, obj) -> Any:
        if isinstance(obj, Enum):
            return obj.name
        return JSONEncoder.default(self, obj)


# ======================
#    Type Validation
# ======================
@validate_arguments()
def validate_type(obj: Any, target: Union[Type, List[Type]], err: bool = True) -> bool:
    """Validates that a given parameter is of a type, or is one of a collection of types.

    Parameters
    ----------
    obj: Any
        A variable to validate the type of.
    target: Union[Type, List[Type]]
        A type, or list of types, to check if the :paramref:`.param` is an instance of.
    err: :py:class:`bool`
        Whether or not to throw an error if a type is not validated.

    Returns
    -------
    :py:class:`bool`
        A boolean representing whether the type was validated.
    """
    if isinstance(target, list):
        for t in target:
            if isinstance(obj, t):
                return True
            if type(obj) is t:
                return True
            if issubclass(type(obj), t):
                return True
    else:
        if isinstance(obj, target):
            return True
        if type(obj) is target:
            return True
        if issubclass(type(obj), target):
            return True

    if err:
        raise errors.ValidationError(f"{obj} is not of type {target}.")

    return False


# =======================
#   Argument Management
# =======================
@validate_arguments()
def flatten_obj(obj: Optional[DictOrModel]) -> Dict:
    """Flattens a given object into a :py:class:`dict`.

    This is mainly used for arguments where a :py:class:`dict` *or* a :class:`BaseModel` can be accepted as
    parameters.

    Arguments
    ---------
        obj: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
            The object or model to flatten into a :py:class:`dict` format.

    Returns
    -------
        :py:class:`dict`
            A mapping of :py:class:`str` keys to Any values.
    """
    return obj.dict(exclude_unset=True) if isinstance(obj, BaseModel) else obj


@validate_arguments()
def flatten_params(obj: Optional[DictOrModel]) -> Dict:
    """Flattens a given object into a :py:class:`dict`.

    This is mainly used for arguments where a :py:class:`dict` *or* a :class:`BaseModel` can be accepted as
    parameters.

    Note
    ----
        The only difference between this method and :func:`flatten_obj` is that this method reduces sub-models to be
        fields in the primary return :py:class:`dict`, rather than maintaining the model structure. For example, a model
        ``User`` with a field ``address`` of type ``Address``, which has a ``city`` field set to ``cityname`` and a
        ``zipcode`` set to ``12345``, would be flattened to ``{"address.city": "cityname", "address.zipcode": 12345}``.


    Arguments
    ---------
        obj: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
            The object or model to flatten into a :py:class:`dict` format.

    Returns
    -------
        :py:class:`dict`
            A mapping of :py:class:`str` keys to Any values.
    """
    return obj.flatten() if isinstance(obj, BaseModel) else obj


@validate_arguments()
def _to_key_val_list(obj: Optional[Dict]) -> Optional[List]:
    """Converts a given :py:class:`dict` to a key/value list.

    Arguments
    ---------
        obj: Optional[:py:class:`dict`]
            A :py:class:`dict` object to be turned into a key value list.

    Returns
    -------
        :py:class:`list`
            A collection of elements from the :paramref:`obj`, flattened into a single :py:class:`list`.

            Example
            -------
                If :paramref:`obj` is set to ``{"A":"a", "B": "b"}``, the return value will be ``["A", "a", "B", "b"]``.
    """
    if obj is None:
        return obj

    if isinstance(obj, (str, bytes, bool, int)):
        raise ValueError("Cannot encode objects that are not key-val paired.")

    if isinstance(obj, Mapping):
        obj = obj.items()

    return list(obj)


@validate_arguments()
def merge_dicts(
        base_dict: Optional[Union[Dict, BaseModel]],
        update_dict: Optional[Union[Dict, BaseModel]]
) -> Optional[Mapping]:
    """Merges the base dict with the update dict, overriding any of the base dict's values
    with the updated values from the update dict.

    Arguments
    ---------
        base_dict: Optional[:py:class:`dict`]
            The default dict to update.
        update_dict: Optional[:py:class:`dict`]
            The new dict to update the :paramref:`base_dict` from.

    Returns
    -------
        :py:class:`dict`
            A mapping of :py:class:`str` to Union[:py:class:`str`, :py:class:`int`, :py:class:`float`] containing the
            merged dictionaries.
    """
    base_dict, update_dict = flatten_obj(base_dict), flatten_obj(update_dict)

    if update_dict is None:
        return base_dict

    if base_dict is None:
        return update_dict

    if not (isinstance(base_dict, Mapping) and isinstance(update_dict, Mapping)):
        return update_dict

    merged = OrderedDict(_to_key_val_list(base_dict))
    merged.update(_to_key_val_list(update_dict))

    none_keys = [k for (k, v) in merged.items() if v is None]
    for k in none_keys:
        del merged[k]

    return merged


# ======================
#        Methods
# ======================
def _is_submodule(parent: str, child: str) -> bool:
    return parent == child or child.startswith(parent + '.')


# ======================
#      Decorators
# ======================
def apiclient(cls):
    """Decorates any :class:`SyncClient <arya_api_framework.SyncClient>`,
    :class:`AsyncClient <arya_api_framework.AsyncClient>`, or :class:`SubClient <arya_api_framework.SubClient>` to
    automatically read any methods decorated with an :deco:`endpoint` decorator. The :meth:`tree <SyncClient.tree>`
    method is then populated using this metadata.

    .. code-block:: python
        :caption: Example:

        @apiclient
        class MyClient(SyncClient, uri='https://example.com/api'):
            @endpoint(
                path='/',
                name='Get Example',
                href='https://example.com/api/docs/',
                method='GET'
            )
            def example(self):
                return self.get()

    .. code-block:: python

        >>> client = MyClient()
        >>> print(client.tree(serialize=True, indent=2))
        {
          "root": {
            "__info__": {
              "uri": "https://example.com/api",
              "uri_root": "https://example.com"
            },
            "__endpoints__": {
              "example": {
                "path": "/",
                "name": "Get Example",
                "href": "https://example.com/api/docs/",
                "methods": [
                  "GET"
                ]
              }
            },
            "__subclients__": {}
          }
        }
    """

    cls.__endpoints__ = {}
    for name, method in cls.__dict__.items():
        if hasattr(method, '__is_endpoint__'):
            cls.__endpoints__[method.__name__] = {
                "path": method.__uri_path__,
                "name": method.__endpoint_name__ or method.__name__,
                "href": method.__href__,
                "methods": method.__request_methods__
            }
    return cls


def endpoint(
        path: str,
        name: str = None,
        href: str = None,
        method: Union[HTTPMethod, str] = HTTPMethod.ANY,
        methods: Optional[List[Union[HTTPMethod, str]]] = None
) -> Callable[..., Callable[..., Any]]:
    """Attaches metadata to a request method in a :class:`SyncClient <arya_api_framework.SyncClient>`,
    :class:`AsyncClient <arya_api_framework.AsyncClient>`, or :class:`SubClient <arya_api_framework.SubClient>`.
    In order for this data to be applied to the client properly, the client must be decorated with a :deco:`apiclient`
    decorator.

    Note
    ----
        To access the metadata attached to a method with :deco:`endpoint`, use the
        :meth:`tree <arya_api_framework.SyncClient.tree>` method of any
        :class:`SyncClient <arya_api_framework.SyncClient>`, :class:`AsyncClient <arya_api_framework.AsyncClient>`,
        or :class:`SubClient <arya_api_framework.SubClient>`.

    Arguments
    ---------
        path: :py:class:`str`
            The relative path of the endpoint from the root URI of the client.
        name: Optional[:py:class:`str`]
            The name of the endpoint. If this is not provided, the function name is used.
        href: Optional[:py:class:`str`]
            A link to documentation for this endpoint. This will usually link to an API's documentation.
        method: Optional[Union[:class:`constants.HTTPMethod`, :py:class:`str`]]
            The :ref:`request method <http-requests>` that the endpoint makes use of.
        methods: Optional[List[Union[:class:`constants.HTTPMethod`, :py:class:`str`]]]
            The :ref:`request methods <http-requests>` that an endpoint can make use of.

            Note
            ----
                The endpoint should include either :paramref:`method` *or* :paramref:`methods` *or* exclude them both.
    """
    if isinstance(methods, list):
        methods = [HTTPMethod(meth) for meth in methods]
    else:
        methods = [HTTPMethod(method)]

    def callback(func: Callable[..., Any]) -> Callable[..., Any]:
        func.__is_endpoint__ = True
        func.__uri_path__ = path
        func.__endpoint_name__ = name
        func.__href__ = href
        func.__request_methods__ = methods

        return func

    return callback


def _requires_parent(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if getattr(self, 'parent') is not None:
            return func(self, *args, **kwargs)
        raise errors.SubClientNoParent(self.name)
    return wrapper
