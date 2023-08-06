import abc
import importlib.util
import logging
import os
import sys
from types import MappingProxyType
from typing import TYPE_CHECKING
from typing import (
    Any,
    Dict,
    List,
    Mapping,
    Optional,
    Type,
    TypeVar,
    Union,
)

from pydantic import SecretStr
from yarl import URL

from .constants import ClientBranch
from . import errors
from .models import Response
from .utils import validate_type, flatten_params, merge_dicts, flatten_obj, _is_submodule


is_sync: bool
try:
    from ratelimit import limits, RateLimitException
    from requests import Session
    from requests.cookies import cookiejar_from_dict
    import time
    from functools import wraps

    is_sync = True
except ImportError:
    is_sync = False

is_async: bool
try:
    import asyncio
    from aiohttp import (
        ClientSession,
        ClientTimeout,
    )
    from aiolimiter import AsyncLimiter

    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    is_async = True
except ImportError:
    is_async = False


if TYPE_CHECKING:
    from types import ModuleType
    import importlib.machinery

    from .models import BaseModel

__all__ = [
    "_ClientInternal",
]

# ======================
#        Typing
# ======================
Num = Union[int, float]
DictStrAny = Dict[str, Any]
DictStrModule = Dict[str, 'ModuleType']
MappingOrModel = Union[Dict[str, Union[str, int]], 'BaseModel']
HttpMapping = Dict[str, Union[str, int, List[Union[str, int]]]]
Parameters = Union[HttpMapping, 'BaseModel']
Cookies = MappingOrModel
Headers = MappingOrModel
Body = Union[Dict[str, Any], 'BaseModel']
ErrorResponses = Dict[int, Type['BaseModel']]
RequestResponse = Union[
    Union[Response, List[Response]],
    Union[DictStrAny, List[DictStrAny]]
]
SyncSessionT = TypeVar('SyncSessionT', bound='Session')
AsyncSessionT = TypeVar('AsyncSessionT', bound='ClientSession')
SessionT = Union[SyncSessionT, AsyncSessionT]


