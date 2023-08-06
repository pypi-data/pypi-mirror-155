# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services 0.348.2

from __future__ import annotations

import warnings
from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource
from .Qix import Doc


@dataclass
class NxApp(Doc):
    """
    Application attributes and user privileges.

    Attributes
    ----------
    attributes: NxAttributes
      App attributes. This structure can also contain extra user-defined attributes.
    create: list[NxAppCreatePrivileges]
      Object create privileges. Hints to the client what type of objects the user is allowed to create.
    privileges: list[str]
      Application privileges.
      Hints to the client what actions the user is allowed to perform.
      Could be any of:

      • read

      • create

      • update

      • delete

      • reload

      • import

      • publish

      • duplicate

      • export

      • exportdata

      • change_owner

      • change_space
    """

    attributes: NxAttributes = None
    create: list[NxAppCreatePrivileges] = None
    privileges: list[str] = None

    def __init__(self_, **kvargs):

        if "attributes" in kvargs:
            if (
                type(kvargs["attributes"]).__name__
                is self_.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = NxAttributes(**kvargs["attributes"])
        if "create" in kvargs:
            if type(kvargs["create"]).__name__ is self_.__annotations__["create"]:
                self_.create = kvargs["create"]
            else:
                self_.create = [NxAppCreatePrivileges(**e) for e in kvargs["create"]]
        if "privileges" in kvargs:
            if (
                type(kvargs["privileges"]).__name__
                is self_.__annotations__["privileges"]
            ):
                self_.privileges = kvargs["privileges"]
            else:
                self_.privileges = kvargs["privileges"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def create_copy(self, data: CreateApp) -> NxApp:
        """
        Copies a specific app.

        Parameters
        ----------
        data: CreateApp
        """

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/apps/{appId}/copy".replace("{appId}", self.attributes.id),
            method="POST",
            params={},
            data=data,
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def get_data_lineages(self) -> list[LineageInfoRest]:
        """
        Retrieves the lineage for an app.
        Returns a JSON-formatted array of strings describing the lineage of the app.

        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/apps/{appId}/data/lineage".replace("{appId}", self.attributes.id),
            method="GET",
            params={},
            data=None,
        )
        return [LineageInfoRest(**e) for e in response.json()]

    def get_data_metadata(self) -> DataModelMetadata:
        """
        Retrieves the data model and reload statistics metadata of an app.
        An empty metadata structure is returned if the metadata is not available in the app.

        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/apps/{appId}/data/metadata".replace("{appId}", self.attributes.id),
            method="GET",
            params={},
            data=None,
        )
        obj = DataModelMetadata(**response.json())
        obj.auth = self.auth
        return obj

    def export(self, NoData: bool = None) -> str:
        """
        Exports a specific app.

        Parameters
        ----------
        NoData: bool = None
        """
        query_params = {}
        if NoData is not None:
            query_params["NoData"] = NoData

        response = self.auth.rest(
            path="/apps/{appId}/export".replace("{appId}", self.attributes.id),
            method="POST",
            params=query_params,
            data=None,
        )
        return response.headers["Location"]

    def get_media_thumbnail(self) -> str:
        """
        Gets media content from file currently used as application thumbnail.
        Returns a stream of bytes containing the media file content on success, or error if file is not found.
        The image selected as thumbnail is only updated when application is saved.

        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/apps/{appId}/media/thumbnail".replace("{appId}", self.attributes.id),
            method="GET",
            params={},
            data=None,
            stream=True,
        )
        return response

    def set_owner(self, data: UpdateOwner) -> NxApp:
        """
        Changes owner of the app.

        Parameters
        ----------
        data: UpdateOwner
        """

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/apps/{appId}/owner".replace("{appId}", self.attributes.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def publish(self, data: PublishApp) -> NxApp:
        """
        Publishes a specific app to a managed space.

        Parameters
        ----------
        data: PublishApp
        """

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/apps/{appId}/publish".replace("{appId}", self.attributes.id),
            method="POST",
            params={},
            data=data,
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def set_publish(self, data: RepublishApp) -> NxApp:
        """
        Republishes a published app to a managed space.

        Parameters
        ----------
        data: RepublishApp
        """

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/apps/{appId}/publish".replace("{appId}", self.attributes.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def get_reloads_logs(self, max_items: int = 10) -> ListableResource[ScriptLogMeta]:
        """
        Experimental
        Retrieves the metadata about all script logs stored for an app.
        Returns an array of ScriptLogMeta objects.

        Parameters
        ----------
        """
        warnings.warn("get_reloads_logs is experimental", UserWarning, stacklevel=2)

        response = self.auth.rest(
            path="/apps/{appId}/reloads/logs".replace("{appId}", self.attributes.id),
            method="GET",
            params={},
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=ScriptLogMeta,
            auth=self.auth,
            path="/apps/{appId}/reloads/logs".replace("{appId}", self.attributes.id),
            max_items=max_items,
            query_params={},
        )

    def delete_space(self) -> NxApp:
        """
        Removes space from a specific app.

        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/apps/{appId}/space".replace("{appId}", self.attributes.id),
            method="DELETE",
            params={},
            data=None,
        )
        self.__init__(**response.json())
        return self

    def set_space(self, data: UpdateSpace) -> NxApp:
        """
        Sets space on a specific app.

        Parameters
        ----------
        data: UpdateSpace
        """

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/apps/{appId}/space".replace("{appId}", self.attributes.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def delete(self) -> None:
        """
        Deletes a specific app.

        Parameters
        ----------
        """

        self.auth.rest(
            path="/apps/{appId}".replace("{appId}", self.attributes.id),
            method="DELETE",
            params={},
            data=None,
        )

    def set(self, data: UpdateApp) -> NxApp:
        """
        Updates the information for a specific app.

        Parameters
        ----------
        data: UpdateApp
        """

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/apps/{appId}".replace("{appId}", self.attributes.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self


