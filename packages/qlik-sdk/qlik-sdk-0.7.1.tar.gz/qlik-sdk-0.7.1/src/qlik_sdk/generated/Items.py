# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services 0.348.2

from __future__ import annotations

import warnings
from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class ItemResultResponseBody:
    """
    An item.

    Attributes
    ----------
    actions: list[str]
      The actions that the user can perform on the item.
    collectionIds: list[str]
      The ID of the collections that the item has been added to.
    createdAt: str
      The RFC3339 datetime when the item was created.
    id: str
      The item's unique identifier.
    isFavorited: bool
      The flag that indicates if item is in the user's favorites collection.
    links: ItemLinksResponseBody
    meta: ItemMetaResponseBody
      Item metadata and computed fields.
    name: str
    resourceAttributes: object
    resourceCreatedAt: str
      The RFC3339 datetime when the resource that the item references was created.
    resourceCustomAttributes: object
    resourceType: str
      The case-sensitive string defining the item's type.
    resourceUpdatedAt: str
      The RFC3339 datetime when the resource that the item references was last updated.
    tenantId: str
      The ID of the tenant that owns the item. This is populated using the JWT.
    updatedAt: str
      The RFC3339 datetime when the item was last updated.
    creatorId: str
      The ID of the user who created the item. This is only populated if the JWT contains a userId.
    description: str
    itemViews: ItemViewsResponseBody
    ownerId: str
      The ID of the user who owns the item.
    resourceId: str
      The case-sensitive string used to search for an item by resourceId. If resourceId is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceLink: str
      The case-sensitive string used to search for an item by resourceLink. If resourceLink is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceReloadEndTime: str
      The RFC3339 datetime when the resource last reload ended.
    resourceReloadStatus: str
      If the resource last reload was successful or not.
    resourceSize: ItemsResourceSizeResponseBody
    resourceSubType: str
      Optional field defining the item's subtype, if any.
    spaceId: str
      The space's unique identifier.
    thumbnailId: str
      The item thumbnail's unique identifier. This is optional for internal resources.
    updaterId: str
      ID of the user who last updated the item. This is only populated if the JWT contains a userId.
    """

    actions: list[str] = None
    collectionIds: list[str] = None
    createdAt: str = None
    id: str = None
    isFavorited: bool = None
    links: ItemLinksResponseBody = None
    meta: ItemMetaResponseBody = None
    name: str = None
    resourceAttributes: object = None
    resourceCreatedAt: str = None
    resourceCustomAttributes: object = None
    resourceType: str = None
    resourceUpdatedAt: str = None
    tenantId: str = None
    updatedAt: str = None
    creatorId: str = None
    description: str = None
    itemViews: ItemViewsResponseBody = None
    ownerId: str = None
    resourceId: str = None
    resourceLink: str = None
    resourceReloadEndTime: str = None
    resourceReloadStatus: str = None
    resourceSize: ItemsResourceSizeResponseBody = None
    resourceSubType: str = None
    spaceId: str = None
    thumbnailId: str = None
    updaterId: str = None

    def __init__(self_, **kvargs):
        if "actions" in kvargs:
            if type(kvargs["actions"]).__name__ is self_.__annotations__["actions"]:
                self_.actions = kvargs["actions"]
            else:
                self_.actions = kvargs["actions"]
        if "collectionIds" in kvargs:
            if (
                type(kvargs["collectionIds"]).__name__
                is self_.__annotations__["collectionIds"]
            ):
                self_.collectionIds = kvargs["collectionIds"]
            else:
                self_.collectionIds = kvargs["collectionIds"]
        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ is self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "isFavorited" in kvargs:
            if (
                type(kvargs["isFavorited"]).__name__
                is self_.__annotations__["isFavorited"]
            ):
                self_.isFavorited = kvargs["isFavorited"]
            else:
                self_.isFavorited = kvargs["isFavorited"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ItemLinksResponseBody(**kvargs["links"])
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ is self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = ItemMetaResponseBody(**kvargs["meta"])
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "resourceAttributes" in kvargs:
            if (
                type(kvargs["resourceAttributes"]).__name__
                is self_.__annotations__["resourceAttributes"]
            ):
                self_.resourceAttributes = kvargs["resourceAttributes"]
            else:
                self_.resourceAttributes = kvargs["resourceAttributes"]
        if "resourceCreatedAt" in kvargs:
            if (
                type(kvargs["resourceCreatedAt"]).__name__
                is self_.__annotations__["resourceCreatedAt"]
            ):
                self_.resourceCreatedAt = kvargs["resourceCreatedAt"]
            else:
                self_.resourceCreatedAt = kvargs["resourceCreatedAt"]
        if "resourceCustomAttributes" in kvargs:
            if (
                type(kvargs["resourceCustomAttributes"]).__name__
                is self_.__annotations__["resourceCustomAttributes"]
            ):
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
            else:
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
        if "resourceType" in kvargs:
            if (
                type(kvargs["resourceType"]).__name__
                is self_.__annotations__["resourceType"]
            ):
                self_.resourceType = kvargs["resourceType"]
            else:
                self_.resourceType = kvargs["resourceType"]
        if "resourceUpdatedAt" in kvargs:
            if (
                type(kvargs["resourceUpdatedAt"]).__name__
                is self_.__annotations__["resourceUpdatedAt"]
            ):
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
            else:
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
        if "tenantId" in kvargs:
            if type(kvargs["tenantId"]).__name__ is self_.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "updatedAt" in kvargs:
            if type(kvargs["updatedAt"]).__name__ is self_.__annotations__["updatedAt"]:
                self_.updatedAt = kvargs["updatedAt"]
            else:
                self_.updatedAt = kvargs["updatedAt"]
        if "creatorId" in kvargs:
            if type(kvargs["creatorId"]).__name__ is self_.__annotations__["creatorId"]:
                self_.creatorId = kvargs["creatorId"]
            else:
                self_.creatorId = kvargs["creatorId"]
        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                is self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "itemViews" in kvargs:
            if type(kvargs["itemViews"]).__name__ is self_.__annotations__["itemViews"]:
                self_.itemViews = kvargs["itemViews"]
            else:
                self_.itemViews = ItemViewsResponseBody(**kvargs["itemViews"])
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ is self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        if "resourceId" in kvargs:
            if (
                type(kvargs["resourceId"]).__name__
                is self_.__annotations__["resourceId"]
            ):
                self_.resourceId = kvargs["resourceId"]
            else:
                self_.resourceId = kvargs["resourceId"]
        if "resourceLink" in kvargs:
            if (
                type(kvargs["resourceLink"]).__name__
                is self_.__annotations__["resourceLink"]
            ):
                self_.resourceLink = kvargs["resourceLink"]
            else:
                self_.resourceLink = kvargs["resourceLink"]
        if "resourceReloadEndTime" in kvargs:
            if (
                type(kvargs["resourceReloadEndTime"]).__name__
                is self_.__annotations__["resourceReloadEndTime"]
            ):
                self_.resourceReloadEndTime = kvargs["resourceReloadEndTime"]
            else:
                self_.resourceReloadEndTime = kvargs["resourceReloadEndTime"]
        if "resourceReloadStatus" in kvargs:
            if (
                type(kvargs["resourceReloadStatus"]).__name__
                is self_.__annotations__["resourceReloadStatus"]
            ):
                self_.resourceReloadStatus = kvargs["resourceReloadStatus"]
            else:
                self_.resourceReloadStatus = kvargs["resourceReloadStatus"]
        if "resourceSize" in kvargs:
            if (
                type(kvargs["resourceSize"]).__name__
                is self_.__annotations__["resourceSize"]
            ):
                self_.resourceSize = kvargs["resourceSize"]
            else:
                self_.resourceSize = ItemsResourceSizeResponseBody(
                    **kvargs["resourceSize"]
                )
        if "resourceSubType" in kvargs:
            if (
                type(kvargs["resourceSubType"]).__name__
                is self_.__annotations__["resourceSubType"]
            ):
                self_.resourceSubType = kvargs["resourceSubType"]
            else:
                self_.resourceSubType = kvargs["resourceSubType"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        if "thumbnailId" in kvargs:
            if (
                type(kvargs["thumbnailId"]).__name__
                is self_.__annotations__["thumbnailId"]
            ):
                self_.thumbnailId = kvargs["thumbnailId"]
            else:
                self_.thumbnailId = kvargs["thumbnailId"]
        if "updaterId" in kvargs:
            if type(kvargs["updaterId"]).__name__ is self_.__annotations__["updaterId"]:
                self_.updaterId = kvargs["updaterId"]
            else:
                self_.updaterId = kvargs["updaterId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def delete(self) -> None:
        """
        Experimental
        Deletes an item.
        Deletes an item and removes the item from all collections.

        Parameters
        ----------
        """
        warnings.warn("delete is experimental", UserWarning, stacklevel=2)

        self.auth.rest(
            path="/items/{itemId}".replace("{itemId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def set(self, data: ItemsUpdateItemRequestBody) -> ItemResultResponseBody:
        """
        Experimental
        Updates an item.
        Updates an item. Omitted and unsupported fields are ignored. To unset a field, provide the field's zero value.

        Parameters
        ----------
        data: ItemsUpdateItemRequestBody
        """
        warnings.warn("set is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/items/{itemId}".replace("{itemId}", self.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def get_collections(
        self,
        next: str = None,
        prev: str = None,
        limit: int = None,
        sort: str = None,
        query: str = None,
        type: str = None,
        name: str = None,
        max_items: int = 10,
    ) -> ListableResource[CollectionResultResponseBody]:
        """
        Returns the collections of an item.
        Finds and returns the collections of an item. This endpoint does not return the user's favorites collection.

        Parameters
        ----------
        next: str = None
        prev: str = None
        limit: int = None
        sort: str = None
        query: str = None
        type: str = None
        name: str = None
        """
        query_params = {}
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if limit is not None:
            query_params["limit"] = limit
        if sort is not None:
            query_params["sort"] = sort
        if query is not None:
            query_params["query"] = query
        if type is not None:
            query_params["type"] = type
        if name is not None:
            query_params["name"] = name

        response = self.auth.rest(
            path="/items/{itemId}/collections".replace("{itemId}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=CollectionResultResponseBody,
            auth=self.auth,
            path="/items/{itemId}/collections".replace("{itemId}", self.id),
            max_items=max_items,
            query_params=query_params,
        )

    def get_publisheditems(
        self,
        next: str = None,
        prev: str = None,
        limit: int = None,
        sort: str = None,
        resourceType: str = None,
        max_items: int = 10,
    ) -> ListableResource[CollectionResultResponseBody]:
        """
        Returns published items for a given item.
        Finds and returns the published items for a given item.

        Parameters
        ----------
        next: str = None
        prev: str = None
        limit: int = None
        sort: str = None
        resourceType: str = None
        """
        query_params = {}
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if limit is not None:
            query_params["limit"] = limit
        if sort is not None:
            query_params["sort"] = sort
        if resourceType is not None:
            query_params["resourceType"] = resourceType

        response = self.auth.rest(
            path="/items/{itemId}/publisheditems".replace("{itemId}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=CollectionResultResponseBody,
            auth=self.auth,
            path="/items/{itemId}/publisheditems".replace("{itemId}", self.id),
            max_items=max_items,
            query_params=query_params,
        )


@dataclass
class ItemsCreateItemRequestBody:
    """

    Attributes
    ----------
    name: str
    resourceCreatedAt: str
      The RFC3339 datetime when the resource that the item references was created.
    resourceType: str
      The case-sensitive string defining the item's type.
    description: str
    resourceAttributes: object
    resourceCustomAttributes: object
    resourceId: str
      The case-sensitive string used to search for an item by resourceId. If resourceId is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceLink: str
      The case-sensitive string used to search for an item by resourceLink. If resourceLink is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceSubType: str
      Optional field defining the item's subtype, if any.
    resourceUpdatedAt: str
      The RFC3339 datetime when the resource that the item references was last updated.
    spaceId: str
      The space's unique identifier.
    thumbnailId: str
      The item thumbnail's unique identifier. This is optional for internal resources.
    """

    name: str = None
    resourceCreatedAt: str = None
    resourceType: str = None
    description: str = None
    resourceAttributes: object = None
    resourceCustomAttributes: object = None
    resourceId: str = None
    resourceLink: str = None
    resourceSubType: str = None
    resourceUpdatedAt: str = None
    spaceId: str = None
    thumbnailId: str = None

    def __init__(self_, **kvargs):
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "resourceCreatedAt" in kvargs:
            if (
                type(kvargs["resourceCreatedAt"]).__name__
                is self_.__annotations__["resourceCreatedAt"]
            ):
                self_.resourceCreatedAt = kvargs["resourceCreatedAt"]
            else:
                self_.resourceCreatedAt = kvargs["resourceCreatedAt"]
        if "resourceType" in kvargs:
            if (
                type(kvargs["resourceType"]).__name__
                is self_.__annotations__["resourceType"]
            ):
                self_.resourceType = kvargs["resourceType"]
            else:
                self_.resourceType = kvargs["resourceType"]
        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                is self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "resourceAttributes" in kvargs:
            if (
                type(kvargs["resourceAttributes"]).__name__
                is self_.__annotations__["resourceAttributes"]
            ):
                self_.resourceAttributes = kvargs["resourceAttributes"]
            else:
                self_.resourceAttributes = kvargs["resourceAttributes"]
        if "resourceCustomAttributes" in kvargs:
            if (
                type(kvargs["resourceCustomAttributes"]).__name__
                is self_.__annotations__["resourceCustomAttributes"]
            ):
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
            else:
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
        if "resourceId" in kvargs:
            if (
                type(kvargs["resourceId"]).__name__
                is self_.__annotations__["resourceId"]
            ):
                self_.resourceId = kvargs["resourceId"]
            else:
                self_.resourceId = kvargs["resourceId"]
        if "resourceLink" in kvargs:
            if (
                type(kvargs["resourceLink"]).__name__
                is self_.__annotations__["resourceLink"]
            ):
                self_.resourceLink = kvargs["resourceLink"]
            else:
                self_.resourceLink = kvargs["resourceLink"]
        if "resourceSubType" in kvargs:
            if (
                type(kvargs["resourceSubType"]).__name__
                is self_.__annotations__["resourceSubType"]
            ):
                self_.resourceSubType = kvargs["resourceSubType"]
            else:
                self_.resourceSubType = kvargs["resourceSubType"]
        if "resourceUpdatedAt" in kvargs:
            if (
                type(kvargs["resourceUpdatedAt"]).__name__
                is self_.__annotations__["resourceUpdatedAt"]
            ):
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
            else:
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        if "thumbnailId" in kvargs:
            if (
                type(kvargs["thumbnailId"]).__name__
                is self_.__annotations__["thumbnailId"]
            ):
                self_.thumbnailId = kvargs["thumbnailId"]
            else:
                self_.thumbnailId = kvargs["thumbnailId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsListItemCollectionsResponseBody:
    """
    ListItemCollectionsResponseBody result type

    Attributes
    ----------
    data: list[CollectionResultResponseBody]
    links: CollectionsLinksResponseBody
    """

    data: list[CollectionResultResponseBody] = None
    links: CollectionsLinksResponseBody = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [CollectionResultResponseBody(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = CollectionsLinksResponseBody(**kvargs["links"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsListItemsResponseBody:
    """
    ListItemsResponseBody result type

    Attributes
    ----------
    data: list[ItemResultResponseBody]
    links: ItemsLinksResponseBody
    """

    data: list[ItemResultResponseBody] = None
    links: ItemsLinksResponseBody = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [ItemResultResponseBody(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ItemsLinksResponseBody(**kvargs["links"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsSettingsPatch:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsSettingsResponseBody:
    """

    Attributes
    ----------
    usageMetricsEnabled: bool
      Decides if the usage metrics will be shown in the hub UI.
    """

    usageMetricsEnabled: bool = None

    def __init__(self_, **kvargs):
        if "usageMetricsEnabled" in kvargs:
            if (
                type(kvargs["usageMetricsEnabled"]).__name__
                is self_.__annotations__["usageMetricsEnabled"]
            ):
                self_.usageMetricsEnabled = kvargs["usageMetricsEnabled"]
            else:
                self_.usageMetricsEnabled = kvargs["usageMetricsEnabled"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsUpdateItemRequestBody:
    """

    Attributes
    ----------
    resourceType: str
      The case-sensitive string defining the item's type.
    description: str
    name: str
    resourceAttributes: object
    resourceCustomAttributes: object
    resourceId: str
      The case-sensitive string used to search for an item by resourceId. If resourceId is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceLink: str
      The case-sensitive string used to search for an item by resourceLink. If resourceLink is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceSubType: str
      Optional field defining the item's subtype, if any.
    resourceUpdatedAt: str
      The RFC3339 datetime when the resource that the item references was last updated.
    spaceId: str
      The space's unique identifier.
    thumbnailId: str
      The item thumbnail's unique identifier. This is optional for internal resources.
    """

    resourceType: str = None
    description: str = None
    name: str = None
    resourceAttributes: object = None
    resourceCustomAttributes: object = None
    resourceId: str = None
    resourceLink: str = None
    resourceSubType: str = None
    resourceUpdatedAt: str = None
    spaceId: str = None
    thumbnailId: str = None

    def __init__(self_, **kvargs):
        if "resourceType" in kvargs:
            if (
                type(kvargs["resourceType"]).__name__
                is self_.__annotations__["resourceType"]
            ):
                self_.resourceType = kvargs["resourceType"]
            else:
                self_.resourceType = kvargs["resourceType"]
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
        if "resourceAttributes" in kvargs:
            if (
                type(kvargs["resourceAttributes"]).__name__
                is self_.__annotations__["resourceAttributes"]
            ):
                self_.resourceAttributes = kvargs["resourceAttributes"]
            else:
                self_.resourceAttributes = kvargs["resourceAttributes"]
        if "resourceCustomAttributes" in kvargs:
            if (
                type(kvargs["resourceCustomAttributes"]).__name__
                is self_.__annotations__["resourceCustomAttributes"]
            ):
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
            else:
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
        if "resourceId" in kvargs:
            if (
                type(kvargs["resourceId"]).__name__
                is self_.__annotations__["resourceId"]
            ):
                self_.resourceId = kvargs["resourceId"]
            else:
                self_.resourceId = kvargs["resourceId"]
        if "resourceLink" in kvargs:
            if (
                type(kvargs["resourceLink"]).__name__
                is self_.__annotations__["resourceLink"]
            ):
                self_.resourceLink = kvargs["resourceLink"]
            else:
                self_.resourceLink = kvargs["resourceLink"]
        if "resourceSubType" in kvargs:
            if (
                type(kvargs["resourceSubType"]).__name__
                is self_.__annotations__["resourceSubType"]
            ):
                self_.resourceSubType = kvargs["resourceSubType"]
            else:
                self_.resourceSubType = kvargs["resourceSubType"]
        if "resourceUpdatedAt" in kvargs:
            if (
                type(kvargs["resourceUpdatedAt"]).__name__
                is self_.__annotations__["resourceUpdatedAt"]
            ):
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
            else:
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        if "thumbnailId" in kvargs:
            if (
                type(kvargs["thumbnailId"]).__name__
                is self_.__annotations__["thumbnailId"]
            ):
                self_.thumbnailId = kvargs["thumbnailId"]
            else:
                self_.thumbnailId = kvargs["thumbnailId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Link:
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
class CollectionLinksResponseBody:
    """

    Attributes
    ----------
    items: Link
    self: Link
    """

    items: Link = None
    self: Link = None

    def __init__(self_, **kvargs):
        if "items" in kvargs:
            if type(kvargs["items"]).__name__ is self_.__annotations__["items"]:
                self_.items = kvargs["items"]
            else:
                self_.items = Link(**kvargs["items"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ is self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionMetaResponseBody:
    """
    Collection metadata and computed fields.

    Attributes
    ----------
    items: ItemsResultResponseBody
      Multiple items.
    """

    items: ItemsResultResponseBody = None

    def __init__(self_, **kvargs):
        if "items" in kvargs:
            if type(kvargs["items"]).__name__ is self_.__annotations__["items"]:
                self_.items = kvargs["items"]
            else:
                self_.items = ItemsResultResponseBody(**kvargs["items"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionResultResponseBody:
    """
    A collection.

    Attributes
    ----------
    createdAt: str
      The RFC3339 datetime when the collection was created.
    id: str
      The collection's unique identifier.
    itemCount: int
      The number of items that have been added to the collection.
    links: CollectionLinksResponseBody
    name: str
    tenantId: str
      The ID of the tenant that owns the collection. This property is populated by using JWT.
    type: str
      The collection's type.
    updatedAt: str
      The RFC3339 datetime when the collection was last updated.
    creatorId: str
      The ID of the user who created the collection. This property is only populated if the JWT contains a userId.
    description: str
    meta: CollectionMetaResponseBody
      Collection metadata and computed fields.
    updaterId: str
      The ID of the user who last updated the collection. This property is only populated if the JWT contains a userId.
    """

    createdAt: str = None
    id: str = None
    itemCount: int = None
    links: CollectionLinksResponseBody = None
    name: str = None
    tenantId: str = None
    type: str = None
    updatedAt: str = None
    creatorId: str = None
    description: str = None
    meta: CollectionMetaResponseBody = None
    updaterId: str = None

    def __init__(self_, **kvargs):
        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ is self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "itemCount" in kvargs:
            if type(kvargs["itemCount"]).__name__ is self_.__annotations__["itemCount"]:
                self_.itemCount = kvargs["itemCount"]
            else:
                self_.itemCount = kvargs["itemCount"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = CollectionLinksResponseBody(**kvargs["links"])
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
        if "creatorId" in kvargs:
            if type(kvargs["creatorId"]).__name__ is self_.__annotations__["creatorId"]:
                self_.creatorId = kvargs["creatorId"]
            else:
                self_.creatorId = kvargs["creatorId"]
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
                self_.meta = CollectionMetaResponseBody(**kvargs["meta"])
        if "updaterId" in kvargs:
            if type(kvargs["updaterId"]).__name__ is self_.__annotations__["updaterId"]:
                self_.updaterId = kvargs["updaterId"]
            else:
                self_.updaterId = kvargs["updaterId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionsLinksResponseBody:
    """

    Attributes
    ----------
    item: Link
    next: Link
    prev: Link
    self: Link
    """

    item: Link = None
    next: Link = None
    prev: Link = None
    self: Link = None

    def __init__(self_, **kvargs):
        if "item" in kvargs:
            if type(kvargs["item"]).__name__ is self_.__annotations__["item"]:
                self_.item = kvargs["item"]
            else:
                self_.item = Link(**kvargs["item"])
        if "next" in kvargs:
            if type(kvargs["next"]).__name__ is self_.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs:
            if type(kvargs["prev"]).__name__ is self_.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ is self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemLinksResponseBody:
    """

    Attributes
    ----------
    collections: Link
    open: Link
    self: Link
    thumbnail: Link
    """

    collections: Link = None
    open: Link = None
    self: Link = None
    thumbnail: Link = None

    def __init__(self_, **kvargs):
        if "collections" in kvargs:
            if (
                type(kvargs["collections"]).__name__
                is self_.__annotations__["collections"]
            ):
                self_.collections = kvargs["collections"]
            else:
                self_.collections = Link(**kvargs["collections"])
        if "open" in kvargs:
            if type(kvargs["open"]).__name__ is self_.__annotations__["open"]:
                self_.open = kvargs["open"]
            else:
                self_.open = Link(**kvargs["open"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ is self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        if "thumbnail" in kvargs:
            if type(kvargs["thumbnail"]).__name__ is self_.__annotations__["thumbnail"]:
                self_.thumbnail = kvargs["thumbnail"]
            else:
                self_.thumbnail = Link(**kvargs["thumbnail"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemMetaResponseBody:
    """
    Item metadata and computed fields.

    Attributes
    ----------
    actions: list[str]
      The actions that the user can perform on the item.
    collections: list[ItemTagResponseBody]
      An array of collections that the item is part of.
    isFavorited: bool
      The flag that indicates if item is in the user's favorites collection.
    tags: list[ItemTagResponseBody]
      An array of tags that the item is part of.
    """

    actions: list[str] = None
    collections: list[ItemTagResponseBody] = None
    isFavorited: bool = None
    tags: list[ItemTagResponseBody] = None

    def __init__(self_, **kvargs):
        if "actions" in kvargs:
            if type(kvargs["actions"]).__name__ is self_.__annotations__["actions"]:
                self_.actions = kvargs["actions"]
            else:
                self_.actions = kvargs["actions"]
        if "collections" in kvargs:
            if (
                type(kvargs["collections"]).__name__
                is self_.__annotations__["collections"]
            ):
                self_.collections = kvargs["collections"]
            else:
                self_.collections = [
                    ItemTagResponseBody(**e) for e in kvargs["collections"]
                ]
        if "isFavorited" in kvargs:
            if (
                type(kvargs["isFavorited"]).__name__
                is self_.__annotations__["isFavorited"]
            ):
                self_.isFavorited = kvargs["isFavorited"]
            else:
                self_.isFavorited = kvargs["isFavorited"]
        if "tags" in kvargs:
            if type(kvargs["tags"]).__name__ is self_.__annotations__["tags"]:
                self_.tags = kvargs["tags"]
            else:
                self_.tags = [ItemTagResponseBody(**e) for e in kvargs["tags"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemTagResponseBody:
    """
    Holds basic information about a tag or collection.

    Attributes
    ----------
    id: str
      The ID of the tag/collection.
    name: str
      The name of the tag/collection.
    """

    id: str = None
    name: str = None

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
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemViewsResponseBody:
    """

    Attributes
    ----------
    total: int
      Total number of views the resource got during the last 28 days.
    trend: float
      Trend in views over the last 4 weeks.
    unique: int
      Number of unique users who viewed the resource during the last 28 days.
    usedBy: int
      Number of apps this dataset is used in (datasets only).
    week: list[ItemViewsWeeksResponseBody]
    """

    total: int = None
    trend: float = None
    unique: int = None
    usedBy: int = None
    week: list[ItemViewsWeeksResponseBody] = None

    def __init__(self_, **kvargs):
        if "total" in kvargs:
            if type(kvargs["total"]).__name__ is self_.__annotations__["total"]:
                self_.total = kvargs["total"]
            else:
                self_.total = kvargs["total"]
        if "trend" in kvargs:
            if type(kvargs["trend"]).__name__ is self_.__annotations__["trend"]:
                self_.trend = kvargs["trend"]
            else:
                self_.trend = kvargs["trend"]
        if "unique" in kvargs:
            if type(kvargs["unique"]).__name__ is self_.__annotations__["unique"]:
                self_.unique = kvargs["unique"]
            else:
                self_.unique = kvargs["unique"]
        if "usedBy" in kvargs:
            if type(kvargs["usedBy"]).__name__ is self_.__annotations__["usedBy"]:
                self_.usedBy = kvargs["usedBy"]
            else:
                self_.usedBy = kvargs["usedBy"]
        if "week" in kvargs:
            if type(kvargs["week"]).__name__ is self_.__annotations__["week"]:
                self_.week = kvargs["week"]
            else:
                self_.week = [ItemViewsWeeksResponseBody(**e) for e in kvargs["week"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemViewsWeeksResponseBody:
    """

    Attributes
    ----------
    start: str
      The RFC3339 datetime representing the start of the referenced week.
    total: int
      Total number of views the resource got during the referenced week.
    unique: int
      Number of unique users who viewed the resource during the referenced week.
    """

    start: str = None
    total: int = None
    unique: int = None

    def __init__(self_, **kvargs):
        if "start" in kvargs:
            if type(kvargs["start"]).__name__ is self_.__annotations__["start"]:
                self_.start = kvargs["start"]
            else:
                self_.start = kvargs["start"]
        if "total" in kvargs:
            if type(kvargs["total"]).__name__ is self_.__annotations__["total"]:
                self_.total = kvargs["total"]
            else:
                self_.total = kvargs["total"]
        if "unique" in kvargs:
            if type(kvargs["unique"]).__name__ is self_.__annotations__["unique"]:
                self_.unique = kvargs["unique"]
            else:
                self_.unique = kvargs["unique"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsLinksResponseBody:
    """

    Attributes
    ----------
    collection: Link
    next: Link
    prev: Link
    self: Link
    """

    collection: Link = None
    next: Link = None
    prev: Link = None
    self: Link = None

    def __init__(self_, **kvargs):
        if "collection" in kvargs:
            if (
                type(kvargs["collection"]).__name__
                is self_.__annotations__["collection"]
            ):
                self_.collection = kvargs["collection"]
            else:
                self_.collection = Link(**kvargs["collection"])
        if "next" in kvargs:
            if type(kvargs["next"]).__name__ is self_.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs:
            if type(kvargs["prev"]).__name__ is self_.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ is self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsResourceSizeResponseBody:
    """

    Attributes
    ----------
    appFile: float
      Size of the app on disk in bytes.
    appMemory: float
      Size of the app in memory in bytes.
    """

    appFile: float = None
    appMemory: float = None

    def __init__(self_, **kvargs):
        if "appFile" in kvargs:
            if type(kvargs["appFile"]).__name__ is self_.__annotations__["appFile"]:
                self_.appFile = kvargs["appFile"]
            else:
                self_.appFile = kvargs["appFile"]
        if "appMemory" in kvargs:
            if type(kvargs["appMemory"]).__name__ is self_.__annotations__["appMemory"]:
                self_.appMemory = kvargs["appMemory"]
            else:
                self_.appMemory = kvargs["appMemory"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsResultResponseBody:
    """
    Multiple items.

    Attributes
    ----------
    data: list[ItemResultResponseBody]
    links: ItemsLinksResponseBody
    """

    data: list[ItemResultResponseBody] = None
    links: ItemsLinksResponseBody = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [ItemResultResponseBody(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ItemsLinksResponseBody(**kvargs["links"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Items:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_items(
        self,
        next: str = None,
        prev: str = None,
        limit: int = None,
        sort: str = None,
        resourceType: str = None,
        resourceSubType: str = None,
        resourceId: str = None,
        resourceLink: str = None,
        spaceId: str = None,
        shared: bool = None,
        collectionId: str = None,
        createdByUserId: str = None,
        notCreatedByUserId: str = None,
        ownerId: str = None,
        notOwnerId: str = None,
        id: str = None,
        query: str = None,
        name: str = None,
        noActions: bool = None,
        max_items: int = 10,
    ) -> ListableResource[ItemResultResponseBody]:
        """
        Retrieves items that the user has access to.
        Finds and returns items that the user has access to.


        next: str
          The cursor to the next page of resources. Provide either the next or prev cursor, but not both.

        prev: str
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.

        limit: int
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).

        sort: str
          The property of a resource to sort on (default sort is +createdAt). The supported properties are createdAt, updatedAt, and name. A property must be prefixed by + or - to indicate ascending or descending sort order respectively.

        resourceType: str
          The case-sensitive string used to filter items by resourceType(s). For example '?resourceType=app,qvapp'

        resourceSubType: str
          the case-sensitive string used to filter items by resourceSubType(s). For example '?resourceSubType=chart-monitoring,qix-df,qvd'

        resourceId: str
          The case-sensitive string used to search for an item by resourceId. If resourceId is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.

        resourceLink: str
          The case-sensitive string used to search for an item by resourceLink. If resourceLink is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.

        spaceId: str
          The space's unique identifier (supports \'personal\' as spaceId).

        shared: bool
          Whether or not to return items in a shared space.

        collectionId: str
          The collection's unique identifier.

        createdByUserId: str
          User's unique identifier.

        notCreatedByUserId: str
          User's unique identifier.

        ownerId: str
          Owner identifier.

        notOwnerId: str
          Owner identifier.

        id: str
          The item's unique identifier.

        query: str
          The case-insensitive string used to search for a resource by name or description.

        name: str
          The case-insensitive string used to search for a resource by name.

        noActions: bool
          If set to true, the user's available actions for each item will not be evaluated meaning the actions-array will be omitted from the response (reduces response time).

        Parameters
        ----------
        next: str = None
        prev: str = None
        limit: int = None
        sort: str = None
        resourceType: str = None
        resourceSubType: str = None
        resourceId: str = None
        resourceLink: str = None
        spaceId: str = None
        shared: bool = None
        collectionId: str = None
        createdByUserId: str = None
        notCreatedByUserId: str = None
        ownerId: str = None
        notOwnerId: str = None
        id: str = None
        query: str = None
        name: str = None
        noActions: bool = None
        """
        query_params = {}
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if limit is not None:
            query_params["limit"] = limit
        if sort is not None:
            query_params["sort"] = sort
        if resourceType is not None:
            query_params["resourceType"] = resourceType
        if resourceSubType is not None:
            query_params["resourceSubType"] = resourceSubType
        if resourceId is not None:
            query_params["resourceId"] = resourceId
        if resourceLink is not None:
            query_params["resourceLink"] = resourceLink
        if spaceId is not None:
            query_params["spaceId"] = spaceId
        if shared is not None:
            query_params["shared"] = shared
        if collectionId is not None:
            query_params["collectionId"] = collectionId
        if createdByUserId is not None:
            query_params["createdByUserId"] = createdByUserId
        if notCreatedByUserId is not None:
            query_params["notCreatedByUserId"] = notCreatedByUserId
        if ownerId is not None:
            query_params["ownerId"] = ownerId
        if notOwnerId is not None:
            query_params["notOwnerId"] = notOwnerId
        if id is not None:
            query_params["id"] = id
        if query is not None:
            query_params["query"] = query
        if name is not None:
            query_params["name"] = name
        if noActions is not None:
            query_params["noActions"] = noActions

        response = self.auth.rest(
            path="/items",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=ItemResultResponseBody,
            auth=self.auth,
            path="/items",
            max_items=max_items,
            query_params=query_params,
        )

    def create(self, data: ItemsCreateItemRequestBody) -> ItemResultResponseBody:
        """
        Experimental
        Creates and returns a new item.
        Creates and returns a new item.
        An item references an internal or external resource. A resource cannot be both internal and external.

        `resourceType` must be provided for both internal and external items.

        `resourceId` must be provided for internal items.

        `resourceLink` must be provided for external items.

        For a given tenant, an item's resourceId or resourceLink is unique.


        Parameters
        ----------
        data: ItemsCreateItemRequestBody
        """
        warnings.warn("create is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/items",
            method="POST",
            params={},
            data=data,
        )
        obj = ItemResultResponseBody(**response.json())
        obj.auth = self.auth
        return obj

    def get_settings(self) -> ItemsSettingsResponseBody:
        """
        Experimental
        Returns tenant specific settings.
        Finds and returns the settings for the current tenant.


        Parameters
        ----------
        """
        warnings.warn("get_settings is experimental", UserWarning, stacklevel=2)

        response = self.auth.rest(
            path="/items/settings",
            method="GET",
            params={},
            data=None,
        )
        obj = ItemsSettingsResponseBody(**response.json())
        obj.auth = self.auth
        return obj

    def patch_settings(self, data: ItemsSettingsPatch) -> ItemsSettingsResponseBody:
        """
        Experimental
        Patches tenant specific settings.
        Updates the settings provided in the patch body.


        Parameters
        ----------
        data: ItemsSettingsPatch
        """
        warnings.warn("patch_settings is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/items/settings",
            method="PATCH",
            params={},
            data=data,
        )
        obj = ItemsSettingsResponseBody(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, itemId: str) -> ItemResultResponseBody:
        """
        Returns an item.
        Finds and returns an item.


        itemId: str
          The item's unique identifier

        Parameters
        ----------
        itemId: str
        """

        response = self.auth.rest(
            path="/items/{itemId}".replace("{itemId}", itemId),
            method="GET",
            params={},
            data=None,
        )
        obj = ItemResultResponseBody(**response.json())
        obj.auth = self.auth
        return obj
