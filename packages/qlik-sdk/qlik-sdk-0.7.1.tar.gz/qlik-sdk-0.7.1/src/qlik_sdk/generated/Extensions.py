# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services 0.348.2

from __future__ import annotations

import io
import json
from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Extension:
    """
    The extension model.

    Attributes
    ----------
    author: str
      Author of the extension.
    bundle: BundleMeta
      Object containing meta data regarding the bundle the extension belongs to. If it does not belong to a bundle, this object is not defined.
    bundled: bool
      If the extension is part of an extension bundle.
    checksum: str
      Checksum of the extension contents.
    createdAt: str
    dependencies: object
      Map of dependencies describing version of the component it requires.
    deprecated: str
      A date noting when the extension was deprecated.
    description: str
      Description of the extension.
    file: object
      The file that was uploaded with the extension.
    homepage: str
      Home page of the extension.
    icon: str
      Icon to show in the client.
    id: str
    keywords: str
      Keywords for the extension.
    license: str
      Under which license this extension is published.
    name: str
      The display name of this extension.
    preview: str
      Path to an image that enables users to preview the extension.
    qextFilename: str
      The name of the qext file that was uploaded with this extension.
    qextVersion: str
      The version from the qext file that was uploaded with this extension.
    repository: str
      Link to the extension source code.
    supernova: bool
      If the extension is a supernova extension or not.
    supplier: str
      Supplier of the extension.
    tags: list[str]
      List of tags.
    tenantId: str
    type: str
      The type of this extension (visualization, etc.).
    updateAt: str
    userId: str
    version: str
      Version of the extension.
    """

    author: str = None
    bundle: BundleMeta = None
    bundled: bool = None
    checksum: str = None
    createdAt: str = None
    dependencies: object = None
    deprecated: str = None
    description: str = None
    file: object = None
    homepage: str = None
    icon: str = None
    id: str = None
    keywords: str = None
    license: str = None
    name: str = None
    preview: str = None
    qextFilename: str = None
    qextVersion: str = None
    repository: str = None
    supernova: bool = None
    supplier: str = None
    tags: list[str] = None
    tenantId: str = None
    type: str = None
    updateAt: str = None
    userId: str = None
    version: str = None

    def __init__(self_, **kvargs):
        if "author" in kvargs:
            if type(kvargs["author"]).__name__ is self_.__annotations__["author"]:
                self_.author = kvargs["author"]
            else:
                self_.author = kvargs["author"]
        if "bundle" in kvargs:
            if type(kvargs["bundle"]).__name__ is self_.__annotations__["bundle"]:
                self_.bundle = kvargs["bundle"]
            else:
                self_.bundle = BundleMeta(**kvargs["bundle"])
        if "bundled" in kvargs:
            if type(kvargs["bundled"]).__name__ is self_.__annotations__["bundled"]:
                self_.bundled = kvargs["bundled"]
            else:
                self_.bundled = kvargs["bundled"]
        if "checksum" in kvargs:
            if type(kvargs["checksum"]).__name__ is self_.__annotations__["checksum"]:
                self_.checksum = kvargs["checksum"]
            else:
                self_.checksum = kvargs["checksum"]
        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ is self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "dependencies" in kvargs:
            if (
                type(kvargs["dependencies"]).__name__
                is self_.__annotations__["dependencies"]
            ):
                self_.dependencies = kvargs["dependencies"]
            else:
                self_.dependencies = kvargs["dependencies"]
        if "deprecated" in kvargs:
            if (
                type(kvargs["deprecated"]).__name__
                is self_.__annotations__["deprecated"]
            ):
                self_.deprecated = kvargs["deprecated"]
            else:
                self_.deprecated = kvargs["deprecated"]
        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                is self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "file" in kvargs:
            if type(kvargs["file"]).__name__ is self_.__annotations__["file"]:
                self_.file = kvargs["file"]
            else:
                self_.file = kvargs["file"]
        if "homepage" in kvargs:
            if type(kvargs["homepage"]).__name__ is self_.__annotations__["homepage"]:
                self_.homepage = kvargs["homepage"]
            else:
                self_.homepage = kvargs["homepage"]
        if "icon" in kvargs:
            if type(kvargs["icon"]).__name__ is self_.__annotations__["icon"]:
                self_.icon = kvargs["icon"]
            else:
                self_.icon = kvargs["icon"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "keywords" in kvargs:
            if type(kvargs["keywords"]).__name__ is self_.__annotations__["keywords"]:
                self_.keywords = kvargs["keywords"]
            else:
                self_.keywords = kvargs["keywords"]
        if "license" in kvargs:
            if type(kvargs["license"]).__name__ is self_.__annotations__["license"]:
                self_.license = kvargs["license"]
            else:
                self_.license = kvargs["license"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "preview" in kvargs:
            if type(kvargs["preview"]).__name__ is self_.__annotations__["preview"]:
                self_.preview = kvargs["preview"]
            else:
                self_.preview = kvargs["preview"]
        if "qextFilename" in kvargs:
            if (
                type(kvargs["qextFilename"]).__name__
                is self_.__annotations__["qextFilename"]
            ):
                self_.qextFilename = kvargs["qextFilename"]
            else:
                self_.qextFilename = kvargs["qextFilename"]
        if "qextVersion" in kvargs:
            if (
                type(kvargs["qextVersion"]).__name__
                is self_.__annotations__["qextVersion"]
            ):
                self_.qextVersion = kvargs["qextVersion"]
            else:
                self_.qextVersion = kvargs["qextVersion"]
        if "repository" in kvargs:
            if (
                type(kvargs["repository"]).__name__
                is self_.__annotations__["repository"]
            ):
                self_.repository = kvargs["repository"]
            else:
                self_.repository = kvargs["repository"]
        if "supernova" in kvargs:
            if type(kvargs["supernova"]).__name__ is self_.__annotations__["supernova"]:
                self_.supernova = kvargs["supernova"]
            else:
                self_.supernova = kvargs["supernova"]
        if "supplier" in kvargs:
            if type(kvargs["supplier"]).__name__ is self_.__annotations__["supplier"]:
                self_.supplier = kvargs["supplier"]
            else:
                self_.supplier = kvargs["supplier"]
        if "tags" in kvargs:
            if type(kvargs["tags"]).__name__ is self_.__annotations__["tags"]:
                self_.tags = kvargs["tags"]
            else:
                self_.tags = kvargs["tags"]
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
        if "updateAt" in kvargs:
            if type(kvargs["updateAt"]).__name__ is self_.__annotations__["updateAt"]:
                self_.updateAt = kvargs["updateAt"]
            else:
                self_.updateAt = kvargs["updateAt"]
        if "userId" in kvargs:
            if type(kvargs["userId"]).__name__ is self_.__annotations__["userId"]:
                self_.userId = kvargs["userId"]
            else:
                self_.userId = kvargs["userId"]
        if "version" in kvargs:
            if type(kvargs["version"]).__name__ is self_.__annotations__["version"]:
                self_.version = kvargs["version"]
            else:
                self_.version = kvargs["version"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def delete(self) -> None:
        """
        Deletes a specific extension.

        Parameters
        ----------
        """

        self.auth.rest(
            path="/extensions/{id}".replace("{id}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patchs(
        self, file: io.BufferedReader, data: Extension = None, max_items: int = 10
    ) -> ListableResource[Extension]:
        """
        Updates a specific extension with provided data. If a file is provided, the data field is not required.

        Parameters
        ----------
        """

        files_dict = {}
        if data is not None:
            try:
                data = asdict(data)
            except:
                pass
            files_dict["data"] = (None, json.dumps(data))

        files_dict["file"] = file

        response = self.auth.rest(
            path="/extensions/{id}".replace("{id}", self.id),
            method="PATCH",
            params={},
            data=None,
            files=files_dict,
        )
        return ListableResource(
            response=response.json(),
            cls=Extension,
            auth=self.auth,
            path="/extensions/{id}".replace("{id}", self.id),
            max_items=max_items,
            query_params={},
        )

    def get_file(self) -> None:
        """
        Downloads the extension as an archive.

        Parameters
        ----------
        """

        self.auth.rest(
            path="/extensions/{id}/file".replace("{id}", self.id),
            method="GET",
            params={},
            data=None,
        )


@dataclass
class BundleMeta:
    """
    Object containing meta data regarding the bundle the extension belongs to. If it does not belong to a bundle, this object is not defined.

    Attributes
    ----------
    description: str
      Description of the bundle.
    id: str
      Unique identifier of the bundle.
    name: str
      Name of the bundle.
    """

    description: str = None
    id: str = None
    name: str = None

    def __init__(self_, **kvargs):
        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                is self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
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
class ExtensionsClass:
    """

    Attributes
    ----------
    data: list[Extension]
    """

    data: list[Extension] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [Extension(**e) for e in kvargs["data"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Extensions:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_extensions(self, max_items: int = 10) -> ListableResource[Extension]:
        """
        Lists all extensions.


        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/extensions",
            method="GET",
            params={},
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Extension,
            auth=self.auth,
            path="/extensions",
            max_items=max_items,
            query_params={},
        )

    def create(self, file: io.BufferedReader, data: Extension = None) -> Extension:
        """
        Creates a new extension. If a file is provided, the data field is not required.


        Parameters
        ----------
        """

        files_dict = {}
        if data is not None:
            try:
                data = asdict(data)
            except:
                pass
            files_dict["data"] = (None, json.dumps(data))

        files_dict["file"] = file

        response = self.auth.rest(
            path="/extensions", method="POST", params={}, data=None, files=files_dict
        )
        obj = Extension(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, id: str) -> Extension:
        """
        Returns a specific extension.


        id: str
          Extension identifier or its qextFilename.

        Parameters
        ----------
        id: str
        """

        response = self.auth.rest(
            path="/extensions/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = Extension(**response.json())
        obj.auth = self.auth
        return obj

    def get_file(self, id: str, filepath: str) -> None:
        """
        Downloads a file from the extension archive.


        id: str
          Extension identifier or its qextFilename.

        filepath: str
          Path to the file archive for the specified extension archive. Folders separated with forward slashes.

        Parameters
        ----------
        id: str
        filepath: str
        """

        self.auth.rest(
            path="/extensions/{id}/file/{filepath}".replace("{id}", id).replace(
                "{filepath}", filepath
            ),
            method="GET",
            params={},
            data=None,
        )
