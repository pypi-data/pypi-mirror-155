"""
Author: Arya Mayfield
Date: June 2022
Description: Models used for the main structure of the module.
"""

# Stdlib modules
import abc
from datetime import datetime
from pathlib import Path
from typing import (
    AbstractSet,
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Set,
    Type,
    Union,
)

# 3rd party modules
from pydantic import (
    BaseModel as PydBaseModel,
    PrivateAttr,
    Protocol,
)
from pydantic.schema import default_ref_template


__all__ = [
    'BaseModel',
    'Response',
    'PaginatedResponse'
]

# ======================
#       Typing
# ======================
StrBytes = Union[str, bytes]
IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]
DictStrAny = Dict[str, Any]

MappingOrModel = Union[Dict[str, Union[str, int]], PydBaseModel]
HttpMapping = Dict[str, Union[str, int, List[Union[str, int]]]]
Parameters = Union[HttpMapping, PydBaseModel]
Cookies = MappingOrModel
Headers = MappingOrModel
Body = Union[Dict[str, Any], PydBaseModel]
ErrorResponses = Dict[int, Type[PydBaseModel]]


# ======================
#     Basic Model
# ======================
# This only exists for the purpose of documentation
# since the Pydantic docs are not compatible with Sphinx.
# The implementation here is merely a wrapper for the Pydantic
# implementation, nothing more.
# ======================
class BaseModel(PydBaseModel):
    """
    .. external_inherits_from::
        :objtype: class
        :root: pydantic
        :path: usage/models/#basic-model-usage

        pydantic.BaseModel

    These models include data validation on the attributes given to them, and allow for very
    direct control over response formats. Additionally, they allow to easily creating database-like
    structures, and outputting the data ina variety of formats.

    Attributes
    ----------
        __fields_set__: :py:class:`set`

            .. external_inherits_from:
                :objtype: attribute
                :root: pydantic
                :link: usage/models/#model-properties

                pydantic.BaseModel.__fields_set__

            A :py:class:`set` of names of fields which were set when the model was initialized.
        __fields__: :py:class:`dict`

            .. external_inherits_from:
                :objtype: attribute
                :root: pydantic
                :link: usage/models/#model-properties

                pydantic.BaseModel.__fields__

            A :py:class:`dict` of the model's fields.
        __config__: :pydantic:`pydantic.BaseConfig <usage/model_config/>`

            .. external_inherits_from:
                :objtype: attribute
                :root: pydantic
                :link: usage/models/#model-properties

                pydantic.BaseModel.__config__

            The configuration class for the model.

            Tip
            ----
                See :pydantic:`this example <>` for information on how to create the model config.
    """

    def dict(
            self,
            *,
            include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
            exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
            by_alias: bool = False,
            skip_defaults: bool = None,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
    ) -> DictStrAny:
        """
        .. external_inherits_from::
            :objtype: method
            :root: pydantic
            :path: usage/exporting_models/#modeldict

            pydantic.BaseModel.dict

        Generate a :py:class:`dict` representation of the model, optionally specifying
        which fields to include or exclude. Look to the
        :pydantic:`pydantic documentation<usage/exporting_models/#modeldict>` for further details.

        Keyword Args
        ------------
            include: Optional[Union[Set[:py:class:`str`]], :py:class:`dict`]]
                Fields to include in the returned dictionary. See this
                :pydantic:`example <usage/exporting_models/#advanced-include-and-exclude>`.
            exclude: Optional[Union[Set[:py:class:`str`]], :py:class:`dict`]]
                Fields to exclude from the returned dictionary. See this
                :pydantic:`example <usage/exporting_models/#advanced-include-and-exclude>`.
            by_alias: Optional[:py:class:`bool`]
                Whether field aliases should be used as keys in the resulting dictionary.
                Defaults to ``False``
            exclude_unset: Optional[:py:class:`bool`]
                Whether or not fields that were not specifically set upon creation of the model
                should be included in the dictionary. Defaults to ``False``.

                Warning
                -------
                    This was previously referred to as ``skip_defaults``. This parameter is still accepted,
                    but has been deprecated and is not recommended.

            exclude_defaults: Optional[:py:class:`bool`]
                Whether or not to include fields that are set to their default values. Even if a field is given a
                value when the model is instanced, if that value is equivalent to the default, it will not be included.
                Defaults to ``False``.
            exclude_none: Optional[:py:class:`bool`]
                Whether of not to include fields which are equal to ``None``. Defaults to ``False``.

        Returns
        -------
            :py:class:`dict`
                A mapping of :py:class:`str` field names to their values.
        """
        return super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none
        )

    def json(
        self,
        *,
        include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        encoder: Optional[Callable[[Any], Any]] = None,
        models_as_dict: bool = True,
        **dumps_kwargs: Any,
    ) -> str:
        """
        .. external_inherits_from::
            :objtype: method
            :root: pydantic
            :path: usage/exporting_models/#modeljson

            pydantic.BaseModel.json

        Serializes the model to a JSON string. Typically will call :meth:`dict` and then
        serialize the result. As such, the parameters are very similar, except for a few extra
        options.

        Tip
        ----
            You can set the :paramref:`models_as_dict` option to ``False`` to implement custom serialization for a
            model. See this :pydantic:`example <usage/exporting_models/#serialising-self-reference-or-other-models>`
            for more info.

        Tip
        ----
            It is possible to implement custom encoders for specific types within an individual model.
            This is helpful to avoid having to create an entire encoder for the :paramref:`encoder` argument.
            See this :pydantic:`example <usage/exporting_models/#serialising-self-reference-or-other-models>`
            for more info.

        Keyword Args
        ------------
            include: Optional[Union[Set[:py:class:`str`]], :py:class:`dict`]]
                Fields to include in the returned dictionary. See this
                :pydantic:`example <usage/exporting_models/#advanced-include-and-exclude>`.
            exclude: Optional[Union[Set[:py:class:`str`]], :py:class:`dict`]]
                Fields to exclude from the returned dictionary. See this
                :pydantic:`example <usage/exporting_models/#advanced-include-and-exclude>`.
            by_alias: Optional[:py:class:`bool`]
                Whether field aliases should be used as keys in the resulting dictionary.
                Defaults to ``False``
            exclude_unset: Optional[:py:class:`bool`]
                Whether or not fields that were not specifically set upon creation of the model
                should be included in the dictionary. Defaults to ``False``.

                Warning
                -------
                    This was previously referred to as ``skip_defaults``. This parameter is still accepted,
                    but has been deprecated and is not recommended.

            exclude_defaults: Optional[:py:class:`bool`]
                Whether or not to include fields that are set to their default values. Even if a field is given a
                value when the model is instanced, if that value is equivalent to the default, it will not be included.
                Defaults to ``False``.
            exclude_none: Optional[:py:class:`bool`]
                Whether of not to include fields which are equal to ``None``. Defaults to ``False``.
            encoder: Optional[Callable[Any, Any]]
                A custom encoder function that is given to :py:func:`json.dumps`. By default, a custom
                :resource:`pydantic <pydantic>` encoder is used, which can serialize many common types
                that the default :py:mod:`json` cannot normally handle, like a :py:class:`datetime <datetime.datetime>`.

            models_as_dict: Optional[:py:class:`bool`]
                Whether or not to serialize other models that are contained within the fields of the target model
                to json. This defaults to ``True``.

            **dumps_kwargs:
                Any extra keyword arguments are passed to :py:func:`json.dumps` directly, such as
                the ``indent`` argument, which will pretty-print the resulting :py:class:`str`,
                using indentations of ``indent`` spaces.

        Returns
        -------
            :py:class:`str`
                A JSON serialized string.
        """
        return super().json(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            encoder=encoder,
            models_as_dict=models_as_dict,
            **dumps_kwargs
        )

    def copy(
        self: PydBaseModel,
        *,
        include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        update: DictStrAny = None,
        deep: bool = False,
    ) -> PydBaseModel:
        """
        .. external_inherits_from::
            :objtype: method
            :root: pydantic
            :path: usage/exporting_models/#modelcopy

            pydantic.BaseModel.copy

        Returns a duplicate of the model. This is very handy for use with immutable models.

        Keyword Args
        ------------
            include: Optional[Union[Set[:py:class:`str`]], :py:class:`dict`]]
                Fields to include in the returned dictionary. See this
                :pydantic:`example <usage/exporting_models/#advanced-include-and-exclude>`.
            exclude: Optional[Union[Set[:py:class:`str`]], :py:class:`dict`]]
                Fields to exclude from the returned dictionary. See this
                :pydantic:`example <usage/exporting_models/#advanced-include-and-exclude>`.
            update: Optional[:py:class:`dict`]
                A dictionary of values to update when creating the copied model. Very similar in
                concept to :py:meth:`dict.update`.
            deep: Optional[:py:class:`bool`]
                Whether to make a deep copy of the object, or a shallow copy. Defaults to ``False``.

        Returns
        -------
            :class:`BaseModel`
                A copied instance of the model.
        """

        return super().copy(
            include=include,
            exclude=exclude,
            update=update,
            deep=deep
        )

    @classmethod
    def parse_obj(cls: Type[PydBaseModel], obj: Any) -> PydBaseModel:
        """
        .. external_inherits_from::
            :objtype: classmethod
            :root: pydantic
            :path: usage/models/#helper-functions

            pydantic.BaseModel.parse_obj

        Instantiates a model from a given :py:class:`dict`.

        Arguments
        ---------
            obj: Any
                The data to instantiate the class from. This should either be a :py:class:`dict` or an object
                that can be cast as one using ``dict(obj)``.

        Raises
        ------
            ``pydantic.ValidationError``
                Raised if the :paramref:`obj` parameter is not :py:class:`dict` and cannot be made into one.

        Returns
        -------
            :class:`BaseModel`
                An instantiated model from the :paramref:`obj` provided.
        """
        return super().parse_obj(obj=obj)

    @classmethod
    def parse_raw(
        cls: Type[PydBaseModel],
        b: StrBytes,
        *,
        content_type: str = None,
        encoding: str = 'utf8',
        proto: Protocol = None,
        allow_pickle: bool = False,
    ) -> PydBaseModel:
        """
        .. external_inherits_from::
            :objtype: classmethod
            :root: pydantic
            :path: usage/models/#helper-functions

            pydantic.BaseModel.parse_raw

        Takes a :py:class:`str` or :py:class:`bytes` and parses it to a JSON structure, then passes that to
        :meth:`parse_obj` to load it into the model. This can also handle loading :py:mod:`pickle` data directly
        via the :paramref:`content_type` argument.

        Arguments
        ---------
            b: Union[:py:class:`str`, :py:class:`bytes`]
                The content to load into the model. This should be either a JSON serialized :py:class:`str`,
                or a :py:func:`pickle.dumps` object.

        Keyword Args
        ------------
            content_type: Optional[:py:class:`str`]
                The content type of the :paramref:`b` data passed. Should either be
                ``application/json`` or ``application/pickle``, if provided. Defaults to ```None``.
            encoding: Optional[:py:class:`str`]
                If a :py:class:`bytes` object is passed with a content type of ``json``,
                it must be decoded using the same method it was encoded in. This defaults to
                ``utf8``.
            proto: Optional[``pydantic.Protocol``]
                Another method of more directly specifying the :paramref:`content_type` of the data passed.
                This should be ``pydantic.Protocol.json`` or ``pydantic.Protocol.pickle`` if given. Otherwise,
                if neither the :paramref:`content_type` or this argument are passed, this is defaulted
                to ``Protocol.json``.
            allow_pickle: Optional[:py:class:`bool`]
                Whether or not to allow reading of pickled input. If the :paramref:`content_type` or
                :paramref:`protocol <proto>` are set to a ``pickle`` data type, this must be set to
                ``True``. Defaults to ``False``

        Raises
        ------
            ``pydantic.ValidationError``
                Raised if the :paramref:`b` cannot be used to instantiate the model,
                or if the :paramref:`content_type` is set to ``aplication/pickle`` without setting
                :paramref:`allow_pickle` to ``True``.
            :py:class:`pickle.UnpicklingError`
                Raised when Pickle fails to load an object.

        Returns
        -------
            :class:`BaseModel`
                An instantiated model from the :paramref:`b` provided.
        """
        return super().parse_raw(
            b=b,
            content_type=content_type,
            encoding=encoding,
            proto=proto,
            allow_pickle=allow_pickle
        )

    @classmethod
    def parse_file(
        cls: Type[PydBaseModel],
        path: Union[str, Path],
        *,
        content_type: str = None,
        encoding: str = 'utf8',
        proto: Protocol = None,
        allow_pickle: bool = False,
    ) -> PydBaseModel:
        """
        .. external_inherits_from::
            :objtype: classmethod
            :root: pydantic
            :path: usage/models/#helper-functions

            pydantic.BaseModel.parse_file

        Takes a file path and parses it to a JSON structure, then passes that to
        :meth:`parse_raw` to load it into the model. This can also handle loading :py:mod:`pickle` data directly
        via the :paramref:`content_type` argument.

        Arguments
        ---------
            path: Union[:py:class:`str`, :py:class:`pathlib.Path`]
                A path to a file to load into the model.

        Keyword Args
        ------------
            content_type: Optional[:py:class:`str`]
                The content type of the date in the file at the given :paramref:`path`. Should either be
                ``application/json`` or ``application/pickle``, if provided. Defaults to ``None``.
            encoding: Optional[:py:class:`str`]
                If a :py:class:`bytes` object is passed with a content type of ``json``,
                it must be decoded using the same method it was encoded in. This defaults to
                ``utf8``.
            proto: Optional[``pydantic.Protocol``]
                Another method of more directly specifying the :paramref:`content_type` of the data passed.
                This should be ``pydantic.Protocol.json`` or ``pydantic.Protocol.pickle`` if given. Otherwise,
                if neither the :paramref:`content_type` or this argument are passed, this is defaulted
                to ``Protocol.json``.
            allow_pickle: Optional[:py:class:`bool`]
                Whether or not to allow reading of pickled input. If the :paramref:`content_type` or
                :paramref:`protocol <proto>` are set to a ``pickle`` data type, this must be set to
                ``True``. Defaults to ``False``

        Raises
        ------
            ``pydantic.ValidationError``
                Raised if the :paramref:`path` cannot be used to instantiate the model.
            :py:class:`FileNotFoundError`
                Raised when the :paramref:`path` provided could not be used to open a file.
            :py:class:`TypeError`
                Raised when trying to decode with pickle without setting :paramref:`allow_pickle` to ``True``.

        Returns
        -------
            :class:`BaseModel`
                An instantiated model from the file :paramref:`path`.
        """
        return super().parse_file(
            path=path,
            content_type=content_type,
            encoding=encoding,
            proto=proto,
            allow_pickle=allow_pickle
        )

    @classmethod
    def from_orm(cls: Type[PydBaseModel], obj: Any) -> PydBaseModel:
        """
        .. external_inherits_from::
            :objtype: classmethod
            :root: pydantic
            :path: usage/models/#orm-mode-aka-arbitrary-class-instances

            pydantic.BaseModel.from_orm

        Instantiates the model from a given ORM class using ORM mode.

        Warning
        -------
            In order to use :meth:`from_orm`, the config property ``orm_mode`` must be set to ``True``.

        Arguments
        ---------
            obj: Any
                The ORM object to construct the model from.

        Raises
        ------
            ``pydantic.ValidationError``
                Raised if the model could not be instantiated from the given ORM :paramref:`obj`.
            ``pydantic.ConfigError``
                Raised when the model does not have the ``orm_mode`` set to ``True`` in the config.

        Returns
        -------
            :class:`BaseModel`
                An instantiated model from the given ORM instance.
        """

        return super().from_orm(obj=obj)

    @classmethod
    def schema(cls, by_alias: bool = True, ref_template: str = default_ref_template) -> DictStrAny:
        """
        .. external_inherits_from::
            :objtype: classmethod
            :root: pydantic
            :path: usage/schema/

            pydantic.BaseModel.schema

        Converts the model into a dictionary schema.

        Parameters
        ----------
            by_alias: Optional[:py:class:`bool`]
                Whether or not to use aliased names for fields when outputting the data schema. See
                :pydantic:`this example <usage/models/#reserved-names>` for creating field aliases.
                Defaults to ``True``.
            ref_template: Optional[:py:class:`str`]
                The string template to use when outputting sub-models to the schema. The template should include
                ``{model}`` somewhere in it as a placeholder for the name of the sub-model. Defaults to
                ``#/definitions/{model}``.

                Note
                ----
                    When outputting the schema structure, all sub-models of the model will be output under the
                    top-level JSON key ``definitions``, and then referenced using the :paramref:`ref_template` template
                    provided inside the parent model.

        Returns
        -------
            :py:class:`dict`
                The model represented as a python dictionary.
        """
        return super().schema(
            by_alias=by_alias,
            ref_template=ref_template
        )

    @classmethod
    def schema_json(
            cls,
            *,
            by_alias: bool = True,
            ref_template: str = default_ref_template,
            **dumps_kwargs: Any
    ) -> str:
        """
        .. external_inherits_from::
            :objtype: classmethod
            :root: pydantic
            :path: usage/schema/

            pydantic.BaseMode.schema_json

        Converts the model to a JSON serialized string.

        Tip
        ----
            Any extra keyword arguments passed to this method will be given to the :py:func:`json.dumps` function
            as keyword arguments. Using this, for example, means that you could pass the ``index`` argument,
            and cause the output string to be pretty-printed with indentation.

        Keyword Args
        ------------
            by_alias: Optional[:py:class:`bool`]
                Whether or not to use aliased names for fields when outputting the data schema. See
                :pydantic:`this example <usage/models/#reserved-names>` for creating field aliases.
                Defaults to ``True``.
            ref_template: Optional[:py:class:`str`]
                The string template to use when outputting sub-models to the schema. The template should include
                ``{model}`` somewhere in it as a placeholder for the name of the sub-model. Defaults to
                ``#/definitions/{model}``.

                Note
                ----
                    When outputting the schema structure, all sub-models of the model will be output under the
                    top-level JSON key ``definitions``, and then referenced using the :paramref:`ref_template` template
                    provided inside the parent model.

        Returns
        -------
            :py:class:`str`
                A JSON serialized :py:class:`str` containing the model schema.
        """
        return super().schema_json(by_alias=by_alias, ref_template=ref_template, **dumps_kwargs)

    @classmethod
    def construct(cls: Type[PydBaseModel], _fields_set: Optional[Set[str]] = None, **values: Any) -> PydBaseModel:
        """
        .. external_inherits_from::
            :objtype: classmethod
            :root: pydantic
            :path: usage/models/#creating-models-without-validation

            pydantic.BaseMode.construct

        Creates the model without running any validation. This can come in handy for slightly more performant code
        when creating models with data that has already been validated. Using :meth:`construct` is usually around
        ``30x`` faster than creating a model with complete validation. See an example
        :pydantic:`here <usage/models/#creating-models-without-validation>`.

        Warning
        -------
            This method is capable of creating `invalid` data in the model, so it should only be used if the data
            has already been validated, or comes from another trusted source.

        Arguments
        ---------
            _fields_set: Optional[:py:class:`set`]
                A :py:class:`set` of :py:class:`str` field names to pass to the model's :attr:`__fields_set__`
                attribute.
            **kwargs
                Any other keyword arguments given to the method will be processed as field names.

                Tip
                ----
                    In many cases, you will likely have a :py:class:`dict` that you want to pass, and you can do so by
                    using ``BaseModel.construct(**my_dict)``. To create a model from another model, you can use
                    ``BaseModel.construct(**model_instance.dict())``.
        """
        return super().construct(_fields_set=_fields_set, **values)


