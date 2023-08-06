from .auth import Auth
from .config import Config
from .generated import (
    Apps,
    Extensions,
    Items,
    Qix_Datafiles,
    Reloads,
    Spaces,
    Themes,
    Users,
)
from .rest import RestClientInstance
from .rpc import RpcClientInstance


class Qlik:
    """
    Qlik Class is the entry-point for the Qlik python Platform SDK

    Parameters
    ----------
    config: Config
        the required configuration object

    Examples
    --------
    >>> from qlik_sdk import Qlik
    ...
    ... qlik = Qlik(Config(host=base_url, auth_type=AuthType.APIKey, api_key=api_key))
    ... user_me = qlik.users.get_me()
    """

    config: Config
    auth: Auth
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
    # And with interceptors.
    >>> auth.rpc.interceptors["request"].use(log_req)
    ... rpc_session = auth.rpc(app_id=session_app_id)
    ...
    ... with rpc_session.open() as rpc_client:
    ...     app = rpc_client.send("OpenDoc", -1, session_app_id)
    """

    rest: RestClientInstance
    """
    rest method can be used to make raw calls against Qlik Cloud

    Parameters
    ----------
    app_id: str
    method: str
        HTTP verb default GET
    path: str
        represents the api endpoint ex: `/users/me`
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
    # And with interceptors.
    >>> auth = Auth(Config(host=self.base_url, auth_type=AuthType.APIKey, api_key=self.api_key))
    ... def log_req(req: requests.Request) -> requests.Request:
    ...     print(req)
    ...     return req
    ...
    ... auth.rpc.interceptors["request"].use(log_req)
    ... app_list = auth.rest(path="/items", params={"resourceType":"app", "limit": 100})
    """

    apps: Apps.Apps
    items: Items.Items
    spaces: Spaces.Spaces
    users: Users.Users
    extensions: Extensions.Extensions
    reloads: Reloads.Reloads
    themes: Themes.Themes
    datafiles: Qix_Datafiles.QixDatafiles

    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config=config)
        self.rest = self.auth.rest
        self.rpc = self.auth.rpc
        self.apps = Apps.Apps(config=config)
        self.extensions = Extensions.Extensions(config=config)
        self.items = Items.Items(config=config)
        self.spaces = Spaces.Spaces(config=config)
        self.users = Users.Users(config=config)
        self.reloads = Reloads.Reloads(config=config)
        self.themes = Themes.Themes(config=config)
        self.datafiles = Qix_Datafiles.QixDatafiles(config=config)
