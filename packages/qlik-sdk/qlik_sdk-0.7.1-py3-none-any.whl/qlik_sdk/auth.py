import typing

import requests

from ._version import __version__
from .config import Config
from .rest import RestClient, RestClientInstance
from .rpc import RpcClient, RpcClientInstance


class Auth:
    """
    Auth can be used to make rest and rpc calls

    Parameters
    ----------
    config: Config
        the required configuration object

    Examples
    --------
    >>> from qlik_sdk import Auth, AuthType, Config
    ...
    ... clients = Auth(Config(host=base_url, auth_type=AuthType.APIKey, api_key=api_key))
    ... get_users_res = clients.rest(path="/users/me")
    """

    config: Config
    rest: RestClientInstance
    """
    rest method can be used to make raw calls against Qlik Cloud

    Parameters
    ----------
    app_id: str
    method: str, default GET
        string HTTP verb
    path: str
        representing the api endpoint ex: `/users/me`
    data: dict, optional
        Dictionary, list of tuples, bytes, or file-like object to send in the body of the Request.
    params: dict, optional
        Dictionary, list of tuples or bytes to send in the query string for the Request.
    headers: dict, optional
        Dictionary of HTTP Headers to send with the Request
    files: dict, optional
        Dictionary of {filename: fileobject} files to multipart upload.

    Attributes
    ----------
    interceptors: Interceptors

    Examples
    ----------
    >>> auth = Auth(Config(host=self.base_url, auth_type=AuthType.APIKey, api_key=self.api_key))
    ... user_me = auth.rest(path="/users/me")
    ...
    # And with interceptors.
    >>> auth = Auth(Config(host=self.base_url, auth_type=AuthType.APIKey, api_key=self.api_key))
    ... def log_req(req: requests.Request) -> requests.Request:
    ...     print(req)
    ...     return req
    ...
    ... auth.rpc.interceptors["request"].use(log_req)
    ... app_list = auth.rest(path="/items", params={"resourceType":"app", "limit": 100})
    """

    rpc: RpcClientInstance
    """
    rpc returns an RpcClient that can be used to
    connect to the engine for a specific app

    Parameters
    ----------
    app_id: str

    Attributes
    ----------
    interceptors: Interceptors

    Examples
    ----------
    >>> rpc_session = auth.rpc(app_id=session_app_id)
    ... with rpc_session.opn() as rpc_client:
    ...     app = rpc_client.send("OpenDoc", -1, session_app_id)
    ...
    # And with interceptors.
    >>> auth.rpc.interceptors["request"].use(log_req)
    ... rpc_session = auth.rpc(app_id=session_app_id)
    ...
    ... with rpc_session.open() as rpc_client:
    ...     app = rpc_client.send("OpenDoc", -1, session_app_id)
    """
    paginate_rest: typing.Callable[[str, str, typing.Dict, any], typing.Iterator[any]]

    def __init__(self, config: Config):
        config.validate()
        self.config = config
        self.rest = RestClientInstance(RestClient(config))

        # register the api-key-auth interceptor
        def add_api_key(req: requests.Request) -> requests.Request:
            req.headers["authorization"] = "Bearer " + self.config.api_key
            return req

        # register the user-agent interceptor
        def add_user_agent(req: requests.Request):
            # version without v in user-agent
            # consistent with format of version in qlik-cli-user-agent
            version = __version__[1:]
            req.headers["User-Agent"] = "qlik-sdk-python/" + version
            return req

        self.rest.interceptors["request"].use([add_api_key, add_user_agent])
        self.rpc_client = RpcClient(self.config)
        self.rpc = RpcClientInstance(self.rpc_client)
        self.paginate_rest = self.rest.paginate_rest