# ======================
#    Request Models
# ======================
class Response(BaseModel, abc.ABC):
    """
    .. inherits_from:: BaseModel

    The basic class that all response models for a request should subclass.
    This class provides a few basic fields that are used in recording
    request responses.

    Example
    --------
        .. code-block:: python

            # Create your response structure:
            class MyAPIResponse(Response):
                index: int
                first_name: str
                last_name: str

            # Pass this into your requests:
            response = my_client.get(..., response_model=MyAPIResponse)       # Sync
            response = await my_client.get(..., response_mode=MyApiResponse)  # Async

            # >>> response.dict()
            {
                "request_base_": "url",
                "request_received_at_": datetime.datetime(...),
                "id": 123,
                "first_name": "First",
                "last_name": "Last"
            }

    Note
    ----
        The :attr:`uri` and :attr:`time` attributes of this response method will not be included in any output methods
        for the model. They are purely intended for programmatic usage.

    Attributes
    -----------
        base_uri: Optional[:py:class:`str`]
            The url of the original request this is holding the response to.
        time: :py:class:`datetime.datetime`
            The time that the response was received at.

    Note
    ----
        The :attr:`uri` and :attr:`time` properties are set by default when a :class:`Response` is created.
        The default implementation is a timezone-aware UTC datetime.
    """

    _request_base: Optional[str] = PrivateAttr(default="")
    _request_received_at: Optional[datetime] = PrivateAttr(default_factory=datetime.utcnow)

    @property
    def base_uri(self) -> str:
        return self._request_base

    @property
    def time(self) -> datetime:
        return self._request_received_at


