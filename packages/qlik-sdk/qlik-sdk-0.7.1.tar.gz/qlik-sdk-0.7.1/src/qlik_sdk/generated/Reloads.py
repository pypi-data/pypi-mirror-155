# This is spectacularly generated code by spectacular v0.0.0 based on
# Reloads 2.2.1

from __future__ import annotations

from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Reload:
    """

    Attributes
    ----------
    appId: str
      The ID of the app.
    creationTime: str
      The time the reload job was created.
    id: str
      The ID of the reload.
    status: str
      The status of the reload (CREATED, QUEUED, RELOADING, FAILED, SUCCEEDED).
    tenantId: str
      The ID of the tenant who owns the reload.
    type: str
      The type of reload event (hub, chronos or external).
    userId: str
      The ID of the user who created the reload.
    duration: str
      The duration of the reload attempt - deprecated.
    endTime: str
      The time the reload job finished.
    engineTime: str
      The timestamp returned from the Sense engine upon successful reload.
    links: ReloadLinks
    log: str
      The log describing the result of the reload request.
    partial: bool
      The boolean value used to present the reload is partial or not
    startTime: str
      The time the reload job was consumed from the queue.
    """

    appId: str = None
    creationTime: str = None
    id: str = None
    status: str = None
    tenantId: str = None
    type: str = None
    userId: str = None
    duration: str = None
    endTime: str = None
    engineTime: str = None
    links: ReloadLinks = None
    log: str = None
    partial: bool = None
    startTime: str = None

    def __init__(self_, **kvargs):
        if "appId" in kvargs:
            if type(kvargs["appId"]).__name__ is self_.__annotations__["appId"]:
                self_.appId = kvargs["appId"]
            else:
                self_.appId = kvargs["appId"]
        if "creationTime" in kvargs:
            if (
                type(kvargs["creationTime"]).__name__
                is self_.__annotations__["creationTime"]
            ):
                self_.creationTime = kvargs["creationTime"]
            else:
                self_.creationTime = kvargs["creationTime"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "status" in kvargs:
            if type(kvargs["status"]).__name__ is self_.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "tenantId" in kvargs:
            if type(kvargs["tenantId"]).__name__ is self_.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ is self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        if "userId" in kvargs:
            if type(kvargs["userId"]).__name__ is self_.__annotations__["userId"]:
                self_.userId = kvargs["userId"]
            else:
                self_.userId = kvargs["userId"]
        if "duration" in kvargs:
            if type(kvargs["duration"]).__name__ is self_.__annotations__["duration"]:
                self_.duration = kvargs["duration"]
            else:
                self_.duration = kvargs["duration"]
        if "endTime" in kvargs:
            if type(kvargs["endTime"]).__name__ is self_.__annotations__["endTime"]:
                self_.endTime = kvargs["endTime"]
            else:
                self_.endTime = kvargs["endTime"]
        if "engineTime" in kvargs:
            if (
                type(kvargs["engineTime"]).__name__
                is self_.__annotations__["engineTime"]
            ):
                self_.engineTime = kvargs["engineTime"]
            else:
                self_.engineTime = kvargs["engineTime"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ReloadLinks(**kvargs["links"])
        if "log" in kvargs:
            if type(kvargs["log"]).__name__ is self_.__annotations__["log"]:
                self_.log = kvargs["log"]
            else:
                self_.log = kvargs["log"]
        if "partial" in kvargs:
            if type(kvargs["partial"]).__name__ is self_.__annotations__["partial"]:
                self_.partial = kvargs["partial"]
            else:
                self_.partial = kvargs["partial"]
        if "startTime" in kvargs:
            if type(kvargs["startTime"]).__name__ is self_.__annotations__["startTime"]:
                self_.startTime = kvargs["startTime"]
            else:
                self_.startTime = kvargs["startTime"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Href:
    """

    Attributes
    ----------
    href: str
    """

    href: str = None

    def __init__(self_, **kvargs):
        if "href" in kvargs:
            if type(kvargs["href"]).__name__ is self_.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ReloadLinks:
    """

    Attributes
    ----------
    self: Href
    """

    self: Href = None

    def __init__(self_, **kvargs):
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ is self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Href(**kvargs["self"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ReloadRequest:
    """

    Attributes
    ----------
    appId: str
      The ID of the app to be reloaded.
    partial: bool
      The boolean value used to present the reload is partial or not
    """

    appId: str = None
    partial: bool = None

    def __init__(self_, **kvargs):
        if "appId" in kvargs:
            if type(kvargs["appId"]).__name__ is self_.__annotations__["appId"]:
                self_.appId = kvargs["appId"]
            else:
                self_.appId = kvargs["appId"]
        if "partial" in kvargs:
            if type(kvargs["partial"]).__name__ is self_.__annotations__["partial"]:
                self_.partial = kvargs["partial"]
            else:
                self_.partial = kvargs["partial"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ReloadsClass:
    """

    Attributes
    ----------
    data: list[Reload]
    links: ReloadsLinks
    """

    data: list[Reload] = None
    links: ReloadsLinks = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [Reload(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ReloadsLinks(**kvargs["links"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ReloadsLinks:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Reloads:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_reloads(
        self,
        appId: str,
        next: str = None,
        prev: str = None,
        limit: int = 10,
        partial: bool = None,
        max_items: int = 10,
    ) -> ListableResource[Reload]:
        """
        Finds and returns the reloads that the user has access to.


        Authorization: str
          JWT containing tenant credentials.

        next: str
          The cursor to the next page of resources. Provide either the next or prev cursor, but not both.

        prev: str
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.

        limit: int
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).

        appId: str
          The UUID formatted string used to search for an app's reload history entries. TenantAdmin users may omit this parameter to list all reload history in the tenant.

        partial: bool
          The boolean value used to search for a reload is partial or not.

        Parameters
        ----------
        next: str = None
        prev: str = None
        limit: int = 10
        appId: str
        partial: bool = None
        """
        query_params = {}
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if limit is not None:
            query_params["limit"] = limit
        query_params["appId"] = appId
        if partial is not None:
            query_params["partial"] = partial

        response = self.auth.rest(
            path="/reloads",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Reload,
            auth=self.auth,
            path="/reloads",
            max_items=max_items,
            query_params=query_params,
        )

    def create(self, data: ReloadRequest) -> Reload:
        """
        Reloads an app specified by an app ID.


        Authorization: str
          JWT containing tenant credentials.

        Parameters
        ----------
        data: ReloadRequest
        """

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/reloads",
            method="POST",
            params={},
            data=data,
        )
        obj = Reload(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, reloadId: str) -> Reload:
        """
        Get reload record
        Finds and returns a reload record


        Authorization: str
          JWT containing tenant credentials.

        reloadId: str
          The unique identifier of the reload.

        Parameters
        ----------
        reloadId: str
        """

        response = self.auth.rest(
            path="/reloads/{reloadId}".replace("{reloadId}", reloadId),
            method="GET",
            params={},
            data=None,
        )
        obj = Reload(**response.json())
        obj.auth = self.auth
        return obj
