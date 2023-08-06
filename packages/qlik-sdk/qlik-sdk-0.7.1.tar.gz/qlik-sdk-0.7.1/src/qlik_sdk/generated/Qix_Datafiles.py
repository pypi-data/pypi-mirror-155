# This is spectacularly generated code by spectacular v0.0.0 based on
# Data Files API 1.30.0

from __future__ import annotations

import io
import warnings
from dataclasses import dataclass

from ..auth import Auth, Config


@dataclass
class DataFileUploadResponse:
    """

    Attributes
    ----------
    createdDate: str
      The date that the uploaded file was created.
    id: str
      The ID for the uploaded file.
    name: str
      The name of the uploaded file.
    ownerId: str
      The 'owner' of a file is the user who last uploaded the file's content.
    size: int
      The size of the uploaded file, in bytes.
    appId: str
      If this file is bound to the lifecycle of a specific app, this is the ID of this app.
    modifiedDate: str
      The date that the updated file was last modified.
    spaceId: str
      If the file was uploaded to a team space, this is the ID of that space.
    """

    createdDate: str = None
    id: str = None
    name: str = None
    ownerId: str = None
    size: int = None
    appId: str = None
    modifiedDate: str = None
    spaceId: str = None

    def __init__(self_, **kvargs):
        if "createdDate" in kvargs:
            if (
                type(kvargs["createdDate"]).__name__
                is self_.__annotations__["createdDate"]
            ):
                self_.createdDate = kvargs["createdDate"]
            else:
                self_.createdDate = kvargs["createdDate"]
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
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ is self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        if "size" in kvargs:
            if type(kvargs["size"]).__name__ is self_.__annotations__["size"]:
                self_.size = kvargs["size"]
            else:
                self_.size = kvargs["size"]
        if "appId" in kvargs:
            if type(kvargs["appId"]).__name__ is self_.__annotations__["appId"]:
                self_.appId = kvargs["appId"]
            else:
                self_.appId = kvargs["appId"]
        if "modifiedDate" in kvargs:
            if (
                type(kvargs["modifiedDate"]).__name__
                is self_.__annotations__["modifiedDate"]
            ):
                self_.modifiedDate = kvargs["modifiedDate"]
            else:
                self_.modifiedDate = kvargs["modifiedDate"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_connection(self) -> ConnectionsResponse:
        """
        Experimental
        Get the built-in connections used by the engine to load/write data files given a connection ID.

        Parameters
        ----------
        """
        warnings.warn("get_connection is experimental", UserWarning, stacklevel=2)

        response = self.auth.rest(
            path="/qix-datafiles/connections/{id}".replace("{id}", self.id),
            method="GET",
            params={},
            data=None,
        )
        obj = ConnectionsResponse(**response.json())
        obj.auth = self.auth
        return obj

    def change_owner(self, ownerId: str = None) -> None:
        """
        Experimental
        Change the owner of an existing data file.  This is primarily and admin-type of operation.  In general, the
        owner of a data file is implicitly set as part of a data file upload.  For data files which reside in a
        personal space, changing the owner has the effect of moving the data file to te new owner's personal space.

        Parameters
        ----------
        ownerId: str = None
        """
        warnings.warn("change-owner is experimental", UserWarning, stacklevel=2)
        query_params = {}
        if ownerId is not None:
            query_params["ownerId"] = ownerId

        self.auth.rest(
            path="/qix-datafiles/{id}/actions/change-owner".replace("{id}", self.id),
            method="POST",
            params=query_params,
            data=None,
        )

    def change_space(self, spaceId: str = None) -> None:
        """
        Experimental
        Change the space that an existing data file resides in.  This is to allow for a separate admin-type of
        operation that is more global in terms of access in cases where admin users may not explicitly have been
        granted full access to a given space within the declared space-level permissions.  If the space ID is set
        to null, then the datafile will end up residing in the personal space of the user who is the owner of the
        file.

        Parameters
        ----------
        spaceId: str = None
        """
        warnings.warn("change-space is experimental", UserWarning, stacklevel=2)
        query_params = {}
        if spaceId is not None:
            query_params["spaceId"] = spaceId

        self.auth.rest(
            path="/qix-datafiles/{id}/actions/change-space".replace("{id}", self.id),
            method="POST",
            params=query_params,
            data=None,
        )

    def delete(self) -> None:
        """
        Experimental
        Delete the specified data file.

        Parameters
        ----------
        """
        warnings.warn("delete is experimental", UserWarning, stacklevel=2)

        self.auth.rest(
            path="/qix-datafiles/{id}".replace("{id}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def set(
        self,
        Data: io.BufferedReader = None,
        Name: str = None,
        AppId: str = None,
        ConnectionId: str = None,
        SourceId: str = None,
        TempContentFileId: str = None,
    ) -> DataFileUploadResponse:
        """
        Experimental
        Re-upload an existing data file.

        Parameters
        ----------
        Name: str = None
        AppId: str = None
        ConnectionId: str = None
        SourceId: str = None
        TempContentFileId: str = None
        """
        warnings.warn("set is experimental", UserWarning, stacklevel=2)
        query_params = {}
        if Name is not None:
            query_params["Name"] = Name
        if AppId is not None:
            query_params["AppId"] = AppId
        if ConnectionId is not None:
            query_params["ConnectionId"] = ConnectionId
        if SourceId is not None:
            query_params["SourceId"] = SourceId
        if TempContentFileId is not None:
            query_params["TempContentFileId"] = TempContentFileId

        files_dict = {}
        files_dict["Data"] = Data

        response = self.auth.rest(
            path="/qix-datafiles/{id}".replace("{id}", self.id),
            method="PUT",
            params=query_params,
            data=None,
            files=files_dict,
        )
        self.__init__(**response.json())
        return self


@dataclass
class ConnectionsResponse:
    """

    Attributes
    ----------
    connectStatement: str
      The connect statement that will be passed to the connector when invoked.
    id: str
    name: str
      The name of the connection.
    type: str
      The type of the connection.
    spaceId: str
      The team space that the given connection is associated with. If null, the connection is not associated
      with any specific team space.
    """

    connectStatement: str = None
    id: str = None
    name: str = None
    type: str = None
    spaceId: str = None

    def __init__(self_, **kvargs):
        if "connectStatement" in kvargs:
            if (
                type(kvargs["connectStatement"]).__name__
                is self_.__annotations__["connectStatement"]
            ):
                self_.connectStatement = kvargs["connectStatement"]
            else:
                self_.connectStatement = kvargs["connectStatement"]
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
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ is self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataFileDeleteRecordResponse:
    """

    Attributes
    ----------
    createdByUser: str
      The user that deleted this datafile.
    deletedDate: str
      The date that the file was deleted.
    fileMetadataId: str
      The unique ID of the file that was deleted.
    name: str
      File Name
    tenantId: str
      The tenant that this file is scoped to.
    spaceId: str
      If not null, the ID of the space that the uploaded file will reside in. If null, this implies that the
      file is stored in the user-private area (DataFiles)
    userId: str
      If the file resided in a user's personal space, the user that this file is scoped to.
    """

    createdByUser: str = None
    deletedDate: str = None
    fileMetadataId: str = None
    name: str = None
    tenantId: str = None
    spaceId: str = None
    userId: str = None

    def __init__(self_, **kvargs):
        if "createdByUser" in kvargs:
            if (
                type(kvargs["createdByUser"]).__name__
                is self_.__annotations__["createdByUser"]
            ):
                self_.createdByUser = kvargs["createdByUser"]
            else:
                self_.createdByUser = kvargs["createdByUser"]
        if "deletedDate" in kvargs:
            if (
                type(kvargs["deletedDate"]).__name__
                is self_.__annotations__["deletedDate"]
            ):
                self_.deletedDate = kvargs["deletedDate"]
            else:
                self_.deletedDate = kvargs["deletedDate"]
        if "fileMetadataId" in kvargs:
            if (
                type(kvargs["fileMetadataId"]).__name__
                is self_.__annotations__["fileMetadataId"]
            ):
                self_.fileMetadataId = kvargs["fileMetadataId"]
            else:
                self_.fileMetadataId = kvargs["fileMetadataId"]
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
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        if "userId" in kvargs:
            if type(kvargs["userId"]).__name__ is self_.__annotations__["userId"]:
                self_.userId = kvargs["userId"]
            else:
                self_.userId = kvargs["userId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataFileModificationResponse:
    """

    Attributes
    ----------
    createdByUser: str
      The ID of the user that created the file.
    createdDate: str
      The date that the uploaded file was created.
    id: str
      The ID for the uploaded file.
    name: str
      The name of the uploaded file.
    ownerId: str
      The 'owner' of a file is the user who last uploaded the file's content.
    size: int
      The size of the uploaded file, in bytes.
    tenantId: str
      The ID of the tenant that this file is scoped to.
    appId: str
      If this file is bound to the lifecycle of a specific app, this is the ID of this app.
    modifiedByUser: str
      The ID of the user that last modified the file.
    modifiedDate: str
      The date that the updated file was last modified.
    spaceId: str
      If the file was uploaded to a team space, this is the ID of that space.
    userId: str
      If the file resides in that user's personal space, the ID of the user that this file is scoped to.
    """

    createdByUser: str = None
    createdDate: str = None
    id: str = None
    name: str = None
    ownerId: str = None
    size: int = None
    tenantId: str = None
    appId: str = None
    modifiedByUser: str = None
    modifiedDate: str = None
    spaceId: str = None
    userId: str = None

    def __init__(self_, **kvargs):
        if "createdByUser" in kvargs:
            if (
                type(kvargs["createdByUser"]).__name__
                is self_.__annotations__["createdByUser"]
            ):
                self_.createdByUser = kvargs["createdByUser"]
            else:
                self_.createdByUser = kvargs["createdByUser"]
        if "createdDate" in kvargs:
            if (
                type(kvargs["createdDate"]).__name__
                is self_.__annotations__["createdDate"]
            ):
                self_.createdDate = kvargs["createdDate"]
            else:
                self_.createdDate = kvargs["createdDate"]
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
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ is self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        if "size" in kvargs:
            if type(kvargs["size"]).__name__ is self_.__annotations__["size"]:
                self_.size = kvargs["size"]
            else:
                self_.size = kvargs["size"]
        if "tenantId" in kvargs:
            if type(kvargs["tenantId"]).__name__ is self_.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "appId" in kvargs:
            if type(kvargs["appId"]).__name__ is self_.__annotations__["appId"]:
                self_.appId = kvargs["appId"]
            else:
                self_.appId = kvargs["appId"]
        if "modifiedByUser" in kvargs:
            if (
                type(kvargs["modifiedByUser"]).__name__
                is self_.__annotations__["modifiedByUser"]
            ):
                self_.modifiedByUser = kvargs["modifiedByUser"]
            else:
                self_.modifiedByUser = kvargs["modifiedByUser"]
        if "modifiedDate" in kvargs:
            if (
                type(kvargs["modifiedDate"]).__name__
                is self_.__annotations__["modifiedDate"]
            ):
                self_.modifiedDate = kvargs["modifiedDate"]
            else:
                self_.modifiedDate = kvargs["modifiedDate"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        if "userId" in kvargs:
            if type(kvargs["userId"]).__name__ is self_.__annotations__["userId"]:
                self_.userId = kvargs["userId"]
            else:
                self_.userId = kvargs["userId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class QuotaResponse:
    """

    Attributes
    ----------
    allowedExtensions: list[str]
      The allowed file extensions on files that are uploaded.
    allowedInternalExtensions: list[str]
      The allowed file extensions for files that are only used internally by the system (and thus not typically
      shown to end users).
    maxFileSize: int
      Maximum allowable size of an uploaded file.
    maxLargeFileSize: int
      Maximum allowable size for a single uploaded large data file (in bytes). This is a file that was indirectly
      uploaded using the temp content service chunked upload capability.
    maxSize: int
      The maximum aggregate size of all files uploaded by a given user.
    size: int
      The current aggregate size of all files uploaded by a given user. If the current aggregate size is greater
      than the maximum aggregate size, this is a quota violation.
    """

    allowedExtensions: list[str] = None
    allowedInternalExtensions: list[str] = None
    maxFileSize: int = None
    maxLargeFileSize: int = None
    maxSize: int = None
    size: int = None

    def __init__(self_, **kvargs):
        if "allowedExtensions" in kvargs:
            if (
                type(kvargs["allowedExtensions"]).__name__
                is self_.__annotations__["allowedExtensions"]
            ):
                self_.allowedExtensions = kvargs["allowedExtensions"]
            else:
                self_.allowedExtensions = kvargs["allowedExtensions"]
        if "allowedInternalExtensions" in kvargs:
            if (
                type(kvargs["allowedInternalExtensions"]).__name__
                is self_.__annotations__["allowedInternalExtensions"]
            ):
                self_.allowedInternalExtensions = kvargs["allowedInternalExtensions"]
            else:
                self_.allowedInternalExtensions = kvargs["allowedInternalExtensions"]
        if "maxFileSize" in kvargs:
            if (
                type(kvargs["maxFileSize"]).__name__
                is self_.__annotations__["maxFileSize"]
            ):
                self_.maxFileSize = kvargs["maxFileSize"]
            else:
                self_.maxFileSize = kvargs["maxFileSize"]
        if "maxLargeFileSize" in kvargs:
            if (
                type(kvargs["maxLargeFileSize"]).__name__
                is self_.__annotations__["maxLargeFileSize"]
            ):
                self_.maxLargeFileSize = kvargs["maxLargeFileSize"]
            else:
                self_.maxLargeFileSize = kvargs["maxLargeFileSize"]
        if "maxSize" in kvargs:
            if type(kvargs["maxSize"]).__name__ is self_.__annotations__["maxSize"]:
                self_.maxSize = kvargs["maxSize"]
            else:
                self_.maxSize = kvargs["maxSize"]
        if "size" in kvargs:
            if type(kvargs["size"]).__name__ is self_.__annotations__["size"]:
                self_.size = kvargs["size"]
            else:
                self_.size = kvargs["size"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class QixDatafiles:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_qix_datafiles(
        self,
        connectionId: str = None,
        appId: str = None,
        name: str = None,
        top: int = None,
        skip: int = None,
        ownerId: str = None,
        allowInternalFiles: bool = None,
    ) -> list[DataFileUploadResponse]:
        """
        Experimental
        Get descriptive info for the specified data files.


        connectionId: str
          Return files that reside in the space referenced by the specified DataFiles connection. If this parameter is not specified, the user's private space is implied.

        appId: str
          Only return files scoped to the specified app. If this parameter is not specified, only files that are not scoped to any app are returned. "*" implies all app-scoped files are returned.

        name: str
          Filter the list of files returned to the given file name.

        top: int
          If present, restrict the number of returned items to this value.

        skip: int
          If present, skip this number of the returned values in the result set (facilitates paging).

        ownerId: str
          If present, fetch the datafiles for the specified owner. If a connectionId is specified in this case, the returned list is constrained to the specified space. If connectionId is not specified, then all files owned by the specified user are returned regardless of the personal space that a given file resides in.

        allowInternalFiles: bool
          If set to false, do not return datafiles with internal extension else return all the datafiles.

        Parameters
        ----------
        connectionId: str = None
        appId: str = None
        name: str = None
        top: int = None
        skip: int = None
        ownerId: str = None
        allowInternalFiles: bool = None
        """
        warnings.warn("get_qix-datafiles is experimental", UserWarning, stacklevel=2)
        query_params = {}
        if connectionId is not None:
            query_params["connectionId"] = connectionId
        if appId is not None:
            query_params["appId"] = appId
        if name is not None:
            query_params["name"] = name
        if top is not None:
            query_params["top"] = top
        if skip is not None:
            query_params["skip"] = skip
        if ownerId is not None:
            query_params["ownerId"] = ownerId
        if allowInternalFiles is not None:
            query_params["allowInternalFiles"] = allowInternalFiles

        response = self.auth.rest(
            path="/qix-datafiles",
            method="GET",
            params=query_params,
            data=None,
        )
        return [DataFileUploadResponse(**e) for e in response.json()]

    def create(
        self,
        Data: io.BufferedReader = None,
        Name: str = None,
        AppId: str = None,
        ConnectionId: str = None,
        SourceId: str = None,
        TempContentFileId: str = None,
    ) -> DataFileUploadResponse:
        """
        Experimental
        Upload a new data file.  For the upload of a new file, the 'name' parameter is required.


        Name: str
          Name that will be given to the uploaded file. If this name is different than the name used when the file
          was last POSTed or PUT, this will result in a rename of the file. It should be noted that the '/' character
          in a datafile name indicates a 'path' separator in a logical folder hierarchy for the name. Names which
          contain '/'s should be used with the assumption that a logical 'folder hierarchy' is being defined for the
          full pathname of that file. IE, '/' is a significant character in the datafile name, and may impact the
          behavior of future APIs which take this folder hierarchy into account.

        AppId: str
          If this file should be bound to the lifecycle of a specific app, this is the ID of this app.

        ConnectionId: str
          If present, this is the DataFiles connection that the upload should occur in the context of. If absent,
          the default is that the upload will occur in the context of the MyDataFiles connection. If the DataFiles
          connection is different from the one specified when the file was last POSTed or PUT, this will result in
          a logical move of this file into the new space.

        SourceId: str
          If a SourceId is specified, this is the ID of the existing datafile whose content should be copied into
          the specified datafile. That is, instead of the file content being specified in the Data element,
          it is effectively copied from an existing. previously uploaded file.

        TempContentFileId: str
          If a TempContentFileId is specified, this is the ID of a previously uploaded temporary content file whose
          content should be copied into the specified datafile. That is, instead of the file content being specified
          in the Data element, it is effectively copied from an existing. previously uploaded file. The expectation
          is that this file was previously uploaded to the temporoary content service, and the ID specified here is
          the one returned from the temp content upload request.

        Parameters
        ----------
        Name: str = None
        AppId: str = None
        ConnectionId: str = None
        SourceId: str = None
        TempContentFileId: str = None
        """
        warnings.warn("create is experimental", UserWarning, stacklevel=2)
        query_params = {}
        if Name is not None:
            query_params["Name"] = Name
        if AppId is not None:
            query_params["AppId"] = AppId
        if ConnectionId is not None:
            query_params["ConnectionId"] = ConnectionId
        if SourceId is not None:
            query_params["SourceId"] = SourceId
        if TempContentFileId is not None:
            query_params["TempContentFileId"] = TempContentFileId

        files_dict = {}
        files_dict["Data"] = Data

        response = self.auth.rest(
            path="/qix-datafiles",
            method="POST",
            params=query_params,
            data=None,
            files=files_dict,
        )
        obj = DataFileUploadResponse(**response.json())
        obj.auth = self.auth
        return obj

    def get_connections(
        self,
        appId: str = None,
        name: str = None,
        spaceId: str = None,
        personal: bool = None,
    ) -> list[ConnectionsResponse]:
        """
        Experimental
        Get the list of built-in connections used by the engine to load/write data files.  The non-filtered list
        contains a set of hardcoded connections, along with 1 connection per team space that the given user has
        access to.


        appId: str
          Optional. If present, get connections with connection strings which are scoped to the given app ID.

        name: str
          Optional. If present, only return connections with the given name.

        spaceId: str
          Optional. If present, only return the connection which accesses data files in the specified space.

        personal: bool
          Optional. If true, only return the connections which access data in a personal space. Default is false.

        Parameters
        ----------
        appId: str = None
        name: str = None
        spaceId: str = None
        personal: bool = None
        """
        warnings.warn("get_connections is experimental", UserWarning, stacklevel=2)
        query_params = {}
        if appId is not None:
            query_params["appId"] = appId
        if name is not None:
            query_params["name"] = name
        if spaceId is not None:
            query_params["spaceId"] = spaceId
        if personal is not None:
            query_params["personal"] = personal

        response = self.auth.rest(
            path="/qix-datafiles/connections",
            method="GET",
            params=query_params,
            data=None,
        )
        return [ConnectionsResponse(**e) for e in response.json()]

    def get_deletes(
        self,
        deleteStartDate: str = None,
        deleteEndDate: str = None,
        top: int = None,
        skip: int = None,
        allowInternalFiles: bool = None,
    ) -> list[DataFileDeleteRecordResponse]:
        """
        Experimental
        Get descriptive info for data files which have been deleted between the specified start and end dates.  This
        endpoint will enumerate all deleted data files across a given tenant regardless of which (personal or shared) space
        the files reside in.  Note that elevated (service-to-service) priviledges are required to invoke this
        endpoint.


        deleteStartDate: str
          If specified, the returned list will only include datafiles which have been deleted since the
          specified date (inclusive). The date should be specified in Zulu time format (for example: 2020-07-07T20:52:40.8534780Z).

        deleteEndDate: str
          If specified, the returned list will only include datafiles which have been deleted prior to the
          specified data (inclusive). The date should be specified in Zulu time format (for example: 2020-07-07T20:52:40.8534780Z).

        top: int
          If present, restrict the number of returned items to this value.

        skip: int
          If present, skip this number of the returned values in the result set (facilitates paging).

        allowInternalFiles: bool
          If set to false, do not return datafiles with internal extension else return all the datafiles.

        Parameters
        ----------
        deleteStartDate: str = None
        deleteEndDate: str = None
        top: int = None
        skip: int = None
        allowInternalFiles: bool = None
        """
        warnings.warn("get_deletes is experimental", UserWarning, stacklevel=2)
        query_params = {}
        if deleteStartDate is not None:
            query_params["deleteStartDate"] = deleteStartDate
        if deleteEndDate is not None:
            query_params["deleteEndDate"] = deleteEndDate
        if top is not None:
            query_params["top"] = top
        if skip is not None:
            query_params["skip"] = skip
        if allowInternalFiles is not None:
            query_params["allowInternalFiles"] = allowInternalFiles

        response = self.auth.rest(
            path="/qix-datafiles/deletes",
            method="GET",
            params=query_params,
            data=None,
        )
        return [DataFileDeleteRecordResponse(**e) for e in response.json()]

    def get_modifications(
        self,
        modifiedStartDate: str = None,
        modifiedEndDate: str = None,
        top: int = None,
        skip: int = None,
        allowInternalFiles: bool = None,
    ) -> list[DataFileModificationResponse]:
        """
        Experimental
        Get descriptive info for data files which have been modified between the specified start and end dates.  This
        endpoint will enumerate all data files across a given tenant regardless of which (personal or shared) space
        the files reside in.  Note that elevated (service-to-service) priviledges are required to invoke this
        endpoint.


        modifiedStartDate: str
          If specified, the returned list will only include datafiles which have been created or modified since the
          specified date (inclusive). The date should be specified in Zulu time format (for example: 2020-07-07T20:52:40.8534780Z).

        modifiedEndDate: str
          If specified, the returned list will only include datafiles which have been created or modified prior to the
          specified data (inclusive). The date should be specified in Zulu time format (for example: 2020-07-07T20:52:40.8534780Z).

        top: int
          If present, restrict the number of returned items to this value.

        skip: int
          If present, skip this number of the returned values in the result set (facilitates paging).

        allowInternalFiles: bool
          If set to false, do not return datafiles with internal extension else return all the datafiles.

        Parameters
        ----------
        modifiedStartDate: str = None
        modifiedEndDate: str = None
        top: int = None
        skip: int = None
        allowInternalFiles: bool = None
        """
        warnings.warn("get_modifications is experimental", UserWarning, stacklevel=2)
        query_params = {}
        if modifiedStartDate is not None:
            query_params["modifiedStartDate"] = modifiedStartDate
        if modifiedEndDate is not None:
            query_params["modifiedEndDate"] = modifiedEndDate
        if top is not None:
            query_params["top"] = top
        if skip is not None:
            query_params["skip"] = skip
        if allowInternalFiles is not None:
            query_params["allowInternalFiles"] = allowInternalFiles

        response = self.auth.rest(
            path="/qix-datafiles/modifications",
            method="GET",
            params=query_params,
            data=None,
        )
        return [DataFileModificationResponse(**e) for e in response.json()]

    def get_quota(self) -> QuotaResponse:
        """
        Experimental
        Get quota information for the calling user.


        Parameters
        ----------
        """
        warnings.warn("get_quota is experimental", UserWarning, stacklevel=2)

        response = self.auth.rest(
            path="/qix-datafiles/quota",
            method="GET",
            params={},
            data=None,
        )
        obj = QuotaResponse(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, id: str) -> DataFileUploadResponse:
        """
        Experimental
        Get descriptive info for the specified data file.


        id: str
          The ID of the data file.

        Parameters
        ----------
        id: str
        """
        warnings.warn("get is experimental", UserWarning, stacklevel=2)

        response = self.auth.rest(
            path="/qix-datafiles/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = DataFileUploadResponse(**response.json())
        obj.auth = self.auth
        return obj
