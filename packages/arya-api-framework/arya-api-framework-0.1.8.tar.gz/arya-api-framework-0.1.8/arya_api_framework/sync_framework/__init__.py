"""
Author: Arya Mayfield
Date: June 2022
Description: A RESTful API client for synchronous API applications.
"""

# Stdlib modules
from json import JSONDecodeError
import logging
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

# 3rd party modules
from pydantic import (
    BaseModel,
    SecretStr,
)
from pydantic import (
    parse_obj_as,
    validate_arguments,
)
from yarl import URL

# Local modules
from ..errors import (
    ERROR_RESPONSE_MAPPING,
    HTTPError,
    MISSING,
    ResponseParseError,
    SyncClientError,
)
from ..framework import Response
from ..utils import (
    flatten_obj,
    merge_dicts,
    validate_type,
)
from .utils import (
    chunk_file_reader,
    sleep_and_retry,
)

# Sync modules
is_sync: bool
try:
    from ratelimit import limits
    from requests import Session
    from requests.cookies import cookiejar_from_dict

    is_sync = True
except ImportError:
    is_sync = False

# Define exposed objects
__all__ = [
    "SyncClient"
]


# ======================
#     Logging Setup
# ======================
_log: logging.Logger = logging.getLogger("arya_api_framework.Sync")


# ======================
#        Typing
# ======================
MappingOrModel = Union[Dict[str, Union[str, int]], BaseModel]
HttpMapping = Dict[str, Union[str, int, List[Union[str, int]]]]
Parameters = Union[HttpMapping, BaseModel]
Cookies = MappingOrModel
Headers = MappingOrModel
Body = Union[Dict[str, Any], BaseModel]
ErrorResponses = Dict[int, Type[BaseModel]]
SessionT = TypeVar('SessionT', bound='Session')