class PaginatedResponse(Response, abc.ABC):
    """
    .. inherits_from:: Response

    This offers a few extra options for a request response to enable easier response pagination.

    Often times when receiving a response for an API query which might include a significant amount of data
    (such as a list of products from an online shop), the API will limit the response to a set number of items.
    Taking this into account, this class can take advantage of the data structure to automatically give the necessary
    information about navigating this pagination.

    Warning
    -------
        This is an :py:class:`abstract <abc.ABC>` class, which means that any subclasses `must` implement
        all methods from this class.
    """

    @abc.abstractmethod
    def is_paginating(self) -> bool:
        """A method that is intended to determine whether any given response is paginated or not.

        If your response is `always` paginating, this should simply return ``True``. Likewise, if the response
        is never paginating, return ``False``. Otherwise, some logic should be implemented to determine
        whether the response is paginated.

        Returns
        -------
            :py:class:`bool`:
                Whether the response is paginated.
        """
        return False

    @abc.abstractmethod
    def next(self) -> Optional[Any]:
        """This will return an identifier for how to navigate to the next page in the paginated response.

        For example, if a response has a ``page_number`` field, you would return ``self.page_number + 1``.
        However, this can also be any return type, to allow for URLs to be returned directly, or some other
        implementation.

        Tip
        ----
            This method, as well as :meth:`previous <previous>`, :meth:`end <end>`, and
            :meth:`start <start>` for navigating pagination, should call :meth:`is_paginating` and return
            ``None`` if the response is not paginating.

            .. code-block:: python

                if not self.is_paginating():
                    return

        Returns
        -------
            Optional[Any]:
                Some identifier for navigating to the next page in the pagination.
        """
        return None

    @abc.abstractmethod
    def previous(self) -> Optional[Any]:
        """This will return an identifier for how to navigate to the previous page in the paginated response.

        For example, if a response has a ``page_number`` field, you would return ``self.page_number - 1``.
        However, this can also be any return type, to allow for URLs to be returned directly, or some other
        implementation.

        Returns
        -------
            Optional[Any]:
                Some identifier for navigating to the previous page in the pagination.
        """
        return None

    @abc.abstractmethod
    def end(self) -> Optional[Any]:
        """This will return an identifier for how to navigate to the last page in the paginated response.

        For example, if a response has a ``page_count`` field, you would want to return ``self.page_count``.
        However, this can also be any return type, to allow for URLs to be returned directly, or some other
        implementation.

        Returns
        -------
            Optional[Any]:
                Some identifier for navigating to the last page in the pagination.
        """
        return None

    @abc.abstractmethod
    def start(self) -> Optional[Any]:
        """This will return an identifier for how to navigate to the first page in the paginated response.

        For example, if you were tracking pagination by numbering each page, you would simply return ``1`` for the
        first page.

        Returns
        -------
            Optional[Any]:
                Some identifier for navigating to the first page in the pagination.
        """
        return None
