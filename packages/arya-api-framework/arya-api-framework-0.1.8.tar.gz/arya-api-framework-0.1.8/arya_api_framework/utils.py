"""
Author: Arya Mayfield
Date: June 2022
Description: Standalone functions created for general purpose use throughout the rest of the program.
"""

# Stdlib modules
from collections import OrderedDict
from typing import (
    Any,
    Dict,
    List,
    Mapping,
    Optional,
    Type,
    Union,
)

# 3rd party modules
from pydantic import validate_arguments, BaseModel

# Local modules
from .errors import ValidationError

# Define exposed objects
__all__ = [
    "flatten_obj",
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
        raise ValidationError(f"{obj} is not of type {target}.")

    return False


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