# ======================
#     Sync Client
# ======================
class SyncClient:
    """ The synchronous API client class. Utilizes the :resource:`requests <requests>` module.

    Arguments
    ---------
        uri: Optional[:py:class:`str`]
            The base URI that will prepend all requests made using the client.

            Warning
            -------
                This should always either be passed as an argument here or as a subclass argument. If neither are given,
                an :class:`errors.SyncClientError` exception will be raised.

    Keyword Args
    ------------
        headers: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
            The default headers to pass with every request. Can be overridden by individual requests.
            Defaults to ``None``.
        cookies: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
            The default cookies to pass with every request. Can be overridden by individual requests.
            Defaults to ``None``.
        parameters: Optional[Union[:py:class:`dict`, :class:`BaseModel`]]
            The default parameters to pass with every request. Can be overridden by individual requests.
            Defaults to ``None``.
        error_responses: Optional[:py:class:`dict`]
            A mapping of :py:class:`int` error codes to :class:`BaseModel` types to use when that error code is
            received. Defaults to ``None`` and raises default exceptions for error codes.
        bearer_token: Optional[:py:class:`str`, :pydantic:`pydantic.SecretStr <usage/types/#secret-types>`
            A ``bearer_token`` that will be sent with requests in the ``Authorization`` header. Defaults to ``None``
        rate_limit: Optional[Union[:py:class:`int`, :py:class:`float`]]
            The number of requests to allow over :paramref:`rate_limit_interval` seconds. Defaults to ``None``
        rate_limit_interval: Optional[Union[:py:class:`int`, :py:class:`float`]]
            The period of time, in seconds, over which to apply the rate limit per every :paramref:`rate_limit`
            requests. Defaults to ``1`` second.

    Tip
    ----
        All of the arguments that can be used when instantiating a client can also be used as subclass parameters:

        .. code-blocK:: python

            class MyClient(SyncClient, uri="https://exampleurl.com", parameters={"arg1": "abc"}):
                pass

        Then, when instantiating the client, any arguments passed directly to the class will update the
        subclass parameters.

    Attributes
    ----------
        closed: :py:class:`bool`
            Whether of not the internal :py:class:`requests.Session` has been closed. If the session has been closed,
            the client will not allow any further requests to be made.
        uri: Optional[:py:class:`str`]
            The base URI that will prepend all requests made using the client.
        uri_root: Optional[:py:class:`str`]
            The root origin of the :attr:`uri` given to the client.
        uri_path: Optional[:py:class:`str`]
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
            The number of requests per :attr:`rate_limit_interval` the client is allowed to send.
        rate_limit_interval: Optional[Union[:py:class:`int`, :py:class:`float`]]
            The interval, in seconds, over which to apply a rate limit for :attr:`rate_limit` requests per interval.
        is_rate_limited: :py:class:`bool`
            Whether or not the client has a rate limit set.
    """

    # ======================
    #   Private Attributes
    # ======================
    _headers: Optional[Dict[str, Any]] = None
    _cookies: Optional[Dict[str, Any]] = None
    _parameters: Optional[Dict[str, Any]] = None
    _error_responses: Optional[ErrorResponses] = None
    _rate_limit_interval: Optional[Union[int, float]] = 1
    _rate_limit: Optional[Union[int, float]] = None
    _rate_limited: bool = False
    _base: Optional[URL] = MISSING
    _session: SessionT
    _closed: bool = False

    # ======================
    #    Initialization
    # ======================
    def __init__(
            self,
            uri: Optional[str] = None,
            *args,
            headers: Optional[Headers] = None,
            cookies: Optional[Cookies] = None,
            parameters: Optional[Parameters] = None,
            error_responses: Optional[ErrorResponses] = None,
            bearer_token: Optional[Union[str, SecretStr]] = None,
            rate_limit: Optional[Union[int, float]] = None,
            rate_limit_interval: Optional[Union[int, float]] = None,
            **kwargs
    ) -> None:
        if not is_sync:
            raise SyncClientError(
                "The sync context is unavailable. Try installing with `python -m pip install arya-api-framework[sync]`."
            )

        if uri:
            if validate_type(uri, str):
                self._base = URL(uri)

        if not self.uri:
            raise SyncClientError(
                "The client needs a base uri specified. "
                "This can be done through init parameters, or subclass parameters."
            )

        if bearer_token:
            if validate_type(bearer_token, SecretStr, err=False):
                bearer_token = bearer_token.get_secret_value()

            if not headers:
                headers = {}

            headers["Authorization"] = f"Bearer {bearer_token}"

        self._cookies = merge_dicts(self.cookies, cookies) or {}
        self._parameters = merge_dicts(self.parameters, parameters) or {}
        self._headers = merge_dicts(self.headers, headers) or {}
        self._error_responses = merge_dicts(self.error_responses, error_responses) or {}

        if rate_limit:
            if validate_type(rate_limit, [int, float]):
                self._rate_limit = rate_limit
        if rate_limit_interval:
            if validate_type(rate_limit_interval, [int, float]):
                self._rate_limit_interval = rate_limit_interval

        if self._rate_limit:
            self.request = sleep_and_retry(
                limits(calls=self._rate_limit, period=self._rate_limit_interval)(self.request)
            )
            self._rate_limited = True

        self._session = Session()
        self._session.headers = self.headers
        self._session.cookies = cookiejar_from_dict(self.cookies)
        self._session.params = self.parameters

        if hasattr(self, '__post_init__'):
            self.__post_init__(*args, **kwargs)

    def __post_init__(self, *args, **kwargs) -> None:
        """This method is run after the ``__init__`` method is called, and is passed any extra arguments or
        keyword arguments that the regular init method did not recognize.

        Tip
        ----
            By using this method, it becomes unnecessary to override the ``__init__`` method. Instead, any extra
            parameters can be provided in this method, which has no implementation at default.

        Example
        -------
            This is a quick example showing how one might add a default ``apiKey`` parameter to their custom API client
            using the :meth:`__post_init__` method.

            .. code-block:: python

                class MySyncClient(SyncClient):
                    api_key: str

                    def __post_init__(self, *args, api_key: str = None, **kwargs):
                        self.api_key = api_key

                        self.parameters['apiKey'] = self.api_key

                client = MySyncClient('https://exampleurl.com', api_key='mysecretkey')

                # >>> client.parameters
                {
                    "apiKey": "mysecretkey"
                }
        """
        pass

    def __init_subclass__(
            cls,
            uri: Optional[str] = None,
            headers: Optional[Headers] = None,
            cookies: Optional[Cookies] = None,
            parameters: Optional[Parameters] = None,
            bearer_token: Optional[Union[str, SecretStr]] = None,
            error_responses: Optional[ErrorResponses] = None,
            rate_limit: Optional[Union[int, float]] = None,
            rate_limit_interval: Optional[Union[int, float]] = None
    ) -> None:
        if uri:
            if validate_type(uri, str):
                cls._base = URL(uri)
        if bearer_token:
            if validate_type(bearer_token, SecretStr, err=False):
                bearer_token = bearer_token.get_secret_value()

            if not headers:
                headers = {}

            headers["Authorization"] = f"Bearer {bearer_token}"
        cls._headers = flatten_obj(headers)
        cls._cookies = flatten_obj(cookies)
        cls._parameters = flatten_obj(parameters)
        cls._error_responses = error_responses or {}
        if rate_limit:
            if validate_type(rate_limit, [int, float]):
                cls._rate_limit = rate_limit
        if rate_limit_interval:
            if validate_type(rate_limit_interval, [int, float]):
                cls._rate_limit_interval = rate_limit_interval

    # ======================
    #      Properties
    # ======================
    # General Information
    @property
    def closed(self) -> bool:
        return self._closed

    # URI Options
    @property
    def uri(self) -> Optional[str]:
        return str(self._base) if self._base is not MISSING else None

    @property
    def uri_root(self) -> Optional[str]:
        return str(self._base.origin()) if self._base is not MISSING else None

    @property
    def uri_path(self) -> Optional[str]:
        return str(self._base.relative()) if self._base is not MISSING else None

    # Default Request Settings
    @property
    def headers(self) -> Optional[Headers]:
        return self._headers

    @headers.setter
    def headers(self, headers: Headers) -> None:
        self._headers = flatten_obj(headers) or {}
        self._session.headers = self._headers

    @property
    def cookies(self) -> Optional[Cookies]:
        return self._cookies

    @cookies.setter
    def cookies(self, cookies: Cookies) -> None:
        self._cookies = flatten_obj(cookies) or {}
        self._session.cookies = self._cookies

    @property
    def parameters(self) -> Optional[Parameters]:
        return self._parameters

    @parameters.setter
    def parameters(self, params: Parameters) -> None:
        self._parameters = flatten_obj(params) or {}
        self._session.params = self._parameters

    @property
    def error_responses(self) -> Optional[ErrorResponses]:
        return self._error_responses

    @error_responses.setter
    @validate_arguments()
    def error_responses(self, error_responses: ErrorResponses) -> None:
        self._error_responses = error_responses or {}

    # Rate Limits
    @property
    def rate_limit(self) -> Optional[Union[int, float]]:
        return self._rate_limit

    @property
    def rate_limit_interval(self) -> Optional[Union[int, float]]:
        return self._rate_limit_interval

    @property
    def is_rate_limited(self) -> bool:
        return self._rate_limited

    # ======================
    #    Request Methods
    # ======================
    @validate_arguments()
    def request(
            self,
            method: str,
            path: str = None,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        """
        * |validated_method|
        * |sync_rate_limited_method|

        Sends a request to the :paramref:`path` specified using the internal :py:class:`requests.Session`.

        Note
        ____
            If the client has been :attr:`closed` (using :meth:`close`), the request will not be processed. Instead,
            a warning will be logged, and this method will return ``None``.

        Arguments
        ---------
            method: :py:class:`str`
                The request method to use for the request (see :ref:`http-requests`).
            path: Optional[:py:class:`str`]
                The path, relative to the client's :attr:`uri`, to send the request to.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
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
            _log.warning(f"The {self.__class__.__name__} session has already been closed, and no further requests will be processed.")
            return

        path = self.uri + path if path else self.uri
        headers = flatten_obj(headers)
        cookies = flatten_obj(cookies)
        parameters = flatten_obj(parameters)
        body = flatten_obj(body)
        error_responses = error_responses or self.error_responses or {}

        with self._session.request(
                method,
                path,
                headers=headers,
                cookies=cookies,
                params=parameters,
                json=body,
                data=data,
                timeout=timeout
        ) as response:
            _log.info(f"[{method} {response.status_code}] {path} {URL(response.request.url).query_string}")

            if response.ok:
                try:
                    response_json = response.json()
                except JSONDecodeError:
                    raise ResponseParseError(raw_response=response.text)

                if response_format is not None:
                    obj = parse_obj_as(response_format, response_json)
                    obj._request_base = response.request.url
                    return obj

                return response_json

            error_class = ERROR_RESPONSE_MAPPING.get(response.status_code, HTTPError)
            error_response_model = error_responses.get(response.status_code)

            try:
                response_json = response.json()
            except JSONDecodeError:
                raise ResponseParseError(raw_response=response.text)

            if bool(error_response_model):
                raise error_class(parse_obj_as(error_response_model, response_json))

            raise error_class(response_json)

    @validate_arguments()
    def upload_file(
            self,
            file: str,
            path: str = None,
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        """
        * |validated_method|
        * |sync_rate_limited_method|

        Sends a :ref:`post` request to the :paramref:`path` specified using the internal :py:class:`requests.Session`,
        which will upload a given :paramref:`file`.

        Tip
        ----
            To stream larger file uploads, use the :meth:`stream_file` method.

        Arguments
        ---------
            file: :py:class:`str`
                The path to the file to upload.
            path: Optional[:py:class:`str`]
                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
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

        return self.post(
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
    def stream_file(
            self,
            file: str,
            path: str = None,
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        """
        * |validated_method|
        * |sync_rate_limited_method|

        Sends a :ref:`post` request to the :paramref:`path` specified using the internal :py:class:`requests.Session`,
        which will upload a given :paramref:`file`.

        Tip
        ----
            This method is meant to upload larger files in a stream manner, while the :meth:`upload_file` method
            uploads the file without streaming it.

        Arguments
        ---------
            file: :py:class:`str`
                The path to the file to upload.
            path: Optional[:py:class:`str`]
                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
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
        return self.post(
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
    def get(
            self,
            path: str = None,
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[Union[Response, Dict]]:
        """
        * |validated_method|
        * |sync_rate_limited_method|

        Sends a :ref:`get` request to the :paramref:`path` specified using the internal :py:class:`requests.Session`.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific headers to send with the :ref:`get` request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific cookies to send with the :ref:`get` request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific query string parameters to send with the :ref:`get` request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
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

        return self.request(
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
    def post(
            self,
            path: str = None,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        """
        * |validated_method|
        * |sync_rate_limited_method|

        Sends a :ref:`post` request to the :paramref:`path` specified using the internal :py:class:`requests.Session`.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
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

        return self.request(
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
    def patch(
            self,
            path: str = None,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        """
        * |validated_method|
        * |sync_rate_limited_method|

        Sends a :ref:`patch` request to the :paramref:`path` specified using the internal :py:class:`requests.Session`.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
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

        return self.request(
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
    def put(
            self,
            path: str = None,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        """
        * |validated_method|
        * |sync_rate_limited_method|

        Sends a :ref:`put` request to the :paramref:`path` specified using the internal :py:class:`requests.Session`.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
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

        return self.request(
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
    def delete(
            self,
            path: str = None,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[Response]:
        """
        * |validated_method|
        * |sync_rate_limited_method|

        Sends a :ref:`delete` request to the :paramref:`path` specified using the internal :py:class:`requests.Session`.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                The path, relative to the client's :attr:`uri`, to send the request to. If this is set to ``None``,
                the request will be sent to the client's :attr:`uri`.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters`.
            response_format: Optional[Type[:class:`Response`]]
                The model to use as the response format. This offers direct data validation and easy object-oriented
                implementation. Defaults to ``None``, and the request will return a JSON structure.
            timeout: Optional[:py:class:`int`]
                The length of time, in seconds, to wait for a response to the request before raising a timeout error.
                Defaults to ``300`` seconds, or 5 minutes.
            error_responses: Optional[:py:class:`dict`]
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

        return self.request(
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
    def close(self):
        """
        Closes the current :py:class:`requests.Session`, if not already closed.
        """
        if not self._closed:
            self._session.close()
            self._closed = True
