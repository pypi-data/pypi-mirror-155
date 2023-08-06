# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services Grafana 1.0.0-202205031030

from __future__ import annotations

import io
import json
from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Theme:
    """
    The theme model.

    Attributes
    ----------
    author: str
      Author of the theme.
    createdAt: str
    dependencies: object
      Map of dependencies describing version of the component it requires.
    description: str
      Description of the theme.
    file: object
      The file that was uploaded with the theme.
    homepage: str
      Home page of the theme.
    icon: str
      Icon to show in the client.
    id: str
    keywords: str
      Keywords for the theme.
    license: str
      Under which license this theme is published.
    name: str
      The display name of this theme.
    qextFilename: str
      The name of the qext file that was uploaded with this theme.
    qextVersion: str
      The version from the qext file that was uploaded with this extension.
    repository: str
      Link to the theme source code.
    supplier: str
      Supplier of the theme.
    tags: list[str]
      List of tags.
    tenantId: str
    type: str
      The type of this theme (visualization, etc.).
    updateAt: str
    userId: str
    version: str
      Version of the theme.
    """

    author: str = None
    createdAt: str = None
    dependencies: object = None
    description: str = None
    file: object = None
    homepage: str = None
    icon: str = None
    id: str = None
    keywords: str = None
    license: str = None
    name: str = None
    qextFilename: str = None
    qextVersion: str = None
    repository: str = None
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
            if k not in self_.__annotations__:
                self_.__setattr__(k, v)

    def delete(self) -> None:
        """
        Deletes a specific theme.

        Parameters
        ----------
        """

        self.auth.rest(
            path="/themes/{id}".replace("{id}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patchs(
        self, file: io.BufferedReader, data: Theme = None, max_items: int = 10
    ) -> ListableResource[Theme]:
        """
        Updates a specific theme with provided data. If a file is provided, the data field is not required.

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
            path="/themes/{id}".replace("{id}", self.id),
            method="PATCH",
            params={},
            data=None,
            files=files_dict,
        )
        return ListableResource(
            response=response.json(),
            cls=Theme,
            auth=self.auth,
            path="/themes/{id}".replace("{id}", self.id),
            max_items=max_items,
            query_params={},
        )

    def get_file(self) -> None:
        """
        Downloads the theme as an archive.

        Parameters
        ----------
        """

        self.auth.rest(
            path="/themes/{id}/file".replace("{id}", self.id),
            method="GET",
            params={},
            data=None,
        )


@dataclass
class ThemesClass:
    """

    Attributes
    ----------
    data: list[Theme]
    """

    data: list[Theme] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [Theme(**e) for e in kvargs["data"]]
        for k, v in kvargs.items():
            if k not in self_.__annotations__:
                self_.__setattr__(k, v)


class Themes:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_themes(self, max_items: int = 10) -> ListableResource[Theme]:
        """
        Lists all themes.


        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/themes",
            method="GET",
            params={},
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Theme,
            auth=self.auth,
            path="/themes",
            max_items=max_items,
            query_params={},
        )

    def create(self, file: io.BufferedReader, data: Theme = None) -> Theme:
        """
        Creates a new theme. If a file is provided, the data field is not required.


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
            path="/themes", method="POST", params={}, data=None, files=files_dict
        )
        obj = Theme(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, id: str) -> Theme:
        """
        Returns a specific theme.


        id: str
          Theme identifier or its qextFilename

        Parameters
        ----------
        id: str
        """

        response = self.auth.rest(
            path="/themes/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = Theme(**response.json())
        obj.auth = self.auth
        return obj

    def get_file(self, id: str, filepath: str) -> None:
        """
        Downloads a file from the theme archive.


        id: str
          Theme identifier or its qextFilename.

        filepath: str
          Path to the file archive for the specified theme archive. Folders separated with forward slashes.

        Parameters
        ----------
        id: str
        filepath: str
        """

        self.auth.rest(
            path="/themes/{id}/file/{filepath}".replace("{id}", id).replace(
                "{filepath}", filepath
            ),
            method="GET",
            params={},
            data=None,
        )