# ======================
#       Classes
# ======================
class _ClientInternal(abc.ABC):
    """ The base API client class.

    Arguments
    ---------
        uri: Optional[:py:class:`str`]
            The base URI that will prepend all requests made using the client.

            Warning
            -------
                This should always either be passed as an argument here or as a subclass argument. If neither are given,
                an :class:`errors.ClientError` exception will be raised.

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

        .. code-block:: python

            class MyClient(SyncClient, uri="https://exampleurl.com", parameters={"arg1": "abc"}):
                pass

        Then, when instantiating the client, any arguments passed directly to the class will update the
        subclass parameters.

    Attributes
    ----------
        closed: :py:class:`bool`
            * |readonly|

            Whether of not the internal :py:class:`requests.Session` has been closed. If the session has been closed,
            the client will not allow any further requests to be made.
        extensions: Mapping[:py:class:`str`, :py:class:`types.ModuleType`]
            * |readonly|

            A mapping of extensions by name to extension.
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
    __extensions: DictStrModule = {}

    _branch: Optional[ClientBranch] = None
    _headers: Optional[DictStrAny] = None
    _cookies: Optional[DictStrAny] = None
    _parameters: Optional[DictStrAny] = None
    _error_responses: Optional[ErrorResponses] = None
    _rate_limit_interval: Optional[Num] = 1
    _rate_limit: Optional[Num] = None
    _rate_limited: bool = False
    _base: Optional['URL'] = errors.MISSING
    _session: SessionT = None
    _closed: bool = False

    # ======================
    #   Public Attributes
    # ======================
    logger: logging.Logger

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
        self._init_branch()
        self._init_logger()

        if uri:
            if validate_type(uri, str):
                self._base = URL(uri.rstrip('/'))

        if not self.uri or self.uri is errors.MISSING:
            raise errors.ClientError(
                "The client needs a base uri specified. "
                "This can be done through init or subclass parameters."
            )

        if bearer_token:
            if validate_type(bearer_token, SecretStr, err=False):
                bearer_token = bearer_token.get_secret_value()

            if not headers:
                headers = {}

            headers['Authorization'] = f'Bearer {bearer_token}'

        self.cookies = merge_dicts(self.cookies, cookies)
        self.parameters = merge_dicts(self.parameters, flatten_params(parameters))
        self.headers = merge_dicts(self.headers, headers)
        self.error_responses = merge_dicts(self.error_responses, error_responses)

        if rate_limit:
            if validate_type(rate_limit, [int, float]):
                self._rate_limit = rate_limit
        if rate_limit_interval:
            if validate_type(rate_limit_interval, [int, float]):
                self._rate_limit_interval = rate_limit_interval

        self._init_rate_limit()
        self._init_session()

        if hasattr(self, '__post_init__'):
            self.__post_init__(*args, **kwargs)

    def __post_init__(self, *args, **kwargs):
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

            >>> client.parameters
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
                cls._base = URL(uri.rstrip('/'))

        if bearer_token:
            if validate_type(bearer_token, SecretStr, err=False):
                bearer_token = bearer_token.get_secret_value()

            if not headers:
                headers = {}
            headers['Authoritzation'] = f'Bearer {bearer_token}'

        cls._headers = flatten_obj(headers)
        cls._cookies = flatten_obj(cookies)
        cls._parameters = flatten_params(parameters)
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

    @property
    def extensions(self) -> Mapping[str, 'ModuleType']:
        return MappingProxyType(self.__extensions)

    # URI Options
    @property
    def uri(self) -> Optional[str]:
        return str(self._base) if self._base is not errors.MISSING else None

    @property
    def uri_root(self) -> Optional[str]:
        return str(self._base.origin()) if self._base is not errors.MISSING else None

    @property
    def uri_path(self) -> Optional[str]:
        return str(self._base.relative()) if self._base is not errors.MISSING else None

    # Default Request Settings
    @property
    def headers(self) -> Optional[Headers]:
        return self._headers

    @headers.setter
    def headers(self, headers: Headers) -> None:
        self._headers = flatten_obj(headers) or {}
        self._update_session_headers()

    @property
    def cookies(self) -> Optional[Cookies]:
        return self._cookies

    @cookies.setter
    def cookies(self, cookies: Cookies) -> None:
        self._cookies = flatten_obj(cookies) or {}
        self._update_session_cookies()

    @property
    def parameters(self) -> Optional[Parameters]:
        return self._parameters

    @parameters.setter
    def parameters(self, parameters: Parameters) -> None:
        self._parameters = flatten_params(parameters) or {}
        self._update_session_parameters()

    @property
    def error_responses(self) -> Optional[ErrorResponses]:
        return self._error_responses

    @error_responses.setter
    def error_responses(self, error_responses: ErrorResponses) -> None:
        self._error_responses = error_responses or {}

    # Rate Limits
    @property
    def rate_limit(self) -> Optional[Num]:
        return self._rate_limit

    @property
    def rate_limit_interval(self) -> Optional[Num]:
        return self._rate_limit_interval

    @property
    def rate_limited(self) -> bool:
        return self._rate_limited

    # ======================
    #    Request Methods
    # ======================
    @abc.abstractmethod
    def request(
            self,
            method: str,
            path: str = None,
            *,
            body: Body = None,
            data: Any = None,
            files: Dict[str, Any] = None,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[RequestResponse]:
        pass

    @abc.abstractmethod
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
    ) -> Optional[RequestResponse]:
        pass

    @abc.abstractmethod
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
    ) -> Optional[RequestResponse]:
        pass

    @abc.abstractmethod
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
    ) -> Optional[RequestResponse]:
        pass

    @abc.abstractmethod
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
    ) -> Optional[RequestResponse]:
        pass

    @abc.abstractmethod
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
    ) -> Optional[RequestResponse]:
        pass

    @abc.abstractmethod
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
    ) -> Optional[RequestResponse]:
        pass

    @abc.abstractmethod
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
    ) -> Optional[RequestResponse]:
        pass

    # ======================
    #    General methods
    # ======================

    @abc.abstractmethod
    def close(self) -> None:
        pass

    def load_extension(self, name: str, *, package: Optional[str] = None) -> None:
        """
        Loads an extension.

        An extension is a separate python module (file) that contains a sub-group of requests.

        Any extension module should include a function ``setup`` defined as the entry point
        for loading the extension, which takes a single argument of a ``client``, either a :class:`SyncClient`
        or an :class:`AsyncClient`.

        Registered extensions can be seen through the :attr:`extensions` property.

        Arguments
        ---------
            name: :py:class:`str`
                The name of the extension to load. This should be in the same format as a normal python import.
                For example, if you wanted to reference the ``extensions/submodule.py`` module, you would set the
                ``name`` parameter to ``extensions.submodule``.

        Keyword Args
        ------------
            package: Optional[:py:class:`str`]
                The name of the package to load relative imports from. For example, if a :paramref:`name` parameter
                is given as ``.submodule`` to reference the ``extensions/submodule.py`` extension, the ``package``
                parameter would be ``extensions``. Defaults to ``None``.

        Raises
        ------
            :class:`ExtensionNotFound`
                The extension could not be imported. This usually means that the extension file could not be found.
            :class:`ExtensionAlreadyLoaded`
                The extension is already loaded to the client.
            :class:`ExtensionEntryPointError`
                The extension has no ``setup`` function in it.
            :class:`ExtensionFailed`
                The extension threw an error while executing the ``setup`` function.
        """

        try:
            name = importlib.util.resolve_name(name, package)
        except ImportError:
            raise errors.ExtensionNotFound(name)

        if name in self.__extensions:
            raise errors.ExtensionAlreadyLoaded(name)

        spec = importlib.util.find_spec(name, package)
        if spec is None:
            raise errors.ExtensionNotFound(name)

        self._load_from_module_spec(spec, name)

    def unload_extension(self, name: str, *, package: Optional[str] = None) -> None:
        """
        Unloads an extension.

        Any sub-clients added in an extension will be removed from that extension when it is unloaded.

        Optionally, an extension module can have a ``teardown`` function which will be called as a module is
        unloaded, which receives a single argument of a ``client``, either a :class:`SyncClient`
        or an :class:`AsyncClient`, similar to ``setup`` from :meth:`load_extension`.

        Registered extensions can be seen through the :attr:`extensions` property.

        Arguments
        ---------
            name: :py:class:`str`
                The name of the extension to load. This should be in the same format as a normal python import.
                For example, if you wanted to reference the ``extensions/submodule.py`` module, you would set the
                ``name`` parameter to ``extensions.submodule``.

        Keyword Args
        ------------
            package: Optional[:py:class:`str`]
                The name of the package to load relative imports from. For example, if a :paramref:`name` parameter
                is given as ``.submodule`` to reference the ``extensions/submodule.py`` extension, the ``package``
                parameter would be ``extensions``. Defaults to ``None``.

        Raises
        ------
            :class:`ExtensionNotFound`
                The extension could not be found. This usually means that the extension file could not be found.
            :class:`ExtensionNotLoaded`
                The extension is not loaded to the client, and therefore cannot be unloaded.
        """

        try:
            name = importlib.util.resolve_name(name, package)
        except ImportError:
            raise errors.ExtensionNotFound(name)

        lib = self.__extensions.get(name)
        if lib is None:
            raise errors.ExtensionNotLoaded(name)

        self._remove_module_reference(lib.__name__)
        self._call_module_finalizers(lib, name)

    def reload_extension(self, name: str, *, package: Optional[str] = None) -> None:
        """
        Unloads, and then loads an extension.

        This is the same as an :meth:`unload_extension` followed by a :meth:`load_extension`. If the reload fails,
        the client will roll-back to the previous working extension version.

        Registered extensions can be seen through the :attr:`extensions` property.

        Arguments
        ---------
            name: :py:class:`str`
                The name of the extension to load. This should be in the same format as a normal python import.
                For example, if you wanted to reference the ``extensions/submodule.py`` module, you would set the
                ``name`` parameter to ``extensions.submodule``.

        Keyword Args
        ------------
            package: Optional[:py:class:`str`]
                The name of the package to load relative imports from. For example, if a :paramref:`name` parameter
                is given as ``.submodule`` to reference the ``extensions/submodule.py`` extension, the ``package``
                parameter would be ``extensions``. Defaults to ``None``.

        Raises
        ------
            :class:`ExtensionNotFound`
                The extension could not be found. This usually means that the extension file could not be found.
            :class:`ExtensionNotLoaded`
                The extension is not loaded to the client, and therefore cannot be unloaded.
        """

        try:
            name = importlib.util.resolve_name(name, package)
        except ImportError:
            raise errors.ExtensionNotFound(name)

        lib = self.__extensions.get(name)
        if lib is None:
            raise errors.ExtensionNotLoaded(name)

        modules = {
            name: module
            for name, module in sys.modules.items()
            if _is_submodule(lib.__name__, name)
        }
        try:
            self._remove_module_reference(lib.__name__)
            self._call_module_finalizers(lib, name)
            self.load_extension(name)
        except Exception:
            lib.setup(self)
            self.__extensions[name] = lib

            sys.modules.update(modules)

    # ======================
    #   Private Methods
    # ======================
    def _init_branch(self) -> None:
        err = False

        template = 'The {msg} context is unavailable. '

        err_types = {
            'sync': 'Try installing it with "python -m pip install arya-api-framework[sync]".',
            'async': 'Try installing it with "python -m pip install arya-api-framework[sync]".',
            'client': 'Try installing with "python -m pip install arya-api-framework[<branch-name>]", with the '
                      '<branch-name> set to either "sync" or "async".'
        }

        msg = None
        if self._branch == ClientBranch.sync and not is_sync:
            err = errors.SyncClientError
            msg = 'sync'

        if self._branch == ClientBranch.async_ and not is_async:
            err = errors.AsyncClientError
            msg = 'async'

        if not self._branch:
            err = errors.ClientError
            msg = 'client'

        if err:
            raise err(template.format(msg=msg) + err_types[msg])

    def _init_logger(self) -> None:
        if self._branch == ClientBranch.sync:
            self.logger = logging.getLogger('arya_api_framework.SyncClient')
        elif self._branch == ClientBranch.async_:
            self.logger = logging.getLogger('arya_api_framework.AsyncClient')
        else:
            self.logger = logging.getLogger('arya_api_framework.NoBranch')

    @abc.abstractmethod
    def _init_rate_limit(self) -> None:
        pass

    def _init_session(self) -> None:
        if not self._session:
            if self._branch == ClientBranch.sync:
                self._session = Session()
                self._session.headers = self.headers
                self._session.cookies = cookiejar_from_dict(self.cookies)
                self._session.params = self.parameters
            elif self._branch == ClientBranch.async_:
                self._session = ClientSession(
                    self.uri_root,
                    headers=self.headers,
                    cookies=self.cookies
                )

    @abc.abstractmethod
    def _update_session_headers(self) -> None:
        pass

    @abc.abstractmethod
    def _update_session_cookies(self) -> None:
        pass

    @abc.abstractmethod
    def _update_session_parameters(self) -> None:
        pass

    def _remove_module_reference(self, name: str) -> None:
        pass

    def _call_module_finalizers(self, lib: 'ModuleType', key: str) -> None:
        try:
            func = getattr(lib, 'teardown')
        except AttributeError:
            pass
        else:
            try:
                func(self)
            except Exception:
                pass
        finally:
            self.__extensions.pop(key, None)
            sys.modules.pop(key, None)
            name = lib.__name__
            for module in list(sys.modules.keys()):
                if _is_submodule(name, module):
                    del sys.modules[module]

    def _load_from_module_spec(self, spec: importlib.machinery.ModuleSpec, key: str) -> None:
        lib = importlib.util.module_from_spec(spec)
        sys.modules[key] = lib

        try:
            spec.loader.exec_module(lib)
        except Exception as e:
            del sys.modules[key]
            raise errors.ExtensionFailed(key, e) from e

        try:
            setup = getattr(lib, 'setup')
        except AttributeError:
            del sys.modules[key]
            raise errors.ExtensionEntryPointError(key)

        try:
            setup(self)
        except Exception as e:
            del sys.modules[key]
            self._remove_module_reference(lib.__name__)
            self._call_module_finalizers(lib, key)
            raise errors.ExtensionFailed(key, e) from e
        else:
            self.__extensions[key] = lib
