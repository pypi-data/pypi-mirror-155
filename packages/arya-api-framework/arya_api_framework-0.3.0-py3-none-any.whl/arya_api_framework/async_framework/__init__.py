"""
Author: Arya Mayfield
Date: June 2022
Description: A RESTful API client for asynchronous API applications.
"""

# Stdlib modules
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Type,
    Union,
)
from json import JSONDecodeError

# 3rd party modules
from multidict import CIMultiDict
from pydantic import (
    BaseModel,
)
from pydantic import (
    parse_obj_as,
    validate_arguments,
)
from yarl import URL

# Local modules
from ..constants import ClientBranch
from ..errors import (
    ERROR_RESPONSE_MAPPING,
    HTTPError,
    ResponseParseError,
)
from ..framework import ClientInternal
from ..models import Response
from ..utils import (
    flatten_obj,
    merge_dicts,
)
from .utils import chunk_file_reader

# Async modules
try:
    from aiohttp import ClientTimeout
    from aiolimiter import AsyncLimiter
except ImportError:
    pass

# Define exposed objects
__all__ = [
    "AsyncClient"
]


# ======================
#        Typing
# ======================
DictStrAny = Dict[str, Any]
MappingOrModel = Union[Dict[str, Union[str, int]], BaseModel]
HttpMapping = Dict[str, Union[str, int, List[Union[str, int]]]]
Parameters = Union[HttpMapping, BaseModel]
Cookies = MappingOrModel
Headers = MappingOrModel
Body = Union[Dict[str, Any], BaseModel]
ErrorResponses = Dict[int, Type[BaseModel]]
RequestResponse = Union[
    Union[Response, List[Response]],
    Union[DictStrAny, List[DictStrAny]]
]