@dataclass
class AppAttributes:
    """

    Attributes
    ----------
    description: str
      The description of the application
    locale: str
      Set custom locale instead of the system default
    name: str
      The name (title) of the application
    spaceId: str
      The space ID of the application
    """

    description: str = None
    locale: str = None
    name: str = None
    spaceId: str = None

    def __init__(self_, **kvargs):
        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                is self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "locale" in kvargs:
            if type(kvargs["locale"]).__name__ is self_.__annotations__["locale"]:
                self_.locale = kvargs["locale"]
            else:
                self_.locale = kvargs["locale"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppContentList:
    """

    Attributes
    ----------
    data: list[AppContentListItem]
      Content list items.
    library: str
      Content library name.
    subpath: str
      Content library relative listing path. Empty in case of root listed or representing actual subpath listed.
    """

    data: list[AppContentListItem] = None
    library: str = None
    subpath: str = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [AppContentListItem(**e) for e in kvargs["data"]]
        if "library" in kvargs:
            if type(kvargs["library"]).__name__ is self_.__annotations__["library"]:
                self_.library = kvargs["library"]
            else:
                self_.library = kvargs["library"]
        if "subpath" in kvargs:
            if type(kvargs["subpath"]).__name__ is self_.__annotations__["subpath"]:
                self_.subpath = kvargs["subpath"]
            else:
                self_.subpath = kvargs["subpath"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppContentListItem:
    """

    Attributes
    ----------
    id: str
      Unique content identifier.
    link: str
      Unique content link.
    name: str
      Content name.
    type: str
      Content type.
    """

    id: str = None
    link: str = None
    name: str = None
    type: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "link" in kvargs:
            if type(kvargs["link"]).__name__ is self_.__annotations__["link"]:
                self_.link = kvargs["link"]
            else:
                self_.link = kvargs["link"]
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
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppUpdateAttributes:
    """

    Attributes
    ----------
    description: str
      The description of the application.
    name: str
      The name (title) of the application.
    """

    description: str = None
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
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CreateApp:
    """

    Attributes
    ----------
    attributes: AppAttributes
    """

    attributes: AppAttributes = None

    def __init__(self_, **kvargs):
        if "attributes" in kvargs:
            if (
                type(kvargs["attributes"]).__name__
                is self_.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = AppAttributes(**kvargs["attributes"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataModelMetadata:
    """

    Attributes
    ----------
    fields: list[FieldMetadata]
      List of field descriptions.
    has_section_access: bool
      If set to true, the app has section access configured.
    is_direct_query_mode: bool
    reload_meta: LastReloadMetadata
    static_byte_size: int
      Static memory usage for the app.
    tables: list[TableMetadata]
      List of table descriptions.
    tables_profiling_data: list[TableProfilingData]
      Profiling data of the tables in the app.
    """

    fields: list[FieldMetadata] = None
    has_section_access: bool = None
    is_direct_query_mode: bool = None
    reload_meta: LastReloadMetadata = None
    static_byte_size: int = None
    tables: list[TableMetadata] = None
    tables_profiling_data: list[TableProfilingData] = None

    def __init__(self_, **kvargs):
        if "fields" in kvargs:
            if type(kvargs["fields"]).__name__ is self_.__annotations__["fields"]:
                self_.fields = kvargs["fields"]
            else:
                self_.fields = [FieldMetadata(**e) for e in kvargs["fields"]]
        if "has_section_access" in kvargs:
            if (
                type(kvargs["has_section_access"]).__name__
                is self_.__annotations__["has_section_access"]
            ):
                self_.has_section_access = kvargs["has_section_access"]
            else:
                self_.has_section_access = kvargs["has_section_access"]
        if "is_direct_query_mode" in kvargs:
            if (
                type(kvargs["is_direct_query_mode"]).__name__
                is self_.__annotations__["is_direct_query_mode"]
            ):
                self_.is_direct_query_mode = kvargs["is_direct_query_mode"]
            else:
                self_.is_direct_query_mode = kvargs["is_direct_query_mode"]
        if "reload_meta" in kvargs:
            if (
                type(kvargs["reload_meta"]).__name__
                is self_.__annotations__["reload_meta"]
            ):
                self_.reload_meta = kvargs["reload_meta"]
            else:
                self_.reload_meta = LastReloadMetadata(**kvargs["reload_meta"])
        if "static_byte_size" in kvargs:
            if (
                type(kvargs["static_byte_size"]).__name__
                is self_.__annotations__["static_byte_size"]
            ):
                self_.static_byte_size = kvargs["static_byte_size"]
            else:
                self_.static_byte_size = kvargs["static_byte_size"]
        if "tables" in kvargs:
            if type(kvargs["tables"]).__name__ is self_.__annotations__["tables"]:
                self_.tables = kvargs["tables"]
            else:
                self_.tables = [TableMetadata(**e) for e in kvargs["tables"]]
        if "tables_profiling_data" in kvargs:
            if (
                type(kvargs["tables_profiling_data"]).__name__
                is self_.__annotations__["tables_profiling_data"]
            ):
                self_.tables_profiling_data = kvargs["tables_profiling_data"]
            else:
                self_.tables_profiling_data = [
                    TableProfilingData(**e) for e in kvargs["tables_profiling_data"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldAttributes:
    """
    Sets the formatting of a field.
    The properties of qFieldAttributes and the formatting mechanism are described below.

    Formatting mechanism:

    The formatting mechanism depends on the type set in qType, as shown below:
    In case of inconsistencies between the type and the format pattern, the format pattern takes precedence over the type.

    Type is DATE, TIME, TIMESTAMP or INTERVAL:

    The following applies:

    • If a format pattern is defined in qFmt , the formatting is as defined in qFmt .

    • If qFmt is empty, the formatting is defined by the number interpretation variables included at the top of the script ( TimeFormat , DateFormat , TimeStampFormat ).

    • The properties qDec , qThou , qnDec , qUseThou are not used.

    Type is INTEGER:

    The following applies:

    • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the formatting mechanism uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

    • If no format pattern is defined in qFmt , no formatting is applied. The properties qDec , qThou , qnDec , qUseThou and the number interpretation variables defined in the script are not used .

    Type is REAL:

    The following applies:

    • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

    • If no format pattern is defined in qFmt , and if the value is almost an integer value (for example, 14,000012), the value is formatted as an integer. The properties qDec , qThou , qnDec , qUseThou are not used.

    • If no format pattern is defined in qFmt , and if qnDec is defined and not 0, the property qDec is used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

    • If no format pattern is defined in qFmt , and if qnDec is 0, the number of decimals is 14 and the property qDec is used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

    Type is FIX:

    The following applies:

    • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

    • If no format pattern is defined in qFmt , the properties qDec and qnDec are used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

    Type is MONEY:

    The following applies:

    • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of any script ( MoneyDecimalSep and MoneyThousandSep ).

    • If no format pattern is defined in qFmt , the engine uses the number interpretation variables included at the top of the script ( MoneyDecimalSep and MoneyThousandSep ).

    Type is ASCII:

    No formatting, qFmt is ignored.

    Attributes
    ----------
    Dec: str
      Defines the decimal separator.
      Example:

      .:
    Fmt: str
      Defines the format pattern that applies to qText .
      Is used in connection to the type of the field (parameter qType ).
      For more information, see Formatting mechanism.
      Example: YYYY-MM-DD for a date.
    Thou: str
      Defines the thousand separator (if any).
      Is used if qUseThou is set to 1.
      Example:

      ,:
    Type: str
      Type of the field.
      Default is U.

      One of:

      • U or UNKNOWN

      • A or ASCII

      • I or INTEGER

      • R or REAL

      • F or FIX

      • M or MONEY

      • D or DATE

      • T or TIME

      • TS or TIMESTAMP

      • IV or INTERVAL
    UseThou: int
      Defines whether or not a thousands separator must be used.
      Default is 0.
    nDec: int
      Number of decimals.
      Default is 10.
    """

    Dec: str = None
    Fmt: str = None
    Thou: str = None
    Type: str = None
    UseThou: int = None
    nDec: int = None

    def __init__(self_, **kvargs):
        if "Dec" in kvargs:
            if type(kvargs["Dec"]).__name__ is self_.__annotations__["Dec"]:
                self_.Dec = kvargs["Dec"]
            else:
                self_.Dec = kvargs["Dec"]
        if "Fmt" in kvargs:
            if type(kvargs["Fmt"]).__name__ is self_.__annotations__["Fmt"]:
                self_.Fmt = kvargs["Fmt"]
            else:
                self_.Fmt = kvargs["Fmt"]
        if "Thou" in kvargs:
            if type(kvargs["Thou"]).__name__ is self_.__annotations__["Thou"]:
                self_.Thou = kvargs["Thou"]
            else:
                self_.Thou = kvargs["Thou"]
        if "Type" in kvargs:
            if type(kvargs["Type"]).__name__ is self_.__annotations__["Type"]:
                self_.Type = kvargs["Type"]
            else:
                self_.Type = kvargs["Type"]
        if "UseThou" in kvargs:
            if type(kvargs["UseThou"]).__name__ is self_.__annotations__["UseThou"]:
                self_.UseThou = kvargs["UseThou"]
            else:
                self_.UseThou = kvargs["UseThou"]
        if "nDec" in kvargs:
            if type(kvargs["nDec"]).__name__ is self_.__annotations__["nDec"]:
                self_.nDec = kvargs["nDec"]
            else:
                self_.nDec = kvargs["nDec"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldInTableProfilingData:
    """

    Attributes
    ----------
    Average: float
      Average of all numerical values. NaN otherwise.
    AvgStringLen: float
      Average string length of textual values. 0 otherwise.
    DistinctNumericValues: int
      Number of distinct numeric values
    DistinctTextValues: int
      Number of distinct text values
    DistinctValues: int
      Number of distinct values
    EmptyStrings: int
      Number of empty strings
    FieldTags: list[str]
      List of tags related to the field.
    FirstSorted: str
      For textual values the first sorted string.
    Fractiles: list[float]
      The .01, .05, .1, .25, .5, .75, .9, .95, .99 fractiles. Array of NaN otherwise.
    FrequencyDistribution: FrequencyDistributionData
    Kurtosis: float
      Kurtosis of the numerical values. NaN otherwise.
    LastSorted: str
      For textual values the last sorted string.
    Max: float
      Maximum value of numerical values. NaN otherwise.
    MaxStringLen: int
      Maximum string length of textual values. 0 otherwise.
    Median: float
      Median of all numerical values. NaN otherwise.
    Min: float
      Minimum value of numerical values. NaN otherwise.
    MinStringLen: int
      Minimum string length of textual values. 0 otherwise.
    MostFrequent: list[SymbolFrequency]
      Three most frequent values and their frequencies
    Name: str
      Name of the field.
    NegValues: int
      Number of negative values
    NullValues: int
      Number of null values
    NumberFormat: FieldAttributes
      Sets the formatting of a field.
      The properties of qFieldAttributes and the formatting mechanism are described below.

      Formatting mechanism:

      The formatting mechanism depends on the type set in qType, as shown below:
      In case of inconsistencies between the type and the format pattern, the format pattern takes precedence over the type.

      Type is DATE, TIME, TIMESTAMP or INTERVAL:

      The following applies:

      • If a format pattern is defined in qFmt , the formatting is as defined in qFmt .

      • If qFmt is empty, the formatting is defined by the number interpretation variables included at the top of the script ( TimeFormat , DateFormat , TimeStampFormat ).

      • The properties qDec , qThou , qnDec , qUseThou are not used.

      Type is INTEGER:

      The following applies:

      • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the formatting mechanism uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

      • If no format pattern is defined in qFmt , no formatting is applied. The properties qDec , qThou , qnDec , qUseThou and the number interpretation variables defined in the script are not used .

      Type is REAL:

      The following applies:

      • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

      • If no format pattern is defined in qFmt , and if the value is almost an integer value (for example, 14,000012), the value is formatted as an integer. The properties qDec , qThou , qnDec , qUseThou are not used.

      • If no format pattern is defined in qFmt , and if qnDec is defined and not 0, the property qDec is used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

      • If no format pattern is defined in qFmt , and if qnDec is 0, the number of decimals is 14 and the property qDec is used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

      Type is FIX:

      The following applies:

      • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

      • If no format pattern is defined in qFmt , the properties qDec and qnDec are used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

      Type is MONEY:

      The following applies:

      • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of any script ( MoneyDecimalSep and MoneyThousandSep ).

      • If no format pattern is defined in qFmt , the engine uses the number interpretation variables included at the top of the script ( MoneyDecimalSep and MoneyThousandSep ).

      Type is ASCII:

      No formatting, qFmt is ignored.
    NumericValues: int
      Number of numeric values
    PosValues: int
      Number of positive values
    Skewness: float
      Skewness of the numerical values. NaN otherwise.
    Std: float
      Standard deviation of numerical values. NaN otherwise.
    Sum: float
      Sum of all numerical values. NaN otherwise.
    Sum2: float
      Squared sum of all numerical values. NaN otherwise.
    SumStringLen: int
      Sum of all characters in strings in the field
    TextValues: int
      Number of textual values
    ZeroValues: int
      Number of zero values for numerical values
    """

    Average: float = None
    AvgStringLen: float = None
    DistinctNumericValues: int = None
    DistinctTextValues: int = None
    DistinctValues: int = None
    EmptyStrings: int = None
    FieldTags: list[str] = None
    FirstSorted: str = None
    Fractiles: list[float] = None
    FrequencyDistribution: FrequencyDistributionData = None
    Kurtosis: float = None
    LastSorted: str = None
    Max: float = None
    MaxStringLen: int = None
    Median: float = None
    Min: float = None
    MinStringLen: int = None
    MostFrequent: list[SymbolFrequency] = None
    Name: str = None
    NegValues: int = None
    NullValues: int = None
    NumberFormat: FieldAttributes = None
    NumericValues: int = None
    PosValues: int = None
    Skewness: float = None
    Std: float = None
    Sum: float = None
    Sum2: float = None
    SumStringLen: int = None
    TextValues: int = None
    ZeroValues: int = None

    def __init__(self_, **kvargs):
        if "Average" in kvargs:
            if type(kvargs["Average"]).__name__ is self_.__annotations__["Average"]:
                self_.Average = kvargs["Average"]
            else:
                self_.Average = kvargs["Average"]
        if "AvgStringLen" in kvargs:
            if (
                type(kvargs["AvgStringLen"]).__name__
                is self_.__annotations__["AvgStringLen"]
            ):
                self_.AvgStringLen = kvargs["AvgStringLen"]
            else:
                self_.AvgStringLen = kvargs["AvgStringLen"]
        if "DistinctNumericValues" in kvargs:
            if (
                type(kvargs["DistinctNumericValues"]).__name__
                is self_.__annotations__["DistinctNumericValues"]
            ):
                self_.DistinctNumericValues = kvargs["DistinctNumericValues"]
            else:
                self_.DistinctNumericValues = kvargs["DistinctNumericValues"]
        if "DistinctTextValues" in kvargs:
            if (
                type(kvargs["DistinctTextValues"]).__name__
                is self_.__annotations__["DistinctTextValues"]
            ):
                self_.DistinctTextValues = kvargs["DistinctTextValues"]
            else:
                self_.DistinctTextValues = kvargs["DistinctTextValues"]
        if "DistinctValues" in kvargs:
            if (
                type(kvargs["DistinctValues"]).__name__
                is self_.__annotations__["DistinctValues"]
            ):
                self_.DistinctValues = kvargs["DistinctValues"]
            else:
                self_.DistinctValues = kvargs["DistinctValues"]
        if "EmptyStrings" in kvargs:
            if (
                type(kvargs["EmptyStrings"]).__name__
                is self_.__annotations__["EmptyStrings"]
            ):
                self_.EmptyStrings = kvargs["EmptyStrings"]
            else:
                self_.EmptyStrings = kvargs["EmptyStrings"]
        if "FieldTags" in kvargs:
            if type(kvargs["FieldTags"]).__name__ is self_.__annotations__["FieldTags"]:
                self_.FieldTags = kvargs["FieldTags"]
            else:
                self_.FieldTags = kvargs["FieldTags"]
        if "FirstSorted" in kvargs:
            if (
                type(kvargs["FirstSorted"]).__name__
                is self_.__annotations__["FirstSorted"]
            ):
                self_.FirstSorted = kvargs["FirstSorted"]
            else:
                self_.FirstSorted = kvargs["FirstSorted"]
        if "Fractiles" in kvargs:
            if type(kvargs["Fractiles"]).__name__ is self_.__annotations__["Fractiles"]:
                self_.Fractiles = kvargs["Fractiles"]
            else:
                self_.Fractiles = kvargs["Fractiles"]
        if "FrequencyDistribution" in kvargs:
            if (
                type(kvargs["FrequencyDistribution"]).__name__
                is self_.__annotations__["FrequencyDistribution"]
            ):
                self_.FrequencyDistribution = kvargs["FrequencyDistribution"]
            else:
                self_.FrequencyDistribution = FrequencyDistributionData(
                    **kvargs["FrequencyDistribution"]
                )
        if "Kurtosis" in kvargs:
            if type(kvargs["Kurtosis"]).__name__ is self_.__annotations__["Kurtosis"]:
                self_.Kurtosis = kvargs["Kurtosis"]
            else:
                self_.Kurtosis = kvargs["Kurtosis"]
        if "LastSorted" in kvargs:
            if (
                type(kvargs["LastSorted"]).__name__
                is self_.__annotations__["LastSorted"]
            ):
                self_.LastSorted = kvargs["LastSorted"]
            else:
                self_.LastSorted = kvargs["LastSorted"]
        if "Max" in kvargs:
            if type(kvargs["Max"]).__name__ is self_.__annotations__["Max"]:
                self_.Max = kvargs["Max"]
            else:
                self_.Max = kvargs["Max"]
        if "MaxStringLen" in kvargs:
            if (
                type(kvargs["MaxStringLen"]).__name__
                is self_.__annotations__["MaxStringLen"]
            ):
                self_.MaxStringLen = kvargs["MaxStringLen"]
            else:
                self_.MaxStringLen = kvargs["MaxStringLen"]
        if "Median" in kvargs:
            if type(kvargs["Median"]).__name__ is self_.__annotations__["Median"]:
                self_.Median = kvargs["Median"]
            else:
                self_.Median = kvargs["Median"]
        if "Min" in kvargs:
            if type(kvargs["Min"]).__name__ is self_.__annotations__["Min"]:
                self_.Min = kvargs["Min"]
            else:
                self_.Min = kvargs["Min"]
        if "MinStringLen" in kvargs:
            if (
                type(kvargs["MinStringLen"]).__name__
                is self_.__annotations__["MinStringLen"]
            ):
                self_.MinStringLen = kvargs["MinStringLen"]
            else:
                self_.MinStringLen = kvargs["MinStringLen"]
        if "MostFrequent" in kvargs:
            if (
                type(kvargs["MostFrequent"]).__name__
                is self_.__annotations__["MostFrequent"]
            ):
                self_.MostFrequent = kvargs["MostFrequent"]
            else:
                self_.MostFrequent = [
                    SymbolFrequency(**e) for e in kvargs["MostFrequent"]
                ]
        if "Name" in kvargs:
            if type(kvargs["Name"]).__name__ is self_.__annotations__["Name"]:
                self_.Name = kvargs["Name"]
            else:
                self_.Name = kvargs["Name"]
        if "NegValues" in kvargs:
            if type(kvargs["NegValues"]).__name__ is self_.__annotations__["NegValues"]:
                self_.NegValues = kvargs["NegValues"]
            else:
                self_.NegValues = kvargs["NegValues"]
        if "NullValues" in kvargs:
            if (
                type(kvargs["NullValues"]).__name__
                is self_.__annotations__["NullValues"]
            ):
                self_.NullValues = kvargs["NullValues"]
            else:
                self_.NullValues = kvargs["NullValues"]
        if "NumberFormat" in kvargs:
            if (
                type(kvargs["NumberFormat"]).__name__
                is self_.__annotations__["NumberFormat"]
            ):
                self_.NumberFormat = kvargs["NumberFormat"]
            else:
                self_.NumberFormat = FieldAttributes(**kvargs["NumberFormat"])
        if "NumericValues" in kvargs:
            if (
                type(kvargs["NumericValues"]).__name__
                is self_.__annotations__["NumericValues"]
            ):
                self_.NumericValues = kvargs["NumericValues"]
            else:
                self_.NumericValues = kvargs["NumericValues"]
        if "PosValues" in kvargs:
            if type(kvargs["PosValues"]).__name__ is self_.__annotations__["PosValues"]:
                self_.PosValues = kvargs["PosValues"]
            else:
                self_.PosValues = kvargs["PosValues"]
        if "Skewness" in kvargs:
            if type(kvargs["Skewness"]).__name__ is self_.__annotations__["Skewness"]:
                self_.Skewness = kvargs["Skewness"]
            else:
                self_.Skewness = kvargs["Skewness"]
        if "Std" in kvargs:
            if type(kvargs["Std"]).__name__ is self_.__annotations__["Std"]:
                self_.Std = kvargs["Std"]
            else:
                self_.Std = kvargs["Std"]
        if "Sum" in kvargs:
            if type(kvargs["Sum"]).__name__ is self_.__annotations__["Sum"]:
                self_.Sum = kvargs["Sum"]
            else:
                self_.Sum = kvargs["Sum"]
        if "Sum2" in kvargs:
            if type(kvargs["Sum2"]).__name__ is self_.__annotations__["Sum2"]:
                self_.Sum2 = kvargs["Sum2"]
            else:
                self_.Sum2 = kvargs["Sum2"]
        if "SumStringLen" in kvargs:
            if (
                type(kvargs["SumStringLen"]).__name__
                is self_.__annotations__["SumStringLen"]
            ):
                self_.SumStringLen = kvargs["SumStringLen"]
            else:
                self_.SumStringLen = kvargs["SumStringLen"]
        if "TextValues" in kvargs:
            if (
                type(kvargs["TextValues"]).__name__
                is self_.__annotations__["TextValues"]
            ):
                self_.TextValues = kvargs["TextValues"]
            else:
                self_.TextValues = kvargs["TextValues"]
        if "ZeroValues" in kvargs:
            if (
                type(kvargs["ZeroValues"]).__name__
                is self_.__annotations__["ZeroValues"]
            ):
                self_.ZeroValues = kvargs["ZeroValues"]
            else:
                self_.ZeroValues = kvargs["ZeroValues"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldMetadata:
    """

    Attributes
    ----------
    always_one_selected: bool
      If set to true, the field has one and only one selection (not 0 and not more than 1).
      If this property is set to true, the field cannot be cleared anymore and no more selections can be performed in that field.
      The default value is false.
    byte_size: int
      Static RAM memory used in bytes.
    cardinal: int
      Number of distinct field values.
    comment: str
      Field comment.
    distinct_only: bool
      If set to true, only distinct field values are shown.
      The default value is false.
    hash: str
      Hash of the data in the field. If the data in a reload is the same, the hash will be consistent.
    is_hidden: bool
      If set to true, the field is hidden.
      The default value is false.
    is_locked: bool
      If set to true, the field is locked.
      The default value is false.
    is_numeric: bool
      Is set to true if the value is a numeric.
      The default value is false.
    is_semantic: bool
      If set to true, the field is semantic.
      The default value is false.
    is_system: bool
      If set to true, the field is a system field.
      The default value is false.
    name: str
      Name of the field.
    src_tables: list[str]
      List of table names.
    tags: list[str]
      Gives information on a field. For example, it can return the type of the field.
      Examples: key, text, ASCII.
    total_count: int
      Total number of field values.
    """

    always_one_selected: bool = None
    byte_size: int = None
    cardinal: int = None
    comment: str = None
    distinct_only: bool = None
    hash: str = None
    is_hidden: bool = None
    is_locked: bool = None
    is_numeric: bool = None
    is_semantic: bool = None
    is_system: bool = None
    name: str = None
    src_tables: list[str] = None
    tags: list[str] = None
    total_count: int = None

    def __init__(self_, **kvargs):
        if "always_one_selected" in kvargs:
            if (
                type(kvargs["always_one_selected"]).__name__
                is self_.__annotations__["always_one_selected"]
            ):
                self_.always_one_selected = kvargs["always_one_selected"]
            else:
                self_.always_one_selected = kvargs["always_one_selected"]
        if "byte_size" in kvargs:
            if type(kvargs["byte_size"]).__name__ is self_.__annotations__["byte_size"]:
                self_.byte_size = kvargs["byte_size"]
            else:
                self_.byte_size = kvargs["byte_size"]
        if "cardinal" in kvargs:
            if type(kvargs["cardinal"]).__name__ is self_.__annotations__["cardinal"]:
                self_.cardinal = kvargs["cardinal"]
            else:
                self_.cardinal = kvargs["cardinal"]
        if "comment" in kvargs:
            if type(kvargs["comment"]).__name__ is self_.__annotations__["comment"]:
                self_.comment = kvargs["comment"]
            else:
                self_.comment = kvargs["comment"]
        if "distinct_only" in kvargs:
            if (
                type(kvargs["distinct_only"]).__name__
                is self_.__annotations__["distinct_only"]
            ):
                self_.distinct_only = kvargs["distinct_only"]
            else:
                self_.distinct_only = kvargs["distinct_only"]
        if "hash" in kvargs:
            if type(kvargs["hash"]).__name__ is self_.__annotations__["hash"]:
                self_.hash = kvargs["hash"]
            else:
                self_.hash = kvargs["hash"]
        if "is_hidden" in kvargs:
            if type(kvargs["is_hidden"]).__name__ is self_.__annotations__["is_hidden"]:
                self_.is_hidden = kvargs["is_hidden"]
            else:
                self_.is_hidden = kvargs["is_hidden"]
        if "is_locked" in kvargs:
            if type(kvargs["is_locked"]).__name__ is self_.__annotations__["is_locked"]:
                self_.is_locked = kvargs["is_locked"]
            else:
                self_.is_locked = kvargs["is_locked"]
        if "is_numeric" in kvargs:
            if (
                type(kvargs["is_numeric"]).__name__
                is self_.__annotations__["is_numeric"]
            ):
                self_.is_numeric = kvargs["is_numeric"]
            else:
                self_.is_numeric = kvargs["is_numeric"]
        if "is_semantic" in kvargs:
            if (
                type(kvargs["is_semantic"]).__name__
                is self_.__annotations__["is_semantic"]
            ):
                self_.is_semantic = kvargs["is_semantic"]
            else:
                self_.is_semantic = kvargs["is_semantic"]
        if "is_system" in kvargs:
            if type(kvargs["is_system"]).__name__ is self_.__annotations__["is_system"]:
                self_.is_system = kvargs["is_system"]
            else:
                self_.is_system = kvargs["is_system"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "src_tables" in kvargs:
            if (
                type(kvargs["src_tables"]).__name__
                is self_.__annotations__["src_tables"]
            ):
                self_.src_tables = kvargs["src_tables"]
            else:
                self_.src_tables = kvargs["src_tables"]
        if "tags" in kvargs:
            if type(kvargs["tags"]).__name__ is self_.__annotations__["tags"]:
                self_.tags = kvargs["tags"]
            else:
                self_.tags = kvargs["tags"]
        if "total_count" in kvargs:
            if (
                type(kvargs["total_count"]).__name__
                is self_.__annotations__["total_count"]
            ):
                self_.total_count = kvargs["total_count"]
            else:
                self_.total_count = kvargs["total_count"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FileData:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FrequencyDistributionData:
    """

    Attributes
    ----------
    BinsEdges: list[float]
      Bins edges.
    Frequencies: list[int]
      Bins frequencies.
    NumberOfBins: int
      Number of bins.
    """

    BinsEdges: list[float] = None
    Frequencies: list[int] = None
    NumberOfBins: int = None

    def __init__(self_, **kvargs):
        if "BinsEdges" in kvargs:
            if type(kvargs["BinsEdges"]).__name__ is self_.__annotations__["BinsEdges"]:
                self_.BinsEdges = kvargs["BinsEdges"]
            else:
                self_.BinsEdges = kvargs["BinsEdges"]
        if "Frequencies" in kvargs:
            if (
                type(kvargs["Frequencies"]).__name__
                is self_.__annotations__["Frequencies"]
            ):
                self_.Frequencies = kvargs["Frequencies"]
            else:
                self_.Frequencies = kvargs["Frequencies"]
        if "NumberOfBins" in kvargs:
            if (
                type(kvargs["NumberOfBins"]).__name__
                is self_.__annotations__["NumberOfBins"]
            ):
                self_.NumberOfBins = kvargs["NumberOfBins"]
            else:
                self_.NumberOfBins = kvargs["NumberOfBins"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class HardwareMeta:
    """

    Attributes
    ----------
    logical_cores: int
      Number of logical cores available.
    total_memory: int
      RAM available.
    """

    logical_cores: int = None
    total_memory: int = None

    def __init__(self_, **kvargs):
        if "logical_cores" in kvargs:
            if (
                type(kvargs["logical_cores"]).__name__
                is self_.__annotations__["logical_cores"]
            ):
                self_.logical_cores = kvargs["logical_cores"]
            else:
                self_.logical_cores = kvargs["logical_cores"]
        if "total_memory" in kvargs:
            if (
                type(kvargs["total_memory"]).__name__
                is self_.__annotations__["total_memory"]
            ):
                self_.total_memory = kvargs["total_memory"]
            else:
                self_.total_memory = kvargs["total_memory"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class JsonObject:
    """
    Contains dynamic JSON data specified by the client.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LastReloadMetadata:
    """

    Attributes
    ----------
    cpu_time_spent_ms: int
      Number of CPU milliseconds it took to reload the app.
    hardware: HardwareMeta
    peak_memory_bytes: int
      Maximum number of bytes used during reload of the app.
    """

    cpu_time_spent_ms: int = None
    hardware: HardwareMeta = None
    peak_memory_bytes: int = None

    def __init__(self_, **kvargs):
        if "cpu_time_spent_ms" in kvargs:
            if (
                type(kvargs["cpu_time_spent_ms"]).__name__
                is self_.__annotations__["cpu_time_spent_ms"]
            ):
                self_.cpu_time_spent_ms = kvargs["cpu_time_spent_ms"]
            else:
                self_.cpu_time_spent_ms = kvargs["cpu_time_spent_ms"]
        if "hardware" in kvargs:
            if type(kvargs["hardware"]).__name__ is self_.__annotations__["hardware"]:
                self_.hardware = kvargs["hardware"]
            else:
                self_.hardware = HardwareMeta(**kvargs["hardware"])
        if "peak_memory_bytes" in kvargs:
            if (
                type(kvargs["peak_memory_bytes"]).__name__
                is self_.__annotations__["peak_memory_bytes"]
            ):
                self_.peak_memory_bytes = kvargs["peak_memory_bytes"]
            else:
                self_.peak_memory_bytes = kvargs["peak_memory_bytes"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LineageInfoRest:
    """

    Attributes
    ----------
    discriminator: str
      A string indicating the origin of the data:

      • [filename]: the data comes from a local file.

      • INLINE: the data is entered inline in the load script.

      • RESIDENT: the data comes from a resident table. The table name is listed.

      • AUTOGENERATE: the data is generated from the load script (no external table of data source).

      • Provider: the data comes from a data connection. The connector source name is listed.

      • [webfile]: the data comes from a web-based file.

      • STORE: path to QVD or TXT file where data is stored.

      • EXTENSION: the data comes from a Server Side Extension (SSE).
    statement: str
      The LOAD and SELECT script statements from the data load script.
    """

    discriminator: str = None
    statement: str = None

    def __init__(self_, **kvargs):
        if "discriminator" in kvargs:
            if (
                type(kvargs["discriminator"]).__name__
                is self_.__annotations__["discriminator"]
            ):
                self_.discriminator = kvargs["discriminator"]
            else:
                self_.discriminator = kvargs["discriminator"]
        if "statement" in kvargs:
            if type(kvargs["statement"]).__name__ is self_.__annotations__["statement"]:
                self_.statement = kvargs["statement"]
            else:
                self_.statement = kvargs["statement"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Log:
    """

    Attributes
    ----------
    log: str
      Provides a link to download the log file.
    """

    log: str = None

    def __init__(self_, **kvargs):
        if "log" in kvargs:
            if type(kvargs["log"]).__name__ is self_.__annotations__["log"]:
                self_.log = kvargs["log"]
            else:
                self_.log = kvargs["log"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAppCreatePrivileges:
    """

    Attributes
    ----------
    canCreate: bool
      Is set to true if the user has privileges to create the resource.
    resource: str
      Type of resource. For example, sheet, story, bookmark, etc.
    """

    canCreate: bool = None
    resource: str = None

    def __init__(self_, **kvargs):
        if "canCreate" in kvargs:
            if type(kvargs["canCreate"]).__name__ is self_.__annotations__["canCreate"]:
                self_.canCreate = kvargs["canCreate"]
            else:
                self_.canCreate = kvargs["canCreate"]
        if "resource" in kvargs:
            if type(kvargs["resource"]).__name__ is self_.__annotations__["resource"]:
                self_.resource = kvargs["resource"]
            else:
                self_.resource = kvargs["resource"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttributes:
    """
    App attributes. This structure can also contain extra user-defined attributes.

    Attributes
    ----------
    createdDate: str
      The date and time when the app was created.
    custom: JsonObject
      Contains dynamic JSON data specified by the client.
    description: str
      App description.
    dynamicColor: str
      The dynamic color of the app.
    encrypted: bool
      If set to true, the app is encrypted.
    hasSectionAccess: bool
      If set to true, the app has section access configured,
    id: str
      The App ID.
    isDirectQueryMode: bool
      True if the app is a Direct Query app, false if not
    lastReloadTime: str
      Date and time of the last reload of the app.
    modifiedDate: str
      The date and time when the app was modified.
    name: str
      App name.
    originAppId: str
      The Origin App ID for published apps.
    owner: str
      The owner of the app.
    ownerId: str
    publishTime: str
      The date and time when the app was published, empty if unpublished.
    published: bool
      True if the app is published on-prem, distributed in QCS, false if not.
    thumbnail: str
      App thumbnail.
    """

    createdDate: str = None
    custom: JsonObject = None
    description: str = None
    dynamicColor: str = None
    encrypted: bool = None
    hasSectionAccess: bool = None
    id: str = None
    isDirectQueryMode: bool = None
    lastReloadTime: str = None
    modifiedDate: str = None
    name: str = None
    originAppId: str = None
    owner: str = None
    ownerId: str = None
    publishTime: str = None
    published: bool = None
    thumbnail: str = None

    def __init__(self_, **kvargs):
        if "createdDate" in kvargs:
            if (
                type(kvargs["createdDate"]).__name__
                is self_.__annotations__["createdDate"]
            ):
                self_.createdDate = kvargs["createdDate"]
            else:
                self_.createdDate = kvargs["createdDate"]
        if "custom" in kvargs:
            if type(kvargs["custom"]).__name__ is self_.__annotations__["custom"]:
                self_.custom = kvargs["custom"]
            else:
                self_.custom = JsonObject(**kvargs["custom"])
        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                is self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "dynamicColor" in kvargs:
            if (
                type(kvargs["dynamicColor"]).__name__
                is self_.__annotations__["dynamicColor"]
            ):
                self_.dynamicColor = kvargs["dynamicColor"]
            else:
                self_.dynamicColor = kvargs["dynamicColor"]
        if "encrypted" in kvargs:
            if type(kvargs["encrypted"]).__name__ is self_.__annotations__["encrypted"]:
                self_.encrypted = kvargs["encrypted"]
            else:
                self_.encrypted = kvargs["encrypted"]
        if "hasSectionAccess" in kvargs:
            if (
                type(kvargs["hasSectionAccess"]).__name__
                is self_.__annotations__["hasSectionAccess"]
            ):
                self_.hasSectionAccess = kvargs["hasSectionAccess"]
            else:
                self_.hasSectionAccess = kvargs["hasSectionAccess"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "isDirectQueryMode" in kvargs:
            if (
                type(kvargs["isDirectQueryMode"]).__name__
                is self_.__annotations__["isDirectQueryMode"]
            ):
                self_.isDirectQueryMode = kvargs["isDirectQueryMode"]
            else:
                self_.isDirectQueryMode = kvargs["isDirectQueryMode"]
        if "lastReloadTime" in kvargs:
            if (
                type(kvargs["lastReloadTime"]).__name__
                is self_.__annotations__["lastReloadTime"]
            ):
                self_.lastReloadTime = kvargs["lastReloadTime"]
            else:
                self_.lastReloadTime = kvargs["lastReloadTime"]
        if "modifiedDate" in kvargs:
            if (
                type(kvargs["modifiedDate"]).__name__
                is self_.__annotations__["modifiedDate"]
            ):
                self_.modifiedDate = kvargs["modifiedDate"]
            else:
                self_.modifiedDate = kvargs["modifiedDate"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "originAppId" in kvargs:
            if (
                type(kvargs["originAppId"]).__name__
                is self_.__annotations__["originAppId"]
            ):
                self_.originAppId = kvargs["originAppId"]
            else:
                self_.originAppId = kvargs["originAppId"]
        if "owner" in kvargs:
            if type(kvargs["owner"]).__name__ is self_.__annotations__["owner"]:
                self_.owner = kvargs["owner"]
            else:
                self_.owner = kvargs["owner"]
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ is self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        if "publishTime" in kvargs:
            if (
                type(kvargs["publishTime"]).__name__
                is self_.__annotations__["publishTime"]
            ):
                self_.publishTime = kvargs["publishTime"]
            else:
                self_.publishTime = kvargs["publishTime"]
        if "published" in kvargs:
            if type(kvargs["published"]).__name__ is self_.__annotations__["published"]:
                self_.published = kvargs["published"]
            else:
                self_.published = kvargs["published"]
        if "thumbnail" in kvargs:
            if type(kvargs["thumbnail"]).__name__ is self_.__annotations__["thumbnail"]:
                self_.thumbnail = kvargs["thumbnail"]
            else:
                self_.thumbnail = kvargs["thumbnail"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class PublishApp:
    """

    Attributes
    ----------
    attributes: AppUpdateAttributes
    data: str
      The published app will have data from source or target app.
      The default is source.


      • source: Publish with source data

      • target: Publish with target data
    spaceId: str
      The managed space ID where the app will be published.
    """

    attributes: AppUpdateAttributes = None
    data: str = None
    spaceId: str = None

    def __init__(self_, **kvargs):
        if "attributes" in kvargs:
            if (
                type(kvargs["attributes"]).__name__
                is self_.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = AppUpdateAttributes(**kvargs["attributes"])
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = kvargs["data"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class RepublishApp:
    """

    Attributes
    ----------
    attributes: AppUpdateAttributes
    checkOriginAppId: bool
      Validate that source app is same as originally published.
    data: str
      The republished app will have data from source or target app.
      The default is source.


      • source: Publish with source data

      • target: Publish with target data
    targetId: str
      The target ID to be republished.
    """

    attributes: AppUpdateAttributes = None
    checkOriginAppId: bool = None
    data: str = None
    targetId: str = None

    def __init__(self_, **kvargs):
        if "attributes" in kvargs:
            if (
                type(kvargs["attributes"]).__name__
                is self_.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = AppUpdateAttributes(**kvargs["attributes"])
        if "checkOriginAppId" in kvargs:
            if (
                type(kvargs["checkOriginAppId"]).__name__
                is self_.__annotations__["checkOriginAppId"]
            ):
                self_.checkOriginAppId = kvargs["checkOriginAppId"]
            else:
                self_.checkOriginAppId = kvargs["checkOriginAppId"]
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = kvargs["data"]
        if "targetId" in kvargs:
            if type(kvargs["targetId"]).__name__ is self_.__annotations__["targetId"]:
                self_.targetId = kvargs["targetId"]
            else:
                self_.targetId = kvargs["targetId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ScriptLogList:
    """

    Attributes
    ----------
    data: list[ScriptLogMeta]
      Array of scriptLogMeta.
    """

    data: list[ScriptLogMeta] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [ScriptLogMeta(**e) for e in kvargs["data"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ScriptLogMeta:
    """

    Attributes
    ----------
    duration: int
      Duration of reload (ms).
    endTime: str
      Time when reload ended.
    links: Log
    reloadId: str
      Reload identifier.
    success: bool
      True if the reload was successful.
    """

    duration: int = None
    endTime: str = None
    links: Log = None
    reloadId: str = None
    success: bool = None

    def __init__(self_, **kvargs):
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
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = Log(**kvargs["links"])
        if "reloadId" in kvargs:
            if type(kvargs["reloadId"]).__name__ is self_.__annotations__["reloadId"]:
                self_.reloadId = kvargs["reloadId"]
            else:
                self_.reloadId = kvargs["reloadId"]
        if "success" in kvargs:
            if type(kvargs["success"]).__name__ is self_.__annotations__["success"]:
                self_.success = kvargs["success"]
            else:
                self_.success = kvargs["success"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SymbolFrequency:
    """

    Attributes
    ----------
    Frequency: int
      Frequency of the above symbol in the field
    Symbol: SymbolValue
    """

    Frequency: int = None
    Symbol: SymbolValue = None

    def __init__(self_, **kvargs):
        if "Frequency" in kvargs:
            if type(kvargs["Frequency"]).__name__ is self_.__annotations__["Frequency"]:
                self_.Frequency = kvargs["Frequency"]
            else:
                self_.Frequency = kvargs["Frequency"]
        if "Symbol" in kvargs:
            if type(kvargs["Symbol"]).__name__ is self_.__annotations__["Symbol"]:
                self_.Symbol = kvargs["Symbol"]
            else:
                self_.Symbol = SymbolValue(**kvargs["Symbol"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SymbolValue:
    """

    Attributes
    ----------
    Number: float
      Numeric value of the symbol. NaN otherwise.
    Text: str
      String value of the symbol. This parameter is optional and present only if Symbol is a string.
    """

    Number: float = None
    Text: str = None

    def __init__(self_, **kvargs):
        if "Number" in kvargs:
            if type(kvargs["Number"]).__name__ is self_.__annotations__["Number"]:
                self_.Number = kvargs["Number"]
            else:
                self_.Number = kvargs["Number"]
        if "Text" in kvargs:
            if type(kvargs["Text"]).__name__ is self_.__annotations__["Text"]:
                self_.Text = kvargs["Text"]
            else:
                self_.Text = kvargs["Text"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableMetadata:
    """

    Attributes
    ----------
    byte_size: int
      Static RAM memory used in bytes.
    comment: str
      Table comment.
    is_loose: bool
      If set to true, the table is loose due to circular connection.
      The default value is false.
    is_semantic: bool
      If set to true, the table is semantic.
      The default value is false.
    is_system: bool
      If set to true, the table is a system table.
      The default value is false.
    name: str
      Name of the table.
    no_of_fields: int
      Number of fields.
    no_of_key_fields: int
      Number of key fields.
    no_of_rows: int
      Number of rows.
    """

    byte_size: int = None
    comment: str = None
    is_loose: bool = None
    is_semantic: bool = None
    is_system: bool = None
    name: str = None
    no_of_fields: int = None
    no_of_key_fields: int = None
    no_of_rows: int = None

    def __init__(self_, **kvargs):
        if "byte_size" in kvargs:
            if type(kvargs["byte_size"]).__name__ is self_.__annotations__["byte_size"]:
                self_.byte_size = kvargs["byte_size"]
            else:
                self_.byte_size = kvargs["byte_size"]
        if "comment" in kvargs:
            if type(kvargs["comment"]).__name__ is self_.__annotations__["comment"]:
                self_.comment = kvargs["comment"]
            else:
                self_.comment = kvargs["comment"]
        if "is_loose" in kvargs:
            if type(kvargs["is_loose"]).__name__ is self_.__annotations__["is_loose"]:
                self_.is_loose = kvargs["is_loose"]
            else:
                self_.is_loose = kvargs["is_loose"]
        if "is_semantic" in kvargs:
            if (
                type(kvargs["is_semantic"]).__name__
                is self_.__annotations__["is_semantic"]
            ):
                self_.is_semantic = kvargs["is_semantic"]
            else:
                self_.is_semantic = kvargs["is_semantic"]
        if "is_system" in kvargs:
            if type(kvargs["is_system"]).__name__ is self_.__annotations__["is_system"]:
                self_.is_system = kvargs["is_system"]
            else:
                self_.is_system = kvargs["is_system"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "no_of_fields" in kvargs:
            if (
                type(kvargs["no_of_fields"]).__name__
                is self_.__annotations__["no_of_fields"]
            ):
                self_.no_of_fields = kvargs["no_of_fields"]
            else:
                self_.no_of_fields = kvargs["no_of_fields"]
        if "no_of_key_fields" in kvargs:
            if (
                type(kvargs["no_of_key_fields"]).__name__
                is self_.__annotations__["no_of_key_fields"]
            ):
                self_.no_of_key_fields = kvargs["no_of_key_fields"]
            else:
                self_.no_of_key_fields = kvargs["no_of_key_fields"]
        if "no_of_rows" in kvargs:
            if (
                type(kvargs["no_of_rows"]).__name__
                is self_.__annotations__["no_of_rows"]
            ):
                self_.no_of_rows = kvargs["no_of_rows"]
            else:
                self_.no_of_rows = kvargs["no_of_rows"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableProfilingData:
    """

    Attributes
    ----------
    FieldProfiling: list[FieldInTableProfilingData]
      Field values profiling info
    NoOfRows: int
      Number of rows in the table.
    """

    FieldProfiling: list[FieldInTableProfilingData] = None
    NoOfRows: int = None

    def __init__(self_, **kvargs):
        if "FieldProfiling" in kvargs:
            if (
                type(kvargs["FieldProfiling"]).__name__
                is self_.__annotations__["FieldProfiling"]
            ):
                self_.FieldProfiling = kvargs["FieldProfiling"]
            else:
                self_.FieldProfiling = [
                    FieldInTableProfilingData(**e) for e in kvargs["FieldProfiling"]
                ]
        if "NoOfRows" in kvargs:
            if type(kvargs["NoOfRows"]).__name__ is self_.__annotations__["NoOfRows"]:
                self_.NoOfRows = kvargs["NoOfRows"]
            else:
                self_.NoOfRows = kvargs["NoOfRows"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UpdateApp:
    """

    Attributes
    ----------
    attributes: AppUpdateAttributes
    """

    attributes: AppUpdateAttributes = None

    def __init__(self_, **kvargs):
        if "attributes" in kvargs:
            if (
                type(kvargs["attributes"]).__name__
                is self_.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = AppUpdateAttributes(**kvargs["attributes"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UpdateOwner:
    """

    Attributes
    ----------
    ownerId: str
    """

    ownerId: str = None

    def __init__(self_, **kvargs):
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ is self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UpdateSpace:
    """

    Attributes
    ----------
    spaceId: str
    """

    spaceId: str = None

    def __init__(self_, **kvargs):
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Apps:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def create(self, data: CreateApp) -> NxApp:
        """
        Creates a new app.


        Parameters
        ----------
        data: CreateApp
        """

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/apps",
            method="POST",
            params={},
            data=data,
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def import_app(
        self,
        data: FileData,
        name: str = None,
        spaceId: str = None,
        mode: str = None,
        appId: str = None,
        fileId: str = None,
        fallbackName: str = None,
        NoData: bool = None,
    ) -> NxApp:
        """
        Imports an app into the system.


        name: str
          The name of the target app.

        spaceId: str
          The space ID of the target app.

        mode: str
          The import mode. In `new` mode (default), the source app will be imported as a new app with generated attributes.
          In `autoreplace` mode, the attributes from the source app will be retained and imported with the app.
          The app-id is extracted from the source app and used as the target app-id. If the app exists, it will be replaced.
          Approved objects in the target app that are not available in the source app will be removed.
          Non-approved objects in the target app will not be removed.

          One of:

          • NEW

          • AUTOREPLACE

        appId: str
          The app ID of the target app when source is qvw file.

        fileId: str
          The file ID to be downloaded from Temporary Content Service (TCS) and used during import.

        fallbackName: str
          The name of the target app when source does not have a specified name, applicable if source is qvw file.

        NoData: bool
          If NoData is true, the data of the existing app will be kept as is, otherwise it will be replaced by the new incoming data.

        Parameters
        ----------
        name: str = None
        spaceId: str = None
        mode: str = None
        appId: str = None
        fileId: str = None
        fallbackName: str = None
        NoData: bool = None
        data: FileData
        """
        query_params = {}
        if name is not None:
            query_params["name"] = name
        if spaceId is not None:
            query_params["spaceId"] = spaceId
        if mode is not None:
            query_params["mode"] = mode
        if appId is not None:
            query_params["appId"] = appId
        if fileId is not None:
            query_params["fileId"] = fileId
        if fallbackName is not None:
            query_params["fallbackName"] = fallbackName
        if NoData is not None:
            query_params["NoData"] = NoData

        try:
            data = asdict(data)
        except:
            data = data

        response = self.auth.rest(
            path="/apps/import",
            method="POST",
            params=query_params,
            data=data,
            headers={"Content-Type": "application/octet-stream"},
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def get_privileges(self) -> list[str]:
        """
        Gets the app privileges for the current user, such as create app and import app. Empty means that the current user has no app privileges.


        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/apps/privileges",
            method="GET",
            params={},
            data=None,
        )
        return response.json()

    def get(self, appId: str) -> NxApp:
        """
        Retrieves information for a specific app.


        appId: str
          Identifier of the app.

        Parameters
        ----------
        appId: str
        """

        response = self.auth.rest(
            path="/apps/{appId}".replace("{appId}", appId),
            method="GET",
            params={},
            data=None,
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def delete_media_file(self, appId: str, path: str) -> None:
        """
        Deletes a media content file or complete directory.
        Returns OK if the bytes containing the media file (or the complete content of a directory) were successfully deleted, or error in case of failure or lack of permission.


        appId: str
          Unique application identifier.

        path: str
          Path to file content.

        Parameters
        ----------
        appId: str
        path: str
        """

        self.auth.rest(
            path="/apps/{appId}/media/files/{path}".replace("{appId}", appId).replace(
                "{path}", path
            ),
            method="DELETE",
            params={},
            data=None,
        )

    def get_media_file(self, appId: str, path: str) -> str:
        """
        Gets media content from file.
        Returns a stream of bytes containing the media file content on success, or error if file is not found.


        appId: str
          Unique application identifier.

        path: str
          Path to file content.

        Parameters
        ----------
        appId: str
        path: str
        """

        response = self.auth.rest(
            path="/apps/{appId}/media/files/{path}".replace("{appId}", appId).replace(
                "{path}", path
            ),
            method="GET",
            params={},
            data=None,
            stream=True,
        )
        return response

    def set_media_file(self, appId: str, path: str, data: FileData) -> None:
        """
        Stores the media content file.
        Returns OK if the bytes containing the media file content were successfully stored, or error in case of failure, lack of permission or file already exists on the supplied path.


        appId: str
          Unique application identifier.

        path: str
          Path to file content.

        Parameters
        ----------
        appId: str
        path: str
        data: FileData
        """

        try:
            data = asdict(data)
        except:
            data = data

        self.auth.rest(
            path="/apps/{appId}/media/files/{path}".replace("{appId}", appId).replace(
                "{path}", path
            ),
            method="PUT",
            params={},
            data=data,
            headers={"Content-Type": "application/octet-stream"},
        )

    def get_media_lists(
        self, appId: str, path: str, show: str = None, max_items: int = 10
    ) -> ListableResource[AppContentListItem]:
        """
        Lists media content.
        Returns a JSON formatted array of strings describing the available media content or error if the optional path supplied is not found.


        appId: str
          Unique application identifier.

        path: str
          The path to sub folder with static content relative to the root folder. Use empty path to access the root folder.

        show: str
          Optional. List output can include files and folders in different ways:

          • Not recursive, default if show option is not supplied or incorrectly specified, results in output with files and empty directories for the path specified only.

          • Recursive(r), use ?show=r or ?show=recursive, results in a recursive output with files, all empty folders are excluded.

          • All(a), use ?show=a or ?show=all, results in a recursive output with files and empty directories.

        Parameters
        ----------
        appId: str
        path: str
        show: str = None
        """
        query_params = {}
        if show is not None:
            query_params["show"] = show

        response = self.auth.rest(
            path="/apps/{appId}/media/list/{path}".replace("{appId}", appId).replace(
                "{path}", path
            ),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=AppContentListItem,
            auth=self.auth,
            path="/apps/{appId}/media/list/{path}".replace("{appId}", appId).replace(
                "{path}", path
            ),
            max_items=max_items,
            query_params=query_params,
        )

    def get_reloads_log(self, appId: str, reloadId: str) -> str:
        """
        Experimental
        Retrieves the log of a specific reload.
        Returns the log as "text/plain; charset=UTF-8".


        appId: str
          Identifier of the app.

        reloadId: str
          Identifier of the reload.

        Parameters
        ----------
        appId: str
        reloadId: str
        """
        warnings.warn("get_reloads_log is experimental", UserWarning, stacklevel=2)

        response = self.auth.rest(
            path="/apps/{appId}/reloads/logs/{reloadId}".replace(
                "{appId}", appId
            ).replace("{reloadId}", reloadId),
            method="GET",
            params={},
            data=None,
            stream=True,
        )
        return response

    def create_session_app(self, session_app_id: str) -> NxApp:
        """
        creates an empty session app

        Parameters
        ----------
        session_app_id: string the a self generated "app_id" prefixed with SessionApp_

        Examples
        ----------
        >>> session_app_id = "SessionApp_" + str(uuid.uuid2())
        ... session_app = apps.create_session_app(session_app_id)
        ... with session_app.open():
        ...     script = "Load RecNo() as N autogenerate(200);"
        ...     session_app.set_script(script)
        ...     session_app.do_reload()
        """
        obj = NxApp(attributes={"id": session_app_id})
        obj.auth = self.auth
        return obj
