# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services 0.348.2

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Union

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class User:
    """

    Attributes
    ----------
    id: str
      The unique user identifier.
    name: str
      The name of the user.
    subject: str
      The unique user identitier from an identity provider.
    tenantId: str
      The tenant that the user belongs too.
    assignedGroups: list[object]
    assignedRoles: list[object]
    created: str
      Deprecated. Use `createdAt` instead.
    createdAt: str
      The timestamp for when the user record was created.
    email: str
      The email address for the user.
    inviteExpiry: float
      The number of seconds until the user invitation will expire.
    lastUpdated: str
      Deprecated. Use `lastUpdatedAt` instead.
    lastUpdatedAt: str
      The timestamp for when the user record was last updated.
    links: object
    locale: str
      Represents the end-user's language tag.
    picture: str
      A static url linking to the avatar of the user.
    preferredLocale: str
      Represents the end-user's preferred language tag.
    preferredZoneinfo: str
      Represents the end-user's preferred time zone.
    roles: list[str]
      List of system roles to which the user has been assigned. Only returned when permitted by access control. Deprecated. Use `assignedRoles` instead.
    status: str
      The status of the user within the tenant.
    zoneinfo: str
      Represents the end-user's time zone.
    """

    id: str = None
    name: str = None
    subject: str = None
    tenantId: str = None
    assignedGroups: list[object] = None
    assignedRoles: list[object] = None
    created: str = None
    createdAt: str = None
    email: str = None
    inviteExpiry: float = None
    lastUpdated: str = None
    lastUpdatedAt: str = None
    links: object = None
    locale: str = None
    picture: str = None
    preferredLocale: str = None
    preferredZoneinfo: str = None
    roles: list[str] = None
    status: str = None
    zoneinfo: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "subject" in kvargs:
            if type(kvargs["subject"]).__name__ is self_.__annotations__["subject"]:
                self_.subject = kvargs["subject"]
            else:
                self_.subject = kvargs["subject"]
        if "tenantId" in kvargs:
            if type(kvargs["tenantId"]).__name__ is self_.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "assignedGroups" in kvargs:
            if (
                type(kvargs["assignedGroups"]).__name__
                is self_.__annotations__["assignedGroups"]
            ):
                self_.assignedGroups = kvargs["assignedGroups"]
            else:
                self_.assignedGroups = kvargs["assignedGroups"]
        if "assignedRoles" in kvargs:
            if (
                type(kvargs["assignedRoles"]).__name__
                is self_.__annotations__["assignedRoles"]
            ):
                self_.assignedRoles = kvargs["assignedRoles"]
            else:
                self_.assignedRoles = kvargs["assignedRoles"]
        if "created" in kvargs:
            if type(kvargs["created"]).__name__ is self_.__annotations__["created"]:
                self_.created = kvargs["created"]
            else:
                self_.created = kvargs["created"]
        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ is self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "email" in kvargs:
            if type(kvargs["email"]).__name__ is self_.__annotations__["email"]:
                self_.email = kvargs["email"]
            else:
                self_.email = kvargs["email"]
        if "inviteExpiry" in kvargs:
            if (
                type(kvargs["inviteExpiry"]).__name__
                is self_.__annotations__["inviteExpiry"]
            ):
                self_.inviteExpiry = kvargs["inviteExpiry"]
            else:
                self_.inviteExpiry = kvargs["inviteExpiry"]
        if "lastUpdated" in kvargs:
            if (
                type(kvargs["lastUpdated"]).__name__
                is self_.__annotations__["lastUpdated"]
            ):
                self_.lastUpdated = kvargs["lastUpdated"]
            else:
                self_.lastUpdated = kvargs["lastUpdated"]
        if "lastUpdatedAt" in kvargs:
            if (
                type(kvargs["lastUpdatedAt"]).__name__
                is self_.__annotations__["lastUpdatedAt"]
            ):
                self_.lastUpdatedAt = kvargs["lastUpdatedAt"]
            else:
                self_.lastUpdatedAt = kvargs["lastUpdatedAt"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]
        if "locale" in kvargs:
            if type(kvargs["locale"]).__name__ is self_.__annotations__["locale"]:
                self_.locale = kvargs["locale"]
            else:
                self_.locale = kvargs["locale"]
        if "picture" in kvargs:
            if type(kvargs["picture"]).__name__ is self_.__annotations__["picture"]:
                self_.picture = kvargs["picture"]
            else:
                self_.picture = kvargs["picture"]
        if "preferredLocale" in kvargs:
            if (
                type(kvargs["preferredLocale"]).__name__
                is self_.__annotations__["preferredLocale"]
            ):
                self_.preferredLocale = kvargs["preferredLocale"]
            else:
                self_.preferredLocale = kvargs["preferredLocale"]
        if "preferredZoneinfo" in kvargs:
            if (
                type(kvargs["preferredZoneinfo"]).__name__
                is self_.__annotations__["preferredZoneinfo"]
            ):
                self_.preferredZoneinfo = kvargs["preferredZoneinfo"]
            else:
                self_.preferredZoneinfo = kvargs["preferredZoneinfo"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ is self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        if "status" in kvargs:
            if type(kvargs["status"]).__name__ is self_.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "zoneinfo" in kvargs:
            if type(kvargs["zoneinfo"]).__name__ is self_.__annotations__["zoneinfo"]:
                self_.zoneinfo = kvargs["zoneinfo"]
            else:
                self_.zoneinfo = kvargs["zoneinfo"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def delete(self) -> None:
        """
        Deletes a user resource.

        Parameters
        ----------
        """

        self.auth.rest(
            path="/users/{userId}".replace("{userId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patch(self, data: UserJSONPatchArray) -> None:
        """
        Updates a user resource.

        Parameters
        ----------
        data: UserJSONPatchArray
        """

        try:
            data = asdict(data)
        except:
            data = data

        self.auth.rest(
            path="/users/{userId}".replace("{userId}", self.id),
            method="PATCH",
            params={},
            data=data,
        )


@dataclass
class Filter:
    """

    Attributes
    ----------
    filter: str
      The advanced filtering to be applied the query. All conditional statements within this query parameter are case insensitive.
    """

    filter: str = None

    def __init__(self_, **kvargs):
        if "filter" in kvargs:
            if type(kvargs["filter"]).__name__ is self_.__annotations__["filter"]:
                self_.filter = kvargs["filter"]
            else:
                self_.filter = kvargs["filter"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Metadata:
    """

    Attributes
    ----------
    valid_roles: list[str]
      List of system roles to which the user can be assigned.
    """

    valid_roles: list[str] = None

    def __init__(self_, **kvargs):
        if "valid_roles" in kvargs:
            if (
                type(kvargs["valid_roles"]).__name__
                is self_.__annotations__["valid_roles"]
            ):
                self_.valid_roles = kvargs["valid_roles"]
            else:
                self_.valid_roles = kvargs["valid_roles"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UserCount:
    """

    Attributes
    ----------
    total: float
    """

    total: float = None

    def __init__(self_, **kvargs):
        if "total" in kvargs:
            if type(kvargs["total"]).__name__ is self_.__annotations__["total"]:
                self_.total = kvargs["total"]
            else:
                self_.total = kvargs["total"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UserJSONPatch:
    """
    A JSON Patch document as defined in http://tools.ietf.org/html/rfc6902.

    Attributes
    ----------
    op: str
      The operation to be performed.
    path: str
      A JSON Pointer.
    value: Union[str,bool,list]
      The value to be used for this operation.
    """

    op: str = None
    path: str = None
    value: Union[str, bool, list] = None

    def __init__(self_, **kvargs):
        if "op" in kvargs:
            if type(kvargs["op"]).__name__ is self_.__annotations__["op"]:
                self_.op = kvargs["op"]
            else:
                self_.op = kvargs["op"]
        if "path" in kvargs:
            if type(kvargs["path"]).__name__ is self_.__annotations__["path"]:
                self_.path = kvargs["path"]
            else:
                self_.path = kvargs["path"]
        if "value" in kvargs:
            if type(kvargs["value"]).__name__ is self_.__annotations__["value"]:
                self_.value = kvargs["value"]
            else:
                self_.value = kvargs["value"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UserJSONPatchArray:
    """
    An array of JSON Patch documents

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UserPostSchema:
    """

    Attributes
    ----------
    subject: str
      The unique user identitier from an identity provider.
    assignedGroups: list[object]
    assignedRoles: list[object]
    email: str
      The email address for the user. This is a required field when inviting a user.
    name: str
      The name of the user.
    picture: str
      A static url linking to the avatar of the user.
    roles: list[str]
      List of system roles to which the user has been assigned. Only returned when permitted by access control.
    status: str
      The status of the created user within the tenant.
    tenantId: str
      The tenant that the user will belong too.
    """

    subject: str = None
    assignedGroups: list[object] = None
    assignedRoles: list[object] = None
    email: str = None
    name: str = None
    picture: str = None
    roles: list[str] = None
    status: str = None
    tenantId: str = None

    def __init__(self_, **kvargs):
        if "subject" in kvargs:
            if type(kvargs["subject"]).__name__ is self_.__annotations__["subject"]:
                self_.subject = kvargs["subject"]
            else:
                self_.subject = kvargs["subject"]
        if "assignedGroups" in kvargs:
            if (
                type(kvargs["assignedGroups"]).__name__
                is self_.__annotations__["assignedGroups"]
            ):
                self_.assignedGroups = kvargs["assignedGroups"]
            else:
                self_.assignedGroups = kvargs["assignedGroups"]
        if "assignedRoles" in kvargs:
            if (
                type(kvargs["assignedRoles"]).__name__
                is self_.__annotations__["assignedRoles"]
            ):
                self_.assignedRoles = kvargs["assignedRoles"]
            else:
                self_.assignedRoles = kvargs["assignedRoles"]
        if "email" in kvargs:
            if type(kvargs["email"]).__name__ is self_.__annotations__["email"]:
                self_.email = kvargs["email"]
            else:
                self_.email = kvargs["email"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "picture" in kvargs:
            if type(kvargs["picture"]).__name__ is self_.__annotations__["picture"]:
                self_.picture = kvargs["picture"]
            else:
                self_.picture = kvargs["picture"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ is self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
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
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UsersClass:
    """

    Attributes
    ----------
    data: list[User]
    links: object
    """

    data: list[User] = None
    links: object = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [User(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Users:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_users(
        self,
        tenantId: str = None,
        subject: str = None,
        email: str = None,
        status: str = "active",
        role: str = None,
        fields: str = None,
        limit: float = 20,
        sort: str = "+name",
        sortBy: str = "name",
        sortOrder: str = "asc",
        startingAfter: str = None,
        endingBefore: str = None,
        filter: str = None,
        next: str = None,
        prev: str = None,
        max_items: int = 20,
    ) -> ListableResource[User]:
        """
        Retrieves a list of users matching the query.


        tenantId: str
          The tenant ID to filter by. Deprecated. Use the new `filter` parameter to provide an advanced query filter.

        subject: str
          The subject to filter by. Deprecated. Use the new `filter` parameter to provide an advanced query filter.

        email: str
          The email to filter by. Deprecated. Use the new `filter` parameter to provide an advanced query filter.

        status: str
          The status to filter by. Supports multiple values delimited by commas. Deprecated. Use the new `filter` parameter to provide an advanced query filter.

        role: str
          The role to filter by. Deprecated. Use the new `filter` parameter to provide an advanced query filter.

        fields: str
          A comma-delimited string of the requested fields per entity. If the 'links' value is omitted, then the entity HATEOAS link will also be omitted.

        limit: float
          The number of user entries to retrieve.

        sort: str
          The field to sort by, with +/- prefix indicating sort order

        sortBy: str
          The user parameter to sort by. Deprecated. Use `sort` instead.

        sortOrder: str
          The sort order, either ascending or descending. Deprecated. Use `sort` instead.

        startingAfter: str
          Get users with IDs that are higher than the target user ID. Cannot be used in conjunction with endingBefore. Deprecated. Use `next` instead.

        endingBefore: str
          Get users with IDs that are lower than the target user ID. Cannot be used in conjunction with startingAfter. Deprecated. Use `prev` instead.

        filter: str
          The advanced filtering to use for the query. Refer to [RFC 7644](https://datatracker.ietf.org/doc/rfc7644/) for the syntax. Cannot be combined with any of the fields marked as deprecated. All conditional statements within this query parameter are case insensitive.

          The following fields support the `eq` operator: `id`, `subject`, `name`, `email`, `status`, `clientId`, `assignedRoles.id` `assignedRoles.name`, `assignedGroups.id`, `assignedGroupsAssignedRoles.name`

          Additionally, the following fields support the `co` operator: `name`, `email`, `subject`

          Queries may be rate limited if they differ greatly from these examples:

          ```
          (id eq "62716ab404a7bd8626af9bd6" or id eq "62716ac4c7e500e13ff5fa22") and (status eq "active" or status eq "disabled")
          ```

          ```
          name co "query" or email co "query" or subject co "query" or id eq "query" or assignedRoles.name eq "query"
          ```

        next: str
          Get users that come after this cursor value when sorted. Cannot be used in conjunction with `prev`.

        prev: str
          Get users that come before this cursor value when sorted. Cannot be used in conjunction with `next`.

        Parameters
        ----------
        tenantId: str = None
        subject: str = None
        email: str = None
        status: str = "active"
        role: str = None
        fields: str = None
        limit: float = 20
        sort: str = "+name"
        sortBy: str = "name"
        sortOrder: str = "asc"
        startingAfter: str = None
        endingBefore: str = None
        filter: str = None
        next: str = None
        prev: str = None
        """
        query_params = {}
        if tenantId is not None:
            query_params["tenantId"] = tenantId
        if subject is not None:
            query_params["subject"] = subject
        if email is not None:
            query_params["email"] = email
        if status is not None:
            query_params["status"] = status
        if role is not None:
            query_params["role"] = role
        if fields is not None:
            query_params["fields"] = fields
        if limit is not None:
            query_params["limit"] = limit
        if sort is not None:
            query_params["sort"] = sort
        if sortBy is not None:
            query_params["sortBy"] = sortBy
        if sortOrder is not None:
            query_params["sortOrder"] = sortOrder
        if startingAfter is not None:
            query_params["startingAfter"] = startingAfter
        if endingBefore is not None:
            query_params["endingBefore"] = endingBefore
        if filter is not None:
            query_params["filter"] = filter
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev

        response = self.auth.rest(
            path="/users",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=User,
            auth=self.auth,
            path="/users",
            max_items=max_items,
            query_params=query_params,
        )

    def create(self, data: UserPostSchema) -> User:
        """
        Creates a user in a given tenant.
        Creates and returns a user in a given tenant. Note that only creating invited status users is supported for users of the given tenant.


        Authorization: str
          The JWT used for authentication. Send the JWT in the Authorization header using the Bearer schema.

        Parameters
        ----------
        data: UserPostSchema
        """

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/users",
            method="POST",
            params={},
            data=data,
        )
        obj = User(**response.json())
        obj.auth = self.auth
        return obj

    def count(self, tenantId: str = None) -> UserCount:
        """
        Returns the number of users in a given tenant


        tenantId: str
          The tenant ID to filter by.

        Parameters
        ----------
        tenantId: str = None
        """
        query_params = {}
        if tenantId is not None:
            query_params["tenantId"] = tenantId

        response = self.auth.rest(
            path="/users/actions/count",
            method="GET",
            params=query_params,
            data=None,
        )
        obj = UserCount(**response.json())
        obj.auth = self.auth
        return obj

    def filter(
        self,
        data: Filter,
        fields: str = None,
        sort: str = "+name",
        next: str = None,
        prev: str = None,
        limit: float = 20,
        max_items: int = 20,
    ) -> ListableResource[User]:
        """
        Retrieves a list of users matching the filter using advanced query string.


        fields: str
          A comma-delimited string of the requested fields per entity. If the 'links' value is omitted, then the entity HATEOAS link will also be omitted.

        sort: str
          The field to sort by, with +/- prefix indicating sort order

        next: str
          Get users with IDs that are higher than the target user ID. Cannot be used in conjunction with prev.

        prev: str
          Get users with IDs that are lower than the target user ID. Cannot be used in conjunction with next.

        limit: float
          The number of user entries to retrieve.

        Parameters
        ----------
        fields: str = None
        sort: str = "+name"
        next: str = None
        prev: str = None
        limit: float = 20
        data: Filter
        """
        query_params = {}
        if fields is not None:
            query_params["fields"] = fields
        if sort is not None:
            query_params["sort"] = sort
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if limit is not None:
            query_params["limit"] = limit

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/users/actions/filter",
            method="POST",
            params=query_params,
            data=data,
        )
        return ListableResource(
            response=response.json(),
            cls=User,
            auth=self.auth,
            path="/users/actions/filter",
            max_items=max_items,
            query_params=query_params,
        )

    def get_me(self) -> any:
        """
        Redirects to retrieve the user resource associated with the JWT claims.


        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/users/me",
            method="GET",
            params={},
            data=None,
        )
        return response.json()

    def get_metadata(self) -> Metadata:
        """
        Returns the metadata with regard to the user configuration.
        Deprecated, use GET /v1/roles instead.


        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/users/metadata",
            method="GET",
            params={},
            data=None,
        )
        obj = Metadata(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, userId: str) -> User:
        """
        Returns the requested user.
        Returns the requested user.


        userId: str
          The user's unique identifier

        Parameters
        ----------
        userId: str
        """

        response = self.auth.rest(
            path="/users/{userId}".replace("{userId}", userId),
            method="GET",
            params={},
            data=None,
        )
        obj = User(**response.json())
        obj.auth = self.auth
        return obj