# ======================
#     Async Client
# ======================
class AsyncClient(ClientInternal):
    """ The core API framework client for asynchronous API integration.

    Warning
    -------
        All of the configuration for this class and its subclasses are done through subclass parameters. This means that
        the ``__init__`` method can be used for any extra setup for your specific use-case. The parameters shown below
        are for subclass parameters only.

        .. code-block:: python
            :caption: Example:

            class MyClient(
                    AsyncClient,
                    uri="https://exampleurl.com",
                    parameters={"arg1": "abc"}
            ):
                ...

    Keyword Args
    ------------
        uri: :py:class:`str`
            * |kwargonly|

            The base URI that will prepend all requests made using the client.

            Warning
            -------
                This should always be passed. If it is not given, an :class:`errors.ClientError` exception will be
                raised.
        headers: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
            * |kwargonly|

            The default headers to pass with every request. Can be overridden by individual requests.
            Defaults to ``None``.
        cookies: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
            * |kwargonly|

            The default cookies to pass with every request. Can be overridden by individual requests.
            Defaults to ``None``.
        parameters: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
            * |kwargonly|

            The default parameters to pass with every request. Can be overridden by individual requests.
            Defaults to ``None``.
        error_responses: Optional[:py:class:`dict`]
            * |kwargonly|

            A mapping of :py:class:`int` error codes to :class:`BaseModel` types to use when that error code is
            received. Defaults to ``None`` and raises default exceptions for error codes.
        bearer_token: Optional[Union[:py:class:`str`, :pydantic:`pydantic.SecretStr <usage/types/#secret-types>`]]
            * |kwargonly|

            A ``bearer_token`` that will be sent with requests in the ``Authorization`` header. Defaults to ``None``
        rate_limit: Optional[Union[:py:class:`int`, :py:class:`float`]]
            * |kwargonly|

            The number of requests to allow over :paramref:`rate_limit_interval` seconds. Defaults to ``None``
        rate_limit_interval: Optional[Union[:py:class:`int`, :py:class:`float`]]
            * |kwargonly|

            The period of time, in seconds, over which to apply the rate limit per every :paramref:`rate_limit`
            requests. Defaults to ``1`` second.

    Attributes
    ----------
        closed: :py:class:`bool`
            * |readonly|

            Whether of not the internal :py:class:`requests.Session` has been closed. If the session has been closed,
            the client will not allow any further requests to be made.
        extensions: Mapping[:py:class:`str`, :py:class:`types.ModuleType`]
            * |readonly|

            A mapping of extensions by name to extension.
        subclients: Mapping[:py:class:`str`, :class:`SubClient`]
            * |readonly|

            A mapping of sub-clients by name to sub-client.
        uri: Optional[:py:class:`str`]
            * |readonly|

            The base URI that will prepend all requests made using the client.
        uri_root: Optional[:py:class:`str`]
            * |readonly|

            The root origin of the :attr:`uri` given to the client.
        uri_path: Optional[:py:class:`str`]
            * |readonly|

            The path from the :attr:`uri_root` to the :attr:`uri` path.
        headers: Optional[:py:class:`dict`]
            The default headers that will be passed into every request, unless overridden.
        cookies: Optional[:py:class:`dict`]
            The default cookies that will be passed into every request, unless overridden.
        parameters: Optional[:py:class:`dict`]
            The default parameters that will be passed into every request, unless overridden.
        error_responses: Optional[:py:class:`dict`]
            A mapping of :py:class:`int` error codes to the :class:`BaseModel` that should be used to represent them.

            Note
            ----
                By default, an internal exception mapping is used. See :ref:`exceptions`.

        rate_limit: Optional[Union[:py:class:`int`, :py:class:`float`]]
            * |readonly|

            The number of requests per :attr:`rate_limit_interval` the client is allowed to send.
        rate_limit_interval: Optional[Union[:py:class:`int`, :py:class:`float`]]
            * |readonly|

            The interval, in seconds, over which to apply a rate limit for :attr:`rate_limit` requests per interval.
        is_rate_limited: :py:class:`bool`
            * |readonly|

            Whether or not the client has a rate limit set.
    """
    # ======================
    #   Private Attributes
    # ======================
    _branch: Optional[ClientBranch] = ClientBranch.async_

    __limiter: Optional['AsyncLimiter'] = None

    # ======================
    #    Request Methods
    # ======================
    @validate_arguments()
    async def request(
            self,
            method: str,
            path: str = '',
            /,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[RequestResponse]:
        """
        * |coro|
        * |validated_method|
        * |async_rate_limited_method|

        Sends a request to the :paramref:`path` specified using the internal :py:class:`aiohttp.ClientSession`.

        Note
        ____
            If the client has been :attr:`closed` (using :meth:`close`), the request will not be processed. Instead,
            a warning will be logged, and this method will return ``None``.

        Arguments
        ---------
            method: :py:class:`str`
                * |positional|

                The request method to use for the request (see :ref:`http-requests`).
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`uri`, to send the request to.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                * |kwargonly|

                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                * |kwargonly|

                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                * |kwargonly|

                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
                * |kwargonly|

                A mapping of :py:class:`int` status codes to :class:`BaseModel` models to use as error responses.
                Defaults to ``None``, and uses the default :attr:`error_responses` attribute. If the
                :attr:`error_responses` is also ``None``, or a status code does not have a specified response format,
                the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        if self.closed:
            self.logger.warning(f"The {self.__class__.__name__} session has already been closed, and no further requests will be processed.")
            return

        if path and not path.startswith('/'):
            path = f'/{path}'

        if self.__limiter:
            if not self.__limiter.has_capacity():
                self.logger.info("Waiting for rate limit")
            await self.__limiter.acquire()

        path = self.uri_path + path if self.uri_path and path else self.uri_path if self.uri_path else path if path else ''
        headers = flatten_obj(headers)
        cookies = flatten_obj(cookies)
        parameters = merge_dicts(self.parameters, parameters)
        body = flatten_obj(body)
        error_responses = error_responses or self.error_responses or {}

        async with self._session.request(
                method,
                path,
                headers=headers,
                cookies=cookies,
                params=parameters,
                json=body,
                data=data,
                timeout=ClientTimeout(total=timeout)
        ) as response:
            self.logger.info(f"[{method} {response.status}] {path} {URL(response.url).query_string}")

            if response.ok:
                try:
                    response_json = await response.json(content_type=None)
                except JSONDecodeError:
                    response_text = await response.text()
                    raise ResponseParseError(raw_response=response_text)

                if response_format is not None:
                    if isinstance(response_json, list):
                        lst = []
                        for dt in response_json:
                            obj = parse_obj_as(response_format, dt)
                            obj._request_base = str(response.url)
                            lst.append(obj)
                        return lst

                    obj = parse_obj_as(response_format, response_json)
                    obj._request_base = str(response.url)
                    return obj

                return response_json

            error_class = ERROR_RESPONSE_MAPPING.get(response.status, HTTPError)
            error_response_model = error_responses.get(response.status)

            try:
                response_json = await response.json(content_type=None)
            except JSONDecodeError:
                response_text = await response.text()
                raise ResponseParseError(raw_response=response_text)

            if bool(error_response_model):
                raise error_class(parse_obj_as(error_response_model, response_json))

            raise error_class(response_json)

    @validate_arguments()
    async def upload_file(
            self,
            file: str,
            path: str = '',
            /,
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[RequestResponse]:
        """
        * |coro|
        * |validated_method|
        * |async_rate_limited_method|

        Sends a :ref:`post` request to the :paramref:`path` specified using the internal
        :py:class:`aiohttp.ClientSession`, which will upload a given :paramref:`file`.

        Tip
        ----
            To stream larger file uploads, use the :meth:`stream_file` method.

        Arguments
        ---------
            file: :py:class:`str`
                * |positional|

                The path to the file to upload.
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            headers: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                * |kwargonly|

                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                * |kwargonly|

                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
                * |kwargonly|

                A mapping of :py:class:`int` status codes to :class:`BaseModel` models to use as error responses.
                Defaults to ``None``, and uses the default :attr:`error_responses` attribute. If the
                :attr:`error_responses` is also ``None``, or a status code does not have a specified response format,
                the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return await self.request(
            'POST',
            path,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            data={'file': open(file, 'rb')},
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses,
        )

    @validate_arguments()
    async def stream_file(
            self,
            file: str,
            path: str = '',
            /,
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[RequestResponse]:
        """
        * |coro|
        * |validated_method|
        * |async_rate_limited_method|

        Sends a :ref:`post` request to the :paramref:`path` specified using the internal
        :py:class:`aiohttp.ClientSession`, which will upload a given :paramref:`file`.

        Tip
        ----
            This method is meant to upload larger files in a stream manner, while the :meth:`upload_file` method
            uploads the file without streaming it.

        Arguments
        ---------
            file: :py:class:`str`
                * |positional|

                The path to the file to upload.
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            headers: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                * |kwargonly|

                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                * |kwargonly|

                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
                * |kwargonly|

                A mapping of :py:class:`int` status codes to :class:`BaseModel` models to use as error responses.
                Defaults to ``None``, and uses the default :attr:`error_responses` attribute. If the
                :attr:`error_responses` is also ``None``, or a status code does not have a specified response format,
                the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return await self.request(
            'POST',
            path,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            data=chunk_file_reader(file),
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses
        )

    @validate_arguments()
    async def get(
            self,
            path: str = '',
            /,
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[RequestResponse]:
        """
        * |coro|
        * |validated_method|
        * |async_rate_limited_method|

        Sends a :ref:`get` request to the :paramref:`path` specified using the internal
        :py:class:`aiohttp.ClientSession`.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            headers: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific headers to send with the :ref:`get` request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific cookies to send with the :ref:`get` request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific query string parameters to send with the :ref:`get` request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                * |kwargonly|

                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                * |kwargonly|

                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
                * |kwargonly|

                A mapping of :py:class:`int` status codes to :class:`BaseModel` models to use as error responses. Defaults
                to ``None``, and uses the default :attr:`error_responses` attribute. If the :attr:`error_responses`
                is also ``None``, or a status code does not have a specified response format, the default status code
                exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return await self.request(
            "GET",
            path,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses,
        )

    @validate_arguments()
    async def post(
            self,
            path: str = '',
            /,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[RequestResponse]:
        """
        * |coro|
        * |validated_method|
        * |async_rate_limited_method|

        Sends a :ref:`post` request to the :paramref:`path` specified using the internal
        :py:class:`aiohttp.ClientSession`.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                * |kwargonly|

                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                * |kwargonly|

                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                * |kwargonly|

                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
                * |kwargonly|

                A mapping of :py:class:`int` status codes to :class:`BaseModel` models to use as error responses.
                Defaults to ``None``, and uses the default :attr:`error_responses` attribute. If the
                :attr:`error_responses` is also ``None``, or a status code does not have a specified response format,
                the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return await self.request(
            "POST",
            path,
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses,
        )

    @validate_arguments()
    async def patch(
            self,
            path: str = '',
            /,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[RequestResponse]:
        """
        * |coro|
        * |validated_method|
        * |async_rate_limited_method|

        Sends a :ref:`patch` request to the :paramref:`path` specified using the internal
        :py:class:`aiohttp.ClientSession`.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                * |kwargonly|

                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                * |kwargonly|

                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                * |kwargonly|

                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
                * |kwargonly|

                A mapping of :py:class:`int` status codes to :class:`BaseModel` models to use as error responses.
                Defaults to ``None``, and uses the default :attr:`error_responses` attribute. If the
                :attr:`error_responses` is also ``None``, or a status code does not have a specified response format,
                the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return await self.request(
            "PATCH",
            path,
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses,
        )

    @validate_arguments()
    async def put(
            self,
            path: str = '',
            /,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[RequestResponse]:
        """
        * |coro|
        * |validated_method|
        * |async_rate_limited_method|

        Sends a :ref:`put` request to the :paramref:`path` specified using the internal
        :py:class:`aiohttp.ClientSession`.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                * |kwargonly|

                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                * |kwargonly|

                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                * |kwargonly|

                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
                * |kwargonly|

                A mapping of :py:class:`int` status codes to :class:`BaseModel` models to use as error responses.
                Defaults to ``None``, and uses the default :attr:`error_responses` attribute. If the
                :attr:`error_responses` is also ``None``, or a status code does not have a specified response format,
                the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return await self.request(
            "PUT",
            path,
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses,
        )

    @validate_arguments()
    async def delete(
            self,
            path: str = '',
            /,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[RequestResponse]:
        """
        * |coro|
        * |validated_method|
        * |async_rate_limited_method|

        Sends a :ref:`delete` request to the :paramref:`path` specified using the internal
        :py:class:`aiohttp.ClientSession`.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                * |kwargonly|

                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                * |kwargonly|

                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                * |kwargonly|

                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
                * |kwargonly|

                A mapping of :py:class:`int` status codes to :class:`BaseModel` models to use as error responses.
                Defaults to ``None``, and uses the default :attr:`error_responses` attribute. If the
                :attr:`error_responses` is also ``None``, or a status code does not have a specified response format,
                the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return await self.request(
            "DELETE",
            path,
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses,
        )

    # ======================
    #    General methods
    # ======================
    async def close(self):
        """
        Closes the current :py:class:`aiohttp.ClientSession`, if not already closed.

        Unloads any loaded extensions and :class:`SubClients <SubClient>`.
        """
        if not self._closed:
            await self._session.close()
            self._closed = True

        self._teardown()

    # ======================
    #   Private Methods
    # ======================
    def _init_rate_limit(self) -> None:
        if self.rate_limit:
            self.__limiter = AsyncLimiter(self.rate_limit, self.rate_limit_interval)
            self._rate_limited = True

    def _update_session_headers(self) -> None:
        if self._session:
            self._session._default_headers = CIMultiDict(self.headers) if self.headers else CIMultiDict()

    def _update_session_cookies(self) -> None:
        if self._session:
            self._session._cookie_jar.update_cookies(self.cookies)

    def _update_session_parameters(self) -> None:
        pass
