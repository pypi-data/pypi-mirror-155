# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services 0.348.2

from __future__ import annotations

import warnings
from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Space:
    """
    A space is a security context simplifying the management of access control by allowing users to control it on the containers instead of on the resources themselves.

    Attributes
    ----------
    id: str
      A unique identifier for the space, for example, 62716f4b39b865ece543cd45.
    links: object
    name: str
      The name of the space. Personal spaces do not have a name.
    tenantId: str
      The ID for the tenant, for example, xqGQ0k66vSR8f9G7J-vYtHZQkiYrCpct.
    createdAt: str
      The date and time when the space was created.
    createdBy: str
      The ID of the user who created the space.
    description: str
      The description of the space. Personal spaces do not have a description.
    meta: object
      Information about the space settings.
    ownerId: str
      The ID for the space owner.
    type: str
      The type of space such as shared, managed, and so on.
    updatedAt: str
      The date and time when the space was updated.
    """

    id: str = None
    links: object = None
    name: str = None
    tenantId: str = None
    createdAt: str = None
    createdBy: str = None
    description: str = None
    meta: object = None
    ownerId: str = None
    type: str = None
    updatedAt: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "tenantId" in kvargs:
            if type(kvargs["tenantId"]).__name__ is self_.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ is self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "createdBy" in kvargs:
            if type(kvargs["createdBy"]).__name__ is self_.__annotations__["createdBy"]:
                self_.createdBy = kvargs["createdBy"]
            else:
                self_.createdBy = kvargs["createdBy"]
        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                is self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ is self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = kvargs["meta"]
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ is self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ is self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        if "updatedAt" in kvargs:
            if type(kvargs["updatedAt"]).__name__ is self_.__annotations__["updatedAt"]:
                self_.updatedAt = kvargs["updatedAt"]
            else:
                self_.updatedAt = kvargs["updatedAt"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def delete(self) -> None:
        """
        Deletes a space.

        Parameters
        ----------
        """

        self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patch(self, data: SpacePatch) -> Space:
        """
        Experimental
        Patches (updates) a space (partially).

        Parameters
        ----------
        data: SpacePatch
        """
        warnings.warn("patch is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", self.id),
            method="PATCH",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def set(self, data: SpaceUpdate) -> Space:
        """
        Experimental
        Updates a space.

        Parameters
        ----------
        data: SpaceUpdate
        """
        warnings.warn("set is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", self.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def get_assignments(
        self, limit: int = 10, next: str = None, prev: str = None, max_items: int = 10
    ) -> ListableResource[Assignment]:
        """
        Retrieves the assignments of the space matching the query.

        Parameters
        ----------
        limit: int = 10
        next: str = None
        prev: str = None
        """
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev

        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments".replace("{spaceId}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Assignment,
            auth=self.auth,
            path="/spaces/{spaceId}/assignments".replace("{spaceId}", self.id),
            max_items=max_items,
            query_params=query_params,
        )

    def create_assignment(self, data: AssignmentCreate) -> Assignment:
        """
        Creates an assignment.

        Parameters
        ----------
        data: AssignmentCreate
        """

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments".replace("{spaceId}", self.id),
            method="POST",
            params={},
            data=data,
        )
        obj = Assignment(**response.json())
        obj.auth = self.auth
        return obj

    def get_shares(
        self,
        name: str = None,
        resourceId: str = None,
        resourceType: str = None,
        groupId: str = None,
        userId: str = None,
        limit: int = 10,
        next: str = None,
        prev: str = None,
        max_items: int = 10,
    ) -> ListableResource[Share]:
        """
        Experimental
        Retrieves the shares of the space matching the query.

        Parameters
        ----------
        name: str = None
        resourceId: str = None
        resourceType: str = None
        groupId: str = None
        userId: str = None
        limit: int = 10
        next: str = None
        prev: str = None
        """
        warnings.warn("get_shares is experimental", UserWarning, stacklevel=2)
        query_params = {}
        if name is not None:
            query_params["name"] = name
        if resourceId is not None:
            query_params["resourceId"] = resourceId
        if resourceType is not None:
            query_params["resourceType"] = resourceType
        if groupId is not None:
            query_params["groupId"] = groupId
        if userId is not None:
            query_params["userId"] = userId
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev

        response = self.auth.rest(
            path="/spaces/{spaceId}/shares".replace("{spaceId}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Share,
            auth=self.auth,
            path="/spaces/{spaceId}/shares".replace("{spaceId}", self.id),
            max_items=max_items,
            query_params=query_params,
        )

    def create_share(self, data: ShareCreate) -> Share:
        """
        Experimental
        Creates a share.

        Parameters
        ----------
        data: ShareCreate
        """
        warnings.warn("create_share is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/spaces/{spaceId}/shares".replace("{spaceId}", self.id),
            method="POST",
            params={},
            data=data,
        )
        obj = Share(**response.json())
        obj.auth = self.auth
        return obj


@dataclass
class Assignment:
    """

    Attributes
    ----------
    assigneeId: str
      The userId or groupId based on the type.
    id: str
    links: object
    roles: list[str]
      The roles assigned to a user or group. Must not be empty.
    spaceId: str
      The unique identifier for the space.
    tenantId: str
      The unique identifier for the tenant.
    type: str
    createdAt: str
      The date and time when the space was created.
    createdBy: str
      The ID of the user who created the assignment.
    updatedAt: str
      The date and time when the space was updated.
    updatedBy: str
      The ID of the user who updated the assignment.
    """

    assigneeId: str = None
    id: str = None
    links: object = None
    roles: list[str] = None
    spaceId: str = None
    tenantId: str = None
    type: str = None
    createdAt: str = None
    createdBy: str = None
    updatedAt: str = None
    updatedBy: str = None

    def __init__(self_, **kvargs):
        if "assigneeId" in kvargs:
            if (
                type(kvargs["assigneeId"]).__name__
                is self_.__annotations__["assigneeId"]
            ):
                self_.assigneeId = kvargs["assigneeId"]
            else:
                self_.assigneeId = kvargs["assigneeId"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ is self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
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
        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ is self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "createdBy" in kvargs:
            if type(kvargs["createdBy"]).__name__ is self_.__annotations__["createdBy"]:
                self_.createdBy = kvargs["createdBy"]
            else:
                self_.createdBy = kvargs["createdBy"]
        if "updatedAt" in kvargs:
            if type(kvargs["updatedAt"]).__name__ is self_.__annotations__["updatedAt"]:
                self_.updatedAt = kvargs["updatedAt"]
            else:
                self_.updatedAt = kvargs["updatedAt"]
        if "updatedBy" in kvargs:
            if type(kvargs["updatedBy"]).__name__ is self_.__annotations__["updatedBy"]:
                self_.updatedBy = kvargs["updatedBy"]
            else:
                self_.updatedBy = kvargs["updatedBy"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentCreate:
    """

    Attributes
    ----------
    assigneeId: str
      The userId or groupId based on the type.
    roles: list[str]
      The roles assigned to the assigneeId.
    type: str
      The type of space such as shared, managed, and so on.
    """

    assigneeId: str = None
    roles: list[str] = None
    type: str = None

    def __init__(self_, **kvargs):
        if "assigneeId" in kvargs:
            if (
                type(kvargs["assigneeId"]).__name__
                is self_.__annotations__["assigneeId"]
            ):
                self_.assigneeId = kvargs["assigneeId"]
            else:
                self_.assigneeId = kvargs["assigneeId"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ is self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ is self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentUpdate:
    """

    Attributes
    ----------
    roles: list[str]
      The roles assigned to the assigneeId.
    """

    roles: list[str] = None

    def __init__(self_, **kvargs):
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ is self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Assignments:
    """

    Attributes
    ----------
    data: list[Assignment]
    links: object
    meta: object
    """

    data: list[Assignment] = None
    links: object = None
    meta: object = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [Assignment(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ is self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = kvargs["meta"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FilterSpaces:
    """

    Attributes
    ----------
    ids: list[str]
    names: list[str]
    """

    ids: list[str] = None
    names: list[str] = None

    def __init__(self_, **kvargs):
        if "ids" in kvargs:
            if type(kvargs["ids"]).__name__ is self_.__annotations__["ids"]:
                self_.ids = kvargs["ids"]
            else:
                self_.ids = kvargs["ids"]
        if "names" in kvargs:
            if type(kvargs["names"]).__name__ is self_.__annotations__["names"]:
                self_.names = kvargs["names"]
            else:
                self_.names = kvargs["names"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Share:
    """

    Attributes
    ----------
    assigneeId: str
      The userId or groupId based on the type.
    id: str
    resourceId: str
      The ID of the shared resource.
    resourceType: str
      The type of the shared resource.
    spaceId: str
    tenantId: str
    type: str
    createdAt: str
    createdBy: str
      The ID of the user who created the share.
    links: object
    resourceName: str
      The name of the shared resource.
    roles: list[ShareRoleType]
      The roles assigned to the assigneeId.
    updatedAt: str
    updatedBy: str
      The ID of the user who updated the share.
    """

    assigneeId: str = None
    id: str = None
    resourceId: str = None
    resourceType: str = None
    spaceId: str = None
    tenantId: str = None
    type: str = None
    createdAt: str = None
    createdBy: str = None
    links: object = None
    resourceName: str = None
    roles: list[ShareRoleType] = None
    updatedAt: str = None
    updatedBy: str = None

    def __init__(self_, **kvargs):
        if "assigneeId" in kvargs:
            if (
                type(kvargs["assigneeId"]).__name__
                is self_.__annotations__["assigneeId"]
            ):
                self_.assigneeId = kvargs["assigneeId"]
            else:
                self_.assigneeId = kvargs["assigneeId"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "resourceId" in kvargs:
            if (
                type(kvargs["resourceId"]).__name__
                is self_.__annotations__["resourceId"]
            ):
                self_.resourceId = kvargs["resourceId"]
            else:
                self_.resourceId = kvargs["resourceId"]
        if "resourceType" in kvargs:
            if (
                type(kvargs["resourceType"]).__name__
                is self_.__annotations__["resourceType"]
            ):
                self_.resourceType = kvargs["resourceType"]
            else:
                self_.resourceType = kvargs["resourceType"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
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
        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ is self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "createdBy" in kvargs:
            if type(kvargs["createdBy"]).__name__ is self_.__annotations__["createdBy"]:
                self_.createdBy = kvargs["createdBy"]
            else:
                self_.createdBy = kvargs["createdBy"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]
        if "resourceName" in kvargs:
            if (
                type(kvargs["resourceName"]).__name__
                is self_.__annotations__["resourceName"]
            ):
                self_.resourceName = kvargs["resourceName"]
            else:
                self_.resourceName = kvargs["resourceName"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ is self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = [ShareRoleType(**e) for e in kvargs["roles"]]
        if "updatedAt" in kvargs:
            if type(kvargs["updatedAt"]).__name__ is self_.__annotations__["updatedAt"]:
                self_.updatedAt = kvargs["updatedAt"]
            else:
                self_.updatedAt = kvargs["updatedAt"]
        if "updatedBy" in kvargs:
            if type(kvargs["updatedBy"]).__name__ is self_.__annotations__["updatedBy"]:
                self_.updatedBy = kvargs["updatedBy"]
            else:
                self_.updatedBy = kvargs["updatedBy"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ShareCreate:
    """

    Attributes
    ----------
    assigneeId: str
      The userId or groupId based on the type.
    resourceId: str
      The resource id for the shared item.
    resourceType: str
      The resource type for the shared item.
    roles: list[ShareRoleType]
      The roles assigned to the assigneeId.
    type: str
    """

    assigneeId: str = None
    resourceId: str = None
    resourceType: str = None
    roles: list[ShareRoleType] = None
    type: str = None

    def __init__(self_, **kvargs):
        if "assigneeId" in kvargs:
            if (
                type(kvargs["assigneeId"]).__name__
                is self_.__annotations__["assigneeId"]
            ):
                self_.assigneeId = kvargs["assigneeId"]
            else:
                self_.assigneeId = kvargs["assigneeId"]
        if "resourceId" in kvargs:
            if (
                type(kvargs["resourceId"]).__name__
                is self_.__annotations__["resourceId"]
            ):
                self_.resourceId = kvargs["resourceId"]
            else:
                self_.resourceId = kvargs["resourceId"]
        if "resourceType" in kvargs:
            if (
                type(kvargs["resourceType"]).__name__
                is self_.__annotations__["resourceType"]
            ):
                self_.resourceType = kvargs["resourceType"]
            else:
                self_.resourceType = kvargs["resourceType"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ is self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = [ShareRoleType(**e) for e in kvargs["roles"]]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ is self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SharePatch:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ShareRoleType:
    """
    Supported roles by space type:
    - Shared: consumer
    - Managed: consumer, contributor

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Shares:
    """

    Attributes
    ----------
    data: list[Share]
    links: object
    meta: object
    """

    data: list[Share] = None
    links: object = None
    meta: object = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [Share(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ is self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = kvargs["meta"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpaceCreate:
    """

    Attributes
    ----------
    name: str
      The name of the space. Personal spaces do not have a name.
    type: str
      The type of space such as shared, managed, and so on.
    description: str
      The description of the space. Personal spaces do not have a description.
    """

    name: str = None
    type: str = None
    description: str = None

    def __init__(self_, **kvargs):
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ is self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                is self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacePatch:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpaceTypes:
    """
    The distinct types of spaces (shared, managed, and so on).

    Attributes
    ----------
    data: list[str]
    """

    data: list[str] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = kvargs["data"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpaceUpdate:
    """

    Attributes
    ----------
    description: str
      The description of the space. Personal spaces do not have a description.
    name: str
      The name of the space.
    ownerId: str
      The user ID of the space owner.
    """

    description: str = None
    name: str = None
    ownerId: str = None

    def __init__(self_, **kvargs):
        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                is self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ is self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacesClass:
    """

    Attributes
    ----------
    data: list[Space]
    links: object
    meta: object
    """

    data: list[Space] = None
    links: object = None
    meta: object = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [Space(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ is self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = kvargs["meta"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Spaces:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_spaces(
        self,
        type: str = None,
        action: str = None,
        sort: str = None,
        name: str = None,
        ownerId: str = None,
        limit: int = 10,
        next: str = None,
        prev: str = None,
        max_items: int = 10,
    ) -> ListableResource[Space]:
        """
        Retrieves spaces that the current user has access to and match the query.


        type: str
          Type(s) of space to filter. For example, "?type=managed,shared".

        action: str
          Action on space. For example, "?action=publish".

        sort: str
          Field to sort by. Prefix with +/- to indicate asc/desc. For example, "?sort=+name" to sort ascending on Name. Supported fields are "type", "name" and "createdAt".

        name: str
          Space name to search and filter for. Case-insensitive open search with wildcards both as prefix and suffix. For example, "?name=fin" will get "finance", "Final" and "Griffin".

        ownerId: str
          Space ownerId to filter by. For example, "?ownerId=123".

        limit: int
          Maximum number of spaces to return.

        next: str
          The next page cursor. Next links make use of this.

        prev: str
          The previous page cursor. Previous links make use of this.

        Parameters
        ----------
        type: str = None
        action: str = None
        sort: str = None
        name: str = None
        ownerId: str = None
        limit: int = 10
        next: str = None
        prev: str = None
        """
        query_params = {}
        if type is not None:
            query_params["type"] = type
        if action is not None:
            query_params["action"] = action
        if sort is not None:
            query_params["sort"] = sort
        if name is not None:
            query_params["name"] = name
        if ownerId is not None:
            query_params["ownerId"] = ownerId
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev

        response = self.auth.rest(
            path="/spaces",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Space,
            auth=self.auth,
            path="/spaces",
            max_items=max_items,
            query_params=query_params,
        )

    def create(self, data: SpaceCreate) -> Space:
        """
        Creates a space.


        Parameters
        ----------
        data: SpaceCreate
        """

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/spaces",
            method="POST",
            params={},
            data=data,
        )
        obj = Space(**response.json())
        obj.auth = self.auth
        return obj

    def create_filters(
        self, data: FilterSpaces, max_items: int = 10
    ) -> ListableResource[Space]:
        """
        Experimental
        Retrieves spaces that the current user has access to with provided space IDs or names.


        Parameters
        ----------
        data: FilterSpaces
        """
        warnings.warn("create_filters is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/spaces/filter",
            method="POST",
            params={},
            data=data,
        )
        return ListableResource(
            response=response.json(),
            cls=Space,
            auth=self.auth,
            path="/spaces/filter",
            max_items=max_items,
            query_params={},
        )

    def get_types(self, max_items: int = 10) -> ListableResource[str]:
        """
        Gets a list of distinct space types.


        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/spaces/types",
            method="GET",
            params={},
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=None,
            auth=self.auth,
            path="/spaces/types",
            max_items=max_items,
            query_params={},
        )

    def get(self, spaceId: str) -> Space:
        """
        Retrieves a single space by ID.


        spaceId: str
          The ID of the space to retrieve.

        Parameters
        ----------
        spaceId: str
        """

        response = self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", spaceId),
            method="GET",
            params={},
            data=None,
        )
        obj = Space(**response.json())
        obj.auth = self.auth
        return obj

    def delete_assignment(self, spaceId: str, assignmentId: str) -> None:
        """
        Deletes an assignment.


        spaceId: str
          The ID of the space of the assignment.

        assignmentId: str
          The ID of the assignment to delete.

        Parameters
        ----------
        spaceId: str
        assignmentId: str
        """

        self.auth.rest(
            path="/spaces/{spaceId}/assignments/{assignmentId}".replace(
                "{spaceId}", spaceId
            ).replace("{assignmentId}", assignmentId),
            method="DELETE",
            params={},
            data=None,
        )

    def get_assignment(self, spaceId: str, assignmentId: str) -> Assignment:
        """
        Retrieves a single assignment by ID.


        spaceId: str
          The ID of the space of the assignment.

        assignmentId: str
          The ID of the assignment to retrieve.

        Parameters
        ----------
        spaceId: str
        assignmentId: str
        """

        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments/{assignmentId}".replace(
                "{spaceId}", spaceId
            ).replace("{assignmentId}", assignmentId),
            method="GET",
            params={},
            data=None,
        )
        obj = Assignment(**response.json())
        obj.auth = self.auth
        return obj

    def set_assignment(
        self, spaceId: str, assignmentId: str, data: AssignmentUpdate
    ) -> Assignment:
        """
        Experimental
        Updates a single assignment by ID. The complete list of roles must be provided.


        spaceId: str
          The ID of the space of the assignment.

        assignmentId: str
          The ID of the assignment to update.

        Parameters
        ----------
        spaceId: str
        assignmentId: str
        data: AssignmentUpdate
        """
        warnings.warn("set_assignment is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments/{assignmentId}".replace(
                "{spaceId}", spaceId
            ).replace("{assignmentId}", assignmentId),
            method="PUT",
            params={},
            data=data,
        )
        obj = Assignment(**response.json())
        obj.auth = self.auth
        return obj

    def delete_share(self, spaceId: str, shareId: str) -> None:
        """
        Experimental
        Deletes a Share.


        spaceId: str
          The ID of the space to which the share belongs.

        shareId: str
          The ID of the share to delete.

        Parameters
        ----------
        spaceId: str
        shareId: str
        """
        warnings.warn("delete_share is experimental", UserWarning, stacklevel=2)

        self.auth.rest(
            path="/spaces/{spaceId}/shares/{shareId}".replace(
                "{spaceId}", spaceId
            ).replace("{shareId}", shareId),
            method="DELETE",
            params={},
            data=None,
        )

    def get_share(self, spaceId: str, shareId: str) -> Share:
        """
        Experimental
        Retrieves a single share by ID.


        spaceId: str
          The ID of the space to which the share belongs.

        shareId: str
          The ID of the share to retrieve.

        Parameters
        ----------
        spaceId: str
        shareId: str
        """
        warnings.warn("get_share is experimental", UserWarning, stacklevel=2)

        response = self.auth.rest(
            path="/spaces/{spaceId}/shares/{shareId}".replace(
                "{spaceId}", spaceId
            ).replace("{shareId}", shareId),
            method="GET",
            params={},
            data=None,
        )
        obj = Share(**response.json())
        obj.auth = self.auth
        return obj

    def patch_share(self, spaceId: str, shareId: str, data: SharePatch) -> Share:
        """
        Experimental
        Patches (updates) a share (partially).


        spaceId: str
          The ID of the space to which the share belongs.

        shareId: str
          The ID of the share to update.

        Parameters
        ----------
        spaceId: str
        shareId: str
        data: SharePatch
        """
        warnings.warn("patch_share is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/spaces/{spaceId}/shares/{shareId}".replace(
                "{spaceId}", spaceId
            ).replace("{shareId}", shareId),
            method="PATCH",
            params={},
            data=data,
        )
        obj = Share(**response.json())
        obj.auth = self.auth
        return obj
