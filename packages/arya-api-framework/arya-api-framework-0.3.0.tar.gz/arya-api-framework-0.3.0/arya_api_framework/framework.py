import abc
from collections.abc import Awaitable
import importlib.util
import json
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
from .utils import validate_type, flatten_params, flatten_obj, _is_submodule, _requires_parent, FrameworkEncoder


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
    from .async_framework import AsyncClient
    from .sync_framework import SyncClient

__all__ = [
    "ClientInternal",
    "SubClient"
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

SyncClientT = TypeVar('SyncClientT', bound='SyncClient')
AsyncClientT = TypeVar('AsyncClientT', bound='AsyncClient')
ClientT = Union[SyncClientT, AsyncClientT]

SubClientT = TypeVar('SubClientT', bound='SubClient')
DictStrSubClient = Dict[str, SubClientT]


# ======================
#       Classes
# ======================
class _ClientMeta(abc.ABCMeta):
    # ======================
    #   Private Attributes
    # ======================
    __extensions__: DictStrModule
    __branch__: Optional[ClientBranch]

    __base_uri__: Optional['URL']
    __headers__: Optional[DictStrAny]
    __cookies__: Optional[DictStrAny]
    __parameters__: Optional[DictStrAny]
    __error_responses__: Optional[ErrorResponses]
    __bearer_token__: Optional[str]
    __rate_limit__: Optional[Num]
    __rate_limit_interval__: Optional[Num]

    # ======================
    #    Initialization
    # ======================
    def __new__(mcs, *args: Any, **kwargs: Any) -> Any:
        name, bases, attrs = args

        uri = kwargs.pop('uri', None)

        if uri and validate_type(uri, str):
            uri = URL(uri.rstrip('/'))

        headers = kwargs.pop('headers', None)
        cookies = kwargs.pop('cookies', None)
        parameters = kwargs.pop('parameters', None)
        error_responses = kwargs.pop('error_responses', None)

        bearer_token: Union[str, SecretStr] = kwargs.pop('bearer_token', None)
        if bearer_token and validate_type(bearer_token, SecretStr, err=False):
            bearer_token = bearer_token.get_secret_value()

        rate_limit = kwargs.pop('rate_limit', None)
        if rate_limit:
            validate_type(rate_limit, [int, float])

        rate_limit_interval = kwargs.pop('rate_limit_interval', None)
        if rate_limit_interval:
            validate_type(rate_limit_interval, [int, float])

        extensions = kwargs.pop('extensions', None)

        attrs['__base_uri__'] = uri
        attrs['__headers__'] = headers
        attrs['__cookies__'] = cookies
        attrs['__parameters__'] = parameters
        attrs['__error_responses__'] = error_responses
        attrs['__bearer_token__'] = bearer_token
        attrs['__rate_limit__'] = rate_limit
        attrs['__rate_limit_interval__'] = rate_limit_interval
        attrs['__extensions__'] = extensions

        return super().__new__(mcs, name, bases, attrs)

    def __init__(cls, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args)


class ClientInternal(abc.ABC, metaclass=_ClientMeta):
    # ======================
    #   Private Attributes
    # ======================
    __base_uri__: Optional['URL']
    __headers__: Optional[DictStrAny]
    __cookies__: Optional[DictStrAny]
    __parameters__: Optional[DictStrAny]
    __error_responses__: Optional[ErrorResponses]
    __bearer_token__: Optional[str]
    __rate_limit__: Optional[Num]
    __rate_limit_interval__: Optional[Num]
    __extensions__: Optional[List[str]]

    __active_extensions: DictStrModule = {}
    __subclients: DictStrSubClient = {}

    _branch: Optional[ClientBranch] = None
    _closed: bool = False
    _rate_limited: bool = False
    _session: SessionT = None

    # ======================
    #   Public Attributes
    # ======================
    logger: logging.Logger

    # ======================
    #    Initialization
    # ======================
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        self = super().__new__(cls)

        self._init_logger()
        self.logger.debug("Verifying class.")

        if not self.__base_uri__:
            raise errors.ClientError(
                "The client needs a \"uri\" subclass parameter specified."
            )
        elif not self.__base_uri__.is_absolute():
            raise ValueError(
                "The \"uri\" parameter must be an absolute url location, not relative."
            )
        self.logger.debug("URI is valid.")

        self._init_branch()
        self.logger.debug('Branch is valid.')

        self.headers = self.__headers__
        self.cookies = self.__cookies__
        self.parameters = self.__parameters__
        self.error_responses = self.__error_responses__
        if self.__bearer_token__:
            self.headers['Authorization'] = f'Bearer {self.__bearer_token__}'

        self.logger.debug('Default request settings set.')

        if self.__rate_limit_interval__ is None:
            self.__rate_limit_interval__ = 1
        self._init_rate_limit()
        if self.rate_limited:
            self.logger.debug('Rate limit set.' if self.rate_limited else 'No rate limit given, skipped.')

        self._init_session()

        self._load_default_extensions()
        self.logger.debug('Loaded default extensions.')

        return self

    # ======================
    #     Dunder Methods
    # ======================
    def __getattr__(self, item: str) -> Optional[SubClientT]:
        return self.__subclients.get(item, None)

    # ======================
    #      Properties
    # ======================
    # General Information
    @property
    def branch(self) -> ClientBranch:
        return self._branch

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def extensions(self) -> Mapping[str, 'ModuleType']:
        return MappingProxyType(self.__active_extensions)

    @property
    def subclients(self) -> Mapping[str, SubClientT]:
        return MappingProxyType(self.__subclients)

    # URI Options
    @property
    def uri(self) -> Optional[str]:
        return str(self.__base_uri__) if self.__base_uri__ else None

    @property
    def uri_root(self) -> Optional[str]:
        return str(self.__base_uri__.origin()) if self.__base_uri__ else None

    @property
    def uri_path(self) -> Optional[str]:
        return str(self.__base_uri__.relative()) if self.__base_uri__ else None

    # Default Request Settings
    @property
    def headers(self) -> Optional[Headers]:
        return self.__headers__

    @headers.setter
    def headers(self, headers: Headers) -> None:
        self.__headers__ = flatten_obj(headers) or {}
        self._update_session_headers()

    @property
    def cookies(self) -> Optional[Cookies]:
        return self.__cookies__

    @cookies.setter
    def cookies(self, cookies: Cookies) -> None:
        self.__cookies__ = flatten_obj(cookies) or {}
        self._update_session_cookies()

    @property
    def parameters(self) -> Optional[Parameters]:
        return self.__parameters__

    @parameters.setter
    def parameters(self, parameters: Parameters) -> None:
        self.__parameters__ = flatten_params(parameters) or {}
        self._update_session_parameters()

    @property
    def error_responses(self) -> Optional[ErrorResponses]:
        return self.__error_responses__

    @error_responses.setter
    def error_responses(self, error_responses: ErrorResponses) -> None:
        self.__error_responses__ = error_responses or {}

    # Rate Limits
    @property
    def rate_limit(self) -> Optional[Num]:
        return self.__rate_limit__

    @property
    def rate_limit_interval(self) -> Optional[Num]:
        return self.__rate_limit_interval__

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
            path: str = '',
            /,
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
        pass

    @abc.abstractmethod
    def stream_file(
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
        pass

    @abc.abstractmethod
    def get(
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
        pass

    @abc.abstractmethod
    def post(
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
        pass

    @abc.abstractmethod
    def patch(
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
        pass

    @abc.abstractmethod
    def put(
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
        pass

    @abc.abstractmethod
    def delete(
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

        if name in self.__active_extensions:
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

        lib = self.__active_extensions.get(name)
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

        lib = self.__active_extensions.get(name)
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
            self.__active_extensions[name] = lib

            sys.modules.update(modules)

    def add_subclient(self, subclient: SubClientT) -> None:
        """Loads a :class:`SubClient` as a child route of the primary client. Loaded sub-clients can be viewed through
        :attr:`subclients`.

        Note
        ----
            Any :class:`SubClient` must meet a few requirements in order to be added to a parent:
                * The SubClient cannot already be loaded to a different parent.
                * The SubClient cannot already be loaded to the current parent.
                * The SubClient cannot be loaded to itself as a parent.

        Arguments
        ---------
            subclient: :class:`SubClient`
                The sub-client to add as a child of the parent client tree.

        Raises
        ------
            :exc:`ValueError`
                Raised if the :paramref:`subclient` is not a :class:`SubClient`.
            :class:`errors.SubClientError`
                Raised if the :paramref:`subclient` is added as a child of itself.
            :class:`errors.SubClientAlreadyLoaded`
                Raised if the :paramref:`subclient` is already loaded to the current client.
            :class:`errors.SubClientParentSet`
                Raised if the :paramref:`subclient` already has a :attr:`parent <SubCLient.parent>` set.
        """
        if not isinstance(subclient, SubClient):
            raise ValueError(
                'The given "subclient" parameter to add must be an instance of a subclass of a "SubClient".'
            )

        if subclient == self:
            raise errors.SubClientError(
                'Some people just want to watch the world burn... '
                f'Don\'t try to set a {subclient.name!r} as its own child.',
                name=subclient.name
            )
        if subclient.name in self.__subclients:
            raise errors.SubClientAlreadyLoaded(subclient.name)
        if subclient.parent is not None:
            raise errors.SubClientParentSet(subclient.name)
        subclient._parent = self
        self.__subclients[subclient.name] = subclient

        subclient.on_loaded()

    def remove_subclient(self, name: str) -> Optional[SubClientT]:
        """Removes a loaded child :class:`SubClient` from the primary client. Loaded sub-clients can be viewed through
        :attr:`subclients`.

        Arguments
        ---------
            name: :py:class:`str`
                The name of the :class:`SubClient` to remove as a child of the parent client tree. This should
                correspond to the :attr`name <SubClient.name>` attribute of the sub-client.

        Returns
        -------
            Optional[:class:`SubClient`]
                The :class:`SubClient` that was unloaded, if one was.
        """

        subclient = self.__subclients.pop(name, None)
        if subclient is None:
            return

        subclient._parent = None

        subclient._teardown()

        subclient.on_unloaded()

        return subclient

    def tree(
            self,
            serialized: Optional[bool] = False,
            indent: Optional[int] = None
    ) -> Union[Dict, str]:
        """Gets meta-information about the client and all :class:`SubClients <SubClient>` registered to the client.
        This includes information about endpoints attached to individual request methods using the
        :deco:`@apiclient <utils.apiclient>` and :deco:`@endpoint() <utils.endpoint>` decorators.

        Arguments
        ---------
            serialized: :py:class:`bool`
                Whether or not to serialized the resulting tree into a string. Defaults to ``False``.
            indent: :py:class:`int`
                The indentation to use for pretty printing serialized data. Only applies if
                :paramref:`serialized` is ``True``. This parameter is directly passed to the
                :py:func:`json.dumps` ``indent`` parameter. Defaults to ``None``, returning a single-line string.

        Returns
        -------
            Union[:py:class:`dict`, :py:class:`str`]
                The client tree dictionary, or the serialized client tree dictionary.
        """

        trunk = {'root': {
            "__info__": {
                "uri": self.uri,
                "uri_root": self.uri_root,
            },
            "__endpoints__": getattr(self, '__endpoints__'),
            "__subclients__": {}
        }}

        for n, cl in self.subclients.items():
            trunk['root']['__subclients__'][n] = cl.tree(serialized, indent, False)

        if serialized:
            if indent:
                return json.dumps(trunk, cls=FrameworkEncoder, indent=indent)
            return json.dumps(trunk, cls=FrameworkEncoder)
        return trunk

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
        if self._branch == ClientBranch.sync:
            if not is_sync:
                err = errors.SyncClientError
                msg = 'sync'

        elif self._branch == ClientBranch.async_:
            if not is_async:
                err = errors.AsyncClientError
                msg = 'async'

        else:
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
        self.logger.debug(f'Logger created: {self.logger.name}')

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
            self.logger.debug('Request session created.')
        else:
            self.logger.warning('The client session already exists, skipping creation.')

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
        for subclient_name, subclient in self.__subclients.copy().items():
            if _is_submodule(name, subclient.__module__):
                self.remove_subclient(subclient_name)

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
            self.__active_extensions.pop(key, None)
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
            self.__active_extensions[key] = lib

    def _load_default_extensions(self) -> None:
        if self.__extensions__:
            for ext in self.__extensions__:
                if isinstance(ext, str):
                    self.load_extension(ext)
                elif isinstance(ext, tuple):
                    self.load_extension(ext[0], package=ext[1])

    def _teardown(self) -> None:
        for extension in tuple(self.__active_extensions):
            try:
                self.unload_extension(extension)
            except Exception:
                pass

        for n, _ in self.__subclients:
            self.remove_subclient(n)


class _SubClientMeta(abc.ABCMeta):
    __subclient_name__: str
    __relative_path__: Optional[str]

    def __new__(mcs, *args: Any, **kwargs: Any) -> Any:
        name, bases, attrs = args

        subclient_name = kwargs.pop('name', name)
        relative_path = kwargs.pop('relative_path', '')

        if relative_path and validate_type(relative_path, str) or relative_path == '':
            if URL(relative_path).is_absolute():
                raise ValueError('The path must be relative, not absolute.')
            relative_path = URL(relative_path.strip('/'))

        attrs['__subclient_name__'] = subclient_name
        attrs['__relative_path__'] = relative_path

        new = super().__new__(mcs, name, bases, attrs)

        return new

    def __init__(cls, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args)


class SubClient(metaclass=_SubClientMeta):
    """
    The secondary API framework client for itemizing and keeping code clean.

    By creating "SubClients" that are subclassed from this class, it is possible to add modules to
    the overall API structure in a relatively simply way.

    Additionally, sub-clients can be nested, allowing for a tree structure that can encompass an entire API
    interface. For more information on modular development with the library, see the :ref:`sub-client-guide`.

    Warning
    -------
        All of the configuration for this class and its subclasses are done through subclass parameters.
        This means that the ``__init__`` method is free reign for you to use as you see fit. The parameters
        shown below are specifically for subclass parameters only.

        .. code-block:: python
            :caption: Example:

            class MySubClient(SubClient, name='sub_client_module', relative_path='/example'):
                pass

    Parameters
    ----------
        name: Optional[:py:class:`str`]
            The name to use for the class internally. This name must be a valid variable name. By using this,
            the name of each individual sub-client can be managed more directly then through the class name, maintaining
            proper code guidelines while also being user-friendly. By default, this is set to ``None``, and the
            :attr:`name` parameter will reference the name of the class.
        relative_path: Optional[:py:class:`str`]
            The relative path from the root URI of the entire API client. For example, if the root URI is
            ``https://example.com/api``, a :class:`SubClient` with a :paramref:`relative_path` set to ``/get`` will
            access the ``https://example.com/api/get`` route for all endpoints within that sub-client. Additionally,
            nested sub-clients will reference their relative paths according to the parent sub-client.

    Attributes
    ----------
        name: :py:class:`str`
            * |readonly|

            The name of the sub-client. This is either the :paramref:`name` subclass parameter, or the
            ``__name__`` attribute of the class itself.
        qualified_name: :py:class:`str`
            * |readonly|

            The full name of the sub-client, showing its location in the overall API structure using the
            ``.`` method, like ``subclient1.subclient2.this_subclient``.
        relative_path: :py:class:`yarl.URL`
            * |readonly|

            A :resource:`yarl <yarl>` URL that contains a relative url path from the :attr:`parent` client or
            sub-client. This is set in the :paramref:`relative_path` subclass parameter, or set to
            the parent URI by default.
        full_relative_path: :py:class:`yarl.URL`
            * |readonly|

            A :resource:`yarl <yarl>` URL that contains the relative path from the base client's :attr:`SyncClient.uri`
            attribute.
        qualified_path: :py:class:`yarl.URL`
            * |readonly|

            A :resource:`yarl <yarl>` URL that contains the full URL path to the resource, includig the root URL.
        parent: Union[:class:`SyncClient`, :class:`AsyncClient`, :class:`SubClient`]
            * |readonly|

            The parent client of the sub-client. This gets set automatically when calling :meth:`add_subclient`.
            This is set to ``None`` by default, and gets reset to ``None`` if the module or client is ever unloaded.

        subclients: Mapping[:py:class:`str`, :class:`SubClient`]
            * |readonly|

            A mapping of :attr:`name` to :class:`SubClient` for all registered sub-clients of the current client.
            Registry is updated automatically when calling :meth:`add_subclient` or :meth:`remove_subclient`.
    """

    # ======================
    #   Private Attributes
    # ======================
    __subclient_name__: str
    __relative_path__: Optional[URL]

    __subclients: DictStrSubClient

    _parent: Optional[Union[ClientT, 'SubClient']] = None

    # ======================
    #    Initialization
    # ======================
    def __new__(cls, *args, **kwargs: Any) -> Any:
        self = super().__new__(cls)

        self.__subclients = {}

        return self

    # ======================
    #     Dunder Methods
    # ======================
    def __getattr__(self, item: str) -> Optional[SubClientT]:
        return self.__subclients.get(item, None)

    # ======================
    #      Properties
    # ======================
    @property
    def name(self) -> str:
        return self.__subclient_name__

    @property
    def qualified_name(self) -> Optional[str]:
        if not self.parent or isinstance(self.parent, ClientInternal):
            return self.name

        return f'{self.parent.qualified_name}.{self.name}'

    @property
    def relative_path(self) -> Optional[URL]:
        return self.__relative_path__

    @property
    def full_relative_path(self) -> Optional[URL]:
        if not self.parent or isinstance(self.parent, ClientInternal):
            return self.relative_path
        return self.parent.full_relative_path / str(self.relative_path)

    @property
    def qualified_path(self) -> Optional[URL]:
        if not self.parent:
            return
        if isinstance(self.parent, ClientInternal):
            return URL(self.parent.uri) / str(self.relative_path)
        if self.parent.qualified_path:
            return self.parent.qualified_path / str(self.relative_path)

    @property
    def parent(self) -> Union[ClientT, 'SubClient']:
        return self._parent

    @property
    def subclients(self) -> Mapping[str, SubClientT]:
        return MappingProxyType(self.__subclients)

    # ======================
    #    Request Methods
    # ======================
    @_requires_parent
    def request(
            self,
            method: str,
            path: str = '',
            /,
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
    ) -> Optional[Union[RequestResponse, Awaitable[RequestResponse]]]:
        """
        * |maybecoro|
        * |validated_method|
        * |rate_limited_method|

        This calls either :meth:`SyncClient.request` or :meth:`AsyncClient.request`, depending on whether the
        core client of the application is either of those types. For specifics, view those documentations.

        Arguments
        ---------
            method: :py:class:`str`
                * |positional|

                The request method to use for the request (see :ref:`http-requests`).
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`relative_path`, to send the request to. If this is not
                provided, the sub-client's :attr:`full_relative_path` is used.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                * |kwargonly|

                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            files: Optional[:py:class:`dict`]
                * |kwargonly|

                A mapping of :py:class:`str` file names to file objects to send in the request.
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers <SyncClient.headers>`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies <SyncClient.cookies>`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters <SyncClient.parameters>`.
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
                :attr:`error_responses <SyncClient.error_responses>` is also ``None``, or a status code does not have a
                specified response format, the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """

        if isinstance(self.parent, ClientInternal) and self.parent.branch == ClientBranch.async_:
            return self.parent.request(
                method,
                str(self.relative_path / path.lstrip('/')),
                body=body,
                data=data,
                headers=headers,
                cookies=cookies,
                parameters=parameters,
                response_format=response_format,
                timeout=timeout,
                error_responses=error_responses
            )

        return self.parent.request(
            method,
            str(self.relative_path / path.lstrip('/')),
            body=body,
            data=data,
            files=files,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses
        )

    @_requires_parent
    def upload_file(
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
    ) -> Optional[Union[RequestResponse, Awaitable[RequestResponse]]]:
        """
        * |maybecoro|
        * |validated_method|
        * |rate_limited_method|

        This calls either :meth:`SyncClient.upload_file` or :meth:`AsyncClient.upload_file`, depending on whether the
        core client of the application is either of those types. For specifics, view those documentations.

        Arguments
        ---------
            file: :py:class:`str`
                * |positional|

                The path to the file to upload.
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`relative_path`, to send the request to. If this is not
                provided, the sub-client's :attr:`full_relative_path` is used.

        Keyword Args
        ------------
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers <SyncClient.headers>`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies <SyncClient.cookies>`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters <SyncClient.parameters>`.
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
                :attr:`error_responses <SyncClient.error_responses>` is also ``None``, or a status code does not have a
                specified response format, the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return self.parent.upload_file(
            file,
            str(self.relative_path / path.lstrip('/')),
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses
        )

    @_requires_parent
    def stream_file(
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
    ) -> Optional[Union[RequestResponse, Awaitable[RequestResponse]]]:
        """
        * |maybecoro|
        * |validated_method|
        * |rate_limited_method|

        This calls either :meth:`SyncClient.stream_file` or :meth:`AsyncClient.stream_file`, depending on whether the
        core client of the application is either of those types. For specifics, view those documentations.

        Arguments
        ---------
            file: :py:class:`str`
                * |positional|

                The path to the file to upload.
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`relative_path`, to send the request to. If this is not
                provided, the sub-client's :attr:`full_relative_path` is used.

        Keyword Args
        ------------
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers <SyncClient.headers>`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies <SyncClient.cookies>`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters <SyncClient.parameters>`.
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
                :attr:`error_responses <SyncClient.error_responses>` is also ``None``, or a status code does not have a
                specified response format, the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return self.parent.stream_file(
            file,
            str(self.relative_path / path.lstrip('/')),
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses
        )

    @_requires_parent
    def get(
            self,
            path: str = '',
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            parameters: Parameters = None,
            response_format: Type[Response] = None,
            timeout: int = 300,
            error_responses: ErrorResponses = None
    ) -> Optional[Union[RequestResponse, Awaitable[RequestResponse]]]:
        """
        * |maybecoro|
        * |validated_method|
        * |rate_limited_method|

        This calls either :meth:`SyncClient.get` or :meth:`AsyncClient.get`, depending on whether the
        core client of the application is either of those types. For specifics, view those documentations.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`relative_path`, to send the request to. If this is not
                provided, the sub-client's :attr:`full_relative_path` is used.

        Keyword Args
        ------------
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers <SyncClient.headers>`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies <SyncClient.cookies>`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters <SyncClient.parameters>`.
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
                :attr:`error_responses <SyncClient.error_responses>` is also ``None``, or a status code does not have a
                specified response format, the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return self.parent.get(
            str(self.relative_path / path.lstrip('/')),
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses
        )

    @_requires_parent
    def post(
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
    ) -> Optional[Union[RequestResponse, Awaitable[RequestResponse]]]:
        """
        * |maybecoro|
        * |validated_method|
        * |rate_limited_method|

        This calls either :meth:`SyncClient.post` or :meth:`AsyncClient.post`, depending on whether the
        core client of the application is either of those types. For specifics, view those documentations.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`relative_path`, to send the request to. If this is not
                provided, the sub-client's :attr:`full_relative_path` is used.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                * |kwargonly|

                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers <SyncClient.headers>`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies <SyncClient.cookies>`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters <SyncClient.parameters>`.
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
                :attr:`error_responses <SyncClient.error_responses>` is also ``None``, or a status code does not have a
                specified response format, the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return self.parent.post(
            str(self.relative_path / path.lstrip('/')),
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses
        )

    @_requires_parent
    def patch(
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
    ) -> Optional[Union[RequestResponse, Awaitable[RequestResponse]]]:
        """
        * |maybecoro|
        * |validated_method|
        * |rate_limited_method|

        This calls either :meth:`SyncClient.patch` or :meth:`AsyncClient.patch`, depending on whether the
        core client of the application is either of those types. For specifics, view those documentations.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`relative_path`, to send the request to. If this is not
                provided, the sub-client's :attr:`full_relative_path` is used.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                * |kwargonly|

                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers <SyncClient.headers>`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies <SyncClient.cookies>`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters <SyncClient.parameters>`.
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
                :attr:`error_responses <SyncClient.error_responses>` is also ``None``, or a status code does not have a
                specified response format, the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return self.parent.patch(
            str(self.relative_path / path.lstrip('/')),
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses
        )

    @_requires_parent
    def put(
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
    ) -> Optional[Union[RequestResponse, Awaitable[RequestResponse]]]:
        """
        * |maybecoro|
        * |validated_method|
        * |rate_limited_method|

        This calls either :meth:`SyncClient.put` or :meth:`AsyncClient.put`, depending on whether the
        core client of the application is either of those types. For specifics, view those documentations.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`relative_path`, to send the request to. If this is not
                provided, the sub-client's :attr:`full_relative_path` is used.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                * |kwargonly|

                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers <SyncClient.headers>`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies <SyncClient.cookies>`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters <SyncClient.parameters>`.
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
                :attr:`error_responses <SyncClient.error_responses>` is also ``None``, or a status code does not have a
                specified response format, the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return self.parent.put(
            str(self.relative_path / path.lstrip('/')),
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses
        )

    @_requires_parent
    def delete(
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
    ) -> Optional[Union[RequestResponse, Awaitable[RequestResponse]]]:
        """
        * |maybecoro|
        * |validated_method|
        * |rate_limited_method|

        This calls either :meth:`SyncClient.delete` or :meth:`AsyncClient.delete`, depending on whether the
        core client of the application is either of those types. For specifics, view those documentations.

        Arguments
        ---------
            path: Optional[:py:class:`str`]
                * |positional|

                The path, relative to the client's :attr:`relative_path`, to send the request to. If this is not
                provided, the sub-client's :attr:`full_relative_path` is used.

        Keyword Args
        ------------
            body: Optional[Union[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Optional data to send as a JSON structure in the body of the request. Defaults to ``None``.
            data: Optional[:py:class:`Any`]
                * |kwargonly|

                Optional data of any type to send in the body of the request, without any pre-processing. Defaults to
                ``None``.
            headers: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific headers to send with the request. Defaults to ``None`` and uses the
                default client :attr:`headers <SyncClient.headers>`.
            cookies: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific cookies to send with the request. Defaults to ``None`` and uses the default
                client :attr:`cookies <SyncClient.cookies>`.
            parameters: Optional[:py:class:`dict`, :class:`BaseModel`]
                * |kwargonly|

                Request-specific query string parameters to send with the request. Defaults to ``None`` and
                uses the default client :attr:`parameters <SyncClient.parameters>`.
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
                :attr:`error_responses <SyncClient.error_responses>` is also ``None``, or a status code does not have a
                specified response format, the default status code exceptions will be raised.

        Returns
        -------
            Optional[Union[:py:class:`dict`, :class:`Response`]]
                The request response JSON, loaded into the :paramref:`response_format` model if provided, or as a raw
                :py:class:`dict` otherwise.
        """
        return self.parent.delete(
            str(self.relative_path / path.lstrip('/')),
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            parameters=parameters,
            response_format=response_format,
            timeout=timeout,
            error_responses=error_responses
        )

    # ======================
    #    General Methods
    # ======================
    def on_loaded(self) -> None:
        """A hook that is called when the :class:`SubClient` is added to a parent. Has no implementation at
        default, so this is for any extra internal setup that a sub-client might need to do after gaining access
        to the parent client tree.
        """
        pass

    def on_unloaded(self) -> None:
        """A hook that is called when the :class:`SubClient` is removed from a parent. Has no implementation at
        default.
        """
        pass

    def add_subclient(self, subclient: SubClientT) -> None:
        if not isinstance(subclient, SubClient):
            raise ValueError(
                'The given "subclient" parameter to add must be an instance of a subclass of a "SubClient".'
            )

        if subclient == self:
            raise errors.SubClientError(
                'Some people just want to watch the world burn... '
                f'Don\'t try to set a {subclient.name!r} as its own child.',
                name=subclient.name
            )
        if subclient.name in self.subclients:
            raise errors.SubClientAlreadyLoaded(subclient.name)
        if subclient.parent is not None:
            raise errors.SubClientParentSet(subclient.name)
        subclient._parent = self
        self.__subclients[subclient.name] = subclient

    def remove_subclient(self, name: str) -> Optional[SubClientT]:
        subclient: SubClient = self.__subclients.pop(name, None)
        if subclient is None:
            return

        subclient._parent = None

        subclient._teardown()

        subclient.on_unloaded()

        return subclient

    def tree(
            self,
            serialized: Optional[bool] = False,
            indent: Optional[int] = None,
            _root: Optional[bool] = True
    ) -> Union[Dict, str]:
        """Gets meta-information about the sub-client and all :class:`SubClients <SubClient>` registered to the client.
        This includes information about endpoints attached to individual request methods using the
        :deco:`@apiclient <utils.apiclient>` and :deco:`@endpoint() <utils.endpoint>` decorators.

        Arguments
        ---------
            serialized: :py:class:`bool`
                Whether or not to serialized the resulting tree into a string. Defaults to ``False``.
            indent: :py:class:`int`
                The indentation to use for pretty printing serialized data. Only applies if
                :paramref:`serialized` is ``True``. This parameter is directly passed to the
                :py:func:`json.dumps` ``indent`` parameter. Defaults to ``None``, returning a single-line string.

        Returns
        -------
            Union[:py:class:`dict`, :py:class:`str`]
                The client tree dictionary, or the serialized client tree dictionary.
        """

        trunk = {
            "__info__": {
                "qualified_name": self.qualified_name,
                "qualified_path": str(self.qualified_path),
                "full_relative_path": str(self.full_relative_path),
                "relative_path": str(self.relative_path)
            },
            "__endpoints__": getattr(self, '__endpoints__'),
            "__subclients__": {}
        }
        for n, cl in self.subclients.items():
            trunk["__subclients__"][n] = cl.tree(serialized, indent, False)

        if serialized and _root:
            if indent:
                return json.dumps(trunk, cls=FrameworkEncoder, indent=indent)
            return json.dumps(trunk, cls=FrameworkEncoder)
        return trunk

    # ======================
    #    Private Methods
    # ======================
    def _teardown(self) -> None:
        for n, _ in self.__subclients.items():
            self.remove_subclient(n)
