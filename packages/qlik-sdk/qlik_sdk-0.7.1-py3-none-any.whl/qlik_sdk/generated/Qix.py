# This is spectacularly generated code by spectacular v0.0.0 based on
# QIX 12.1351.0

from __future__ import annotations

import warnings
from dataclasses import dataclass

from ..rpc import RpcSession


@dataclass
class AlfaNumString:
    """

    Attributes
    ----------
    qString: str
      Calculated value.
    qIsNum: bool
      Is set to true if the value is a numeric.
    """

    qString: str = None
    qIsNum: bool = None

    def __init__(self_, **kvargs):
        if "qString" in kvargs:
            if type(kvargs["qString"]).__name__ is self_.__annotations__["qString"]:
                self_.qString = kvargs["qString"]
            else:
                self_.qString = kvargs["qString"]
        if "qIsNum" in kvargs:
            if type(kvargs["qIsNum"]).__name__ is self_.__annotations__["qIsNum"]:
                self_.qIsNum = kvargs["qIsNum"]
            else:
                self_.qIsNum = kvargs["qIsNum"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BNFDefMetaType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BNFType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Blob:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BookmarkFieldPage:
    """
    Defines the range of the bookmark fields that are returned.

    Attributes
    ----------
    qStartIndex: int
      The start value of the range.
    qEndIndex: int
      The end value of the range.
    """

    qStartIndex: int = None
    qEndIndex: int = None

    def __init__(self_, **kvargs):
        if "qStartIndex" in kvargs:
            if (
                type(kvargs["qStartIndex"]).__name__
                is self_.__annotations__["qStartIndex"]
            ):
                self_.qStartIndex = kvargs["qStartIndex"]
            else:
                self_.qStartIndex = kvargs["qStartIndex"]
        if "qEndIndex" in kvargs:
            if type(kvargs["qEndIndex"]).__name__ is self_.__annotations__["qEndIndex"]:
                self_.qEndIndex = kvargs["qEndIndex"]
            else:
                self_.qEndIndex = kvargs["qEndIndex"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CalendarStrings:
    """

    Attributes
    ----------
    qDayNames: list[str]
      List of short day names.
    qMonthNames: list[str]
      List of short month names.
    qLongDayNames: list[str]
      List of long day names.
    qLongMonthNames: list[str]
      List of long month names.
    """

    qDayNames: list[str] = None
    qMonthNames: list[str] = None
    qLongDayNames: list[str] = None
    qLongMonthNames: list[str] = None

    def __init__(self_, **kvargs):
        if "qDayNames" in kvargs:
            if type(kvargs["qDayNames"]).__name__ is self_.__annotations__["qDayNames"]:
                self_.qDayNames = kvargs["qDayNames"]
            else:
                self_.qDayNames = kvargs["qDayNames"]
        if "qMonthNames" in kvargs:
            if (
                type(kvargs["qMonthNames"]).__name__
                is self_.__annotations__["qMonthNames"]
            ):
                self_.qMonthNames = kvargs["qMonthNames"]
            else:
                self_.qMonthNames = kvargs["qMonthNames"]
        if "qLongDayNames" in kvargs:
            if (
                type(kvargs["qLongDayNames"]).__name__
                is self_.__annotations__["qLongDayNames"]
            ):
                self_.qLongDayNames = kvargs["qLongDayNames"]
            else:
                self_.qLongDayNames = kvargs["qLongDayNames"]
        if "qLongMonthNames" in kvargs:
            if (
                type(kvargs["qLongMonthNames"]).__name__
                is self_.__annotations__["qLongMonthNames"]
            ):
                self_.qLongMonthNames = kvargs["qLongMonthNames"]
            else:
                self_.qLongMonthNames = kvargs["qLongMonthNames"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CharEncodingType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CharRange:
    """

    Attributes
    ----------
    qCharPos: int
      Position of the first search occurrence.
    qCharCount: int
      Number of occurrences found.
    """

    qCharPos: int = None
    qCharCount: int = None

    def __init__(self_, **kvargs):
        if "qCharPos" in kvargs:
            if type(kvargs["qCharPos"]).__name__ is self_.__annotations__["qCharPos"]:
                self_.qCharPos = kvargs["qCharPos"]
            else:
                self_.qCharPos = kvargs["qCharPos"]
        if "qCharCount" in kvargs:
            if (
                type(kvargs["qCharCount"]).__name__
                is self_.__annotations__["qCharCount"]
            ):
                self_.qCharCount = kvargs["qCharCount"]
            else:
                self_.qCharCount = kvargs["qCharCount"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CodePage:
    """

    Attributes
    ----------
    qNumber: int
      Number of the code page.
    qName: str
      Name of the code page.
    qDescription: str
      Description of the code page.
    """

    qNumber: int = None
    qName: str = None
    qDescription: str = None

    def __init__(self_, **kvargs):
        if "qNumber" in kvargs:
            if type(kvargs["qNumber"]).__name__ is self_.__annotations__["qNumber"]:
                self_.qNumber = kvargs["qNumber"]
            else:
                self_.qNumber = kvargs["qNumber"]
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qDescription" in kvargs:
            if (
                type(kvargs["qDescription"]).__name__
                is self_.__annotations__["qDescription"]
            ):
                self_.qDescription = kvargs["qDescription"]
            else:
                self_.qDescription = kvargs["qDescription"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataField:
    """

    Attributes
    ----------
    qName: str
      Name of the field.
    qIsKey: bool
      Is set to true if the field is a primary key.
    qOriginalFieldName: str
      Is shown for fixed records.
      _qOriginalFieldName_ and qName are identical if no field names are used in the file.
      _qOriginalFieldName_ differs from qName if embedded file names are used in the file.
    """

    qName: str = None
    qIsKey: bool = None
    qOriginalFieldName: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qIsKey" in kvargs:
            if type(kvargs["qIsKey"]).__name__ is self_.__annotations__["qIsKey"]:
                self_.qIsKey = kvargs["qIsKey"]
            else:
                self_.qIsKey = kvargs["qIsKey"]
        if "qOriginalFieldName" in kvargs:
            if (
                type(kvargs["qOriginalFieldName"]).__name__
                is self_.__annotations__["qOriginalFieldName"]
            ):
                self_.qOriginalFieldName = kvargs["qOriginalFieldName"]
            else:
                self_.qOriginalFieldName = kvargs["qOriginalFieldName"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataRecord:
    """

    Attributes
    ----------
    qValues: list[str]
      List of values inside the table.
      The first values (in result/qPreview/0/qValues ) correspond to the field names in the table.
      The following values (from result/qPreview/1/qValues ) are the values of the fields in the table.
    """

    qValues: list[str] = None

    def __init__(self_, **kvargs):
        if "qValues" in kvargs:
            if type(kvargs["qValues"]).__name__ is self_.__annotations__["qValues"]:
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = kvargs["qValues"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataTable:
    """

    Attributes
    ----------
    qName: str
      Name of the table.
    qType: str
      Type of the table.
      For example: Table or View.
    """

    qName: str = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataTableEx:
    """

    Attributes
    ----------
    qName: str
      Name of the table.
    qFields: list[DataField]
      List of the fields in the table.
    qFormatSpec: str
      List of format specification items, within brackets.
      Examples of specification items:

      • file type

      • embedded labels, no labels

      • table is <table name>
    """

    qName: str = None
    qFields: list[DataField] = None
    qFormatSpec: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qFields" in kvargs:
            if type(kvargs["qFields"]).__name__ is self_.__annotations__["qFields"]:
                self_.qFields = kvargs["qFields"]
            else:
                self_.qFields = [DataField(**e) for e in kvargs["qFields"]]
        if "qFormatSpec" in kvargs:
            if (
                type(kvargs["qFormatSpec"]).__name__
                is self_.__annotations__["qFormatSpec"]
            ):
                self_.qFormatSpec = kvargs["qFormatSpec"]
            else:
                self_.qFormatSpec = kvargs["qFormatSpec"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Database:
    """

    Attributes
    ----------
    qName: str
      Name of the database.
    qIsDefault: bool
      Is set to true if the database is set by default.
    """

    qName: str = None
    qIsDefault: bool = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qIsDefault" in kvargs:
            if (
                type(kvargs["qIsDefault"]).__name__
                is self_.__annotations__["qIsDefault"]
            ):
                self_.qIsDefault = kvargs["qIsDefault"]
            else:
                self_.qIsDefault = kvargs["qIsDefault"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DatabaseInfo:
    """

    Attributes
    ----------
    qDBMSName: str
      Name of the product accessed by the provider.
    qDBUsage: bool
      If set to true, it means that the data source contains some databases.
    qOwnerUsage: bool
      If set to true, it means that the data source contains some owners.
    qDBSeparator: str
      Character string used after the database name.
      Example with separator " . ":
      FROM LinkedTablesData.dbo.Months
      Where:

      • LinkedTablesData is the database name

      • dbo is the owner name

      • Months is the table name
    qOwnerSeparator: str
      Character string used after the owner name.
      Example with separator " . ":
      FROM LinkedTablesData.dbo.Months
      Where:

      • LinkedTablesData is the database name

      • dbo is the owner name

      • Months is the table name
    qDBFirst: bool
      If set to true, it means that the database is displayed first, before the owners and tables.
    qQuotePreffix: str
      Prefix used with field, database or owner names that contain special characters or keywords.
    qQuoteSuffix: str
      Suffix used with field, database or owner names that contain special characters or keywords.
    qSpecialChars: str
      List of the special characters.
    qDefaultDatabase: str
      Name of the default database.
    qKeywords: list[str]
      List of the script keywords.
    """

    qDBMSName: str = None
    qDBUsage: bool = None
    qOwnerUsage: bool = None
    qDBSeparator: str = None
    qOwnerSeparator: str = None
    qDBFirst: bool = None
    qQuotePreffix: str = None
    qQuoteSuffix: str = None
    qSpecialChars: str = None
    qDefaultDatabase: str = None
    qKeywords: list[str] = None

    def __init__(self_, **kvargs):
        if "qDBMSName" in kvargs:
            if type(kvargs["qDBMSName"]).__name__ is self_.__annotations__["qDBMSName"]:
                self_.qDBMSName = kvargs["qDBMSName"]
            else:
                self_.qDBMSName = kvargs["qDBMSName"]
        if "qDBUsage" in kvargs:
            if type(kvargs["qDBUsage"]).__name__ is self_.__annotations__["qDBUsage"]:
                self_.qDBUsage = kvargs["qDBUsage"]
            else:
                self_.qDBUsage = kvargs["qDBUsage"]
        if "qOwnerUsage" in kvargs:
            if (
                type(kvargs["qOwnerUsage"]).__name__
                is self_.__annotations__["qOwnerUsage"]
            ):
                self_.qOwnerUsage = kvargs["qOwnerUsage"]
            else:
                self_.qOwnerUsage = kvargs["qOwnerUsage"]
        if "qDBSeparator" in kvargs:
            if (
                type(kvargs["qDBSeparator"]).__name__
                is self_.__annotations__["qDBSeparator"]
            ):
                self_.qDBSeparator = kvargs["qDBSeparator"]
            else:
                self_.qDBSeparator = kvargs["qDBSeparator"]
        if "qOwnerSeparator" in kvargs:
            if (
                type(kvargs["qOwnerSeparator"]).__name__
                is self_.__annotations__["qOwnerSeparator"]
            ):
                self_.qOwnerSeparator = kvargs["qOwnerSeparator"]
            else:
                self_.qOwnerSeparator = kvargs["qOwnerSeparator"]
        if "qDBFirst" in kvargs:
            if type(kvargs["qDBFirst"]).__name__ is self_.__annotations__["qDBFirst"]:
                self_.qDBFirst = kvargs["qDBFirst"]
            else:
                self_.qDBFirst = kvargs["qDBFirst"]
        if "qQuotePreffix" in kvargs:
            if (
                type(kvargs["qQuotePreffix"]).__name__
                is self_.__annotations__["qQuotePreffix"]
            ):
                self_.qQuotePreffix = kvargs["qQuotePreffix"]
            else:
                self_.qQuotePreffix = kvargs["qQuotePreffix"]
        if "qQuoteSuffix" in kvargs:
            if (
                type(kvargs["qQuoteSuffix"]).__name__
                is self_.__annotations__["qQuoteSuffix"]
            ):
                self_.qQuoteSuffix = kvargs["qQuoteSuffix"]
            else:
                self_.qQuoteSuffix = kvargs["qQuoteSuffix"]
        if "qSpecialChars" in kvargs:
            if (
                type(kvargs["qSpecialChars"]).__name__
                is self_.__annotations__["qSpecialChars"]
            ):
                self_.qSpecialChars = kvargs["qSpecialChars"]
            else:
                self_.qSpecialChars = kvargs["qSpecialChars"]
        if "qDefaultDatabase" in kvargs:
            if (
                type(kvargs["qDefaultDatabase"]).__name__
                is self_.__annotations__["qDefaultDatabase"]
            ):
                self_.qDefaultDatabase = kvargs["qDefaultDatabase"]
            else:
                self_.qDefaultDatabase = kvargs["qDefaultDatabase"]
        if "qKeywords" in kvargs:
            if type(kvargs["qKeywords"]).__name__ is self_.__annotations__["qKeywords"]:
                self_.qKeywords = kvargs["qKeywords"]
            else:
                self_.qKeywords = kvargs["qKeywords"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DatabaseOwner:
    """

    Attributes
    ----------
    qName: str
      Name of the owner.
    """

    qName: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DelimiterInfo:
    """

    Attributes
    ----------
    qName: str
      Name of the delimiter.
      Example:
      "Tab_DELIMITER"
    qScriptCode: str
      Representation of the delimiter value that is used in the script.
      Example:
      "'\t'"
    qNumber: int
      Delimiter character number used by the engine to determine how to separate the values.
    qIsMultiple: bool
      Is set to true if multiple spaces are used to separate the values.
    """

    qName: str = None
    qScriptCode: str = None
    qNumber: int = None
    qIsMultiple: bool = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qScriptCode" in kvargs:
            if (
                type(kvargs["qScriptCode"]).__name__
                is self_.__annotations__["qScriptCode"]
            ):
                self_.qScriptCode = kvargs["qScriptCode"]
            else:
                self_.qScriptCode = kvargs["qScriptCode"]
        if "qNumber" in kvargs:
            if type(kvargs["qNumber"]).__name__ is self_.__annotations__["qNumber"]:
                self_.qNumber = kvargs["qNumber"]
            else:
                self_.qNumber = kvargs["qNumber"]
        if "qIsMultiple" in kvargs:
            if (
                type(kvargs["qIsMultiple"]).__name__
                is self_.__annotations__["qIsMultiple"]
            ):
                self_.qIsMultiple = kvargs["qIsMultiple"]
            else:
                self_.qIsMultiple = kvargs["qIsMultiple"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DerivedFieldsInTableData:
    """

    Attributes
    ----------
    qDefinitionName: str
      Name of the derived definition.
    qTags: list[str]
      List of tags.
    qActive: bool
      Is set to true is the derived field is in use.
    """

    qDefinitionName: str = None
    qTags: list[str] = None
    qActive: bool = None

    def __init__(self_, **kvargs):
        if "qDefinitionName" in kvargs:
            if (
                type(kvargs["qDefinitionName"]).__name__
                is self_.__annotations__["qDefinitionName"]
            ):
                self_.qDefinitionName = kvargs["qDefinitionName"]
            else:
                self_.qDefinitionName = kvargs["qDefinitionName"]
        if "qTags" in kvargs:
            if type(kvargs["qTags"]).__name__ is self_.__annotations__["qTags"]:
                self_.qTags = kvargs["qTags"]
            else:
                self_.qTags = kvargs["qTags"]
        if "qActive" in kvargs:
            if type(kvargs["qActive"]).__name__ is self_.__annotations__["qActive"]:
                self_.qActive = kvargs["qActive"]
            else:
                self_.qActive = kvargs["qActive"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DoReloadExParams:
    """
    Parameters for a reload.

    Attributes
    ----------
    qMode: int
      0: for default mode.
      1: for ABEND; the reload of the script ends if an error occurs.
      2: for ignore; the reload of the script continues even if an error is detected in the script.
    qPartial: bool
      Set to true for partial reload.
      The default value is false.
    qDebug: bool
      Set to true to debug reload.
      The default value is false.
    qReloadId: str
      Optional reload ID.
      ID will be automatically generated if not set.
    """

    qMode: int = None
    qPartial: bool = None
    qDebug: bool = None
    qReloadId: str = None

    def __init__(self_, **kvargs):
        if "qMode" in kvargs:
            if type(kvargs["qMode"]).__name__ is self_.__annotations__["qMode"]:
                self_.qMode = kvargs["qMode"]
            else:
                self_.qMode = kvargs["qMode"]
        if "qPartial" in kvargs:
            if type(kvargs["qPartial"]).__name__ is self_.__annotations__["qPartial"]:
                self_.qPartial = kvargs["qPartial"]
            else:
                self_.qPartial = kvargs["qPartial"]
        if "qDebug" in kvargs:
            if type(kvargs["qDebug"]).__name__ is self_.__annotations__["qDebug"]:
                self_.qDebug = kvargs["qDebug"]
            else:
                self_.qDebug = kvargs["qDebug"]
        if "qReloadId" in kvargs:
            if type(kvargs["qReloadId"]).__name__ is self_.__annotations__["qReloadId"]:
                self_.qReloadId = kvargs["qReloadId"]
            else:
                self_.qReloadId = kvargs["qReloadId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DoReloadExResult:
    """
    The result and path to script log for a reload.

    Attributes
    ----------
    qSuccess: bool
      The reload is successful if True.
    qScriptLogFile: str
      Path to the script log file.
    """

    qSuccess: bool = None
    qScriptLogFile: str = None

    def __init__(self_, **kvargs):
        if "qSuccess" in kvargs:
            if type(kvargs["qSuccess"]).__name__ is self_.__annotations__["qSuccess"]:
                self_.qSuccess = kvargs["qSuccess"]
            else:
                self_.qSuccess = kvargs["qSuccess"]
        if "qScriptLogFile" in kvargs:
            if (
                type(kvargs["qScriptLogFile"]).__name__
                is self_.__annotations__["qScriptLogFile"]
            ):
                self_.qScriptLogFile = kvargs["qScriptLogFile"]
            else:
                self_.qScriptLogFile = kvargs["qScriptLogFile"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DriveType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EditorBreakpoint:
    """

    Attributes
    ----------
    qbufferName: str
      Name of the breakpoint.
    qlineIx: int
      Line number in the script where the breakpoint is set.
    qEnabled: bool
      If set to true then the breakpoint is enabled (in use).
    """

    qbufferName: str = None
    qlineIx: int = None
    qEnabled: bool = None

    def __init__(self_, **kvargs):
        if "qbufferName" in kvargs:
            if (
                type(kvargs["qbufferName"]).__name__
                is self_.__annotations__["qbufferName"]
            ):
                self_.qbufferName = kvargs["qbufferName"]
            else:
                self_.qbufferName = kvargs["qbufferName"]
        if "qlineIx" in kvargs:
            if type(kvargs["qlineIx"]).__name__ is self_.__annotations__["qlineIx"]:
                self_.qlineIx = kvargs["qlineIx"]
            else:
                self_.qlineIx = kvargs["qlineIx"]
        if "qEnabled" in kvargs:
            if type(kvargs["qEnabled"]).__name__ is self_.__annotations__["qEnabled"]:
                self_.qEnabled = kvargs["qEnabled"]
            else:
                self_.qEnabled = kvargs["qEnabled"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EmbeddedSnapshot:
    """
    Renders the embedded snapshot in an object.
    The following is returned:

    • Any dynamic properties defined in the bookmark

    • Any properties defined in qEmbeddedSnapshot

    Properties:

    "qEmbeddedSnapshot": {}

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EmbeddedSnapshotDef:
    """
    Defines the embedded snapshot in a generic object.

    Properties:

    "EmbeddedSnapshotDef": {}

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ErrorDataCode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ExtendedPivotStateData:
    """

    Attributes
    ----------
    qExpressionPosition: int
    qNumberOfLeftDimensions: int
    qDimensionNames: list[str]
    qEnableConditions: list[str]
    """

    qExpressionPosition: int = None
    qNumberOfLeftDimensions: int = None
    qDimensionNames: list[str] = None
    qEnableConditions: list[str] = None

    def __init__(self_, **kvargs):
        if "qExpressionPosition" in kvargs:
            if (
                type(kvargs["qExpressionPosition"]).__name__
                is self_.__annotations__["qExpressionPosition"]
            ):
                self_.qExpressionPosition = kvargs["qExpressionPosition"]
            else:
                self_.qExpressionPosition = kvargs["qExpressionPosition"]
        if "qNumberOfLeftDimensions" in kvargs:
            if (
                type(kvargs["qNumberOfLeftDimensions"]).__name__
                is self_.__annotations__["qNumberOfLeftDimensions"]
            ):
                self_.qNumberOfLeftDimensions = kvargs["qNumberOfLeftDimensions"]
            else:
                self_.qNumberOfLeftDimensions = kvargs["qNumberOfLeftDimensions"]
        if "qDimensionNames" in kvargs:
            if (
                type(kvargs["qDimensionNames"]).__name__
                is self_.__annotations__["qDimensionNames"]
            ):
                self_.qDimensionNames = kvargs["qDimensionNames"]
            else:
                self_.qDimensionNames = kvargs["qDimensionNames"]
        if "qEnableConditions" in kvargs:
            if (
                type(kvargs["qEnableConditions"]).__name__
                is self_.__annotations__["qEnableConditions"]
            ):
                self_.qEnableConditions = kvargs["qEnableConditions"]
            else:
                self_.qEnableConditions = kvargs["qEnableConditions"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ExtensionList:
    """
    Obsolete, use qrs API's to fetch extensions.

    Attributes
    ----------
    qItems: list[str]
    """

    qItems: list[str] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs:
            if type(kvargs["qItems"]).__name__ is self_.__annotations__["qItems"]:
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = kvargs["qItems"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ExtensionListDef:
    """
    Obsolete, use qrs API's to fetch extensions.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldAttrType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
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
    qType: str
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
    qnDec: int
      Number of decimals.
      Default is 10.
    qUseThou: int
      Defines whether or not a thousands separator must be used.
      Default is 0.
    qFmt: str
      Defines the format pattern that applies to qText .
      Is used in connection to the type of the field (parameter qType ).
      For more information, see Formatting mechanism.
      Example: YYYY-MM-DD for a date.
    qDec: str
      Defines the decimal separator.
      Example:

      .:
    qThou: str
      Defines the thousand separator (if any).
      Is used if qUseThou is set to 1.
      Example:

      ,:
    """

    qType: str = "UNKNOWN"
    qnDec: int = 10
    qUseThou: int = None
    qFmt: str = None
    qDec: str = None
    qThou: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qnDec" in kvargs:
            if type(kvargs["qnDec"]).__name__ is self_.__annotations__["qnDec"]:
                self_.qnDec = kvargs["qnDec"]
            else:
                self_.qnDec = kvargs["qnDec"]
        if "qUseThou" in kvargs:
            if type(kvargs["qUseThou"]).__name__ is self_.__annotations__["qUseThou"]:
                self_.qUseThou = kvargs["qUseThou"]
            else:
                self_.qUseThou = kvargs["qUseThou"]
        if "qFmt" in kvargs:
            if type(kvargs["qFmt"]).__name__ is self_.__annotations__["qFmt"]:
                self_.qFmt = kvargs["qFmt"]
            else:
                self_.qFmt = kvargs["qFmt"]
        if "qDec" in kvargs:
            if type(kvargs["qDec"]).__name__ is self_.__annotations__["qDec"]:
                self_.qDec = kvargs["qDec"]
            else:
                self_.qDec = kvargs["qDec"]
        if "qThou" in kvargs:
            if type(kvargs["qThou"]).__name__ is self_.__annotations__["qThou"]:
                self_.qThou = kvargs["qThou"]
            else:
                self_.qThou = kvargs["qThou"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldDescription:
    """

    Attributes
    ----------
    qInternalNumber: int
      Internal number of the field.
    qName: str
      Name of the field.
    qSrcTables: list[str]
      List of table names.
    qIsSystem: bool
      If set to true, it means that the field is a system field.
      The default value is false.
    qIsHidden: bool
      If set to true, it means that the field is hidden.
      The default value is false.
    qIsSemantic: bool
      If set to true, it means that the field is a semantic.
      The default value is false.
    qDistinctOnly: bool
      If set to true, only distinct field values are shown.
      The default value is false.
    qCardinal: int
      Number of distinct field values.
    qTotalCount: int
      Total number of field values.
    qPossibleCount_OBSOLETE: int
    qHasInfo_OBSOLETE: bool
    qIsLocked: bool
      If set to true, it means that the field is locked.
      The default value is false.
    qAlwaysOneSelected: bool
      If set to true, it means that the field has one and only one selection (not 0 and not more than 1).
      If this property is set to true, the field cannot be cleared anymore and no more selections can be performed in that field.
      The default value is false.
    qAndMode: bool
      If set to true a logical AND (instead of a logical OR) is used when making selections in a field.
      The default value is false.
    qIsNumeric: bool
      Is set to true if the value is a numeric.
      The default value is false.
    qComment: str
      Field comment.
    qTags: list[str]
      Gives information on a field. For example, it can return the type of the field.
      Examples: key, text, ASCII.
    qIsDefinitionOnly: bool
      If set to true, it means that the field is a field on the fly.
      The default value is false.
    qByteSize: int
      Static RAM memory used in bytes.
    """

    qInternalNumber: int = None
    qName: str = None
    qSrcTables: list[str] = None
    qIsSystem: bool = None
    qIsHidden: bool = None
    qIsSemantic: bool = None
    qDistinctOnly: bool = None
    qCardinal: int = None
    qTotalCount: int = None
    qPossibleCount_OBSOLETE: int = None
    qHasInfo_OBSOLETE: bool = None
    qIsLocked: bool = None
    qAlwaysOneSelected: bool = None
    qAndMode: bool = None
    qIsNumeric: bool = None
    qComment: str = None
    qTags: list[str] = None
    qIsDefinitionOnly: bool = None
    qByteSize: int = None

    def __init__(self_, **kvargs):
        if "qInternalNumber" in kvargs:
            if (
                type(kvargs["qInternalNumber"]).__name__
                is self_.__annotations__["qInternalNumber"]
            ):
                self_.qInternalNumber = kvargs["qInternalNumber"]
            else:
                self_.qInternalNumber = kvargs["qInternalNumber"]
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qSrcTables" in kvargs:
            if (
                type(kvargs["qSrcTables"]).__name__
                is self_.__annotations__["qSrcTables"]
            ):
                self_.qSrcTables = kvargs["qSrcTables"]
            else:
                self_.qSrcTables = kvargs["qSrcTables"]
        if "qIsSystem" in kvargs:
            if type(kvargs["qIsSystem"]).__name__ is self_.__annotations__["qIsSystem"]:
                self_.qIsSystem = kvargs["qIsSystem"]
            else:
                self_.qIsSystem = kvargs["qIsSystem"]
        if "qIsHidden" in kvargs:
            if type(kvargs["qIsHidden"]).__name__ is self_.__annotations__["qIsHidden"]:
                self_.qIsHidden = kvargs["qIsHidden"]
            else:
                self_.qIsHidden = kvargs["qIsHidden"]
        if "qIsSemantic" in kvargs:
            if (
                type(kvargs["qIsSemantic"]).__name__
                is self_.__annotations__["qIsSemantic"]
            ):
                self_.qIsSemantic = kvargs["qIsSemantic"]
            else:
                self_.qIsSemantic = kvargs["qIsSemantic"]
        if "qDistinctOnly" in kvargs:
            if (
                type(kvargs["qDistinctOnly"]).__name__
                is self_.__annotations__["qDistinctOnly"]
            ):
                self_.qDistinctOnly = kvargs["qDistinctOnly"]
            else:
                self_.qDistinctOnly = kvargs["qDistinctOnly"]
        if "qCardinal" in kvargs:
            if type(kvargs["qCardinal"]).__name__ is self_.__annotations__["qCardinal"]:
                self_.qCardinal = kvargs["qCardinal"]
            else:
                self_.qCardinal = kvargs["qCardinal"]
        if "qTotalCount" in kvargs:
            if (
                type(kvargs["qTotalCount"]).__name__
                is self_.__annotations__["qTotalCount"]
            ):
                self_.qTotalCount = kvargs["qTotalCount"]
            else:
                self_.qTotalCount = kvargs["qTotalCount"]
        if "qPossibleCount_OBSOLETE" in kvargs:
            if (
                type(kvargs["qPossibleCount_OBSOLETE"]).__name__
                is self_.__annotations__["qPossibleCount_OBSOLETE"]
            ):
                self_.qPossibleCount_OBSOLETE = kvargs["qPossibleCount_OBSOLETE"]
            else:
                self_.qPossibleCount_OBSOLETE = kvargs["qPossibleCount_OBSOLETE"]
        if "qHasInfo_OBSOLETE" in kvargs:
            if (
                type(kvargs["qHasInfo_OBSOLETE"]).__name__
                is self_.__annotations__["qHasInfo_OBSOLETE"]
            ):
                self_.qHasInfo_OBSOLETE = kvargs["qHasInfo_OBSOLETE"]
            else:
                self_.qHasInfo_OBSOLETE = kvargs["qHasInfo_OBSOLETE"]
        if "qIsLocked" in kvargs:
            if type(kvargs["qIsLocked"]).__name__ is self_.__annotations__["qIsLocked"]:
                self_.qIsLocked = kvargs["qIsLocked"]
            else:
                self_.qIsLocked = kvargs["qIsLocked"]
        if "qAlwaysOneSelected" in kvargs:
            if (
                type(kvargs["qAlwaysOneSelected"]).__name__
                is self_.__annotations__["qAlwaysOneSelected"]
            ):
                self_.qAlwaysOneSelected = kvargs["qAlwaysOneSelected"]
            else:
                self_.qAlwaysOneSelected = kvargs["qAlwaysOneSelected"]
        if "qAndMode" in kvargs:
            if type(kvargs["qAndMode"]).__name__ is self_.__annotations__["qAndMode"]:
                self_.qAndMode = kvargs["qAndMode"]
            else:
                self_.qAndMode = kvargs["qAndMode"]
        if "qIsNumeric" in kvargs:
            if (
                type(kvargs["qIsNumeric"]).__name__
                is self_.__annotations__["qIsNumeric"]
            ):
                self_.qIsNumeric = kvargs["qIsNumeric"]
            else:
                self_.qIsNumeric = kvargs["qIsNumeric"]
        if "qComment" in kvargs:
            if type(kvargs["qComment"]).__name__ is self_.__annotations__["qComment"]:
                self_.qComment = kvargs["qComment"]
            else:
                self_.qComment = kvargs["qComment"]
        if "qTags" in kvargs:
            if type(kvargs["qTags"]).__name__ is self_.__annotations__["qTags"]:
                self_.qTags = kvargs["qTags"]
            else:
                self_.qTags = kvargs["qTags"]
        if "qIsDefinitionOnly" in kvargs:
            if (
                type(kvargs["qIsDefinitionOnly"]).__name__
                is self_.__annotations__["qIsDefinitionOnly"]
            ):
                self_.qIsDefinitionOnly = kvargs["qIsDefinitionOnly"]
            else:
                self_.qIsDefinitionOnly = kvargs["qIsDefinitionOnly"]
        if "qByteSize" in kvargs:
            if type(kvargs["qByteSize"]).__name__ is self_.__annotations__["qByteSize"]:
                self_.qByteSize = kvargs["qByteSize"]
            else:
                self_.qByteSize = kvargs["qByteSize"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldListDef:
    """
    Defines the fields to show.

    Attributes
    ----------
    qShowSystem: bool
      Shows the system tables if set to true.
      Default is false.
    qShowHidden: bool
      Shows the hidden fields if set to true.
      Default is false.
    qShowSemantic: bool
      Show the semantic fields if set to true.
      Default is false.
    qShowSrcTables: bool
      Shows the tables and fields present in the data model viewer if set to true.
      Default is false.
    qShowDefinitionOnly: bool
      Shows the fields defined on the fly if set to true.
      Default is false.
    qShowDerivedFields: bool
      Shows the fields and derived fields if set to true.
      Default is false.
    qShowImplicit: bool
      Shows the Direct Discovery measure fields if set to true.
      Default is false.
    """

    qShowSystem: bool = None
    qShowHidden: bool = None
    qShowSemantic: bool = None
    qShowSrcTables: bool = None
    qShowDefinitionOnly: bool = None
    qShowDerivedFields: bool = None
    qShowImplicit: bool = None

    def __init__(self_, **kvargs):
        if "qShowSystem" in kvargs:
            if (
                type(kvargs["qShowSystem"]).__name__
                is self_.__annotations__["qShowSystem"]
            ):
                self_.qShowSystem = kvargs["qShowSystem"]
            else:
                self_.qShowSystem = kvargs["qShowSystem"]
        if "qShowHidden" in kvargs:
            if (
                type(kvargs["qShowHidden"]).__name__
                is self_.__annotations__["qShowHidden"]
            ):
                self_.qShowHidden = kvargs["qShowHidden"]
            else:
                self_.qShowHidden = kvargs["qShowHidden"]
        if "qShowSemantic" in kvargs:
            if (
                type(kvargs["qShowSemantic"]).__name__
                is self_.__annotations__["qShowSemantic"]
            ):
                self_.qShowSemantic = kvargs["qShowSemantic"]
            else:
                self_.qShowSemantic = kvargs["qShowSemantic"]
        if "qShowSrcTables" in kvargs:
            if (
                type(kvargs["qShowSrcTables"]).__name__
                is self_.__annotations__["qShowSrcTables"]
            ):
                self_.qShowSrcTables = kvargs["qShowSrcTables"]
            else:
                self_.qShowSrcTables = kvargs["qShowSrcTables"]
        if "qShowDefinitionOnly" in kvargs:
            if (
                type(kvargs["qShowDefinitionOnly"]).__name__
                is self_.__annotations__["qShowDefinitionOnly"]
            ):
                self_.qShowDefinitionOnly = kvargs["qShowDefinitionOnly"]
            else:
                self_.qShowDefinitionOnly = kvargs["qShowDefinitionOnly"]
        if "qShowDerivedFields" in kvargs:
            if (
                type(kvargs["qShowDerivedFields"]).__name__
                is self_.__annotations__["qShowDerivedFields"]
            ):
                self_.qShowDerivedFields = kvargs["qShowDerivedFields"]
            else:
                self_.qShowDerivedFields = kvargs["qShowDerivedFields"]
        if "qShowImplicit" in kvargs:
            if (
                type(kvargs["qShowImplicit"]).__name__
                is self_.__annotations__["qShowImplicit"]
            ):
                self_.qShowImplicit = kvargs["qShowImplicit"]
            else:
                self_.qShowImplicit = kvargs["qShowImplicit"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldOrColumn:
    """

    Attributes
    ----------
    qFieldName: str
      Name of the field or column to be matched.
    qTableName: str
      Name of the table to be matched on. This parameter is optional. If TableName is set, FieldName represent the Table column with that name. If TableName is not set, FieldName represents the the field with that name.
    """

    qFieldName: str = None
    qTableName: str = None

    def __init__(self_, **kvargs):
        if "qFieldName" in kvargs:
            if (
                type(kvargs["qFieldName"]).__name__
                is self_.__annotations__["qFieldName"]
            ):
                self_.qFieldName = kvargs["qFieldName"]
            else:
                self_.qFieldName = kvargs["qFieldName"]
        if "qTableName" in kvargs:
            if (
                type(kvargs["qTableName"]).__name__
                is self_.__annotations__["qTableName"]
            ):
                self_.qTableName = kvargs["qTableName"]
            else:
                self_.qTableName = kvargs["qTableName"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldScores:
    """

    Attributes
    ----------
    qFieldName: str
      Field name.
      One of the field names defined in qFieldPairName.
    qReadableName: str
    qCardinalRatio: float
      Cardinality of a column/field divided by the number of rows in the table.
      If the cardinal ratio is 1, it means that the column is a candidate/primary key.
    qSymbolScore: float
      Number of distinct matches between the two fields defined in qFieldPairName divided by the number of distinct values in the field qFieldName .
      If 0, it means that there are no common values between the two fields defined in qFieldPairName .
    qRowScore: float
      Number of matches between the two fields defined in qFieldPairName divided by the number of values in the field qFieldName .
      If 0, it means that there are no common values between the two fields defined in qFieldPairName .
    """

    qFieldName: str = None
    qReadableName: str = None
    qCardinalRatio: float = None
    qSymbolScore: float = None
    qRowScore: float = None

    def __init__(self_, **kvargs):
        if "qFieldName" in kvargs:
            if (
                type(kvargs["qFieldName"]).__name__
                is self_.__annotations__["qFieldName"]
            ):
                self_.qFieldName = kvargs["qFieldName"]
            else:
                self_.qFieldName = kvargs["qFieldName"]
        if "qReadableName" in kvargs:
            if (
                type(kvargs["qReadableName"]).__name__
                is self_.__annotations__["qReadableName"]
            ):
                self_.qReadableName = kvargs["qReadableName"]
            else:
                self_.qReadableName = kvargs["qReadableName"]
        if "qCardinalRatio" in kvargs:
            if (
                type(kvargs["qCardinalRatio"]).__name__
                is self_.__annotations__["qCardinalRatio"]
            ):
                self_.qCardinalRatio = kvargs["qCardinalRatio"]
            else:
                self_.qCardinalRatio = kvargs["qCardinalRatio"]
        if "qSymbolScore" in kvargs:
            if (
                type(kvargs["qSymbolScore"]).__name__
                is self_.__annotations__["qSymbolScore"]
            ):
                self_.qSymbolScore = kvargs["qSymbolScore"]
            else:
                self_.qSymbolScore = kvargs["qSymbolScore"]
        if "qRowScore" in kvargs:
            if type(kvargs["qRowScore"]).__name__ is self_.__annotations__["qRowScore"]:
                self_.qRowScore = kvargs["qRowScore"]
            else:
                self_.qRowScore = kvargs["qRowScore"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldValue:
    """

    Attributes
    ----------
    qText: str
      Text related to the field value.
      This parameter is optional.
    qIsNumeric: bool
      Is set to true if the value is a numeric.
      This parameter is optional. Default is false.
    qNumber: float
      Numeric value of the field.
      This parameter is displayed if qIsNumeric is set to true.
      This parameter is optional.
    """

    qText: str = None
    qIsNumeric: bool = None
    qNumber: float = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qIsNumeric" in kvargs:
            if (
                type(kvargs["qIsNumeric"]).__name__
                is self_.__annotations__["qIsNumeric"]
            ):
                self_.qIsNumeric = kvargs["qIsNumeric"]
            else:
                self_.qIsNumeric = kvargs["qIsNumeric"]
        if "qNumber" in kvargs:
            if type(kvargs["qNumber"]).__name__ is self_.__annotations__["qNumber"]:
                self_.qNumber = kvargs["qNumber"]
            else:
                self_.qNumber = kvargs["qNumber"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FileType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FilterType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FolderItemType:
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
    qNumberOfBins: int
      Number of bins.
    qBinsEdges: list[float]
      Bins edges.
    qFrequencies: list[int]
      Bins frequencies.
    """

    qNumberOfBins: int = None
    qBinsEdges: list[float] = None
    qFrequencies: list[int] = None

    def __init__(self_, **kvargs):
        if "qNumberOfBins" in kvargs:
            if (
                type(kvargs["qNumberOfBins"]).__name__
                is self_.__annotations__["qNumberOfBins"]
            ):
                self_.qNumberOfBins = kvargs["qNumberOfBins"]
            else:
                self_.qNumberOfBins = kvargs["qNumberOfBins"]
        if "qBinsEdges" in kvargs:
            if (
                type(kvargs["qBinsEdges"]).__name__
                is self_.__annotations__["qBinsEdges"]
            ):
                self_.qBinsEdges = kvargs["qBinsEdges"]
            else:
                self_.qBinsEdges = kvargs["qBinsEdges"]
        if "qFrequencies" in kvargs:
            if (
                type(kvargs["qFrequencies"]).__name__
                is self_.__annotations__["qFrequencies"]
            ):
                self_.qFrequencies = kvargs["qFrequencies"]
            else:
                self_.qFrequencies = kvargs["qFrequencies"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FunctionGroup:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericConnectMachine:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericDimensionInfo:
    """

    Attributes
    ----------
    qApprMaxGlyphCount: int
      Length of the longest value in the field.
    qCardinal: int
      Number of distinct field values
    qTags: list[str]
      Gives information on a field. For example, it can return the type of the field.
      Examples: key, text, ASCII
    qIsSemantic: bool
      If set to true, it means that the field is a semantic.
    qAndMode: bool
      If set to true a logical AND (instead of a logical OR) is used when making selections in a field.
      The default value is false.
    """

    qApprMaxGlyphCount: int = None
    qCardinal: int = None
    qTags: list[str] = None
    qIsSemantic: bool = None
    qAndMode: bool = None

    def __init__(self_, **kvargs):
        if "qApprMaxGlyphCount" in kvargs:
            if (
                type(kvargs["qApprMaxGlyphCount"]).__name__
                is self_.__annotations__["qApprMaxGlyphCount"]
            ):
                self_.qApprMaxGlyphCount = kvargs["qApprMaxGlyphCount"]
            else:
                self_.qApprMaxGlyphCount = kvargs["qApprMaxGlyphCount"]
        if "qCardinal" in kvargs:
            if type(kvargs["qCardinal"]).__name__ is self_.__annotations__["qCardinal"]:
                self_.qCardinal = kvargs["qCardinal"]
            else:
                self_.qCardinal = kvargs["qCardinal"]
        if "qTags" in kvargs:
            if type(kvargs["qTags"]).__name__ is self_.__annotations__["qTags"]:
                self_.qTags = kvargs["qTags"]
            else:
                self_.qTags = kvargs["qTags"]
        if "qIsSemantic" in kvargs:
            if (
                type(kvargs["qIsSemantic"]).__name__
                is self_.__annotations__["qIsSemantic"]
            ):
                self_.qIsSemantic = kvargs["qIsSemantic"]
            else:
                self_.qIsSemantic = kvargs["qIsSemantic"]
        if "qAndMode" in kvargs:
            if type(kvargs["qAndMode"]).__name__ is self_.__annotations__["qAndMode"]:
                self_.qAndMode = kvargs["qAndMode"]
            else:
                self_.qAndMode = kvargs["qAndMode"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GraphMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupBookmarkData:
    """

    Attributes
    ----------
    qId: str
    qCyclePos: int
    """

    qId: str = None
    qCyclePos: int = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs:
            if type(kvargs["qId"]).__name__ is self_.__annotations__["qId"]:
                self_.qId = kvargs["qId"]
            else:
                self_.qId = kvargs["qId"]
        if "qCyclePos" in kvargs:
            if type(kvargs["qCyclePos"]).__name__ is self_.__annotations__["qCyclePos"]:
                self_.qCyclePos = kvargs["qCyclePos"]
            else:
                self_.qCyclePos = kvargs["qCyclePos"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupStateInfo:
    """

    Attributes
    ----------
    qGroupName: str
    qCurrentItemName: str
    """

    qGroupName: str = None
    qCurrentItemName: str = None

    def __init__(self_, **kvargs):
        if "qGroupName" in kvargs:
            if (
                type(kvargs["qGroupName"]).__name__
                is self_.__annotations__["qGroupName"]
            ):
                self_.qGroupName = kvargs["qGroupName"]
            else:
                self_.qGroupName = kvargs["qGroupName"]
        if "qCurrentItemName" in kvargs:
            if (
                type(kvargs["qCurrentItemName"]).__name__
                is self_.__annotations__["qCurrentItemName"]
            ):
                self_.qCurrentItemName = kvargs["qCurrentItemName"]
            else:
                self_.qCurrentItemName = kvargs["qCurrentItemName"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class InputFieldItem:
    """

    Attributes
    ----------
    qFieldName: str
    qValues: list[FieldValue]
    qPackedHashKeys: list[int]
    """

    qFieldName: str = None
    qValues: list[FieldValue] = None
    qPackedHashKeys: list[int] = None

    def __init__(self_, **kvargs):
        if "qFieldName" in kvargs:
            if (
                type(kvargs["qFieldName"]).__name__
                is self_.__annotations__["qFieldName"]
            ):
                self_.qFieldName = kvargs["qFieldName"]
            else:
                self_.qFieldName = kvargs["qFieldName"]
        if "qValues" in kvargs:
            if type(kvargs["qValues"]).__name__ is self_.__annotations__["qValues"]:
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [FieldValue(**e) for e in kvargs["qValues"]]
        if "qPackedHashKeys" in kvargs:
            if (
                type(kvargs["qPackedHashKeys"]).__name__
                is self_.__annotations__["qPackedHashKeys"]
            ):
                self_.qPackedHashKeys = kvargs["qPackedHashKeys"]
            else:
                self_.qPackedHashKeys = kvargs["qPackedHashKeys"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class InterFieldSortData:
    """

    Attributes
    ----------
    qName: str
    qReversed: bool
    """

    qName: str = None
    qReversed: bool = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qReversed" in kvargs:
            if type(kvargs["qReversed"]).__name__ is self_.__annotations__["qReversed"]:
                self_.qReversed = kvargs["qReversed"]
            else:
                self_.qReversed = kvargs["qReversed"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class InteractType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
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
class KeyType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LayoutExclude:
    """
    Contains JSON to be excluded from validation.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LayoutFieldInfo:
    """
    Meta data about the selection in a field.

    Attributes
    ----------
    qFieldName: str
      The name of the field.
    qValuesCount: int
      Number of selected values in the field.
    qExcludedValuesCount: int
      Number of excluded values in the field.
    """

    qFieldName: str = None
    qValuesCount: int = None
    qExcludedValuesCount: int = None

    def __init__(self_, **kvargs):
        if "qFieldName" in kvargs:
            if (
                type(kvargs["qFieldName"]).__name__
                is self_.__annotations__["qFieldName"]
            ):
                self_.qFieldName = kvargs["qFieldName"]
            else:
                self_.qFieldName = kvargs["qFieldName"]
        if "qValuesCount" in kvargs:
            if (
                type(kvargs["qValuesCount"]).__name__
                is self_.__annotations__["qValuesCount"]
            ):
                self_.qValuesCount = kvargs["qValuesCount"]
            else:
                self_.qValuesCount = kvargs["qValuesCount"]
        if "qExcludedValuesCount" in kvargs:
            if (
                type(kvargs["qExcludedValuesCount"]).__name__
                is self_.__annotations__["qExcludedValuesCount"]
            ):
                self_.qExcludedValuesCount = kvargs["qExcludedValuesCount"]
            else:
                self_.qExcludedValuesCount = kvargs["qExcludedValuesCount"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LineageInfo:
    """

    Attributes
    ----------
    qDiscriminator: str
      A string indicating the origin of the data:

      • [filename]: the data comes from a local file.

      • INLINE: the data is entered inline in the load script.

      • RESIDENT: the data comes from a resident table. The table name is listed.

      • AUTOGENERATE: the data is generated from the load script (no external table of data source).

      • Provider: the data comes from a data connection. The connector source name is listed.

      • [webfile]: the data comes from a web-based file.

      • STORE: path to QVD or TXT file where data is stored.

      • EXTENSION: the data comes from a Server Side Extension (SSE).
    qStatement: str
      The LOAD and SELECT script statements from the data load script.
    """

    qDiscriminator: str = None
    qStatement: str = None

    def __init__(self_, **kvargs):
        if "qDiscriminator" in kvargs:
            if (
                type(kvargs["qDiscriminator"]).__name__
                is self_.__annotations__["qDiscriminator"]
            ):
                self_.qDiscriminator = kvargs["qDiscriminator"]
            else:
                self_.qDiscriminator = kvargs["qDiscriminator"]
        if "qStatement" in kvargs:
            if (
                type(kvargs["qStatement"]).__name__
                is self_.__annotations__["qStatement"]
            ):
                self_.qStatement = kvargs["qStatement"]
            else:
                self_.qStatement = kvargs["qStatement"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LocaleInfo:
    """

    Attributes
    ----------
    qDecimalSep: str
      Decimal separator.
    qThousandSep: str
      Thousand separator.
    qListSep: str
      List separator.
    qMoneyDecimalSep: str
      Money decimal separator.
    qMoneyThousandSep: str
      Money thousand separator.
    qCurrentYear: int
      Current year.
    qMoneyFmt: str
      Money format.
      Example:

      .

      0,00 kr;-#.##0,00 kr:

      :
    qTimeFmt: str
      Time format.
      Example: hh:mm:ss
    qDateFmt: str
      Date format.
      Example: YYYY-MM-DD
    qTimestampFmt: str
      Time stamp format.
      Example: YYYY-MM-DD hh:mm:ss[.fff]
    qCalendarStrings: CalendarStrings
      Information about the calendar.
    qFirstWeekDay: int
      First day of the week, starting from 0.
      According to ISO 8601, Monday is the first day of the week.

      • 0 = Monday

      • 1 = Tuesday

      • ...

      • 6 = Sunday

      If this property has not been set in a script, the returned value comes from the Windows operating system.
    qBrokenWeeks: bool
      Is set to true if broken weeks are allowed in a year.
      According to ISO 8601, no broken weeks should be allowed.
      This property is not shown if set to false.
      If qBrokenWeeks is set to true, qReferenceDay is irrelevant.
      If this property has not been set in a script, the returned value comes from the Windows operating system.
    qReferenceDay: int
      Day in the year that is always in week 1.
      According to ISO 8601, January 4th should always be part of the first week of the year ( qReferenceDay =4).
      Recommended values are in the range 1 and 7.
      If this property has not been set in a script, the returned value comes from the Windows operating system.
      This property is not relevant if there are broken weeks in the year.
    qFirstMonthOfYear: int
      First month of the year, starting from 1.
      According to ISO 8601, January is the first month of the year.

      • 1 = January

      • 2 = February

      • 12 = January

      If this property has not been set in a script, the returned value comes from the Windows operating system.
    qCollation: str
      Locale name (following language tagging convention RFC 4646):
      _< language>-<REGION>_
      Where:

      • language is a lowercase ISO  639 language code

      • REGION specifies an uppercase ISO 3166 country code.

      If this property has not been set in a script, the returned value comes from the Windows operating system.
    qNumericalAbbreviation: str
      Number format.
      Example: 3:k;6:M;9:G;12:T;15:P;18:E;21:Z;24:Y;-3:m;-6:μ;-9:n;-12:p;-15:f;-18:a;-21:z;-24:y
    """

    qDecimalSep: str = None
    qThousandSep: str = None
    qListSep: str = None
    qMoneyDecimalSep: str = None
    qMoneyThousandSep: str = None
    qCurrentYear: int = None
    qMoneyFmt: str = None
    qTimeFmt: str = None
    qDateFmt: str = None
    qTimestampFmt: str = None
    qCalendarStrings: CalendarStrings = None
    qFirstWeekDay: int = None
    qBrokenWeeks: bool = None
    qReferenceDay: int = None
    qFirstMonthOfYear: int = None
    qCollation: str = None
    qNumericalAbbreviation: str = None

    def __init__(self_, **kvargs):
        if "qDecimalSep" in kvargs:
            if (
                type(kvargs["qDecimalSep"]).__name__
                is self_.__annotations__["qDecimalSep"]
            ):
                self_.qDecimalSep = kvargs["qDecimalSep"]
            else:
                self_.qDecimalSep = kvargs["qDecimalSep"]
        if "qThousandSep" in kvargs:
            if (
                type(kvargs["qThousandSep"]).__name__
                is self_.__annotations__["qThousandSep"]
            ):
                self_.qThousandSep = kvargs["qThousandSep"]
            else:
                self_.qThousandSep = kvargs["qThousandSep"]
        if "qListSep" in kvargs:
            if type(kvargs["qListSep"]).__name__ is self_.__annotations__["qListSep"]:
                self_.qListSep = kvargs["qListSep"]
            else:
                self_.qListSep = kvargs["qListSep"]
        if "qMoneyDecimalSep" in kvargs:
            if (
                type(kvargs["qMoneyDecimalSep"]).__name__
                is self_.__annotations__["qMoneyDecimalSep"]
            ):
                self_.qMoneyDecimalSep = kvargs["qMoneyDecimalSep"]
            else:
                self_.qMoneyDecimalSep = kvargs["qMoneyDecimalSep"]
        if "qMoneyThousandSep" in kvargs:
            if (
                type(kvargs["qMoneyThousandSep"]).__name__
                is self_.__annotations__["qMoneyThousandSep"]
            ):
                self_.qMoneyThousandSep = kvargs["qMoneyThousandSep"]
            else:
                self_.qMoneyThousandSep = kvargs["qMoneyThousandSep"]
        if "qCurrentYear" in kvargs:
            if (
                type(kvargs["qCurrentYear"]).__name__
                is self_.__annotations__["qCurrentYear"]
            ):
                self_.qCurrentYear = kvargs["qCurrentYear"]
            else:
                self_.qCurrentYear = kvargs["qCurrentYear"]
        if "qMoneyFmt" in kvargs:
            if type(kvargs["qMoneyFmt"]).__name__ is self_.__annotations__["qMoneyFmt"]:
                self_.qMoneyFmt = kvargs["qMoneyFmt"]
            else:
                self_.qMoneyFmt = kvargs["qMoneyFmt"]
        if "qTimeFmt" in kvargs:
            if type(kvargs["qTimeFmt"]).__name__ is self_.__annotations__["qTimeFmt"]:
                self_.qTimeFmt = kvargs["qTimeFmt"]
            else:
                self_.qTimeFmt = kvargs["qTimeFmt"]
        if "qDateFmt" in kvargs:
            if type(kvargs["qDateFmt"]).__name__ is self_.__annotations__["qDateFmt"]:
                self_.qDateFmt = kvargs["qDateFmt"]
            else:
                self_.qDateFmt = kvargs["qDateFmt"]
        if "qTimestampFmt" in kvargs:
            if (
                type(kvargs["qTimestampFmt"]).__name__
                is self_.__annotations__["qTimestampFmt"]
            ):
                self_.qTimestampFmt = kvargs["qTimestampFmt"]
            else:
                self_.qTimestampFmt = kvargs["qTimestampFmt"]
        if "qCalendarStrings" in kvargs:
            if (
                type(kvargs["qCalendarStrings"]).__name__
                is self_.__annotations__["qCalendarStrings"]
            ):
                self_.qCalendarStrings = kvargs["qCalendarStrings"]
            else:
                self_.qCalendarStrings = CalendarStrings(**kvargs["qCalendarStrings"])
        if "qFirstWeekDay" in kvargs:
            if (
                type(kvargs["qFirstWeekDay"]).__name__
                is self_.__annotations__["qFirstWeekDay"]
            ):
                self_.qFirstWeekDay = kvargs["qFirstWeekDay"]
            else:
                self_.qFirstWeekDay = kvargs["qFirstWeekDay"]
        if "qBrokenWeeks" in kvargs:
            if (
                type(kvargs["qBrokenWeeks"]).__name__
                is self_.__annotations__["qBrokenWeeks"]
            ):
                self_.qBrokenWeeks = kvargs["qBrokenWeeks"]
            else:
                self_.qBrokenWeeks = kvargs["qBrokenWeeks"]
        if "qReferenceDay" in kvargs:
            if (
                type(kvargs["qReferenceDay"]).__name__
                is self_.__annotations__["qReferenceDay"]
            ):
                self_.qReferenceDay = kvargs["qReferenceDay"]
            else:
                self_.qReferenceDay = kvargs["qReferenceDay"]
        if "qFirstMonthOfYear" in kvargs:
            if (
                type(kvargs["qFirstMonthOfYear"]).__name__
                is self_.__annotations__["qFirstMonthOfYear"]
            ):
                self_.qFirstMonthOfYear = kvargs["qFirstMonthOfYear"]
            else:
                self_.qFirstMonthOfYear = kvargs["qFirstMonthOfYear"]
        if "qCollation" in kvargs:
            if (
                type(kvargs["qCollation"]).__name__
                is self_.__annotations__["qCollation"]
            ):
                self_.qCollation = kvargs["qCollation"]
            else:
                self_.qCollation = kvargs["qCollation"]
        if "qNumericalAbbreviation" in kvargs:
            if (
                type(kvargs["qNumericalAbbreviation"]).__name__
                is self_.__annotations__["qNumericalAbbreviation"]
            ):
                self_.qNumericalAbbreviation = kvargs["qNumericalAbbreviation"]
            else:
                self_.qNumericalAbbreviation = kvargs["qNumericalAbbreviation"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LogOnType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MeasureListDef:
    """
    Defines the list of measures.

    Attributes
    ----------
    qType: str
      Type of the list.
    qData: JsonObject
      Data
    """

    qType: str = None
    qData: JsonObject = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qData" in kvargs:
            if type(kvargs["qData"]).__name__ is self_.__annotations__["qData"]:
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(**kvargs["qData"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MediaListDef:
    """
    Defines the list of media files.
    This struct is deprecated.

    Properties:

    "qMediaListDef": {}
    _qMediaListDef_ has an empty structure. No properties need to be set.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MediaListItem:
    """
    In addition, this structure can return dynamic properties.

    Attributes
    ----------
    qUrlDef: str
      Relative path to the media file. The URL is static.
      Media files located:

      • in the /content/default/ folder are outside the qvf file.

      • in the /media/ folder are embedded in the qvf file.
    qUrl: str
      Relative path to the media file.
      Media files located:

      • in the /content/default/ folder are outside the qvf file.

      • in the /media/ folder are embedded in the qvf file.
    """

    qUrlDef: str = None
    qUrl: str = None

    def __init__(self_, **kvargs):
        if "qUrlDef" in kvargs:
            if type(kvargs["qUrlDef"]).__name__ is self_.__annotations__["qUrlDef"]:
                self_.qUrlDef = kvargs["qUrlDef"]
            else:
                self_.qUrlDef = kvargs["qUrlDef"]
        if "qUrl" in kvargs:
            if type(kvargs["qUrl"]).__name__ is self_.__annotations__["qUrl"]:
                self_.qUrl = kvargs["qUrl"]
            else:
                self_.qUrl = kvargs["qUrl"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MetaData:
    """

    Attributes
    ----------
    qShared: bool
    qUtcModifyTime: float
    qSheetId: str
    qTemporary: bool
    qRestrictedAccess: bool
    qAccessList: list[str]
    qPersonalEditionHash_OBSOLETE: str
    qHidden: bool
    qLinkedTo: list[str]
    """

    qShared: bool = None
    qUtcModifyTime: float = None
    qSheetId: str = None
    qTemporary: bool = None
    qRestrictedAccess: bool = None
    qAccessList: list[str] = None
    qPersonalEditionHash_OBSOLETE: str = None
    qHidden: bool = None
    qLinkedTo: list[str] = None

    def __init__(self_, **kvargs):
        if "qShared" in kvargs:
            if type(kvargs["qShared"]).__name__ is self_.__annotations__["qShared"]:
                self_.qShared = kvargs["qShared"]
            else:
                self_.qShared = kvargs["qShared"]
        if "qUtcModifyTime" in kvargs:
            if (
                type(kvargs["qUtcModifyTime"]).__name__
                is self_.__annotations__["qUtcModifyTime"]
            ):
                self_.qUtcModifyTime = kvargs["qUtcModifyTime"]
            else:
                self_.qUtcModifyTime = kvargs["qUtcModifyTime"]
        if "qSheetId" in kvargs:
            if type(kvargs["qSheetId"]).__name__ is self_.__annotations__["qSheetId"]:
                self_.qSheetId = kvargs["qSheetId"]
            else:
                self_.qSheetId = kvargs["qSheetId"]
        if "qTemporary" in kvargs:
            if (
                type(kvargs["qTemporary"]).__name__
                is self_.__annotations__["qTemporary"]
            ):
                self_.qTemporary = kvargs["qTemporary"]
            else:
                self_.qTemporary = kvargs["qTemporary"]
        if "qRestrictedAccess" in kvargs:
            if (
                type(kvargs["qRestrictedAccess"]).__name__
                is self_.__annotations__["qRestrictedAccess"]
            ):
                self_.qRestrictedAccess = kvargs["qRestrictedAccess"]
            else:
                self_.qRestrictedAccess = kvargs["qRestrictedAccess"]
        if "qAccessList" in kvargs:
            if (
                type(kvargs["qAccessList"]).__name__
                is self_.__annotations__["qAccessList"]
            ):
                self_.qAccessList = kvargs["qAccessList"]
            else:
                self_.qAccessList = kvargs["qAccessList"]
        if "qPersonalEditionHash_OBSOLETE" in kvargs:
            if (
                type(kvargs["qPersonalEditionHash_OBSOLETE"]).__name__
                is self_.__annotations__["qPersonalEditionHash_OBSOLETE"]
            ):
                self_.qPersonalEditionHash_OBSOLETE = kvargs[
                    "qPersonalEditionHash_OBSOLETE"
                ]
            else:
                self_.qPersonalEditionHash_OBSOLETE = kvargs[
                    "qPersonalEditionHash_OBSOLETE"
                ]
        if "qHidden" in kvargs:
            if type(kvargs["qHidden"]).__name__ is self_.__annotations__["qHidden"]:
                self_.qHidden = kvargs["qHidden"]
            else:
                self_.qHidden = kvargs["qHidden"]
        if "qLinkedTo" in kvargs:
            if type(kvargs["qLinkedTo"]).__name__ is self_.__annotations__["qLinkedTo"]:
                self_.qLinkedTo = kvargs["qLinkedTo"]
            else:
                self_.qLinkedTo = kvargs["qLinkedTo"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttrExprDef:
    """

    Attributes
    ----------
    qExpression: str
      Definition of the attribute expression.
      Example: "Max(OrderID)"
    qLibraryId: str
      Definition of the attribute expression stored in the library.
      Example: "MyGenericMeasure"
    qAttribute: bool
      If set to true, this measure will not affect the number of rows in the cube.
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    qLabel: str
      Label of the attribute expression.
    qLabelExpression: str
      Optional expression used for dynamic label.
    """

    qExpression: str = None
    qLibraryId: str = None
    qAttribute: bool = None
    qNumFormat: FieldAttributes = None
    qLabel: str = None
    qLabelExpression: str = None

    def __init__(self_, **kvargs):
        if "qExpression" in kvargs:
            if (
                type(kvargs["qExpression"]).__name__
                is self_.__annotations__["qExpression"]
            ):
                self_.qExpression = kvargs["qExpression"]
            else:
                self_.qExpression = kvargs["qExpression"]
        if "qLibraryId" in kvargs:
            if (
                type(kvargs["qLibraryId"]).__name__
                is self_.__annotations__["qLibraryId"]
            ):
                self_.qLibraryId = kvargs["qLibraryId"]
            else:
                self_.qLibraryId = kvargs["qLibraryId"]
        if "qAttribute" in kvargs:
            if (
                type(kvargs["qAttribute"]).__name__
                is self_.__annotations__["qAttribute"]
            ):
                self_.qAttribute = kvargs["qAttribute"]
            else:
                self_.qAttribute = kvargs["qAttribute"]
        if "qNumFormat" in kvargs:
            if (
                type(kvargs["qNumFormat"]).__name__
                is self_.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(**kvargs["qNumFormat"])
        if "qLabel" in kvargs:
            if type(kvargs["qLabel"]).__name__ is self_.__annotations__["qLabel"]:
                self_.qLabel = kvargs["qLabel"]
            else:
                self_.qLabel = kvargs["qLabel"]
        if "qLabelExpression" in kvargs:
            if (
                type(kvargs["qLabelExpression"]).__name__
                is self_.__annotations__["qLabelExpression"]
            ):
                self_.qLabelExpression = kvargs["qLabelExpression"]
            else:
                self_.qLabelExpression = kvargs["qLabelExpression"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttrExprInfo:
    """
    Layout for NxAttrExprDef.

    Attributes
    ----------
    qMin: float
      Minimum value.
    qMax: float
      Maximum value.
    qFallbackTitle: str
    qMinText: str
      String version of the minimum Value.
    qMaxText: str
      String version of the maximum Value.
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    qIsAutoFormat: bool
      This parameter is set to true if qNumFormat is set to U (unknown). The engine guesses the type of the field based on the field's expression.
    """

    qMin: float = None
    qMax: float = None
    qFallbackTitle: str = None
    qMinText: str = None
    qMaxText: str = None
    qNumFormat: FieldAttributes = None
    qIsAutoFormat: bool = None

    def __init__(self_, **kvargs):
        if "qMin" in kvargs:
            if type(kvargs["qMin"]).__name__ is self_.__annotations__["qMin"]:
                self_.qMin = kvargs["qMin"]
            else:
                self_.qMin = kvargs["qMin"]
        if "qMax" in kvargs:
            if type(kvargs["qMax"]).__name__ is self_.__annotations__["qMax"]:
                self_.qMax = kvargs["qMax"]
            else:
                self_.qMax = kvargs["qMax"]
        if "qFallbackTitle" in kvargs:
            if (
                type(kvargs["qFallbackTitle"]).__name__
                is self_.__annotations__["qFallbackTitle"]
            ):
                self_.qFallbackTitle = kvargs["qFallbackTitle"]
            else:
                self_.qFallbackTitle = kvargs["qFallbackTitle"]
        if "qMinText" in kvargs:
            if type(kvargs["qMinText"]).__name__ is self_.__annotations__["qMinText"]:
                self_.qMinText = kvargs["qMinText"]
            else:
                self_.qMinText = kvargs["qMinText"]
        if "qMaxText" in kvargs:
            if type(kvargs["qMaxText"]).__name__ is self_.__annotations__["qMaxText"]:
                self_.qMaxText = kvargs["qMaxText"]
            else:
                self_.qMaxText = kvargs["qMaxText"]
        if "qNumFormat" in kvargs:
            if (
                type(kvargs["qNumFormat"]).__name__
                is self_.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(**kvargs["qNumFormat"])
        if "qIsAutoFormat" in kvargs:
            if (
                type(kvargs["qIsAutoFormat"]).__name__
                is self_.__annotations__["qIsAutoFormat"]
            ):
                self_.qIsAutoFormat = kvargs["qIsAutoFormat"]
            else:
                self_.qIsAutoFormat = kvargs["qIsAutoFormat"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAutoSortByStateDef:
    """

    Attributes
    ----------
    qDisplayNumberOfRows: int
      This parameter applies to list objects.
      If the number of selected values in the list object is greater than the value set in qDisplayNumberOfRows , the selected lines are promoted at the top of the list object.
      If qDisplayNumberOfRows is set to a negative value or to 0, the sort by state is disabled.
    """

    qDisplayNumberOfRows: int = None

    def __init__(self_, **kvargs):
        if "qDisplayNumberOfRows" in kvargs:
            if (
                type(kvargs["qDisplayNumberOfRows"]).__name__
                is self_.__annotations__["qDisplayNumberOfRows"]
            ):
                self_.qDisplayNumberOfRows = kvargs["qDisplayNumberOfRows"]
            else:
                self_.qDisplayNumberOfRows = kvargs["qDisplayNumberOfRows"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxCardinalities:
    """

    Attributes
    ----------
    qCardinal: int
      Number of distinct field values.
    qHypercubeCardinal: int
      Number of distinct hypercube values.
    qAllValuesCardinal: int
      Number of distinct values when paging for AllValues in a Tree Structure.
      Default is -1 if not part of a Tree structure.
    """

    qCardinal: int = None
    qHypercubeCardinal: int = None
    qAllValuesCardinal: int = -1

    def __init__(self_, **kvargs):
        if "qCardinal" in kvargs:
            if type(kvargs["qCardinal"]).__name__ is self_.__annotations__["qCardinal"]:
                self_.qCardinal = kvargs["qCardinal"]
            else:
                self_.qCardinal = kvargs["qCardinal"]
        if "qHypercubeCardinal" in kvargs:
            if (
                type(kvargs["qHypercubeCardinal"]).__name__
                is self_.__annotations__["qHypercubeCardinal"]
            ):
                self_.qHypercubeCardinal = kvargs["qHypercubeCardinal"]
            else:
                self_.qHypercubeCardinal = kvargs["qHypercubeCardinal"]
        if "qAllValuesCardinal" in kvargs:
            if (
                type(kvargs["qAllValuesCardinal"]).__name__
                is self_.__annotations__["qAllValuesCardinal"]
            ):
                self_.qAllValuesCardinal = kvargs["qAllValuesCardinal"]
            else:
                self_.qAllValuesCardinal = kvargs["qAllValuesCardinal"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxCellPosition:
    """

    Attributes
    ----------
    qx: int
      Position of the cell on the x-axis.
    qy: int
      Position of the cell on the y-axis.
    """

    qx: int = None
    qy: int = None

    def __init__(self_, **kvargs):
        if "qx" in kvargs:
            if type(kvargs["qx"]).__name__ is self_.__annotations__["qx"]:
                self_.qx = kvargs["qx"]
            else:
                self_.qx = kvargs["qx"]
        if "qy" in kvargs:
            if type(kvargs["qy"]).__name__ is self_.__annotations__["qy"]:
                self_.qy = kvargs["qy"]
            else:
                self_.qy = kvargs["qy"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxContinuousDataOptions:
    """

    Attributes
    ----------
    qStart: float
      Start value.
    qEnd: float
      End value.
    qNbrPoints: int
      Number of bins for binning.
    qMaxNbrTicks: int
      Maximum number of ticks.
    qMaxNumberLines: int
      Maximum number of lines.
    """

    qStart: float = None
    qEnd: float = None
    qNbrPoints: int = None
    qMaxNbrTicks: int = None
    qMaxNumberLines: int = -1

    def __init__(self_, **kvargs):
        if "qStart" in kvargs:
            if type(kvargs["qStart"]).__name__ is self_.__annotations__["qStart"]:
                self_.qStart = kvargs["qStart"]
            else:
                self_.qStart = kvargs["qStart"]
        if "qEnd" in kvargs:
            if type(kvargs["qEnd"]).__name__ is self_.__annotations__["qEnd"]:
                self_.qEnd = kvargs["qEnd"]
            else:
                self_.qEnd = kvargs["qEnd"]
        if "qNbrPoints" in kvargs:
            if (
                type(kvargs["qNbrPoints"]).__name__
                is self_.__annotations__["qNbrPoints"]
            ):
                self_.qNbrPoints = kvargs["qNbrPoints"]
            else:
                self_.qNbrPoints = kvargs["qNbrPoints"]
        if "qMaxNbrTicks" in kvargs:
            if (
                type(kvargs["qMaxNbrTicks"]).__name__
                is self_.__annotations__["qMaxNbrTicks"]
            ):
                self_.qMaxNbrTicks = kvargs["qMaxNbrTicks"]
            else:
                self_.qMaxNbrTicks = kvargs["qMaxNbrTicks"]
        if "qMaxNumberLines" in kvargs:
            if (
                type(kvargs["qMaxNumberLines"]).__name__
                is self_.__annotations__["qMaxNumberLines"]
            ):
                self_.qMaxNumberLines = kvargs["qMaxNumberLines"]
            else:
                self_.qMaxNumberLines = kvargs["qMaxNumberLines"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxContinuousMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDataAreaPage:
    """

    Attributes
    ----------
    qLeft: float
      Position from the left.
      Corresponds to the lowest possible value of the first measure (the measure on the x-axis).
    qTop: float
      Position from the top.
      Corresponds to the highest possible value of the second measure (the measure on the y-axis).
    qWidth: float
      Width of the page.
      Corresponds to the highest possible value of the first measure (the measure on the x-axis).
    qHeight: float
      Height of the page.
      The difference between qTop and qHeight gives the lowest possible value of the second measure (the measure on the y-axis).
    """

    qLeft: float = None
    qTop: float = None
    qWidth: float = None
    qHeight: float = None

    def __init__(self_, **kvargs):
        if "qLeft" in kvargs:
            if type(kvargs["qLeft"]).__name__ is self_.__annotations__["qLeft"]:
                self_.qLeft = kvargs["qLeft"]
            else:
                self_.qLeft = kvargs["qLeft"]
        if "qTop" in kvargs:
            if type(kvargs["qTop"]).__name__ is self_.__annotations__["qTop"]:
                self_.qTop = kvargs["qTop"]
            else:
                self_.qTop = kvargs["qTop"]
        if "qWidth" in kvargs:
            if type(kvargs["qWidth"]).__name__ is self_.__annotations__["qWidth"]:
                self_.qWidth = kvargs["qWidth"]
            else:
                self_.qWidth = kvargs["qWidth"]
        if "qHeight" in kvargs:
            if type(kvargs["qHeight"]).__name__ is self_.__annotations__["qHeight"]:
                self_.qHeight = kvargs["qHeight"]
            else:
                self_.qHeight = kvargs["qHeight"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDataReductionMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDerivedField:
    """

    Attributes
    ----------
    qId: str
      Identifier of the derived field.
      The identifier is unique.
    qName: str
      Combination of field name, definition and method.
      Example:
      _OrderDate.MyDefinition.Year_
    qMethod: str
      Method name associated to the derived field.
    qExpr: str
      Expression of the derived field.
      Example:
      If qName is OrderDate.MyDefinition.Year , the expression is as follows:
      _=${Mydefinition(OrderDate).Year}_
    qTags: list[str]
      List of tags.
    """

    qId: str = None
    qName: str = None
    qMethod: str = None
    qExpr: str = None
    qTags: list[str] = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs:
            if type(kvargs["qId"]).__name__ is self_.__annotations__["qId"]:
                self_.qId = kvargs["qId"]
            else:
                self_.qId = kvargs["qId"]
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qMethod" in kvargs:
            if type(kvargs["qMethod"]).__name__ is self_.__annotations__["qMethod"]:
                self_.qMethod = kvargs["qMethod"]
            else:
                self_.qMethod = kvargs["qMethod"]
        if "qExpr" in kvargs:
            if type(kvargs["qExpr"]).__name__ is self_.__annotations__["qExpr"]:
                self_.qExpr = kvargs["qExpr"]
            else:
                self_.qExpr = kvargs["qExpr"]
        if "qTags" in kvargs:
            if type(kvargs["qTags"]).__name__ is self_.__annotations__["qTags"]:
                self_.qTags = kvargs["qTags"]
            else:
                self_.qTags = kvargs["qTags"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDimCellType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDimensionType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDownloadInfo:
    """

    Attributes
    ----------
    qUrl: str
      URL to download the reduced app on.
    qFileSize: int
      The filesize of the reduced app.
    """

    qUrl: str = None
    qFileSize: int = -1

    def __init__(self_, **kvargs):
        if "qUrl" in kvargs:
            if type(kvargs["qUrl"]).__name__ is self_.__annotations__["qUrl"]:
                self_.qUrl = kvargs["qUrl"]
            else:
                self_.qUrl = kvargs["qUrl"]
        if "qFileSize" in kvargs:
            if type(kvargs["qFileSize"]).__name__ is self_.__annotations__["qFileSize"]:
                self_.qFileSize = kvargs["qFileSize"]
            else:
                self_.qFileSize = kvargs["qFileSize"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDownloadOptions:
    """

    Attributes
    ----------
    qBookmarkId: str
      Bookmark Id to apply before reducing the application.
    qExpires: int
      Time in seconds for how long the download link is valid.
    qServeOnce: bool
    """

    qBookmarkId: str = None
    qExpires: int = 3600
    qServeOnce: bool = None

    def __init__(self_, **kvargs):
        if "qBookmarkId" in kvargs:
            if (
                type(kvargs["qBookmarkId"]).__name__
                is self_.__annotations__["qBookmarkId"]
            ):
                self_.qBookmarkId = kvargs["qBookmarkId"]
            else:
                self_.qBookmarkId = kvargs["qBookmarkId"]
        if "qExpires" in kvargs:
            if type(kvargs["qExpires"]).__name__ is self_.__annotations__["qExpires"]:
                self_.qExpires = kvargs["qExpires"]
            else:
                self_.qExpires = kvargs["qExpires"]
        if "qServeOnce" in kvargs:
            if (
                type(kvargs["qServeOnce"]).__name__
                is self_.__annotations__["qServeOnce"]
            ):
                self_.qServeOnce = kvargs["qServeOnce"]
            else:
                self_.qServeOnce = kvargs["qServeOnce"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxEngineVersion:
    """

    Attributes
    ----------
    qComponentVersion: str
      Version number of the Qlik engine component.
    """

    qComponentVersion: str = None

    def __init__(self_, **kvargs):
        if "qComponentVersion" in kvargs:
            if (
                type(kvargs["qComponentVersion"]).__name__
                is self_.__annotations__["qComponentVersion"]
            ):
                self_.qComponentVersion = kvargs["qComponentVersion"]
            else:
                self_.qComponentVersion = kvargs["qComponentVersion"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxExportFileType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxExportState:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFeature:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFieldProperties:
    """

    Attributes
    ----------
    qOneAndOnlyOne: bool
      This parameter is set to true, if the field has one and only one selection (not 0 and not more than 1).
      If this property is set to true, the field cannot be cleared anymore and no more selections can be performed in that field.
      The property OneAndOnlyOne can be set to true if one and only value has been selected in the field prior to setting the property.
    """

    qOneAndOnlyOne: bool = None

    def __init__(self_, **kvargs):
        if "qOneAndOnlyOne" in kvargs:
            if (
                type(kvargs["qOneAndOnlyOne"]).__name__
                is self_.__annotations__["qOneAndOnlyOne"]
            ):
                self_.qOneAndOnlyOne = kvargs["qOneAndOnlyOne"]
            else:
                self_.qOneAndOnlyOne = kvargs["qOneAndOnlyOne"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFieldSelectionMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFieldTableResourceId:
    """

    Attributes
    ----------
    qTable: str
      Name of the table that the field belongs to get the resource id for
    qResourceId: str
      Resource identifier for the field
    """

    qTable: str = None
    qResourceId: str = None

    def __init__(self_, **kvargs):
        if "qTable" in kvargs:
            if type(kvargs["qTable"]).__name__ is self_.__annotations__["qTable"]:
                self_.qTable = kvargs["qTable"]
            else:
                self_.qTable = kvargs["qTable"]
        if "qResourceId" in kvargs:
            if (
                type(kvargs["qResourceId"]).__name__
                is self_.__annotations__["qResourceId"]
            ):
                self_.qResourceId = kvargs["qResourceId"]
            else:
                self_.qResourceId = kvargs["qResourceId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFrequencyMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxGetBookmarkOptions:
    """

    Attributes
    ----------
    qTypes: list[str]
      List of object types.
    qData: JsonObject
      Set of data.
    """

    qTypes: list[str] = None
    qData: JsonObject = None

    def __init__(self_, **kvargs):
        if "qTypes" in kvargs:
            if type(kvargs["qTypes"]).__name__ is self_.__annotations__["qTypes"]:
                self_.qTypes = kvargs["qTypes"]
            else:
                self_.qTypes = kvargs["qTypes"]
        if "qData" in kvargs:
            if type(kvargs["qData"]).__name__ is self_.__annotations__["qData"]:
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(**kvargs["qData"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxGetObjectOptions:
    """

    Attributes
    ----------
    qTypes: list[str]
      List of object types.
    qIncludeSessionObjects: bool
      Set to true to include session objects.
      The default value is false.
    qData: JsonObject
      Set of data.
    """

    qTypes: list[str] = None
    qIncludeSessionObjects: bool = None
    qData: JsonObject = None

    def __init__(self_, **kvargs):
        if "qTypes" in kvargs:
            if type(kvargs["qTypes"]).__name__ is self_.__annotations__["qTypes"]:
                self_.qTypes = kvargs["qTypes"]
            else:
                self_.qTypes = kvargs["qTypes"]
        if "qIncludeSessionObjects" in kvargs:
            if (
                type(kvargs["qIncludeSessionObjects"]).__name__
                is self_.__annotations__["qIncludeSessionObjects"]
            ):
                self_.qIncludeSessionObjects = kvargs["qIncludeSessionObjects"]
            else:
                self_.qIncludeSessionObjects = kvargs["qIncludeSessionObjects"]
        if "qData" in kvargs:
            if type(kvargs["qData"]).__name__ is self_.__annotations__["qData"]:
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(**kvargs["qData"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxGroupTail:
    """

    Attributes
    ----------
    qUp: int
      Number of elements that are part of the previous tail.
      This number depends on the paging, more particularly it depends on the values defined in qTop and qHeight .
      Is not shown if the value is 0.
      This parameter is optional.
    qDown: int
      Number of elements that are part of the next tail.
      This number depends on the paging, more particularly it depends on the values defined in qTop and qHeight
      Is not shown if the value is 0.
      This parameter is optional.
    """

    qUp: int = None
    qDown: int = None

    def __init__(self_, **kvargs):
        if "qUp" in kvargs:
            if type(kvargs["qUp"]).__name__ is self_.__annotations__["qUp"]:
                self_.qUp = kvargs["qUp"]
            else:
                self_.qUp = kvargs["qUp"]
        if "qDown" in kvargs:
            if type(kvargs["qDown"]).__name__ is self_.__annotations__["qDown"]:
                self_.qDown = kvargs["qDown"]
            else:
                self_.qDown = kvargs["qDown"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxGrpType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxHighlightRanges:
    """

    Attributes
    ----------
    qRanges: list[CharRange]
      Ranges of highlighted values.
    """

    qRanges: list[CharRange] = None

    def __init__(self_, **kvargs):
        if "qRanges" in kvargs:
            if type(kvargs["qRanges"]).__name__ is self_.__annotations__["qRanges"]:
                self_.qRanges = kvargs["qRanges"]
            else:
                self_.qRanges = [CharRange(**e) for e in kvargs["qRanges"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxHypercubeMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxInfo:
    """

    Attributes
    ----------
    qId: str
      Identifier of the object.
      If the chosen identifier is already in use, the engine automatically sets another one.
      If an identifier is not set, the engine automatically sets one.
      This parameter is optional.
    qType: str
      Type of the object.
      This parameter is mandatory.
    """

    qId: str = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs:
            if type(kvargs["qId"]).__name__ is self_.__annotations__["qId"]:
                self_.qId = kvargs["qId"]
            else:
                self_.qId = kvargs["qId"]
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxInlineMeasureDef:
    """

    Attributes
    ----------
    qLabel: str
      Name of the measure.
      An empty string is returned as a default value.
      This parameter is optional.
    qDescription: str
      Description of the measure.
      An empty string is returned as a default value.
      This parameter is optional.
    qTags: list[str]
      Name connected to the measure that is used for search purposes.
      A measure can have several tags.
      This parameter is optional.
    qGrouping: str
      Default value is no grouping.
      This parameter is optional.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qDef: str
      Definition of the expression in the measure.
      Example: Sum (OrderTotal)
      This parameter is mandatory.
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    qRelative: bool
      If set to true, percentage values are returned instead of absolute numbers.
      Default value is false.
      This parameter is optional.
    qBrutalSum: bool
      If set to true, the sum of rows total should be used rather than real expression total.
      This parameter is optional and applies to straight tables.
      Default value is false.
      If using the Qlik Sense interface, it means that the total mode is set to Expression Total .
    qAggrFunc: str
      Aggregate function.
      For more information on the aggregate function syntax, see the section Working with Qlik Sense on the online help portal.
      The default value is 0 (Sum of rows)
      This parameter is optional.
    qAccumulate: int
      * 0 means no accumulation

      • 1 means full accumulation (each y-value accumulates all previous y-values of the expression)

      • ≥ 2 means accumulate as many steps as the qAccumulate value
      Default value is 0.
      This parameter is optional.
    qReverseSort: bool
      If set to true, it inverts the sort criteria in the field.
    qActiveExpression: int
      Index of the active expression in a cyclic measure. The indexing starts from 0.
      The default value is 0.
      This parameter is optional.
    qExpressions: list[str]
      Array of expressions. This parameter is used in case of cyclic measures ( qGrouping is C). List of the expressions in the cyclic group.
    qLabelExpression: str
      Label expression.
      This parameter is optional.
    """

    qLabel: str = None
    qDescription: str = None
    qTags: list[str] = None
    qGrouping: str = None
    qDef: str = None
    qNumFormat: FieldAttributes = None
    qRelative: bool = None
    qBrutalSum: bool = None
    qAggrFunc: str = None
    qAccumulate: int = None
    qReverseSort: bool = None
    qActiveExpression: int = None
    qExpressions: list[str] = None
    qLabelExpression: str = None

    def __init__(self_, **kvargs):
        if "qLabel" in kvargs:
            if type(kvargs["qLabel"]).__name__ is self_.__annotations__["qLabel"]:
                self_.qLabel = kvargs["qLabel"]
            else:
                self_.qLabel = kvargs["qLabel"]
        if "qDescription" in kvargs:
            if (
                type(kvargs["qDescription"]).__name__
                is self_.__annotations__["qDescription"]
            ):
                self_.qDescription = kvargs["qDescription"]
            else:
                self_.qDescription = kvargs["qDescription"]
        if "qTags" in kvargs:
            if type(kvargs["qTags"]).__name__ is self_.__annotations__["qTags"]:
                self_.qTags = kvargs["qTags"]
            else:
                self_.qTags = kvargs["qTags"]
        if "qGrouping" in kvargs:
            if type(kvargs["qGrouping"]).__name__ is self_.__annotations__["qGrouping"]:
                self_.qGrouping = kvargs["qGrouping"]
            else:
                self_.qGrouping = kvargs["qGrouping"]
        if "qDef" in kvargs:
            if type(kvargs["qDef"]).__name__ is self_.__annotations__["qDef"]:
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = kvargs["qDef"]
        if "qNumFormat" in kvargs:
            if (
                type(kvargs["qNumFormat"]).__name__
                is self_.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(**kvargs["qNumFormat"])
        if "qRelative" in kvargs:
            if type(kvargs["qRelative"]).__name__ is self_.__annotations__["qRelative"]:
                self_.qRelative = kvargs["qRelative"]
            else:
                self_.qRelative = kvargs["qRelative"]
        if "qBrutalSum" in kvargs:
            if (
                type(kvargs["qBrutalSum"]).__name__
                is self_.__annotations__["qBrutalSum"]
            ):
                self_.qBrutalSum = kvargs["qBrutalSum"]
            else:
                self_.qBrutalSum = kvargs["qBrutalSum"]
        if "qAggrFunc" in kvargs:
            if type(kvargs["qAggrFunc"]).__name__ is self_.__annotations__["qAggrFunc"]:
                self_.qAggrFunc = kvargs["qAggrFunc"]
            else:
                self_.qAggrFunc = kvargs["qAggrFunc"]
        if "qAccumulate" in kvargs:
            if (
                type(kvargs["qAccumulate"]).__name__
                is self_.__annotations__["qAccumulate"]
            ):
                self_.qAccumulate = kvargs["qAccumulate"]
            else:
                self_.qAccumulate = kvargs["qAccumulate"]
        if "qReverseSort" in kvargs:
            if (
                type(kvargs["qReverseSort"]).__name__
                is self_.__annotations__["qReverseSort"]
            ):
                self_.qReverseSort = kvargs["qReverseSort"]
            else:
                self_.qReverseSort = kvargs["qReverseSort"]
        if "qActiveExpression" in kvargs:
            if (
                type(kvargs["qActiveExpression"]).__name__
                is self_.__annotations__["qActiveExpression"]
            ):
                self_.qActiveExpression = kvargs["qActiveExpression"]
            else:
                self_.qActiveExpression = kvargs["qActiveExpression"]
        if "qExpressions" in kvargs:
            if (
                type(kvargs["qExpressions"]).__name__
                is self_.__annotations__["qExpressions"]
            ):
                self_.qExpressions = kvargs["qExpressions"]
            else:
                self_.qExpressions = kvargs["qExpressions"]
        if "qLabelExpression" in kvargs:
            if (
                type(kvargs["qLabelExpression"]).__name__
                is self_.__annotations__["qLabelExpression"]
            ):
                self_.qLabelExpression = kvargs["qLabelExpression"]
            else:
                self_.qLabelExpression = kvargs["qLabelExpression"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLTrendlineType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLayoutErrors:
    """

    Attributes
    ----------
    qErrorCode: int
      Error code.
    """

    qErrorCode: int = None

    def __init__(self_, **kvargs):
        if "qErrorCode" in kvargs:
            if (
                type(kvargs["qErrorCode"]).__name__
                is self_.__annotations__["qErrorCode"]
            ):
                self_.qErrorCode = kvargs["qErrorCode"]
            else:
                self_.qErrorCode = kvargs["qErrorCode"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLibraryDimension:
    """

    Attributes
    ----------
    qGrouping: str
      Information about the grouping.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qFieldDefs: list[str]
      Array of dimension names.
    qFieldLabels: list[str]
      Array of dimension labels.
    qLabelExpression: str
    """

    qGrouping: str = None
    qFieldDefs: list[str] = None
    qFieldLabels: list[str] = None
    qLabelExpression: str = None

    def __init__(self_, **kvargs):
        if "qGrouping" in kvargs:
            if type(kvargs["qGrouping"]).__name__ is self_.__annotations__["qGrouping"]:
                self_.qGrouping = kvargs["qGrouping"]
            else:
                self_.qGrouping = kvargs["qGrouping"]
        if "qFieldDefs" in kvargs:
            if (
                type(kvargs["qFieldDefs"]).__name__
                is self_.__annotations__["qFieldDefs"]
            ):
                self_.qFieldDefs = kvargs["qFieldDefs"]
            else:
                self_.qFieldDefs = kvargs["qFieldDefs"]
        if "qFieldLabels" in kvargs:
            if (
                type(kvargs["qFieldLabels"]).__name__
                is self_.__annotations__["qFieldLabels"]
            ):
                self_.qFieldLabels = kvargs["qFieldLabels"]
            else:
                self_.qFieldLabels = kvargs["qFieldLabels"]
        if "qLabelExpression" in kvargs:
            if (
                type(kvargs["qLabelExpression"]).__name__
                is self_.__annotations__["qLabelExpression"]
            ):
                self_.qLabelExpression = kvargs["qLabelExpression"]
            else:
                self_.qLabelExpression = kvargs["qLabelExpression"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLibraryDimensionDef:
    """

    Attributes
    ----------
    qGrouping: str
      Information about the grouping.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qFieldDefs: list[str]
      Array of dimension names.
    qFieldLabels: list[str]
      Array of dimension labels.
    qLabelExpression: str
    """

    qGrouping: str = None
    qFieldDefs: list[str] = None
    qFieldLabels: list[str] = None
    qLabelExpression: str = None

    def __init__(self_, **kvargs):
        if "qGrouping" in kvargs:
            if type(kvargs["qGrouping"]).__name__ is self_.__annotations__["qGrouping"]:
                self_.qGrouping = kvargs["qGrouping"]
            else:
                self_.qGrouping = kvargs["qGrouping"]
        if "qFieldDefs" in kvargs:
            if (
                type(kvargs["qFieldDefs"]).__name__
                is self_.__annotations__["qFieldDefs"]
            ):
                self_.qFieldDefs = kvargs["qFieldDefs"]
            else:
                self_.qFieldDefs = kvargs["qFieldDefs"]
        if "qFieldLabels" in kvargs:
            if (
                type(kvargs["qFieldLabels"]).__name__
                is self_.__annotations__["qFieldLabels"]
            ):
                self_.qFieldLabels = kvargs["qFieldLabels"]
            else:
                self_.qFieldLabels = kvargs["qFieldLabels"]
        if "qLabelExpression" in kvargs:
            if (
                type(kvargs["qLabelExpression"]).__name__
                is self_.__annotations__["qLabelExpression"]
            ):
                self_.qLabelExpression = kvargs["qLabelExpression"]
            else:
                self_.qLabelExpression = kvargs["qLabelExpression"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLibraryMeasure:
    """
    Information about the library measure. Is the layout for NxLibraryMeasureDef.

    Attributes
    ----------
    qLabel: str
    qDef: str
    qGrouping: str
      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qExpressions: list[str]
    qActiveExpression: int
    qLabelExpression: str
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    """

    qLabel: str = None
    qDef: str = None
    qGrouping: str = None
    qExpressions: list[str] = None
    qActiveExpression: int = None
    qLabelExpression: str = None
    qNumFormat: FieldAttributes = None

    def __init__(self_, **kvargs):
        if "qLabel" in kvargs:
            if type(kvargs["qLabel"]).__name__ is self_.__annotations__["qLabel"]:
                self_.qLabel = kvargs["qLabel"]
            else:
                self_.qLabel = kvargs["qLabel"]
        if "qDef" in kvargs:
            if type(kvargs["qDef"]).__name__ is self_.__annotations__["qDef"]:
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = kvargs["qDef"]
        if "qGrouping" in kvargs:
            if type(kvargs["qGrouping"]).__name__ is self_.__annotations__["qGrouping"]:
                self_.qGrouping = kvargs["qGrouping"]
            else:
                self_.qGrouping = kvargs["qGrouping"]
        if "qExpressions" in kvargs:
            if (
                type(kvargs["qExpressions"]).__name__
                is self_.__annotations__["qExpressions"]
            ):
                self_.qExpressions = kvargs["qExpressions"]
            else:
                self_.qExpressions = kvargs["qExpressions"]
        if "qActiveExpression" in kvargs:
            if (
                type(kvargs["qActiveExpression"]).__name__
                is self_.__annotations__["qActiveExpression"]
            ):
                self_.qActiveExpression = kvargs["qActiveExpression"]
            else:
                self_.qActiveExpression = kvargs["qActiveExpression"]
        if "qLabelExpression" in kvargs:
            if (
                type(kvargs["qLabelExpression"]).__name__
                is self_.__annotations__["qLabelExpression"]
            ):
                self_.qLabelExpression = kvargs["qLabelExpression"]
            else:
                self_.qLabelExpression = kvargs["qLabelExpression"]
        if "qNumFormat" in kvargs:
            if (
                type(kvargs["qNumFormat"]).__name__
                is self_.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(**kvargs["qNumFormat"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLibraryMeasureDef:
    """

    Attributes
    ----------
    qLabel: str
      Label of the measure.
    qDef: str
      Definition of the measure.
    qGrouping: str
      Used to define a cyclic group or drill-down group.
      Default value is no grouping.
      This parameter is optional.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qExpressions: list[str]
      Array of expressions.
    qActiveExpression: int
      Index to the active expression in a measure.
    qLabelExpression: str
      Optional expression used for dynamic label.
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    """

    qLabel: str = None
    qDef: str = None
    qGrouping: str = None
    qExpressions: list[str] = None
    qActiveExpression: int = None
    qLabelExpression: str = None
    qNumFormat: FieldAttributes = None

    def __init__(self_, **kvargs):
        if "qLabel" in kvargs:
            if type(kvargs["qLabel"]).__name__ is self_.__annotations__["qLabel"]:
                self_.qLabel = kvargs["qLabel"]
            else:
                self_.qLabel = kvargs["qLabel"]
        if "qDef" in kvargs:
            if type(kvargs["qDef"]).__name__ is self_.__annotations__["qDef"]:
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = kvargs["qDef"]
        if "qGrouping" in kvargs:
            if type(kvargs["qGrouping"]).__name__ is self_.__annotations__["qGrouping"]:
                self_.qGrouping = kvargs["qGrouping"]
            else:
                self_.qGrouping = kvargs["qGrouping"]
        if "qExpressions" in kvargs:
            if (
                type(kvargs["qExpressions"]).__name__
                is self_.__annotations__["qExpressions"]
            ):
                self_.qExpressions = kvargs["qExpressions"]
            else:
                self_.qExpressions = kvargs["qExpressions"]
        if "qActiveExpression" in kvargs:
            if (
                type(kvargs["qActiveExpression"]).__name__
                is self_.__annotations__["qActiveExpression"]
            ):
                self_.qActiveExpression = kvargs["qActiveExpression"]
            else:
                self_.qActiveExpression = kvargs["qActiveExpression"]
        if "qLabelExpression" in kvargs:
            if (
                type(kvargs["qLabelExpression"]).__name__
                is self_.__annotations__["qLabelExpression"]
            ):
                self_.qLabelExpression = kvargs["qLabelExpression"]
            else:
                self_.qLabelExpression = kvargs["qLabelExpression"]
        if "qNumFormat" in kvargs:
            if (
                type(kvargs["qNumFormat"]).__name__
                is self_.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(**kvargs["qNumFormat"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLinkedObjectInfo:
    """

    Attributes
    ----------
    qRootId: str
      Identifier of the root object.
      If the linked object is a child, the root identifier is the identifier of the parent.
      If the linked object is an app object, the root identifier is the same than the identifier of the linked object since the linked object is a root object.
    qInfo: NxInfo
      Information about the linked object.
    """

    qRootId: str = None
    qInfo: NxInfo = None

    def __init__(self_, **kvargs):
        if "qRootId" in kvargs:
            if type(kvargs["qRootId"]).__name__ is self_.__annotations__["qRootId"]:
                self_.qRootId = kvargs["qRootId"]
            else:
                self_.qRootId = kvargs["qRootId"]
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxListObjectExpression:
    """

    Attributes
    ----------
    qExpr: str
      Value of the expression.
    qError: NxLayoutErrors
      Gives information on the error.
      This parameter is optional.
    """

    qExpr: str = None
    qError: NxLayoutErrors = None

    def __init__(self_, **kvargs):
        if "qExpr" in kvargs:
            if type(kvargs["qExpr"]).__name__ is self_.__annotations__["qExpr"]:
                self_.qExpr = kvargs["qExpr"]
            else:
                self_.qExpr = kvargs["qExpr"]
        if "qError" in kvargs:
            if type(kvargs["qError"]).__name__ is self_.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxLayoutErrors(**kvargs["qError"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxListObjectExpressionDef:
    """

    Attributes
    ----------
    qExpr: str
      Value of the expression.
    qLibraryId: str
      Refers to an expression stored in the library.
    """

    qExpr: str = None
    qLibraryId: str = None

    def __init__(self_, **kvargs):
        if "qExpr" in kvargs:
            if type(kvargs["qExpr"]).__name__ is self_.__annotations__["qExpr"]:
                self_.qExpr = kvargs["qExpr"]
            else:
                self_.qExpr = kvargs["qExpr"]
        if "qLibraryId" in kvargs:
            if (
                type(kvargs["qLibraryId"]).__name__
                is self_.__annotations__["qLibraryId"]
            ):
                self_.qLibraryId = kvargs["qLibraryId"]
            else:
                self_.qLibraryId = kvargs["qLibraryId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLocalizedErrorCode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLocalizedWarningCode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMatchingFieldInfo:
    """

    Attributes
    ----------
    qName: str
      Name of the field.
    qTags: list[str]
      List of tags.
    """

    qName: str = None
    qTags: list[str] = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qTags" in kvargs:
            if type(kvargs["qTags"]).__name__ is self_.__annotations__["qTags"]:
                self_.qTags = kvargs["qTags"]
            else:
                self_.qTags = kvargs["qTags"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMatchingFieldMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMeta:
    """
    Layout for NxMetaDef.

    Attributes
    ----------
    qName: str
      Name.
      This property is optional.
    """

    qName: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMetaDef:
    """
    Used to collect meta data.

    Properties:

    Semantic type with an empty structure.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPage:
    """

    Attributes
    ----------
    qLeft: int
      Position from the left.
      Corresponds to the first column.
    qTop: int
      Position from the top.
      Corresponds to the first row.
    qWidth: int
      Number of columns in the page. The indexing of the columns may vary depending on whether the cells are expanded or not (parameter qAlwaysFullyExpanded in HyperCubeDef ).
    qHeight: int
      Number of rows or elements in the page. The indexing of the rows may vary depending on whether the cells are expanded or not (parameter qAlwaysFullyExpanded in HyperCubeDef ).
    """

    qLeft: int = None
    qTop: int = None
    qWidth: int = None
    qHeight: int = None

    def __init__(self_, **kvargs):
        if "qLeft" in kvargs:
            if type(kvargs["qLeft"]).__name__ is self_.__annotations__["qLeft"]:
                self_.qLeft = kvargs["qLeft"]
            else:
                self_.qLeft = kvargs["qLeft"]
        if "qTop" in kvargs:
            if type(kvargs["qTop"]).__name__ is self_.__annotations__["qTop"]:
                self_.qTop = kvargs["qTop"]
            else:
                self_.qTop = kvargs["qTop"]
        if "qWidth" in kvargs:
            if type(kvargs["qWidth"]).__name__ is self_.__annotations__["qWidth"]:
                self_.qWidth = kvargs["qWidth"]
            else:
                self_.qWidth = kvargs["qWidth"]
        if "qHeight" in kvargs:
            if type(kvargs["qHeight"]).__name__ is self_.__annotations__["qHeight"]:
                self_.qHeight = kvargs["qHeight"]
            else:
                self_.qHeight = kvargs["qHeight"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPageTreeLevel:
    """

    Attributes
    ----------
    qLeft: int
      The first dimension that is to be part of the tree, counted from the left. For example, if qLeft is equal to 1, omit nodes from the first dimension in the current sort order.
    qDepth: int
      Number of dimensions to include in the tree.
    """

    qLeft: int = None
    qDepth: int = -1

    def __init__(self_, **kvargs):
        if "qLeft" in kvargs:
            if type(kvargs["qLeft"]).__name__ is self_.__annotations__["qLeft"]:
                self_.qLeft = kvargs["qLeft"]
            else:
                self_.qLeft = kvargs["qLeft"]
        if "qDepth" in kvargs:
            if type(kvargs["qDepth"]).__name__ is self_.__annotations__["qDepth"]:
                self_.qDepth = kvargs["qDepth"]
            else:
                self_.qDepth = kvargs["qDepth"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPatchOperationType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxRange:
    """

    Attributes
    ----------
    qFrom: int
      Position in the expression of the first character of the field name.
    qCount: int
      Number of characters in the field name.
    """

    qFrom: int = None
    qCount: int = None

    def __init__(self_, **kvargs):
        if "qFrom" in kvargs:
            if type(kvargs["qFrom"]).__name__ is self_.__annotations__["qFrom"]:
                self_.qFrom = kvargs["qFrom"]
            else:
                self_.qFrom = kvargs["qFrom"]
        if "qCount" in kvargs:
            if type(kvargs["qCount"]).__name__ is self_.__annotations__["qCount"]:
                self_.qCount = kvargs["qCount"]
            else:
                self_.qCount = kvargs["qCount"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxSelectionCellType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxSelectionInfo:
    """

    Attributes
    ----------
    qInSelections: bool
      Is set to true if the visualization is in selection mode.
      For more information about the selection mode, see BeginSelections Method.
    qMadeSelections: bool
      Is set to true if the visualization is in selection mode and if some selections have been made while in selection mode.
      For more information about the selection mode, see BeginSelections Method.
    """

    qInSelections: bool = None
    qMadeSelections: bool = None

    def __init__(self_, **kvargs):
        if "qInSelections" in kvargs:
            if (
                type(kvargs["qInSelections"]).__name__
                is self_.__annotations__["qInSelections"]
            ):
                self_.qInSelections = kvargs["qInSelections"]
            else:
                self_.qInSelections = kvargs["qInSelections"]
        if "qMadeSelections" in kvargs:
            if (
                type(kvargs["qMadeSelections"]).__name__
                is self_.__annotations__["qMadeSelections"]
            ):
                self_.qMadeSelections = kvargs["qMadeSelections"]
            else:
                self_.qMadeSelections = kvargs["qMadeSelections"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxSimpleDimValue:
    """

    Attributes
    ----------
    qText: str
      Text related to the attribute expression value.
      This property is optional. No text is returned if the attribute expression value is a numeric.
    qElemNo: int
      Element number.
    """

    qText: str = None
    qElemNo: int = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qElemNo" in kvargs:
            if type(kvargs["qElemNo"]).__name__ is self_.__annotations__["qElemNo"]:
                self_.qElemNo = kvargs["qElemNo"]
            else:
                self_.qElemNo = kvargs["qElemNo"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxSimpleValue:
    """

    Attributes
    ----------
    qText: str
      Text related to the attribute expression value.
    qNum: float
      Numeric value of the attribute expression.
      Set to NaN (Not a Number) if the attribute expression value is not numeric.
    """

    qText: str = None
    qNum: float = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qNum" in kvargs:
            if type(kvargs["qNum"]).__name__ is self_.__annotations__["qNum"]:
                self_.qNum = kvargs["qNum"]
            else:
                self_.qNum = kvargs["qNum"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxSortIndicatorType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxStateCounts:
    """

    Attributes
    ----------
    qLocked: int
      Number of values in locked state.
    qSelected: int
      Number of values in selected state.
    qOption: int
      Number of values in optional state.
    qDeselected: int
      Number of values in deselected state.
    qAlternative: int
      Number of values in alternative state.
    qExcluded: int
      Number of values in excluded state.
    qSelectedExcluded: int
      Number of values in selected excluded state.
    qLockedExcluded: int
      Number of values in locked excluded state.
    """

    qLocked: int = None
    qSelected: int = None
    qOption: int = None
    qDeselected: int = None
    qAlternative: int = None
    qExcluded: int = None
    qSelectedExcluded: int = None
    qLockedExcluded: int = None

    def __init__(self_, **kvargs):
        if "qLocked" in kvargs:
            if type(kvargs["qLocked"]).__name__ is self_.__annotations__["qLocked"]:
                self_.qLocked = kvargs["qLocked"]
            else:
                self_.qLocked = kvargs["qLocked"]
        if "qSelected" in kvargs:
            if type(kvargs["qSelected"]).__name__ is self_.__annotations__["qSelected"]:
                self_.qSelected = kvargs["qSelected"]
            else:
                self_.qSelected = kvargs["qSelected"]
        if "qOption" in kvargs:
            if type(kvargs["qOption"]).__name__ is self_.__annotations__["qOption"]:
                self_.qOption = kvargs["qOption"]
            else:
                self_.qOption = kvargs["qOption"]
        if "qDeselected" in kvargs:
            if (
                type(kvargs["qDeselected"]).__name__
                is self_.__annotations__["qDeselected"]
            ):
                self_.qDeselected = kvargs["qDeselected"]
            else:
                self_.qDeselected = kvargs["qDeselected"]
        if "qAlternative" in kvargs:
            if (
                type(kvargs["qAlternative"]).__name__
                is self_.__annotations__["qAlternative"]
            ):
                self_.qAlternative = kvargs["qAlternative"]
            else:
                self_.qAlternative = kvargs["qAlternative"]
        if "qExcluded" in kvargs:
            if type(kvargs["qExcluded"]).__name__ is self_.__annotations__["qExcluded"]:
                self_.qExcluded = kvargs["qExcluded"]
            else:
                self_.qExcluded = kvargs["qExcluded"]
        if "qSelectedExcluded" in kvargs:
            if (
                type(kvargs["qSelectedExcluded"]).__name__
                is self_.__annotations__["qSelectedExcluded"]
            ):
                self_.qSelectedExcluded = kvargs["qSelectedExcluded"]
            else:
                self_.qSelectedExcluded = kvargs["qSelectedExcluded"]
        if "qLockedExcluded" in kvargs:
            if (
                type(kvargs["qLockedExcluded"]).__name__
                is self_.__annotations__["qLockedExcluded"]
            ):
                self_.qLockedExcluded = kvargs["qLockedExcluded"]
            else:
                self_.qLockedExcluded = kvargs["qLockedExcluded"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxStreamListEntry:
    """
    This struct is deprecated (not recommended to use).

    Attributes
    ----------
    qName: str
      Name of the stream.
    qId: str
      Identifier of the stream.
    """

    qName: str = None
    qId: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qId" in kvargs:
            if type(kvargs["qId"]).__name__ is self_.__annotations__["qId"]:
                self_.qId = kvargs["qId"]
            else:
                self_.qId = kvargs["qId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTickCell:
    """

    Attributes
    ----------
    qText: str
      Tick's label.
    qStart: float
      Start value.
    qEnd: float
      End value.
    """

    qText: str = None
    qStart: float = None
    qEnd: float = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qStart" in kvargs:
            if type(kvargs["qStart"]).__name__ is self_.__annotations__["qStart"]:
                self_.qStart = kvargs["qStart"]
            else:
                self_.qStart = kvargs["qStart"]
        if "qEnd" in kvargs:
            if type(kvargs["qEnd"]).__name__ is self_.__annotations__["qEnd"]:
                self_.qEnd = kvargs["qEnd"]
            else:
                self_.qEnd = kvargs["qEnd"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTrendlineMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxValidationError:
    """

    Attributes
    ----------
    qErrorCode: int
      Error code.
      This parameter is always displayed in case of error.
    qContext: str
      Context related to the error, from the user app domain.
      It can be the identifier of an object, a field name, a table name.
      This parameter is optional.
    qExtendedMessage: str
      Internal information from the server.
      This parameter is optional.
    """

    qErrorCode: int = None
    qContext: str = None
    qExtendedMessage: str = None

    def __init__(self_, **kvargs):
        if "qErrorCode" in kvargs:
            if (
                type(kvargs["qErrorCode"]).__name__
                is self_.__annotations__["qErrorCode"]
            ):
                self_.qErrorCode = kvargs["qErrorCode"]
            else:
                self_.qErrorCode = kvargs["qErrorCode"]
        if "qContext" in kvargs:
            if type(kvargs["qContext"]).__name__ is self_.__annotations__["qContext"]:
                self_.qContext = kvargs["qContext"]
            else:
                self_.qContext = kvargs["qContext"]
        if "qExtendedMessage" in kvargs:
            if (
                type(kvargs["qExtendedMessage"]).__name__
                is self_.__annotations__["qExtendedMessage"]
            ):
                self_.qExtendedMessage = kvargs["qExtendedMessage"]
            else:
                self_.qExtendedMessage = kvargs["qExtendedMessage"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxVariableListItem:
    """

    Attributes
    ----------
    qName: str
      Name of the variable.
    qDescription: str
      Description of the variable.
    qDefinition: str
      Definition of the variable. It can be a value or an expression.
    qIsConfig: bool
      If set to true, it means that the variable is a system variable.
      A system variable provides information about the system and is set by the engine. The content cannot be changed by the user.
      This parameter is optional.
      The default value is false.
    qIsReserved: bool
      If set to true, it means that the variable is reserved.
      The default value is false.
      This parameter is optional.
      Examples:

      • ScriptError is a reserved variable, set by the engine.

      • DayNames is a reserved variable, set by the user.
    qMeta: NxMeta
      Information about publishing and permissions.
      This parameter is optional.
    qInfo: NxInfo
      Identifier and type of the object.
      This parameter is mandatory.
    qData: JsonObject
      Data.
    qIsScriptCreated: bool
      If set to true, it means that the variable was defined via script.
    """

    qName: str = None
    qDescription: str = None
    qDefinition: str = None
    qIsConfig: bool = None
    qIsReserved: bool = None
    qMeta: NxMeta = None
    qInfo: NxInfo = None
    qData: JsonObject = None
    qIsScriptCreated: bool = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qDescription" in kvargs:
            if (
                type(kvargs["qDescription"]).__name__
                is self_.__annotations__["qDescription"]
            ):
                self_.qDescription = kvargs["qDescription"]
            else:
                self_.qDescription = kvargs["qDescription"]
        if "qDefinition" in kvargs:
            if (
                type(kvargs["qDefinition"]).__name__
                is self_.__annotations__["qDefinition"]
            ):
                self_.qDefinition = kvargs["qDefinition"]
            else:
                self_.qDefinition = kvargs["qDefinition"]
        if "qIsConfig" in kvargs:
            if type(kvargs["qIsConfig"]).__name__ is self_.__annotations__["qIsConfig"]:
                self_.qIsConfig = kvargs["qIsConfig"]
            else:
                self_.qIsConfig = kvargs["qIsConfig"]
        if "qIsReserved" in kvargs:
            if (
                type(kvargs["qIsReserved"]).__name__
                is self_.__annotations__["qIsReserved"]
            ):
                self_.qIsReserved = kvargs["qIsReserved"]
            else:
                self_.qIsReserved = kvargs["qIsReserved"]
        if "qMeta" in kvargs:
            if type(kvargs["qMeta"]).__name__ is self_.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(**kvargs["qMeta"])
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        if "qData" in kvargs:
            if type(kvargs["qData"]).__name__ is self_.__annotations__["qData"]:
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(**kvargs["qData"])
        if "qIsScriptCreated" in kvargs:
            if (
                type(kvargs["qIsScriptCreated"]).__name__
                is self_.__annotations__["qIsScriptCreated"]
            ):
                self_.qIsScriptCreated = kvargs["qIsScriptCreated"]
            else:
                self_.qIsScriptCreated = kvargs["qIsScriptCreated"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxVariableProperties:
    """

    Attributes
    ----------
    qName: str
      Name of the variable.
    qNumberPresentation: FieldAttributes
      Defines the format of the value of a variable.
    qIncludeInBookmark: bool
      Set this property to true to update the variable when applying a bookmark.
      The value of a variable can affect the state of the selections.
      The default value is false.
    qUsePredefListedValues: bool
      The value of a variable can be an enumeration.
      Set this property to true to reflect the predefined values in an enumeration.
    qPreDefinedList: list[str]
      List of enumerations.
      This property is used if qUsePredefListedValues is set to true.
    """

    qName: str = None
    qNumberPresentation: FieldAttributes = None
    qIncludeInBookmark: bool = None
    qUsePredefListedValues: bool = None
    qPreDefinedList: list[str] = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qNumberPresentation" in kvargs:
            if (
                type(kvargs["qNumberPresentation"]).__name__
                is self_.__annotations__["qNumberPresentation"]
            ):
                self_.qNumberPresentation = kvargs["qNumberPresentation"]
            else:
                self_.qNumberPresentation = FieldAttributes(
                    **kvargs["qNumberPresentation"]
                )
        if "qIncludeInBookmark" in kvargs:
            if (
                type(kvargs["qIncludeInBookmark"]).__name__
                is self_.__annotations__["qIncludeInBookmark"]
            ):
                self_.qIncludeInBookmark = kvargs["qIncludeInBookmark"]
            else:
                self_.qIncludeInBookmark = kvargs["qIncludeInBookmark"]
        if "qUsePredefListedValues" in kvargs:
            if (
                type(kvargs["qUsePredefListedValues"]).__name__
                is self_.__annotations__["qUsePredefListedValues"]
            ):
                self_.qUsePredefListedValues = kvargs["qUsePredefListedValues"]
            else:
                self_.qUsePredefListedValues = kvargs["qUsePredefListedValues"]
        if "qPreDefinedList" in kvargs:
            if (
                type(kvargs["qPreDefinedList"]).__name__
                is self_.__annotations__["qPreDefinedList"]
            ):
                self_.qPreDefinedList = kvargs["qPreDefinedList"]
            else:
                self_.qPreDefinedList = kvargs["qPreDefinedList"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxViewPort:
    """

    Attributes
    ----------
    qWidth: int
      Width of the canvas in pixels.
    qHeight: int
      Height of the canvas in pixels.
    qZoomLevel: int
      Zoom level.
    """

    qWidth: int = None
    qHeight: int = None
    qZoomLevel: int = None

    def __init__(self_, **kvargs):
        if "qWidth" in kvargs:
            if type(kvargs["qWidth"]).__name__ is self_.__annotations__["qWidth"]:
                self_.qWidth = kvargs["qWidth"]
            else:
                self_.qWidth = kvargs["qWidth"]
        if "qHeight" in kvargs:
            if type(kvargs["qHeight"]).__name__ is self_.__annotations__["qHeight"]:
                self_.qHeight = kvargs["qHeight"]
            else:
                self_.qHeight = kvargs["qHeight"]
        if "qZoomLevel" in kvargs:
            if (
                type(kvargs["qZoomLevel"]).__name__
                is self_.__annotations__["qZoomLevel"]
            ):
                self_.qZoomLevel = kvargs["qZoomLevel"]
            else:
                self_.qZoomLevel = kvargs["qZoomLevel"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ObjectInterface:
    """

    Attributes
    ----------
    qType: str
      The native type of the object.
    qHandle: int
      The handle used to connect to object.
    qGenericType: str
      The type of the object.
    qGenericId: str
      Object ID.
    """

    qType: str = None
    qHandle: int = None
    qGenericType: str = None
    qGenericId: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qHandle" in kvargs:
            if type(kvargs["qHandle"]).__name__ is self_.__annotations__["qHandle"]:
                self_.qHandle = kvargs["qHandle"]
            else:
                self_.qHandle = kvargs["qHandle"]
        if "qGenericType" in kvargs:
            if (
                type(kvargs["qGenericType"]).__name__
                is self_.__annotations__["qGenericType"]
            ):
                self_.qGenericType = kvargs["qGenericType"]
            else:
                self_.qGenericType = kvargs["qGenericType"]
        if "qGenericId" in kvargs:
            if (
                type(kvargs["qGenericId"]).__name__
                is self_.__annotations__["qGenericId"]
            ):
                self_.qGenericId = kvargs["qGenericId"]
            else:
                self_.qGenericId = kvargs["qGenericId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class OdbcDsn:
    """

    Attributes
    ----------
    qName: str
      Name of the ODBC connection.
    qDescription: str
      Description of the ODBC connection.
    qBit32: bool
      Is set to true if the version of ODBC is 32-bit.
      This parameter is optional. Default is false.
    qUserOnly: bool
      Is set to true if the connection is User DSN. The connection works only for a specific user.
      Default is false.
      This parameter is optional.
    """

    qName: str = None
    qDescription: str = None
    qBit32: bool = None
    qUserOnly: bool = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qDescription" in kvargs:
            if (
                type(kvargs["qDescription"]).__name__
                is self_.__annotations__["qDescription"]
            ):
                self_.qDescription = kvargs["qDescription"]
            else:
                self_.qDescription = kvargs["qDescription"]
        if "qBit32" in kvargs:
            if type(kvargs["qBit32"]).__name__ is self_.__annotations__["qBit32"]:
                self_.qBit32 = kvargs["qBit32"]
            else:
                self_.qBit32 = kvargs["qBit32"]
        if "qUserOnly" in kvargs:
            if type(kvargs["qUserOnly"]).__name__ is self_.__annotations__["qUserOnly"]:
                self_.qUserOnly = kvargs["qUserOnly"]
            else:
                self_.qUserOnly = kvargs["qUserOnly"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class OleDbProvider:
    """

    Attributes
    ----------
    qName: str
      Name of the OLEDB provider.
    qDescription: str
      Description of the OLEDB provider.
    qBit32: bool
      Is set to true if the version of the OLEDB provider is 32-bit.
      Default is false.
      This parameter is optional.
    """

    qName: str = None
    qDescription: str = None
    qBit32: bool = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qDescription" in kvargs:
            if (
                type(kvargs["qDescription"]).__name__
                is self_.__annotations__["qDescription"]
            ):
                self_.qDescription = kvargs["qDescription"]
            else:
                self_.qDescription = kvargs["qDescription"]
        if "qBit32" in kvargs:
            if type(kvargs["qBit32"]).__name__ is self_.__annotations__["qBit32"]:
                self_.qBit32 = kvargs["qBit32"]
            else:
                self_.qBit32 = kvargs["qBit32"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class OtherLimitMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class OtherMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class OtherSortMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Point:
    """

    Attributes
    ----------
    qx: int
      x-coordinate in pixels.
      The origin is the top left of the screen.
    qy: int
      y-coordinate in pixels.
      The origin is the top left of the screen.
    """

    qx: int = None
    qy: int = None

    def __init__(self_, **kvargs):
        if "qx" in kvargs:
            if type(kvargs["qx"]).__name__ is self_.__annotations__["qx"]:
                self_.qx = kvargs["qx"]
            else:
                self_.qx = kvargs["qx"]
        if "qy" in kvargs:
            if type(kvargs["qy"]).__name__ is self_.__annotations__["qy"]:
                self_.qy = kvargs["qy"]
            else:
                self_.qy = kvargs["qy"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class PositionMark:
    """

    Attributes
    ----------
    qDimName: str
    qElemNo: list[int]
    qElemValues: list[Blob]
    """

    qDimName: str = None
    qElemNo: list[int] = None
    qElemValues: list[Blob] = None

    def __init__(self_, **kvargs):
        if "qDimName" in kvargs:
            if type(kvargs["qDimName"]).__name__ is self_.__annotations__["qDimName"]:
                self_.qDimName = kvargs["qDimName"]
            else:
                self_.qDimName = kvargs["qDimName"]
        if "qElemNo" in kvargs:
            if type(kvargs["qElemNo"]).__name__ is self_.__annotations__["qElemNo"]:
                self_.qElemNo = kvargs["qElemNo"]
            else:
                self_.qElemNo = kvargs["qElemNo"]
        if "qElemValues" in kvargs:
            if (
                type(kvargs["qElemValues"]).__name__
                is self_.__annotations__["qElemValues"]
            ):
                self_.qElemValues = kvargs["qElemValues"]
            else:
                self_.qElemValues = [Blob(**e) for e in kvargs["qElemValues"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ProgressMessage:
    """

    Attributes
    ----------
    qMessageCode: int
      Code number to the corresponding localized message string.
    qMessageParameters: list[str]
      Parameters to be inserted in the localized message string.
    """

    qMessageCode: int = None
    qMessageParameters: list[str] = None

    def __init__(self_, **kvargs):
        if "qMessageCode" in kvargs:
            if (
                type(kvargs["qMessageCode"]).__name__
                is self_.__annotations__["qMessageCode"]
            ):
                self_.qMessageCode = kvargs["qMessageCode"]
            else:
                self_.qMessageCode = kvargs["qMessageCode"]
        if "qMessageParameters" in kvargs:
            if (
                type(kvargs["qMessageParameters"]).__name__
                is self_.__annotations__["qMessageParameters"]
            ):
                self_.qMessageParameters = kvargs["qMessageParameters"]
            else:
                self_.qMessageParameters = kvargs["qMessageParameters"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Range:
    """

    Attributes
    ----------
    qMin: float
      Lowest value in the range
    qMax: float
      Highest value in the range
    qMinInclEq: bool
      If set to true, the range includes the lowest value in the range of selections (Equals to ). [bn(50500)]
      Example:
      The range is [1,10]. If qMinInclEq is set to true it means that 1 is included in the range of selections.
    qMaxInclEq: bool
      If set to true, the range includes the highest value in the range of selections (Equals to ). [bn(50500)]
      Example:
      The range is [1,10]. If qMinInclEq is set to true it means that 10 is included in the range of selections.
    """

    qMin: float = None
    qMax: float = None
    qMinInclEq: bool = None
    qMaxInclEq: bool = None

    def __init__(self_, **kvargs):
        if "qMin" in kvargs:
            if type(kvargs["qMin"]).__name__ is self_.__annotations__["qMin"]:
                self_.qMin = kvargs["qMin"]
            else:
                self_.qMin = kvargs["qMin"]
        if "qMax" in kvargs:
            if type(kvargs["qMax"]).__name__ is self_.__annotations__["qMax"]:
                self_.qMax = kvargs["qMax"]
            else:
                self_.qMax = kvargs["qMax"]
        if "qMinInclEq" in kvargs:
            if (
                type(kvargs["qMinInclEq"]).__name__
                is self_.__annotations__["qMinInclEq"]
            ):
                self_.qMinInclEq = kvargs["qMinInclEq"]
            else:
                self_.qMinInclEq = kvargs["qMinInclEq"]
        if "qMaxInclEq" in kvargs:
            if (
                type(kvargs["qMaxInclEq"]).__name__
                is self_.__annotations__["qMaxInclEq"]
            ):
                self_.qMaxInclEq = kvargs["qMaxInclEq"]
            else:
                self_.qMaxInclEq = kvargs["qMaxInclEq"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class RangeSelectInfo:
    """

    Attributes
    ----------
    qRangeLo: float
      Lowest value in the range.
    qRangeHi: float
      Highest value in the range.
    qMeasure: str
      Label of the measure.
    """

    qRangeLo: float = -1e300
    qRangeHi: float = -1e300
    qMeasure: str = None

    def __init__(self_, **kvargs):
        if "qRangeLo" in kvargs:
            if type(kvargs["qRangeLo"]).__name__ is self_.__annotations__["qRangeLo"]:
                self_.qRangeLo = kvargs["qRangeLo"]
            else:
                self_.qRangeLo = kvargs["qRangeLo"]
        if "qRangeHi" in kvargs:
            if type(kvargs["qRangeHi"]).__name__ is self_.__annotations__["qRangeHi"]:
                self_.qRangeHi = kvargs["qRangeHi"]
            else:
                self_.qRangeHi = kvargs["qRangeHi"]
        if "qMeasure" in kvargs:
            if type(kvargs["qMeasure"]).__name__ is self_.__annotations__["qMeasure"]:
                self_.qMeasure = kvargs["qMeasure"]
            else:
                self_.qMeasure = kvargs["qMeasure"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Rect:
    """

    Attributes
    ----------
    qLeft: int
      Position from the left.
      Corresponds to the first column.
    qTop: int
      Position from the top.
      Corresponds to the first row.
    qWidth: int
      Number of columns in the page. The indexing of the columns may vary depending on whether the cells are expanded or not (parameter qAlwaysFullyExpanded in HyperCubeDef ).
    qHeight: int
      Number of rows or elements in the page. The indexing of the rows may vary depending on whether the cells are expanded or not (parameter qAlwaysFullyExpanded in HyperCubeDef ).
    """

    qLeft: int = None
    qTop: int = None
    qWidth: int = None
    qHeight: int = None

    def __init__(self_, **kvargs):
        if "qLeft" in kvargs:
            if type(kvargs["qLeft"]).__name__ is self_.__annotations__["qLeft"]:
                self_.qLeft = kvargs["qLeft"]
            else:
                self_.qLeft = kvargs["qLeft"]
        if "qTop" in kvargs:
            if type(kvargs["qTop"]).__name__ is self_.__annotations__["qTop"]:
                self_.qTop = kvargs["qTop"]
            else:
                self_.qTop = kvargs["qTop"]
        if "qWidth" in kvargs:
            if type(kvargs["qWidth"]).__name__ is self_.__annotations__["qWidth"]:
                self_.qWidth = kvargs["qWidth"]
            else:
                self_.qWidth = kvargs["qWidth"]
        if "qHeight" in kvargs:
            if type(kvargs["qHeight"]).__name__ is self_.__annotations__["qHeight"]:
                self_.qHeight = kvargs["qHeight"]
            else:
                self_.qHeight = kvargs["qHeight"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SampleResult:
    """

    Attributes
    ----------
    qFieldOrColumn: FieldOrColumn
      Name of field or column.
    qValues: list[FieldValue]
      Matched values part of the sample.
    """

    qFieldOrColumn: FieldOrColumn = None
    qValues: list[FieldValue] = None

    def __init__(self_, **kvargs):
        if "qFieldOrColumn" in kvargs:
            if (
                type(kvargs["qFieldOrColumn"]).__name__
                is self_.__annotations__["qFieldOrColumn"]
            ):
                self_.qFieldOrColumn = kvargs["qFieldOrColumn"]
            else:
                self_.qFieldOrColumn = FieldOrColumn(**kvargs["qFieldOrColumn"])
        if "qValues" in kvargs:
            if type(kvargs["qValues"]).__name__ is self_.__annotations__["qValues"]:
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [FieldValue(**e) for e in kvargs["qValues"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ScriptSyntaxError:
    """

    Attributes
    ----------
    qErrLen: int
      Length of the word where the error is located.
    qTabIx: int
      Number of the faulty section.
    qLineInTab: int
      Line number in the section where the error is located.
    qColInLine: int
      Position of the erroneous text from the beginning of the line.
    qTextPos: int
      Position of the erroneous text from the beginning of the script.
    qSecondaryFailure: bool
      The default value is false.
    """

    qErrLen: int = None
    qTabIx: int = None
    qLineInTab: int = None
    qColInLine: int = None
    qTextPos: int = None
    qSecondaryFailure: bool = None

    def __init__(self_, **kvargs):
        if "qErrLen" in kvargs:
            if type(kvargs["qErrLen"]).__name__ is self_.__annotations__["qErrLen"]:
                self_.qErrLen = kvargs["qErrLen"]
            else:
                self_.qErrLen = kvargs["qErrLen"]
        if "qTabIx" in kvargs:
            if type(kvargs["qTabIx"]).__name__ is self_.__annotations__["qTabIx"]:
                self_.qTabIx = kvargs["qTabIx"]
            else:
                self_.qTabIx = kvargs["qTabIx"]
        if "qLineInTab" in kvargs:
            if (
                type(kvargs["qLineInTab"]).__name__
                is self_.__annotations__["qLineInTab"]
            ):
                self_.qLineInTab = kvargs["qLineInTab"]
            else:
                self_.qLineInTab = kvargs["qLineInTab"]
        if "qColInLine" in kvargs:
            if (
                type(kvargs["qColInLine"]).__name__
                is self_.__annotations__["qColInLine"]
            ):
                self_.qColInLine = kvargs["qColInLine"]
            else:
                self_.qColInLine = kvargs["qColInLine"]
        if "qTextPos" in kvargs:
            if type(kvargs["qTextPos"]).__name__ is self_.__annotations__["qTextPos"]:
                self_.qTextPos = kvargs["qTextPos"]
            else:
                self_.qTextPos = kvargs["qTextPos"]
        if "qSecondaryFailure" in kvargs:
            if (
                type(kvargs["qSecondaryFailure"]).__name__
                is self_.__annotations__["qSecondaryFailure"]
            ):
                self_.qSecondaryFailure = kvargs["qSecondaryFailure"]
            else:
                self_.qSecondaryFailure = kvargs["qSecondaryFailure"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ScrollPosition:
    """

    Attributes
    ----------
    qUsePosition: bool
    qPos: Point
    """

    qUsePosition: bool = None
    qPos: Point = None

    def __init__(self_, **kvargs):
        if "qUsePosition" in kvargs:
            if (
                type(kvargs["qUsePosition"]).__name__
                is self_.__annotations__["qUsePosition"]
            ):
                self_.qUsePosition = kvargs["qUsePosition"]
            else:
                self_.qUsePosition = kvargs["qUsePosition"]
        if "qPos" in kvargs:
            if type(kvargs["qPos"]).__name__ is self_.__annotations__["qPos"]:
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = Point(**kvargs["qPos"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchAttribute:
    """

    Attributes
    ----------
    qKey: str
      String corresponding to SearchObjectOptions.qAttributes. It will be qProperty for SearchObjectOptions.
    qValue: str
      String corresponding to qKey for the current SearchGroupItemMatch. For example, if the match is Make by Price found in the title of a generic object, qValue will be qMetaDef/title.
    """

    qKey: str = None
    qValue: str = None

    def __init__(self_, **kvargs):
        if "qKey" in kvargs:
            if type(kvargs["qKey"]).__name__ is self_.__annotations__["qKey"]:
                self_.qKey = kvargs["qKey"]
            else:
                self_.qKey = kvargs["qKey"]
        if "qValue" in kvargs:
            if type(kvargs["qValue"]).__name__ is self_.__annotations__["qValue"]:
                self_.qValue = kvargs["qValue"]
            else:
                self_.qValue = kvargs["qValue"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchCharRange:
    """

    Attributes
    ----------
    qCharPos: int
      Starting position of the match in the search result, starting from 0.
    qCharCount: int
      Length of the match in the search result.
    qTerm: int
      Position of the term in the list of search terms, starting from 0.
    """

    qCharPos: int = None
    qCharCount: int = None
    qTerm: int = None

    def __init__(self_, **kvargs):
        if "qCharPos" in kvargs:
            if type(kvargs["qCharPos"]).__name__ is self_.__annotations__["qCharPos"]:
                self_.qCharPos = kvargs["qCharPos"]
            else:
                self_.qCharPos = kvargs["qCharPos"]
        if "qCharCount" in kvargs:
            if (
                type(kvargs["qCharCount"]).__name__
                is self_.__annotations__["qCharCount"]
            ):
                self_.qCharCount = kvargs["qCharCount"]
            else:
                self_.qCharCount = kvargs["qCharCount"]
        if "qTerm" in kvargs:
            if type(kvargs["qTerm"]).__name__ is self_.__annotations__["qTerm"]:
                self_.qTerm = kvargs["qTerm"]
            else:
                self_.qTerm = kvargs["qTerm"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchContextType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchFieldMatch:
    """

    Attributes
    ----------
    qField: int
      Position of the field in the list of fields, starting from 0.
      The list of fields is defined in qResults/qFieldNames and contains the search associations.
    qValues: list[int]
      Positions of the matching values in the search results.
      The maximum number of values in this list is defined by qMaxNbrFieldMatches .
    qTerms: list[int]
      Positions of the search terms, starting from 0.
    qNoOfMatches: int
      Number of search hits in the field.
      The number of values in qValues and the value of qNoOfMatches are equal if qMaxNbrFieldMatches is -1.
    """

    qField: int = None
    qValues: list[int] = None
    qTerms: list[int] = None
    qNoOfMatches: int = None

    def __init__(self_, **kvargs):
        if "qField" in kvargs:
            if type(kvargs["qField"]).__name__ is self_.__annotations__["qField"]:
                self_.qField = kvargs["qField"]
            else:
                self_.qField = kvargs["qField"]
        if "qValues" in kvargs:
            if type(kvargs["qValues"]).__name__ is self_.__annotations__["qValues"]:
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = kvargs["qValues"]
        if "qTerms" in kvargs:
            if type(kvargs["qTerms"]).__name__ is self_.__annotations__["qTerms"]:
                self_.qTerms = kvargs["qTerms"]
            else:
                self_.qTerms = kvargs["qTerms"]
        if "qNoOfMatches" in kvargs:
            if (
                type(kvargs["qNoOfMatches"]).__name__
                is self_.__annotations__["qNoOfMatches"]
            ):
                self_.qNoOfMatches = kvargs["qNoOfMatches"]
            else:
                self_.qNoOfMatches = kvargs["qNoOfMatches"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchFieldMatchesItem:
    """

    Attributes
    ----------
    qText: str
    qElemNo: int
    qSearchTermsMatched: list[int]
    """

    qText: str = None
    qElemNo: int = None
    qSearchTermsMatched: list[int] = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qElemNo" in kvargs:
            if type(kvargs["qElemNo"]).__name__ is self_.__annotations__["qElemNo"]:
                self_.qElemNo = kvargs["qElemNo"]
            else:
                self_.qElemNo = kvargs["qElemNo"]
        if "qSearchTermsMatched" in kvargs:
            if (
                type(kvargs["qSearchTermsMatched"]).__name__
                is self_.__annotations__["qSearchTermsMatched"]
            ):
                self_.qSearchTermsMatched = kvargs["qSearchTermsMatched"]
            else:
                self_.qSearchTermsMatched = kvargs["qSearchTermsMatched"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchFieldSelectionMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchFieldValueItem:
    """

    Attributes
    ----------
    qFieldName: str
      Field name of matches.
    qValues: list[SearchFieldMatchesItem]
      List of search matches.
    """

    qFieldName: str = None
    qValues: list[SearchFieldMatchesItem] = None

    def __init__(self_, **kvargs):
        if "qFieldName" in kvargs:
            if (
                type(kvargs["qFieldName"]).__name__
                is self_.__annotations__["qFieldName"]
            ):
                self_.qFieldName = kvargs["qFieldName"]
            else:
                self_.qFieldName = kvargs["qFieldName"]
        if "qValues" in kvargs:
            if type(kvargs["qValues"]).__name__ is self_.__annotations__["qValues"]:
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [SearchFieldMatchesItem(**e) for e in kvargs["qValues"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroupItemMatch:
    """

    Attributes
    ----------
    qText: str
      Search match value.
      Value of the search group item.
      If the match is found in a field, it corresponds to the value of the field.
      If the match is found in a generic object property, it corresponds to the property value.
    qFieldSelectionMode: str
      Selection mode of a field.
      Suppressed by default. One and always one field value is selected when set to OneAndOnlyOne.
    qRanges: list[SearchCharRange]
      List of ranges.
      For example, if the search terms are Price and Make, and the search group item value is Make by Price vs Mileage, then there are two ranges: one for Price and one for Make.
    qAttributes: list[SearchAttribute]
      Provides detail of the match as requested by the user in SearchObjectsOptions.qAttributes or SearchCombinationOptions.qAttributes
      If the user requests SearchObjects or SearchResults with an empty qAttributes option, the outputted qAttributes is returned empty.
      For SearchObjects requested with qProperty , the SearchGroupItemMatch.qAttributes return value contains [“qProperty”, "qMetaDef/title”] if the match has been found in the title of the item. For dimension values, the returned qProperty will be “*” .
      For SearchResults requested with qNum , the SearchGroupItemMatch.qAttributes return value contains ["qNum", N] where N is the numeric value of the element or NaN if the value is not numeric.
      For SearchResults requested with qElemNum , the SearchGroupItemMatch.qAttributes return value contains ["qElemNum", N] where N is the value index of the element.
    """

    qText: str = None
    qFieldSelectionMode: str = None
    qRanges: list[SearchCharRange] = None
    qAttributes: list[SearchAttribute] = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qFieldSelectionMode" in kvargs:
            if (
                type(kvargs["qFieldSelectionMode"]).__name__
                is self_.__annotations__["qFieldSelectionMode"]
            ):
                self_.qFieldSelectionMode = kvargs["qFieldSelectionMode"]
            else:
                self_.qFieldSelectionMode = kvargs["qFieldSelectionMode"]
        if "qRanges" in kvargs:
            if type(kvargs["qRanges"]).__name__ is self_.__annotations__["qRanges"]:
                self_.qRanges = kvargs["qRanges"]
            else:
                self_.qRanges = [SearchCharRange(**e) for e in kvargs["qRanges"]]
        if "qAttributes" in kvargs:
            if (
                type(kvargs["qAttributes"]).__name__
                is self_.__annotations__["qAttributes"]
            ):
                self_.qAttributes = kvargs["qAttributes"]
            else:
                self_.qAttributes = [
                    SearchAttribute(**e) for e in kvargs["qAttributes"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroupItemType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroupType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchMatchCombination:
    """

    Attributes
    ----------
    qId: int
      Index of the search result, starting from 0.
    qFieldMatches: list[SearchFieldMatch]
      Information about the search matches.
    """

    qId: int = None
    qFieldMatches: list[SearchFieldMatch] = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs:
            if type(kvargs["qId"]).__name__ is self_.__annotations__["qId"]:
                self_.qId = kvargs["qId"]
            else:
                self_.qId = kvargs["qId"]
        if "qFieldMatches" in kvargs:
            if (
                type(kvargs["qFieldMatches"]).__name__
                is self_.__annotations__["qFieldMatches"]
            ):
                self_.qFieldMatches = kvargs["qFieldMatches"]
            else:
                self_.qFieldMatches = [
                    SearchFieldMatch(**e) for e in kvargs["qFieldMatches"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchMatchCombinations:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchObjectOptions:
    """

    Attributes
    ----------
    qAttributes: list[str]
      This array is either empty or contains qProperty .
    qCharEncoding: str
      Encoding used to compute qRanges of type SearchCharRange.
      Only affects the computation of the ranges. It does not impact the encoding of the text.

      One of:

      • Utf8 or CHAR_ENCODING_UTF8

      • Utf16 or CHAR_ENCODING_UTF16
    """

    qAttributes: list[str] = None
    qCharEncoding: str = "CHAR_ENCODING_UTF8"

    def __init__(self_, **kvargs):
        if "qAttributes" in kvargs:
            if (
                type(kvargs["qAttributes"]).__name__
                is self_.__annotations__["qAttributes"]
            ):
                self_.qAttributes = kvargs["qAttributes"]
            else:
                self_.qAttributes = kvargs["qAttributes"]
        if "qCharEncoding" in kvargs:
            if (
                type(kvargs["qCharEncoding"]).__name__
                is self_.__annotations__["qCharEncoding"]
            ):
                self_.qCharEncoding = kvargs["qCharEncoding"]
            else:
                self_.qCharEncoding = kvargs["qCharEncoding"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchSuggestItem:
    """

    Attributes
    ----------
    qValue: str
      Value of the suggestion.
    qTerm: int
      Index of the suggestion value.
      The indexing starts from 0 and from the left.
    """

    qValue: str = None
    qTerm: int = None

    def __init__(self_, **kvargs):
        if "qValue" in kvargs:
            if type(kvargs["qValue"]).__name__ is self_.__annotations__["qValue"]:
                self_.qValue = kvargs["qValue"]
            else:
                self_.qValue = kvargs["qValue"]
        if "qTerm" in kvargs:
            if type(kvargs["qTerm"]).__name__ is self_.__annotations__["qTerm"]:
                self_.qTerm = kvargs["qTerm"]
            else:
                self_.qTerm = kvargs["qTerm"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchSuggestionResult:
    """

    Attributes
    ----------
    qSuggestions: list[SearchSuggestItem]
      List of suggestions.
    qFieldNames: list[str]
      List of field names that contain search hits.
    """

    qSuggestions: list[SearchSuggestItem] = None
    qFieldNames: list[str] = None

    def __init__(self_, **kvargs):
        if "qSuggestions" in kvargs:
            if (
                type(kvargs["qSuggestions"]).__name__
                is self_.__annotations__["qSuggestions"]
            ):
                self_.qSuggestions = kvargs["qSuggestions"]
            else:
                self_.qSuggestions = [
                    SearchSuggestItem(**e) for e in kvargs["qSuggestions"]
                ]
        if "qFieldNames" in kvargs:
            if (
                type(kvargs["qFieldNames"]).__name__
                is self_.__annotations__["qFieldNames"]
            ):
                self_.qFieldNames = kvargs["qFieldNames"]
            else:
                self_.qFieldNames = kvargs["qFieldNames"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchTermResult:
    """

    Attributes
    ----------
    qText: str
      Text of the associated value.
    qElemNumber: int
      Element number of the associated value.
    qRanges: list[SearchCharRange]
      List of ranges.
      For example, if the user searches the term read and the associative value is Reading , then the corresponding range would be Read in Reading .
    """

    qText: str = None
    qElemNumber: int = None
    qRanges: list[SearchCharRange] = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qElemNumber" in kvargs:
            if (
                type(kvargs["qElemNumber"]).__name__
                is self_.__annotations__["qElemNumber"]
            ):
                self_.qElemNumber = kvargs["qElemNumber"]
            else:
                self_.qElemNumber = kvargs["qElemNumber"]
        if "qRanges" in kvargs:
            if type(kvargs["qRanges"]).__name__ is self_.__annotations__["qRanges"]:
                self_.qRanges = kvargs["qRanges"]
            else:
                self_.qRanges = [SearchCharRange(**e) for e in kvargs["qRanges"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchValueOptions:
    """

    Attributes
    ----------
    qSearchFields: list[str]
      List of the search fields.
      If empty, the search is performed in all fields of the app.
    """

    qSearchFields: list[str] = None

    def __init__(self_, **kvargs):
        if "qSearchFields" in kvargs:
            if (
                type(kvargs["qSearchFields"]).__name__
                is self_.__annotations__["qSearchFields"]
            ):
                self_.qSearchFields = kvargs["qSearchFields"]
            else:
                self_.qSearchFields = kvargs["qSearchFields"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchValuePage:
    """

    Attributes
    ----------
    qOffset: int
      Position from the top, starting from 0.
      If the offset is set to 0, the first search result to be returned is at position 0.
    qCount: int
      Number of search fields to return
    qMaxNbrFieldMatches: int
      Maximum number of matching values to return per search result.
    """

    qOffset: int = None
    qCount: int = None
    qMaxNbrFieldMatches: int = -1

    def __init__(self_, **kvargs):
        if "qOffset" in kvargs:
            if type(kvargs["qOffset"]).__name__ is self_.__annotations__["qOffset"]:
                self_.qOffset = kvargs["qOffset"]
            else:
                self_.qOffset = kvargs["qOffset"]
        if "qCount" in kvargs:
            if type(kvargs["qCount"]).__name__ is self_.__annotations__["qCount"]:
                self_.qCount = kvargs["qCount"]
            else:
                self_.qCount = kvargs["qCount"]
        if "qMaxNbrFieldMatches" in kvargs:
            if (
                type(kvargs["qMaxNbrFieldMatches"]).__name__
                is self_.__annotations__["qMaxNbrFieldMatches"]
            ):
                self_.qMaxNbrFieldMatches = kvargs["qMaxNbrFieldMatches"]
            else:
                self_.qMaxNbrFieldMatches = kvargs["qMaxNbrFieldMatches"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchValueResult:
    """

    Attributes
    ----------
    qSearchTerms: list[str]
      List of the search terms.
    qFieldMatches: list[SearchFieldValueItem]
      List of search groups.
      The groups are numbered from the value of SearchPage.qOffset to the value of SearchPage.qOffset + SearchPage.qCount .
    """

    qSearchTerms: list[str] = None
    qFieldMatches: list[SearchFieldValueItem] = None

    def __init__(self_, **kvargs):
        if "qSearchTerms" in kvargs:
            if (
                type(kvargs["qSearchTerms"]).__name__
                is self_.__annotations__["qSearchTerms"]
            ):
                self_.qSearchTerms = kvargs["qSearchTerms"]
            else:
                self_.qSearchTerms = kvargs["qSearchTerms"]
        if "qFieldMatches" in kvargs:
            if (
                type(kvargs["qFieldMatches"]).__name__
                is self_.__annotations__["qFieldMatches"]
            ):
                self_.qFieldMatches = kvargs["qFieldMatches"]
            else:
                self_.qFieldMatches = [
                    SearchFieldValueItem(**e) for e in kvargs["qFieldMatches"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SelectInfo:
    """

    Attributes
    ----------
    qTextSearch: str
      Text search string.
      Everything that matches the text is selected.
      This parameter is optional.
    qRangeLo: float
      Lower value of the search range.
      This parameter is used when performing range selections or text searches in dimensions.
      Default is Null.
    qRangeHi: float
      Highest value of the search range.
      This parameter is used when performing range selections or text searches in dimensions.
      Default is Null.
    qNumberFormat: FieldAttributes
      Gives information about the formatting of the range.
      This parameter is used when performing range selections or text searches in dimensions.
    qRangeInfo: list[RangeSelectInfo]
      This parameter is used when performing range selections or text searches in measures.
      Gives information about the range of selections.
    qSoftLock: bool
      Set to true to ignore locks; in that case, locked fields can be selected.
      The default value is false.
    qContinuousRangeInfo: list[Range]
      List of information about ranges for selections.
    qSelectFieldSearch: bool
      This parameter is true if the TextSearch is a result of a Select Field operation.
    """

    qTextSearch: str = None
    qRangeLo: float = -1e300
    qRangeHi: float = -1e300
    qNumberFormat: FieldAttributes = None
    qRangeInfo: list[RangeSelectInfo] = None
    qSoftLock: bool = None
    qContinuousRangeInfo: list[Range] = None
    qSelectFieldSearch: bool = None

    def __init__(self_, **kvargs):
        if "qTextSearch" in kvargs:
            if (
                type(kvargs["qTextSearch"]).__name__
                is self_.__annotations__["qTextSearch"]
            ):
                self_.qTextSearch = kvargs["qTextSearch"]
            else:
                self_.qTextSearch = kvargs["qTextSearch"]
        if "qRangeLo" in kvargs:
            if type(kvargs["qRangeLo"]).__name__ is self_.__annotations__["qRangeLo"]:
                self_.qRangeLo = kvargs["qRangeLo"]
            else:
                self_.qRangeLo = kvargs["qRangeLo"]
        if "qRangeHi" in kvargs:
            if type(kvargs["qRangeHi"]).__name__ is self_.__annotations__["qRangeHi"]:
                self_.qRangeHi = kvargs["qRangeHi"]
            else:
                self_.qRangeHi = kvargs["qRangeHi"]
        if "qNumberFormat" in kvargs:
            if (
                type(kvargs["qNumberFormat"]).__name__
                is self_.__annotations__["qNumberFormat"]
            ):
                self_.qNumberFormat = kvargs["qNumberFormat"]
            else:
                self_.qNumberFormat = FieldAttributes(**kvargs["qNumberFormat"])
        if "qRangeInfo" in kvargs:
            if (
                type(kvargs["qRangeInfo"]).__name__
                is self_.__annotations__["qRangeInfo"]
            ):
                self_.qRangeInfo = kvargs["qRangeInfo"]
            else:
                self_.qRangeInfo = [RangeSelectInfo(**e) for e in kvargs["qRangeInfo"]]
        if "qSoftLock" in kvargs:
            if type(kvargs["qSoftLock"]).__name__ is self_.__annotations__["qSoftLock"]:
                self_.qSoftLock = kvargs["qSoftLock"]
            else:
                self_.qSoftLock = kvargs["qSoftLock"]
        if "qContinuousRangeInfo" in kvargs:
            if (
                type(kvargs["qContinuousRangeInfo"]).__name__
                is self_.__annotations__["qContinuousRangeInfo"]
            ):
                self_.qContinuousRangeInfo = kvargs["qContinuousRangeInfo"]
            else:
                self_.qContinuousRangeInfo = [
                    Range(**e) for e in kvargs["qContinuousRangeInfo"]
                ]
        if "qSelectFieldSearch" in kvargs:
            if (
                type(kvargs["qSelectFieldSearch"]).__name__
                is self_.__annotations__["qSelectFieldSearch"]
            ):
                self_.qSelectFieldSearch = kvargs["qSelectFieldSearch"]
            else:
                self_.qSelectFieldSearch = kvargs["qSelectFieldSearch"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SelectionObjectDef:
    """
    To display the current selections.
    Can be added to any generic object but is particularly meaningful when using session objects to monitor an app.

    Properties:

    "qSelectionObjectDef": {}

    Attributes
    ----------
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    """

    qStateName: str = None

    def __init__(self_, **kvargs):
        if "qStateName" in kvargs:
            if (
                type(kvargs["qStateName"]).__name__
                is self_.__annotations__["qStateName"]
            ):
                self_.qStateName = kvargs["qStateName"]
            else:
                self_.qStateName = kvargs["qStateName"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Size:
    """

    Attributes
    ----------
    qcx: int
      Number of pixels on the x axis.
    qcy: int
      Number of pixels on the y axis.
    """

    qcx: int = None
    qcy: int = None

    def __init__(self_, **kvargs):
        if "qcx" in kvargs:
            if type(kvargs["qcx"]).__name__ is self_.__annotations__["qcx"]:
                self_.qcx = kvargs["qcx"]
            else:
                self_.qcx = kvargs["qcx"]
        if "qcy" in kvargs:
            if type(kvargs["qcy"]).__name__ is self_.__annotations__["qcy"]:
                self_.qcy = kvargs["qcy"]
            else:
                self_.qcy = kvargs["qcy"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SourceKeyRecord:
    """

    Attributes
    ----------
    qKeyFields: list[str]
      Name of the key field.
    qTables: list[str]
      Table the key belongs to.
    """

    qKeyFields: list[str] = None
    qTables: list[str] = None

    def __init__(self_, **kvargs):
        if "qKeyFields" in kvargs:
            if (
                type(kvargs["qKeyFields"]).__name__
                is self_.__annotations__["qKeyFields"]
            ):
                self_.qKeyFields = kvargs["qKeyFields"]
            else:
                self_.qKeyFields = kvargs["qKeyFields"]
        if "qTables" in kvargs:
            if type(kvargs["qTables"]).__name__ is self_.__annotations__["qTables"]:
                self_.qTables = kvargs["qTables"]
            else:
                self_.qTables = kvargs["qTables"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StateEnumType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StaticContentListItem:
    """
    In addition, this structure can return dynamic properties.

    Attributes
    ----------
    qUrlDef: str
      Relative path to the content file. The URL is static.
      In Qlik Sense Enterprise, content files located:

      • In the /content/ <content library name>/ folder are part of a global content library.

      • In the /appcontent/ folder are part of the app specific library.
      The content files are never embedded in the qvf file.
      In Qlik Sense Desktop, content files located:

      • In the /content/default/ folder are outside the qvf file.

      • In the /media/ folder are embedded in the qvf file.
    qUrl: str
      Relative path to the content file. The URL is static.
      In Qlik Sense Enterprise, content files located:

      • In the /content/ <content library name>/ folder are part of a global content library.

      • In the /appcontent/ folder are part of the app specific library.
      The content files are never embedded in the qvf file.
      In Qlik Sense Desktop, content files located:

      • In the /content/default/ folder are outside the qvf file.

      • In the /media/ folder are embedded in the qvf file.
    """

    qUrlDef: str = None
    qUrl: str = None

    def __init__(self_, **kvargs):
        if "qUrlDef" in kvargs:
            if type(kvargs["qUrlDef"]).__name__ is self_.__annotations__["qUrlDef"]:
                self_.qUrlDef = kvargs["qUrlDef"]
            else:
                self_.qUrlDef = kvargs["qUrlDef"]
        if "qUrl" in kvargs:
            if type(kvargs["qUrl"]).__name__ is self_.__annotations__["qUrl"]:
                self_.qUrl = kvargs["qUrl"]
            else:
                self_.qUrl = kvargs["qUrl"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StaticContentUrl:
    """
    In addition, this structure can return dynamic properties.

    Attributes
    ----------
    qUrl: str
      Relative path of the thumbnail.
    """

    qUrl: str = None

    def __init__(self_, **kvargs):
        if "qUrl" in kvargs:
            if type(kvargs["qUrl"]).__name__ is self_.__annotations__["qUrl"]:
                self_.qUrl = kvargs["qUrl"]
            else:
                self_.qUrl = kvargs["qUrl"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StaticContentUrlDef:
    """
    In addition, this structure can contain dynamic properties.

    Attributes
    ----------
    qUrl: str
      Relative path of the thumbnail.
    """

    qUrl: str = None

    def __init__(self_, **kvargs):
        if "qUrl" in kvargs:
            if type(kvargs["qUrl"]).__name__ is self_.__annotations__["qUrl"]:
                self_.qUrl = kvargs["qUrl"]
            else:
                self_.qUrl = kvargs["qUrl"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StringExpr:
    """

    Attributes
    ----------
    qv: str
      Expression evaluated to string.
    """

    qv: str = None

    def __init__(self_, **kvargs):
        if "qv" in kvargs:
            if type(kvargs["qv"]).__name__ is self_.__annotations__["qv"]:
                self_.qv = kvargs["qv"]
            else:
                self_.qv = kvargs["qv"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StringExpression:
    """
    Properties:

    Abbreviated syntax:
    "qStringExpression":"=<expression>"
    Extended object syntax:
    "qStringExpression":{"qExpr":"=<expression>"}
    Where:

    • < expression > is a string

    The "=" sign in the string expression is not mandatory. Even if the "=" sign is not given, the expression is evaluated.
    A string expression is not evaluated, if the expression is surrounded by simple quotes.

    The result of the evaluation of the expression can be of any type, as it is returned as a JSON (quoted) string.

    Attributes
    ----------
    qExpr: str
    """

    qExpr: str = None

    def __init__(self_, **kvargs):
        if "qExpr" in kvargs:
            if type(kvargs["qExpr"]).__name__ is self_.__annotations__["qExpr"]:
                self_.qExpr = kvargs["qExpr"]
            else:
                self_.qExpr = kvargs["qExpr"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SymbolValue:
    """

    Attributes
    ----------
    qText: str
      String value of the symbol. This parameter is optional and present only if Symbol is a string.
    qNumber: float
      Numeric value of the symbol. NaN otherwise.
    """

    qText: str = None
    qNumber: float = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qNumber" in kvargs:
            if type(kvargs["qNumber"]).__name__ is self_.__annotations__["qNumber"]:
                self_.qNumber = kvargs["qNumber"]
            else:
                self_.qNumber = kvargs["qNumber"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableRow:
    """

    Attributes
    ----------
    qValue: list[FieldValue]
      Array of field values.
    """

    qValue: list[FieldValue] = None

    def __init__(self_, **kvargs):
        if "qValue" in kvargs:
            if type(kvargs["qValue"]).__name__ is self_.__annotations__["qValue"]:
                self_.qValue = kvargs["qValue"]
            else:
                self_.qValue = [FieldValue(**e) for e in kvargs["qValue"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableViewBroomPointSaveInfo:
    """

    Attributes
    ----------
    qPos: Point
      Information about the position of the broom point.
    qTable: str
      Name of the table.
    qFields: list[str]
      List of fields in the table.
    """

    qPos: Point = None
    qTable: str = None
    qFields: list[str] = None

    def __init__(self_, **kvargs):
        if "qPos" in kvargs:
            if type(kvargs["qPos"]).__name__ is self_.__annotations__["qPos"]:
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = Point(**kvargs["qPos"])
        if "qTable" in kvargs:
            if type(kvargs["qTable"]).__name__ is self_.__annotations__["qTable"]:
                self_.qTable = kvargs["qTable"]
            else:
                self_.qTable = kvargs["qTable"]
        if "qFields" in kvargs:
            if type(kvargs["qFields"]).__name__ is self_.__annotations__["qFields"]:
                self_.qFields = kvargs["qFields"]
            else:
                self_.qFields = kvargs["qFields"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableViewConnectionPointSaveInfo:
    """

    Attributes
    ----------
    qPos: Point
      Information about the position of the connection point.
    qFields: list[str]
      List of the fields in the table.
    """

    qPos: Point = None
    qFields: list[str] = None

    def __init__(self_, **kvargs):
        if "qPos" in kvargs:
            if type(kvargs["qPos"]).__name__ is self_.__annotations__["qPos"]:
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = Point(**kvargs["qPos"])
        if "qFields" in kvargs:
            if type(kvargs["qFields"]).__name__ is self_.__annotations__["qFields"]:
                self_.qFields = kvargs["qFields"]
            else:
                self_.qFields = kvargs["qFields"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableViewTableWinSaveInfo:
    """

    Attributes
    ----------
    qPos: Rect
      Information about the position of the table.
    qCaption: str
      Table name.
    """

    qPos: Rect = None
    qCaption: str = None

    def __init__(self_, **kvargs):
        if "qPos" in kvargs:
            if type(kvargs["qPos"]).__name__ is self_.__annotations__["qPos"]:
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = Rect(**kvargs["qPos"])
        if "qCaption" in kvargs:
            if type(kvargs["qCaption"]).__name__ is self_.__annotations__["qCaption"]:
                self_.qCaption = kvargs["qCaption"]
            else:
                self_.qCaption = kvargs["qCaption"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TextMacro:
    """

    Attributes
    ----------
    qTag: str
      Name of the variable.
    qRefSeqNo: int
      Order in which the variable was referenced during the script execution.
      The same number sequence is used for both qRefSeqNo and qSetSeqNo .
    qSetSeqNo: int
      Order in which the variable was updated during the script execution.
      The same number sequence is used for both qRefSeqNo and qSetSeqNo .
    qDisplayString: str
      Variable value.
    qIsSystem: bool
      Is set to true if the variable is a system variable.
    qIsReserved: bool
      Is set to true if the variable is a reserved variable.
    """

    qTag: str = None
    qRefSeqNo: int = None
    qSetSeqNo: int = None
    qDisplayString: str = None
    qIsSystem: bool = None
    qIsReserved: bool = None

    def __init__(self_, **kvargs):
        if "qTag" in kvargs:
            if type(kvargs["qTag"]).__name__ is self_.__annotations__["qTag"]:
                self_.qTag = kvargs["qTag"]
            else:
                self_.qTag = kvargs["qTag"]
        if "qRefSeqNo" in kvargs:
            if type(kvargs["qRefSeqNo"]).__name__ is self_.__annotations__["qRefSeqNo"]:
                self_.qRefSeqNo = kvargs["qRefSeqNo"]
            else:
                self_.qRefSeqNo = kvargs["qRefSeqNo"]
        if "qSetSeqNo" in kvargs:
            if type(kvargs["qSetSeqNo"]).__name__ is self_.__annotations__["qSetSeqNo"]:
                self_.qSetSeqNo = kvargs["qSetSeqNo"]
            else:
                self_.qSetSeqNo = kvargs["qSetSeqNo"]
        if "qDisplayString" in kvargs:
            if (
                type(kvargs["qDisplayString"]).__name__
                is self_.__annotations__["qDisplayString"]
            ):
                self_.qDisplayString = kvargs["qDisplayString"]
            else:
                self_.qDisplayString = kvargs["qDisplayString"]
        if "qIsSystem" in kvargs:
            if type(kvargs["qIsSystem"]).__name__ is self_.__annotations__["qIsSystem"]:
                self_.qIsSystem = kvargs["qIsSystem"]
            else:
                self_.qIsSystem = kvargs["qIsSystem"]
        if "qIsReserved" in kvargs:
            if (
                type(kvargs["qIsReserved"]).__name__
                is self_.__annotations__["qIsReserved"]
            ):
                self_.qIsReserved = kvargs["qIsReserved"]
            else:
                self_.qIsReserved = kvargs["qIsReserved"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TotalMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UndoInfo:
    """
    Displays information about the number of possible undos and redos. Is the layout for UndoInfoDef.

    Attributes
    ----------
    qUndoCount: int
      Number of possible undos.
    qRedoCount: int
      Number of possible redos.
    """

    qUndoCount: int = None
    qRedoCount: int = None

    def __init__(self_, **kvargs):
        if "qUndoCount" in kvargs:
            if (
                type(kvargs["qUndoCount"]).__name__
                is self_.__annotations__["qUndoCount"]
            ):
                self_.qUndoCount = kvargs["qUndoCount"]
            else:
                self_.qUndoCount = kvargs["qUndoCount"]
        if "qRedoCount" in kvargs:
            if (
                type(kvargs["qRedoCount"]).__name__
                is self_.__annotations__["qRedoCount"]
            ):
                self_.qRedoCount = kvargs["qRedoCount"]
            else:
                self_.qRedoCount = kvargs["qRedoCount"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UndoInfoDef:
    """
    Defines if an object should contain information on the number of possible undo and redo.

    Properties:

    "qUndoInfoDef": {}
    The numbers of undos and redos are empty when an object is created. The number of possible undos is increased every time an action (for example, create a child, set some properties) on the object is performed. The number of possible redos is increased every time an undo action is performed.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ValueExpr:
    """

    Attributes
    ----------
    qv: str
      Expression evaluated to dual.
    """

    qv: str = None

    def __init__(self_, **kvargs):
        if "qv" in kvargs:
            if type(kvargs["qv"]).__name__ is self_.__annotations__["qv"]:
                self_.qv = kvargs["qv"]
            else:
                self_.qv = kvargs["qv"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ValueExpression:
    """
    Properties:

    Abbreviated syntax:
    "qValueExpression":"=<expression>"
    Extended object syntax:
    "qValueExpression":{"qExpr":"=<expression>"}
    Where:

    • < expression > is a string.

    The "=" sign in the value expression is not mandatory. Even if the "=" sign is not given, the expression is evaluated.

    The expression is evaluated as a numeric.

    Attributes
    ----------
    qExpr: str
    """

    qExpr: str = None

    def __init__(self_, **kvargs):
        if "qExpr" in kvargs:
            if type(kvargs["qExpr"]).__name__ is self_.__annotations__["qExpr"]:
                self_.qExpr = kvargs["qExpr"]
            else:
                self_.qExpr = kvargs["qExpr"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Variable:
    """

    Attributes
    ----------
    qType: str
      The native type of the object.
    qHandle: int
      The handle used to connect to object.
    qGenericType: str
      The type of the object.
    qGenericId: str
      Object ID.
    """

    qType: str = None
    qHandle: int = None
    qGenericType: str = None
    qGenericId: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qHandle" in kvargs:
            if type(kvargs["qHandle"]).__name__ is self_.__annotations__["qHandle"]:
                self_.qHandle = kvargs["qHandle"]
            else:
                self_.qHandle = kvargs["qHandle"]
        if "qGenericType" in kvargs:
            if (
                type(kvargs["qGenericType"]).__name__
                is self_.__annotations__["qGenericType"]
            ):
                self_.qGenericType = kvargs["qGenericType"]
            else:
                self_.qGenericType = kvargs["qGenericType"]
        if "qGenericId" in kvargs:
            if (
                type(kvargs["qGenericId"]).__name__
                is self_.__annotations__["qGenericId"]
            ):
                self_.qGenericId = kvargs["qGenericId"]
            else:
                self_.qGenericId = kvargs["qGenericId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_content(self) -> AlfaNumString:
        """
        Deprecated
        Returns the calculated value of a variable.


        """
        warnings.warn("GetContent is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetContent", handle)["qContent"]
        obj = AlfaNumString(**response)
        obj._session = self._session
        return obj

    def get_raw_content(self) -> str:
        """
        Deprecated
        Returns the raw value of a variable.


        """
        warnings.warn("GetRawContent is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetRawContent", handle)["qReturn"]
        return response

    def set_content(self, qContent: str, qUpdateMRU: bool) -> bool:
        """
        Deprecated
        Sets a value to a variable.


        qContent: str
          Value of the variable.

        qUpdateMRU: bool
          If set to true, the value is added to the Most Recently Used (MRU) list.

        """
        warnings.warn("SetContent is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qContent"] = qContent
        params["qUpdateMRU"] = qUpdateMRU
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetContent", handle, **params)["qReturn"]
        return response

    def force_content(self, qs: str, qd: float) -> object:
        """
        Deprecated
        Sets the value of a dual variable overriding any input constraints.


        qs: str
          String representation of a dual value.
          Set this parameter to "", if the string representation is to be Null.

        qd: float
          Numeric representation of a dual value.

        """
        warnings.warn("ForceContent is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qs"] = qs
        params["qd"] = qd
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ForceContent", handle, **params)
        return response

    def get_nx_properties(self) -> NxVariableProperties:
        """
        Deprecated
        Gets the properties of a variable.


        """
        warnings.warn("GetNxProperties is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetNxProperties", handle)["qProperties"]
        obj = NxVariableProperties(**response)
        obj._session = self._session
        return obj

    def set_nx_properties(self, qProperties: NxVariableProperties) -> object:
        """
        Deprecated
        Sets some properties to a variable.


        qProperties: NxVariableProperties
          Information about the properties of the variable

        """
        warnings.warn("SetNxProperties is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qProperties"] = qProperties
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetNxProperties", handle, **params)
        return response


@dataclass
class VariableList:
    """
    Lists the variables in an app. Is the layout for VariableListDef.

    Attributes
    ----------
    qItems: list[NxVariableListItem]
      List of the variables.
    """

    qItems: list[NxVariableListItem] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs:
            if type(kvargs["qItems"]).__name__ is self_.__annotations__["qItems"]:
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [NxVariableListItem(**e) for e in kvargs["qItems"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class VariableListDef:
    """
    Defines the list of variables in an app.

    Attributes
    ----------
    qType: str
      Type of variables to include in the list.
    qShowReserved: bool
      Shows the reserved variables if set to true.
    qShowConfig: bool
      Shows the system variables if set to true.
    qData: JsonObject
      Data
    qShowSession: bool
      Shows the session variables if set to true.
    """

    qType: str = None
    qShowReserved: bool = None
    qShowConfig: bool = None
    qData: JsonObject = None
    qShowSession: bool = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qShowReserved" in kvargs:
            if (
                type(kvargs["qShowReserved"]).__name__
                is self_.__annotations__["qShowReserved"]
            ):
                self_.qShowReserved = kvargs["qShowReserved"]
            else:
                self_.qShowReserved = kvargs["qShowReserved"]
        if "qShowConfig" in kvargs:
            if (
                type(kvargs["qShowConfig"]).__name__
                is self_.__annotations__["qShowConfig"]
            ):
                self_.qShowConfig = kvargs["qShowConfig"]
            else:
                self_.qShowConfig = kvargs["qShowConfig"]
        if "qData" in kvargs:
            if type(kvargs["qData"]).__name__ is self_.__annotations__["qData"]:
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(**kvargs["qData"])
        if "qShowSession" in kvargs:
            if (
                type(kvargs["qShowSession"]).__name__
                is self_.__annotations__["qShowSession"]
            ):
                self_.qShowSession = kvargs["qShowSession"]
            else:
                self_.qShowSession = kvargs["qShowSession"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppEntry:
    """

    Attributes
    ----------
    qID: str
      Identifier of the app.
    qTitle: str
      Title of the app.
    qPath: str
      Path of the app.
    qLastReloadTime: str
      Last reload time of the app.
    qReadOnly: bool
      Is set to true if the app is read-only.
    qMeta: NxMeta
      Meta data.
    qThumbnail: StaticContentUrl
      App thumbnail.
    qFileSize: int
    qHasSectionAccess: bool
      If true the app has section access configured.
    """

    qID: str = None
    qTitle: str = None
    qPath: str = None
    qLastReloadTime: str = None
    qReadOnly: bool = None
    qMeta: NxMeta = None
    qThumbnail: StaticContentUrl = None
    qFileSize: int = None
    qHasSectionAccess: bool = None

    def __init__(self_, **kvargs):
        if "qID" in kvargs:
            if type(kvargs["qID"]).__name__ is self_.__annotations__["qID"]:
                self_.qID = kvargs["qID"]
            else:
                self_.qID = kvargs["qID"]
        if "qTitle" in kvargs:
            if type(kvargs["qTitle"]).__name__ is self_.__annotations__["qTitle"]:
                self_.qTitle = kvargs["qTitle"]
            else:
                self_.qTitle = kvargs["qTitle"]
        if "qPath" in kvargs:
            if type(kvargs["qPath"]).__name__ is self_.__annotations__["qPath"]:
                self_.qPath = kvargs["qPath"]
            else:
                self_.qPath = kvargs["qPath"]
        if "qLastReloadTime" in kvargs:
            if (
                type(kvargs["qLastReloadTime"]).__name__
                is self_.__annotations__["qLastReloadTime"]
            ):
                self_.qLastReloadTime = kvargs["qLastReloadTime"]
            else:
                self_.qLastReloadTime = kvargs["qLastReloadTime"]
        if "qReadOnly" in kvargs:
            if type(kvargs["qReadOnly"]).__name__ is self_.__annotations__["qReadOnly"]:
                self_.qReadOnly = kvargs["qReadOnly"]
            else:
                self_.qReadOnly = kvargs["qReadOnly"]
        if "qMeta" in kvargs:
            if type(kvargs["qMeta"]).__name__ is self_.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(**kvargs["qMeta"])
        if "qThumbnail" in kvargs:
            if (
                type(kvargs["qThumbnail"]).__name__
                is self_.__annotations__["qThumbnail"]
            ):
                self_.qThumbnail = kvargs["qThumbnail"]
            else:
                self_.qThumbnail = StaticContentUrl(**kvargs["qThumbnail"])
        if "qFileSize" in kvargs:
            if type(kvargs["qFileSize"]).__name__ is self_.__annotations__["qFileSize"]:
                self_.qFileSize = kvargs["qFileSize"]
            else:
                self_.qFileSize = kvargs["qFileSize"]
        if "qHasSectionAccess" in kvargs:
            if (
                type(kvargs["qHasSectionAccess"]).__name__
                is self_.__annotations__["qHasSectionAccess"]
            ):
                self_.qHasSectionAccess = kvargs["qHasSectionAccess"]
            else:
                self_.qHasSectionAccess = kvargs["qHasSectionAccess"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppObjectListDef:
    """
    Defines the list of objects in an app.
    An app object is a generic object created at app level.

    Attributes
    ----------
    qType: str
      Type of the app list.
    qData: JsonObject
      Data that you want to include in the app list definition.
      You need to enter the paths to the information you want to retrieve.
    """

    qType: str = None
    qData: JsonObject = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qData" in kvargs:
            if type(kvargs["qData"]).__name__ is self_.__annotations__["qData"]:
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(**kvargs["qData"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppScript:
    """

    Attributes
    ----------
    qScript: str
      Script text.
    qMeta: NxMeta
      Information about publishing and permissions.
      This parameter is optional.
    """

    qScript: str = None
    qMeta: NxMeta = None

    def __init__(self_, **kvargs):
        if "qScript" in kvargs:
            if type(kvargs["qScript"]).__name__ is self_.__annotations__["qScript"]:
                self_.qScript = kvargs["qScript"]
            else:
                self_.qScript = kvargs["qScript"]
        if "qMeta" in kvargs:
            if type(kvargs["qMeta"]).__name__ is self_.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(**kvargs["qMeta"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssociationScore:
    """

    Attributes
    ----------
    qFieldPairName: str
      Pair of fields.
      _< FieldName1>_ / < FieldName2>
      Where:
      < FieldName1 > is a field in the table 1 (defined in qTable1 )
      < FieldName2 > is a field in the table 2 (defined in qTable2 )
      If the field is a synthetic key, the name of the field is preceded by [Synthetic key]: .
    qScoreSummary: int
      Flag used to interpret calculated scores.
      One of the following values or sum of values that apply:

      • 0: The cardinal ratio cannot be zero but the symbol score and the row score can be zero.

      • -1: The fields do not have the same type.

      • -2: The number of rows of the field FieldName1 is zero.

      • -4: The number of distinct values of the field FieldName1 is zero.

      • -8: The number of rows of the field FieldName2 is zero.

      • -16: The number of distinct values of the field FieldName2 is zero.

      Example:
      The number of rows of the field FieldName1 is zero, and the number of distinct values of the field FieldName2 is zero, then qScoreSummary is -18.
    qField1Scores: FieldScores
      Association information about the field FieldName1 defined in qFieldPairName .
    qField2Scores: FieldScores
      Association information about the field FieldName2 defined in qFieldPairName .
    """

    qFieldPairName: str = None
    qScoreSummary: int = None
    qField1Scores: FieldScores = None
    qField2Scores: FieldScores = None

    def __init__(self_, **kvargs):
        if "qFieldPairName" in kvargs:
            if (
                type(kvargs["qFieldPairName"]).__name__
                is self_.__annotations__["qFieldPairName"]
            ):
                self_.qFieldPairName = kvargs["qFieldPairName"]
            else:
                self_.qFieldPairName = kvargs["qFieldPairName"]
        if "qScoreSummary" in kvargs:
            if (
                type(kvargs["qScoreSummary"]).__name__
                is self_.__annotations__["qScoreSummary"]
            ):
                self_.qScoreSummary = kvargs["qScoreSummary"]
            else:
                self_.qScoreSummary = kvargs["qScoreSummary"]
        if "qField1Scores" in kvargs:
            if (
                type(kvargs["qField1Scores"]).__name__
                is self_.__annotations__["qField1Scores"]
            ):
                self_.qField1Scores = kvargs["qField1Scores"]
            else:
                self_.qField1Scores = FieldScores(**kvargs["qField1Scores"])
        if "qField2Scores" in kvargs:
            if (
                type(kvargs["qField2Scores"]).__name__
                is self_.__annotations__["qField2Scores"]
            ):
                self_.qField2Scores = kvargs["qField2Scores"]
            else:
                self_.qField2Scores = FieldScores(**kvargs["qField2Scores"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BNFDef:
    """

    Attributes
    ----------
    qBnf: list[int]
      Array of token references that all together build up the definition of the current token.
      Generally, if the array is not empty, the definition is a BNF rule (_qIsBnfRule_ is set to true). However, some BNF  rules do have an empty array (_qIsBnfRule_ is set to true, but qBnf is empty).
    qNbr: int
      Number of the current token definition.
    qPNbr: int
      Number of the parent rule definition.
    qHelpId: int
      Reference identifier to a function described in the documentation. The identifier is stored in the definition of the token containing the function name.
      Is not used in Qlik Sense.
    qName: str
      Token name.
      One of:

      • A rule name

      • An identifier

      • A literal value
    qStr: str
      Literal string of the token.
      Examples: 'Round' and '('.
    qIsBnfRule: bool
      If set to true, a list of related rule tokens is assigned to qBnf .
      This parameter is optional. The default value is false.
    qScriptStatement: bool
      If set to true, the definition specifies a script statement.
      This parameter is optional. The default value is false.
    qControlStatement: bool
      If set to true, the definition specifies a control statement.
      This parameter is optional. The default value is false.
    qBnfLiteral: bool
      If set to true, the definition specifies a literal token.
      This parameter is optional. The default value is false.
    qQvFunc: bool
      If set to true, the definition is related to a Qlik Sense function. It cannot be an aggregation function.
      This parameter is optional. The default value is false.
    qAggrFunc: bool
      If set to true, the definition is related to an aggregation function.
      This parameter is optional. The default value is false.
    qFG: str
      Group of the function.

      One of:

      • ALL or FUNC_GROUP_ALL

      • U or FUNC_GROUP_UNKNOWN

      • NONE or FUNC_GROUP_NONE

      • AGGR or FUNC_GROUP_AGGR

      • NUM or FUNC_GROUP_NUMERIC

      • RNG or FUNC_GROUP_RANGE

      • EXP or FUNC_GROUP_EXPONENTIAL_AND_LOGARITHMIC

      • TRIG or FUNC_GROUP_TRIGONOMETRIC_AND_HYPERBOLIC

      • FIN or FUNC_GROUP_FINANCIAL

      • MATH or FUNC_GROUP_MATH_CONSTANT_AND_PARAM_FREE

      • COUNT or FUNC_GROUP_COUNTER

      • STR or FUNC_GROUP_STRING

      • MAPP or FUNC_GROUP_MAPPING

      • RCRD or FUNC_GROUP_INTER_RECORD

      • CND or FUNC_GROUP_CONDITIONAL

      • LOG or FUNC_GROUP_LOGICAL

      • NULL or FUNC_GROUP_NULL

      • SYS or FUNC_GROUP_SYSTEM

      • FILE or FUNC_GROUP_FILE

      • TBL or FUNC_GROUP_TABLE

      • DATE or FUNC_GROUP_DATE_AND_TIME

      • NUMI or FUNC_GROUP_NUMBER_INTERPRET

      • FRMT or FUNC_GROUP_FORMATTING

      • CLR or FUNC_GROUP_COLOR

      • RNK or FUNC_GROUP_RANKING

      • GEO or FUNC_GROUP_GEO

      • EXT or FUNC_GROUP_EXTERNAL

      • PROB or FUNC_GROUP_PROBABILITY

      • ARRAY or FUNC_GROUP_ARRAY

      • LEG or FUNC_GROUP_LEGACY
    qFieldFlag: bool
      If set to true, the definition is related to a field.
      This parameter is optional. The default value is false.
    qMT: str
      Type of the data.

      One of:

      • N or NOT_META

      • D or META_DOC_NAME

      • R or META_RET_TYPE

      • V or META_DEFAULT_VALUE
    qDepr: bool
      Indicates whether a script statement, a chart or a script function is deprecated (not recommended for use).
      If set to true, the script statement or the function is not recommended for use in Qlik Sense.
      This parameter is optional. The default value is false.
    qFGList: list[FunctionGroup]
      List of groups the function belongs to.
    """

    qBnf: list[int] = None
    qNbr: int = None
    qPNbr: int = None
    qHelpId: int = None
    qName: str = None
    qStr: str = None
    qIsBnfRule: bool = None
    qScriptStatement: bool = None
    qControlStatement: bool = None
    qBnfLiteral: bool = None
    qQvFunc: bool = None
    qAggrFunc: bool = None
    qFG: str = None
    qFieldFlag: bool = None
    qMT: str = None
    qDepr: bool = None
    qFGList: list[FunctionGroup] = None

    def __init__(self_, **kvargs):
        if "qBnf" in kvargs:
            if type(kvargs["qBnf"]).__name__ is self_.__annotations__["qBnf"]:
                self_.qBnf = kvargs["qBnf"]
            else:
                self_.qBnf = kvargs["qBnf"]
        if "qNbr" in kvargs:
            if type(kvargs["qNbr"]).__name__ is self_.__annotations__["qNbr"]:
                self_.qNbr = kvargs["qNbr"]
            else:
                self_.qNbr = kvargs["qNbr"]
        if "qPNbr" in kvargs:
            if type(kvargs["qPNbr"]).__name__ is self_.__annotations__["qPNbr"]:
                self_.qPNbr = kvargs["qPNbr"]
            else:
                self_.qPNbr = kvargs["qPNbr"]
        if "qHelpId" in kvargs:
            if type(kvargs["qHelpId"]).__name__ is self_.__annotations__["qHelpId"]:
                self_.qHelpId = kvargs["qHelpId"]
            else:
                self_.qHelpId = kvargs["qHelpId"]
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qStr" in kvargs:
            if type(kvargs["qStr"]).__name__ is self_.__annotations__["qStr"]:
                self_.qStr = kvargs["qStr"]
            else:
                self_.qStr = kvargs["qStr"]
        if "qIsBnfRule" in kvargs:
            if (
                type(kvargs["qIsBnfRule"]).__name__
                is self_.__annotations__["qIsBnfRule"]
            ):
                self_.qIsBnfRule = kvargs["qIsBnfRule"]
            else:
                self_.qIsBnfRule = kvargs["qIsBnfRule"]
        if "qScriptStatement" in kvargs:
            if (
                type(kvargs["qScriptStatement"]).__name__
                is self_.__annotations__["qScriptStatement"]
            ):
                self_.qScriptStatement = kvargs["qScriptStatement"]
            else:
                self_.qScriptStatement = kvargs["qScriptStatement"]
        if "qControlStatement" in kvargs:
            if (
                type(kvargs["qControlStatement"]).__name__
                is self_.__annotations__["qControlStatement"]
            ):
                self_.qControlStatement = kvargs["qControlStatement"]
            else:
                self_.qControlStatement = kvargs["qControlStatement"]
        if "qBnfLiteral" in kvargs:
            if (
                type(kvargs["qBnfLiteral"]).__name__
                is self_.__annotations__["qBnfLiteral"]
            ):
                self_.qBnfLiteral = kvargs["qBnfLiteral"]
            else:
                self_.qBnfLiteral = kvargs["qBnfLiteral"]
        if "qQvFunc" in kvargs:
            if type(kvargs["qQvFunc"]).__name__ is self_.__annotations__["qQvFunc"]:
                self_.qQvFunc = kvargs["qQvFunc"]
            else:
                self_.qQvFunc = kvargs["qQvFunc"]
        if "qAggrFunc" in kvargs:
            if type(kvargs["qAggrFunc"]).__name__ is self_.__annotations__["qAggrFunc"]:
                self_.qAggrFunc = kvargs["qAggrFunc"]
            else:
                self_.qAggrFunc = kvargs["qAggrFunc"]
        if "qFG" in kvargs:
            if type(kvargs["qFG"]).__name__ is self_.__annotations__["qFG"]:
                self_.qFG = kvargs["qFG"]
            else:
                self_.qFG = kvargs["qFG"]
        if "qFieldFlag" in kvargs:
            if (
                type(kvargs["qFieldFlag"]).__name__
                is self_.__annotations__["qFieldFlag"]
            ):
                self_.qFieldFlag = kvargs["qFieldFlag"]
            else:
                self_.qFieldFlag = kvargs["qFieldFlag"]
        if "qMT" in kvargs:
            if type(kvargs["qMT"]).__name__ is self_.__annotations__["qMT"]:
                self_.qMT = kvargs["qMT"]
            else:
                self_.qMT = kvargs["qMT"]
        if "qDepr" in kvargs:
            if type(kvargs["qDepr"]).__name__ is self_.__annotations__["qDepr"]:
                self_.qDepr = kvargs["qDepr"]
            else:
                self_.qDepr = kvargs["qDepr"]
        if "qFGList" in kvargs:
            if type(kvargs["qFGList"]).__name__ is self_.__annotations__["qFGList"]:
                self_.qFGList = kvargs["qFGList"]
            else:
                self_.qFGList = [FunctionGroup(**e) for e in kvargs["qFGList"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BookmarkListDef:
    """
    Defines the list of bookmarks.

    Attributes
    ----------
    qType: str
      Type of the list.
    qData: JsonObject
      Data
    """

    qType: str = None
    qData: JsonObject = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qData" in kvargs:
            if type(kvargs["qData"]).__name__ is self_.__annotations__["qData"]:
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(**kvargs["qData"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BookmarkVariableItem:
    """

    Attributes
    ----------
    qName: str
      Name of the variable.
    qValue: FieldValue
      Value of the variable.
    """

    qName: str = None
    qValue: FieldValue = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qValue" in kvargs:
            if type(kvargs["qValue"]).__name__ is self_.__annotations__["qValue"]:
                self_.qValue = kvargs["qValue"]
            else:
                self_.qValue = FieldValue(**kvargs["qValue"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ChildListDef:
    """
    Defines the list of children of a generic object.
    What is defined in ChildListDef has an impact on what the GetLayout method returns. See Example for more information.

    Attributes
    ----------
    qData: JsonObject
      Data that you want to include in the child list definition.
      You need to enter the paths to the information you want to retrieve.
    """

    qData: JsonObject = None

    def __init__(self_, **kvargs):
        if "qData" in kvargs:
            if type(kvargs["qData"]).__name__ is self_.__annotations__["qData"]:
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(**kvargs["qData"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CondDef:
    """

    Attributes
    ----------
    qAlways: bool
    qExpression: ValueExpr
    """

    qAlways: bool = True
    qExpression: ValueExpr = None

    def __init__(self_, **kvargs):
        if "qAlways" in kvargs:
            if type(kvargs["qAlways"]).__name__ is self_.__annotations__["qAlways"]:
                self_.qAlways = kvargs["qAlways"]
            else:
                self_.qAlways = kvargs["qAlways"]
        if "qExpression" in kvargs:
            if (
                type(kvargs["qExpression"]).__name__
                is self_.__annotations__["qExpression"]
            ):
                self_.qExpression = kvargs["qExpression"]
            else:
                self_.qExpression = ValueExpr(**kvargs["qExpression"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Connection:
    """

    Attributes
    ----------
    qId: str
      Identifier of the connection.
      Is generated by the engine and is unique.
    qName: str
      Name of the connection.
      This parameter is mandatory and must be set when creating or modifying a connection.
    qConnectionString: str
      One of:

      • ODBC CONNECT TO [<provider name>]

      • OLEDB CONNECT TO [<provider name>]

      • CUSTOM CONNECT TO [<provider name>]

      • "<local absolute or relative path, UNC path>"

      • "<URL>"

      Connection string.
      This parameter is mandatory and must be set when creating or modifying a connection.
    qType: str
      One of:

      • ODBC

      • OLEDB

      • <Name of the custom connection file>

      • folder

      • internet

      Type of the connection.
      This parameter is mandatory and must be set when creating or modifying a connection.
      For ODBC, OLEDB and custom connections, the engine checks that the connection type matches the connection string.
      The type is not case sensitive.
    qUserName: str
      Name of the user who creates the connection.
      This parameter is optional; it is only used for OLEDB, ODBC and CUSTOM connections.
      A call to GetConnection Method does not return the user name.
    qPassword: str
      Password of the user who creates the connection.
      This parameter is optional; it is only used for OLEDB, ODBC and CUSTOM connections.
      A call to GetConnection Method does not return the password.
    qModifiedDate: str
      Is generated by the engine.
      Creation date of the connection or last modification date of the connection.
    qMeta: NxMeta
      Information about the connection.
    qLogOn: str
      Select which user credentials to use to connect to the source.

      • LOG_ON_SERVICE_USER: Disables

      • LOG_ON_CURRENT_USER: Enables

      One of:

      • LOG_ON_SERVICE_USER

      • LOG_ON_CURRENT_USER
    """

    qId: str = None
    qName: str = None
    qConnectionString: str = None
    qType: str = None
    qUserName: str = None
    qPassword: str = None
    qModifiedDate: str = None
    qMeta: NxMeta = None
    qLogOn: str = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs:
            if type(kvargs["qId"]).__name__ is self_.__annotations__["qId"]:
                self_.qId = kvargs["qId"]
            else:
                self_.qId = kvargs["qId"]
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qConnectionString" in kvargs:
            if (
                type(kvargs["qConnectionString"]).__name__
                is self_.__annotations__["qConnectionString"]
            ):
                self_.qConnectionString = kvargs["qConnectionString"]
            else:
                self_.qConnectionString = kvargs["qConnectionString"]
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qUserName" in kvargs:
            if type(kvargs["qUserName"]).__name__ is self_.__annotations__["qUserName"]:
                self_.qUserName = kvargs["qUserName"]
            else:
                self_.qUserName = kvargs["qUserName"]
        if "qPassword" in kvargs:
            if type(kvargs["qPassword"]).__name__ is self_.__annotations__["qPassword"]:
                self_.qPassword = kvargs["qPassword"]
            else:
                self_.qPassword = kvargs["qPassword"]
        if "qModifiedDate" in kvargs:
            if (
                type(kvargs["qModifiedDate"]).__name__
                is self_.__annotations__["qModifiedDate"]
            ):
                self_.qModifiedDate = kvargs["qModifiedDate"]
            else:
                self_.qModifiedDate = kvargs["qModifiedDate"]
        if "qMeta" in kvargs:
            if type(kvargs["qMeta"]).__name__ is self_.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(**kvargs["qMeta"])
        if "qLogOn" in kvargs:
            if type(kvargs["qLogOn"]).__name__ is self_.__annotations__["qLogOn"]:
                self_.qLogOn = kvargs["qLogOn"]
            else:
                self_.qLogOn = kvargs["qLogOn"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ContentLibraryListItem:
    """

    Attributes
    ----------
    qName: str
      Name of the library.
    qAppSpecific: bool
      Is set to true if the library is specific to the app (not a global content library).
    qMeta: NxMeta
      Information about publishing and permissions.
    """

    qName: str = None
    qAppSpecific: bool = None
    qMeta: NxMeta = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qAppSpecific" in kvargs:
            if (
                type(kvargs["qAppSpecific"]).__name__
                is self_.__annotations__["qAppSpecific"]
            ):
                self_.qAppSpecific = kvargs["qAppSpecific"]
            else:
                self_.qAppSpecific = kvargs["qAppSpecific"]
        if "qMeta" in kvargs:
            if type(kvargs["qMeta"]).__name__ is self_.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(**kvargs["qMeta"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CustomConnector:
    """

    Attributes
    ----------
    qProvider: str
      Name of the custom connector file.
    qParent: str
      Name of the parent folder that contains the custom connector file.
    qDisplayName: str
      Name of the custom connector as displayed in the Qlik interface.
    qMachineMode: str
      Mode of the machine (64 or 32 bits).

      One of:

      • CONNECT_DEFAULT

      • CONNECT_64

      • CONNECT_32
    qSupportFileStreaming: bool
    """

    qProvider: str = None
    qParent: str = None
    qDisplayName: str = None
    qMachineMode: str = None
    qSupportFileStreaming: bool = None

    def __init__(self_, **kvargs):
        if "qProvider" in kvargs:
            if type(kvargs["qProvider"]).__name__ is self_.__annotations__["qProvider"]:
                self_.qProvider = kvargs["qProvider"]
            else:
                self_.qProvider = kvargs["qProvider"]
        if "qParent" in kvargs:
            if type(kvargs["qParent"]).__name__ is self_.__annotations__["qParent"]:
                self_.qParent = kvargs["qParent"]
            else:
                self_.qParent = kvargs["qParent"]
        if "qDisplayName" in kvargs:
            if (
                type(kvargs["qDisplayName"]).__name__
                is self_.__annotations__["qDisplayName"]
            ):
                self_.qDisplayName = kvargs["qDisplayName"]
            else:
                self_.qDisplayName = kvargs["qDisplayName"]
        if "qMachineMode" in kvargs:
            if (
                type(kvargs["qMachineMode"]).__name__
                is self_.__annotations__["qMachineMode"]
            ):
                self_.qMachineMode = kvargs["qMachineMode"]
            else:
                self_.qMachineMode = kvargs["qMachineMode"]
        if "qSupportFileStreaming" in kvargs:
            if (
                type(kvargs["qSupportFileStreaming"]).__name__
                is self_.__annotations__["qSupportFileStreaming"]
            ):
                self_.qSupportFileStreaming = kvargs["qSupportFileStreaming"]
            else:
                self_.qSupportFileStreaming = kvargs["qSupportFileStreaming"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DimensionListDef:
    """
    Defines the lists of dimensions.

    Attributes
    ----------
    qType: str
      Type of the list.
    qData: JsonObject
      Data
    """

    qType: str = None
    qData: JsonObject = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qData" in kvargs:
            if type(kvargs["qData"]).__name__ is self_.__annotations__["qData"]:
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(**kvargs["qData"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Doc:
    """

    Attributes
    ----------
    qType: str
      The native type of the object.
    qHandle: int
      The handle used to connect to object.
    qGenericType: str
      The type of the object.
    qGenericId: str
      Object ID.
    """

    qType: str = None
    qHandle: int = None
    qGenericType: str = None
    qGenericId: str = None
    Global: Qix = None

    def get_field(self, qFieldName: str, qStateName: str = None) -> Field:
        """
        Returns a handle to a field.


        qFieldName: str
          Name of the field.

        qStateName: str
          Name of the alternate state.
          Default state is current selections.

        """
        params = {}
        params["qFieldName"] = qFieldName
        if qStateName is not None:
            params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetField", handle, **params)["qReturn"]
        obj = Field(**response)
        obj._session = self._session
        return obj

    def get_field_description(self, qFieldName: str) -> FieldDescription:
        """
        Returns the description of a field.


        qFieldName: str
          Name of the field.

        """
        params = {}
        params["qFieldName"] = qFieldName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFieldDescription", handle, **params)[
            "qReturn"
        ]
        obj = FieldDescription(**response)
        obj._session = self._session
        return obj

    def get_variable(self, qName: str) -> GenericVariable:
        """
        Deprecated
        Returns a handle to a variable.


        qName: str
          Name of the variable.

        """
        warnings.warn("GetVariable is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetVariable", handle, **params)["qReturn"]
        obj = GenericVariable(**response)
        obj._session = self._session
        return obj

    def get_loosely_coupled_vector(self) -> list[int]:
        """
        Returns a list of table states.

        The following states apply:

        • 0 The table is not loosely coupled.

        • 1 The table is loosely coupled.

        • 2 The table is loosely coupled and cannot be changed to another state using the Qlik Engine API.

        The last three values in the vector are for internal use.

        In case of circular references, the engine automatically sets the table state to loosely coupled to avoid creating loops.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLooselyCoupledVector", handle)["qv"]
        return response

    def set_loosely_coupled_vector(self, qv: list[int]) -> bool:
        """
        Sets a list of table states, one for each table.

        The following states apply:

        • 0 The table is not loosely coupled.

        • 1 The table is loosely coupled.

        • 2 The table is loosely coupled and cannot be changed to another state using the Qlik Engine API.

        The last three values in the vector are for internal use.


        qv: list[int]
          The list of table states to set. A state will not be changed if already set to 2.

        """
        params = {}
        params["qv"] = qv
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetLooselyCoupledVector", handle, **params)[
            "qReturn"
        ]
        return response

    def evaluate(self, qExpression: str) -> str:
        """
        Evaluates an expression and returns the result as a string.

        Example:

        The client sends:
        ```
        {
        "handle": 1,
        "method": "Evaluate",
        "params": {
        "qExpression": "Sum(Holes)"
        },
        "id": 6,
        "jsonrpc": "2.0"
        }
        ```
        The engine returns:
        ```
        {
        "jsonrpc": "2.0",
        "id": 6,
        "result": {
        "qReturn": "361716"
        }
        }
        ```


        qExpression: str
          Expression to evaluate.

        """
        params = {}
        params["qExpression"] = qExpression
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Evaluate", handle, **params)["qReturn"]
        return response

    def evaluate_ex(self, qExpression: str) -> FieldValue:
        """
        Evaluates an expression and returns the result as a dual.

        Example:

        The client sends:
        ```
        {
        "handle": 1,
        "method": "EvaluateEx",
        "params": {
        "qExpression": "Sum(Holes)"
        },
        "id": 7,
        "jsonrpc": "2.0"
        }
        ```
        The engine returns:
        ```
        {
        "jsonrpc": "2.0",
        "id": 7,
        "result": {
        "qReturn": "361716"
        }
        }
        ```


        qExpression: str
          Expression to evaluate.

        """
        params = {}
        params["qExpression"] = qExpression
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("EvaluateEx", handle, **params)["qValue"]
        obj = FieldValue(**response)
        obj._session = self._session
        return obj

    def clear_all(self, qLockedAlso: bool = None, qStateName: str = None) -> object:
        """
        Clear selections in fields for current state. Locked fields are not cleared by default.


        qLockedAlso: bool
          When true, clears the selection for locked fields.

        qStateName: str
          Alternate state name. When set, applies to alternate state instead of current

        """
        params = {}
        if qLockedAlso is not None:
            params["qLockedAlso"] = qLockedAlso
        if qStateName is not None:
            params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ClearAll", handle, **params)
        return response

    def lock_all(self, qStateName: str = None) -> object:
        """
        Locks all selections in fields for current state.


        qStateName: str
          Alternate state name. When set, applies to alternate state instead of current.

        """
        params = {}
        if qStateName is not None:
            params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("LockAll", handle, **params)
        return response

    def unlock_all(self, qStateName: str = None) -> object:
        """
        Unlocks all selections in fields for current state.


        qStateName: str
          Alternate state name. When set, applies to alternate state instead of current.

        """
        params = {}
        if qStateName is not None:
            params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnlockAll", handle, **params)
        return response

    def back(self) -> object:
        """
        Loads the last logical operation (if any).


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Back", handle)
        return response

    def forward(self) -> object:
        """
        Loads the next logical operation (if any).


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Forward", handle)
        return response

    def create_variable(self, qName: str) -> bool:
        """
        Deprecated
        Creates a variable.


        qName: str
          Name of the variable. Variable names are case sensitive.

        """
        warnings.warn("CreateVariable is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateVariable", handle, **params)["qReturn"]
        return response

    def remove_variable(self, qName: str) -> bool:
        """
        Deprecated
        Removes a variable.


        qName: str
          Name of the variable. Variable names are case sensitive.

        """
        warnings.warn("RemoveVariable is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("RemoveVariable", handle, **params)["qReturn"]
        return response

    def get_locale_info(self) -> LocaleInfo:
        """
        Returns locale information.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLocaleInfo", handle)["qReturn"]
        obj = LocaleInfo(**response)
        obj._session = self._session
        return obj

    def get_tables_and_keys(
        self,
        qWindowSize: Size,
        qNullSize: Size,
        qCellHeight: int,
        qSyntheticMode: bool,
        qIncludeSysVars: bool,
        qIncludeProfiling: bool = None,
    ) -> object:
        """
        Returns:

        • The list of tables in an app and the fields inside each table.

        • The list of derived fields.

        • The list of key fields.


        qWindowSize: Size
          Size of the window that is used to display the results.

        qNullSize: Size


        qCellHeight: int
          Height of a cell in a table in pixels.

        qSyntheticMode: bool
          One of:

          • true for internal table viewer:
          Shows a more detailed view on how the Qlik engine defines the relations between fields and the quality of the keys.

          • false for source table viewer:
          Shows the natural relation between fields without reference to synthetic keys and resultant linking synthetic tables. Instead synthetic keys are represented by multiple connectors between tables.

        qIncludeSysVars: bool
          If set to true, the system variables are included.

        qIncludeProfiling: bool
          If set to true, profiling information is included.

        """
        params = {}
        params["qWindowSize"] = qWindowSize
        params["qNullSize"] = qNullSize
        params["qCellHeight"] = qCellHeight
        params["qSyntheticMode"] = qSyntheticMode
        params["qIncludeSysVars"] = qIncludeSysVars
        if qIncludeProfiling is not None:
            params["qIncludeProfiling"] = qIncludeProfiling
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetTablesAndKeys", handle, **params)
        return response

    def get_view_dlg_save_info(self) -> TableViewDlgSaveInfo:
        """
        Returns information about the position of the tables in the data model viewer.
        The position of the broom points and the position of the connection points cannot be retrieved in Qlik Sense.

        Representation of tables, broom points and connection points:

        ![](images/ui_gen_BroomConnectionPoints_dmv.png)

        The green circles represent the broom points.
        The red circle represents a connection point.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetViewDlgSaveInfo", handle)["qReturn"]
        obj = TableViewDlgSaveInfo(**response)
        obj._session = self._session
        return obj

    def set_view_dlg_save_info(self, qInfo: TableViewDlgSaveInfo) -> object:
        """
        Sets the positions of the tables in the data model viewer.
        The position of the broom points and the position of the connection points cannot be set in Qlik Sense.

        Representation of tables, broom points and connection points:

        ![](images/ui_gen_BroomConnectionPoints_dmv.png)

        The green circles represent the broom points.
        The red circle represents a connection point.


        qInfo: TableViewDlgSaveInfo
          Information about the table.

        """
        params = {}
        params["qInfo"] = qInfo
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetViewDlgSaveInfo", handle, **params)
        return response

    def get_empty_script(self, qLocalizedMainSection: str = None) -> str:
        """
        Creates a script that contains one section. This section contains SET statements that give localized information from the regional settings of the computer.
        The computer regional settings are retrieved when the engine starts.


        qLocalizedMainSection: str
          Name of the script section.
          The default value is Main .

        """
        params = {}
        if qLocalizedMainSection is not None:
            params["qLocalizedMainSection"] = qLocalizedMainSection
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetEmptyScript", handle, **params)["qReturn"]
        return response

    def do_reload(
        self, qMode: int = None, qPartial: bool = None, qDebug: bool = None
    ) -> bool:
        """
        Reloads the script that is set in an app.

        Logs:

        When this method is called, audit activity logs are produced to track the user activity.
        In the case of errors, both audit activity logs and system services logs are produced.
        The log files are named as follows:

          +----------------------------------------+----------------------------------+
          |           AUDIT ACTIVITY LOG           |        SYSTEM SERVICE LOG        |
          +----------------------------------------+----------------------------------+
          | <MachineName>_AuditActivity_Engine.txt | <MachineName>_Service_Engine.txt |
          | in Qlik Sense Enterprise               | in Qlik Sense Enterprise         |
          | <MachineName>_AuditActivity_Engine.log | <MachineName>_Service_Engine.log |
          | in Qlik Sense Desktop                  | in Qlik Sense Desktop            |
          +----------------------------------------+----------------------------------+

        Where to find the log files:

        The location of the log files depends on whether you have installed Qlik Sense Enterprise or Qlik Sense Desktop.

          +-------------------------------------+----------------------------------------+
          |        QLIK SENSE ENTERPRISE        |           QLIK SENSE DESKTOP           |
          +-------------------------------------+----------------------------------------+
          | %ProgramData%/Qlik/Sense/Log/Engine | %UserProfile%/Documents/Qlik/Sense/Log |
          +-------------------------------------+----------------------------------------+


        qMode: int
          Error handling mode
          One of:

          • 0: for default mode.

          • 1: for ABEND; the reload of the script ends if an error occurs.

          • 2: for ignore; the reload of the script continues even if an error is detected in the script.

        qPartial: bool
          Set to true for partial reload.
          The default value is false.

        qDebug: bool
          Set to true if debug breakpoints are to be honored. The execution of the script will be in debug mode.
          The default value is false.

        """
        params = {}
        if qMode is not None:
            params["qMode"] = qMode
        if qPartial is not None:
            params["qPartial"] = qPartial
        if qDebug is not None:
            params["qDebug"] = qDebug
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DoReload", handle, **params)["qReturn"]
        return response

    def get_script_breakpoints(self) -> list[EditorBreakpoint]:
        """
        Lists the breakpoints in the script of an app.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetScriptBreakpoints", handle)["qBreakpoints"]
        return [EditorBreakpoint(e) for e in response]

    def set_script_breakpoints(self, qBreakpoints: list[EditorBreakpoint]) -> object:
        """
        Set some breakpoints in the script of an app.


        qBreakpoints: list[EditorBreakpoint]
          Information about the breakpoints.

        """
        params = {}
        params["qBreakpoints"] = qBreakpoints
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetScriptBreakpoints", handle, **params)
        return response

    def get_script(self) -> str:
        """
        Gets values in script.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetScript", handle)["qScript"]
        return response

    def get_text_macros(self) -> list[TextMacro]:
        """
        Fetches updated variables after a statement execution.

        If qRefSeqNo and qSetSeqNo are set to 0, it means that the variables were not updated.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetTextMacros", handle)["qMacros"]
        return [TextMacro(e) for e in response]

    def set_fetch_limit(self, qLimit: int) -> object:
        """
        Limits the number of rows of data to load from a data source.
        This method works when reloading in debug mode.


        qLimit: int
          Fetch limit.
          Number of rows to load.

        """
        params = {}
        params["qLimit"] = qLimit
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetFetchLimit", handle, **params)
        return response

    def do_save(self, qFileName: str = None) -> object:
        """
        Saves an app. All objects and data in the data model are saved.


        qFileName: str
          Name of the file to save.

        """
        params = {}
        if qFileName is not None:
            params["qFileName"] = qFileName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DoSave", handle, **params)
        return response

    def get_table_data(
        self, qOffset: int, qRows: int, qSyntheticMode: bool, qTableName: str
    ) -> list[TableRow]:
        """
        Retrieves the data of a specific table.


        qOffset: int
          Position from the top, starting from 0.
          If the offset is set to 0, the rows starting from the position/index 0 are shown.

        qRows: int
          Number of rows to show.

        qSyntheticMode: bool
          If this parameter is set to true, the internal data/table representation is shown. Synthetic fields are present (if any).

        qTableName: str
          Name of the table.

        """
        params = {}
        params["qOffset"] = qOffset
        params["qRows"] = qRows
        params["qSyntheticMode"] = qSyntheticMode
        params["qTableName"] = qTableName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetTableData", handle, **params)["qData"]
        return [TableRow(e) for e in response]

    def get_app_layout(self) -> NxAppLayout:
        """
        Evaluates an app.
        Returns dynamic properties (if any) in addition to the engine (fixed) properties.
        A data set is returned.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAppLayout", handle)["qLayout"]
        obj = NxAppLayout(**response)
        obj._session = self._session
        return obj

    def set_app_properties(self, qProp: NxAppProperties) -> object:
        """
        Sets properties to an app.
        The qLastReloadTime, qMigrationHash and qSavedInProductVersion properties does not need to be set but if they are, they should match the current values in the app layout.


        qProp: NxAppProperties
          Information about the properties of an app.

        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetAppProperties", handle, **params)
        return response

    def get_app_properties(self) -> NxAppProperties:
        """
        Gets the properties of an app.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAppProperties", handle)["qProp"]
        obj = NxAppProperties(**response)
        obj._session = self._session
        return obj

    def get_lineage(self) -> list[LineageInfo]:
        """
        Gets the lineage information of the app. The lineage information includes the LOAD and STORE statements from the data load script associated with this app.
        An array of lineage information.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLineage", handle)["qLineage"]
        return [LineageInfo(e) for e in response]

    def create_session_object(self, qProp: GenericObjectProperties) -> GenericObject:
        """
        Creates a transient object. For example, you can use a transient object to create an app overview or a story overview.
        It is possible to create a transient object that is linked to another object.
        A linked object is an object that points to a linking object. The linking object is defined in the properties of the linked object (in qExtendsId ).
        The linked object has the same properties as the linking object.
        The linking object cannot be a transient object.


        qProp: GenericObjectProperties
          Information about the object.

        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateSessionObject", handle, **params)[
            "qReturn"
        ]
        obj = GenericObject(**response)
        obj._session = self._session
        return obj

    def destroy_session_object(self, qId: str) -> bool:
        """
        Removes a transient object.

        The operation is successful if qSuccess is set to true.


        qId: str
          Identifier of the transient object to remove.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroySessionObject", handle, **params)[
            "qSuccess"
        ]
        return response

    def create_object(self, qProp: GenericObjectProperties) -> object:
        """
        Creates a generic object at app level. For more information on generic objects, see Generic object.
        It is possible to create a generic object that is linked to another object.
        A linked object is an object that points to a linking object. The linking object is defined in the properties of the linked object (in qExtendsId ).
        The linked object has the same properties as the linking object.
        The linking object cannot be a transient object.


        qProp: GenericObjectProperties
          Information about the object.

        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateObject", handle, **params)
        return response

    def destroy_object(self, qId: str) -> bool:
        """
        Removes an app object.
        The children of the object (if any) are removed as well.

        The operation is successful if qSuccess is set to true.


        qId: str
          Identifier of the object to remove.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyObject", handle, **params)["qSuccess"]
        return response

    def get_object(self, qId: str) -> GenericObject:
        """
        Returns the type of the app object and the corresponding handle.


        qId: str
          Identifier of the object to retrieve.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetObject", handle, **params)["qReturn"]
        obj = GenericObject(**response)
        obj._session = self._session
        return obj

    def get_objects(self, qOptions: NxGetObjectOptions) -> list[NxContainerEntry]:
        """
        Returns all objects compatible with options.


        qOptions: NxGetObjectOptions
          Object type filter and requested properties.

        """
        params = {}
        params["qOptions"] = qOptions
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetObjects", handle, **params)["qList"]
        return [NxContainerEntry(e) for e in response]

    def get_bookmarks(self, qOptions: NxGetBookmarkOptions) -> list[NxContainerEntry]:
        """
        Returns all bookmarks compatible with options.


        qOptions: NxGetBookmarkOptions
          Bookmark type filter and requested properties.

        """
        params = {}
        params["qOptions"] = qOptions
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetBookmarks", handle, **params)["qList"]
        return [NxContainerEntry(e) for e in response]

    def clone_object(self, qId: str) -> str:
        """
        Clones root level objects, such as sheets and stories. The CloneObject method works for both app objects and child objects.
        When you clone an object that contains children, the children are cloned as well.
        If you for example want to clone a visualization, you must provide the qID of the root object, in this case the sheet since CloneObject clones root level objects.
        It is not possible to clone a session object.

        The identifier is set by the engine.


        qId: str
          Identifier of the object to clone. The identifier must be a root object.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CloneObject", handle, **params)["qCloneId"]
        return response

    def create_draft(self, qId: str) -> str:
        """
        Deprecated
        Creates a draft of an object.
        This method can be used to create a draft of a sheet or a story that is published. This is a way to continue working on a sheet or a story that is published.
        Replace the published object by the content of the draft by invoking the CommitDraft method.

        The identifier is set by the engine.


        qId: str
          Identifier of the object to create a draft from.

        """
        warnings.warn("CreateDraft is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateDraft", handle, **params)["qDraftId"]
        return response

    def commit_draft(self, qId: str) -> object:
        """
        Deprecated
        Commits the draft of an object that was previously created by invoking the CreateDraft method.
        Committing a draft replaces the corresponding published object.


        qId: str
          Identifier of the draft to commit.

        """
        warnings.warn("CommitDraft is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CommitDraft", handle, **params)
        return response

    def destroy_draft(self, qId: str, qSourceId: str) -> bool:
        """
        Deprecated
        Removes the draft of an object.
        The children of the draft object (if any) are removed as well.
        This method can be used to cancel the work on the draft of an object. For example, if you had created a draft of a sheet that is published, you might not want anymore to replace the published sheet.

        The operation is successful if qSuccess is set to true.


        qId: str
          Identifier of the draft object to remove.

        qSourceId: str
          Identifier of the source object (the object from which a draft was created).

        """
        warnings.warn("DestroyDraft is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qId"] = qId
        params["qSourceId"] = qSourceId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyDraft", handle, **params)["qSuccess"]
        return response

    def undo(self) -> bool:
        """
        Undoes the previous operation.

        The operation is successful if qSuccess is set to true.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Undo", handle)["qSuccess"]
        return response

    def redo(self) -> bool:
        """
        Redoes the previous operation.

        The operation is successful if qSuccess is set to true.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Redo", handle)["qSuccess"]
        return response

    def clear_undo_buffer(self) -> object:
        """
        Clears entirely the undo and redo buffer.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ClearUndoBuffer", handle)
        return response

    def create_dimension(self, qProp: GenericDimensionProperties) -> object:
        """
        Creates a master dimension.
        A master dimension is stored in the library of an app and can be used in many objects. Several generic objects can contain the same dimension.


        qProp: GenericDimensionProperties
          Information about the properties.

        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateDimension", handle, **params)
        return response

    def destroy_dimension(self, qId: str) -> bool:
        """
        Removes a dimension.

        The operation is successful if qSuccess is set to true.


        qId: str
          Identifier of the dimension to remove.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyDimension", handle, **params)["qSuccess"]
        return response

    def get_dimension(self, qId: str) -> GenericDimension:
        """
        Returns the handle of a dimension.


        qId: str
          Identifier of the dimension.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDimension", handle, **params)["qReturn"]
        obj = GenericDimension(**response)
        obj._session = self._session
        return obj

    def clone_dimension(self, qId: str) -> str:
        """
        Clones a dimension.

        The identifier is set by the engine.


        qId: str
          Identifier of the object to clone.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CloneDimension", handle, **params)["qCloneId"]
        return response

    def create_measure(self, qProp: GenericMeasureProperties) -> object:
        """
        Creates a master measure.
        A master measure is stored in the library of an app and can be used in many objects. Several generic objects can contain the same measure.


        qProp: GenericMeasureProperties
          Information about the properties.

        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateMeasure", handle, **params)
        return response

    def destroy_measure(self, qId: str) -> bool:
        """
        Removes a generic measure.

        The operation is successful if qSuccess is set to true.


        qId: str
          Identifier of the measure to remove.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyMeasure", handle, **params)["qSuccess"]
        return response

    def get_measure(self, qId: str) -> GenericMeasure:
        """
        Returns the handle of a measure.


        qId: str
          Identifier of the measure.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetMeasure", handle, **params)["qReturn"]
        obj = GenericMeasure(**response)
        obj._session = self._session
        return obj

    def clone_measure(self, qId: str) -> str:
        """
        Clones a measure.

        The identifier is set by the engine.


        qId: str
          Identifier of the object to clone.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CloneMeasure", handle, **params)["qCloneId"]
        return response

    def create_session_variable(
        self, qProp: GenericVariableProperties
    ) -> GenericVariable:
        """
        Creates a transient variable.
        To set some properties to the variable, use the SetProperties method.

        Definition:

        A variable in Qlik Sense is a named entity, containing a data value. This value can be static or be the result of a calculation. A variable acquires its value at the same time that the variable is created or after when updating the properties of the variable. Variables can be used in bookmarks and can contain numeric or alphanumeric data. Any change made to the variable is applied everywhere the variable is used.
        When a variable is used in an expression, it is substituted by its value or the variable's definition.

        Example:

        The variable x contains the text string Sum(Sales) .
        In a chart, you define the expression $(x)/12 . The effect is exactly the same as having the chart expression Sum(Sales)/12 .
        However, if you change the value of the variable x to Sum(Budget) , the data in the chart are immediately recalculated with the expression interpreted as Sum(Budget)/12 .


        qProp: GenericVariableProperties
          Name of the variable. Variable names are case sensitive.

        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateSessionVariable", handle, **params)[
            "qReturn"
        ]
        obj = GenericVariable(**response)
        obj._session = self._session
        return obj

    def destroy_session_variable(self, qId: str) -> bool:
        """
        Removes a transient variable.

        The operation is successful if qSuccess is set to true.


        qId: str
          Identifier of the variable.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroySessionVariable", handle, **params)[
            "qSuccess"
        ]
        return response

    def create_variable_ex(self, qProp: GenericVariableProperties) -> object:
        """
        Creates a variable.
        To create a variable via a script, you need to use the SetScript method. For more information, see Create a variable.
        To set some properties to the variable, use the SetProperties method.
        In a published app, only transient variables can be created. See CreateSessionVariable method.

        Definition:

        A variable in Qlik Sense is a named entity, containing a data value. This value can be static or be the result of a calculation. A variable acquires its value at the same time that the variable is created or after when updating the properties of the variable. Variables can be used in bookmarks and can contain numeric or alphanumeric data. Any change made to the variable is applied everywhere the variable is used.
        When a variable is used in an expression, it is substituted by its value or the variable's definition.

        Example:

        The variable x contains the text string Sum(Sales) .
        In a chart, you define the expression $(x)/12 . The effect is exactly the same as having the chart expression Sum(Sales)/12 .
        However, if you change the value of the variable x to Sum(Budget) , the data in the chart are immediately recalculated with the expression interpreted as Sum(Budget)/12 .


        qProp: GenericVariableProperties
          Name of the variable. Variable names are case sensitive and must be unique.

        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateVariableEx", handle, **params)
        return response

    def destroy_variable_by_id(self, qId: str) -> bool:
        """
        Removes a variable.
        Script-defined variables cannot be removed using the DestroyVariableById method or the DestroyVariableByName method. For more information, see Remove a variable.

        The operation is successful if qSuccess is set to true.


        qId: str
          Identifier of the variable.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyVariableById", handle, **params)[
            "qSuccess"
        ]
        return response

    def destroy_variable_by_name(self, qName: str) -> bool:
        """
        Removes a variable.
        Script-defined variables cannot be removed using the DestroyVariableById method or the DestroyVariableByName method. For more information, see Remove a variable.

        The operation is successful if qSuccess is set to true.


        qName: str
          Name of the variable.

        """
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyVariableByName", handle, **params)[
            "qSuccess"
        ]
        return response

    def get_variable_by_id(self, qId: str) -> GenericVariable:
        """
        Gets the handle of a variable.


        qId: str
          Identifier of the variable.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetVariableById", handle, **params)["qReturn"]
        obj = GenericVariable(**response)
        obj._session = self._session
        return obj

    def get_variable_by_name(self, qName: str) -> GenericVariable:
        """
        Gets the handle of a variable.


        qName: str
          Name of the variable.

        """
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetVariableByName", handle, **params)["qReturn"]
        obj = GenericVariable(**response)
        obj._session = self._session
        return obj

    def check_expression(self, qExpr: str, qLabels: list[str] = None) -> object:
        """
        Checks if a given expression is valid.
        The expression is correct if the parameters qErrorMsg , qBadFieldNames and qDangerousFieldNames are empty.


        qExpr: str
          Expression to check.

        qLabels: list[str]
          List of labels.

        """
        params = {}
        params["qExpr"] = qExpr
        if qLabels is not None:
            params["qLabels"] = qLabels
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CheckExpression", handle, **params)
        return response

    def check_number_or_expression(self, qExpr: str) -> object:
        """
        Checks if:

        • A given expression is valid.

        • A number is correct according to the locale.


        qExpr: str
          Expression to check.

        """
        params = {}
        params["qExpr"] = qExpr
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CheckNumberOrExpression", handle, **params)
        return response

    def add_alternate_state(self, qStateName: str) -> object:
        """
        Adds an alternate state in the app.
        You can create multiple states within a Qlik Sense app and apply these states to specific objects within the app. Objects in a given state are not affected by user selections in the other states.


        qStateName: str
          Name of the alternate state.

        """
        params = {}
        params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AddAlternateState", handle, **params)
        return response

    def remove_alternate_state(self, qStateName: str) -> object:
        """
        Removes an alternate state in the app.


        qStateName: str
          Name of the alternate state.

        """
        params = {}
        params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("RemoveAlternateState", handle, **params)
        return response

    def add_session_alternate_state(
        self, qStateName: str, qSourceStateName: str = None
    ) -> object:
        """
        Adds an session alternate state in the app.
        You can create multiple states within a Qlik Sense app and apply these states to specific objects within the app. Objects in a given state are not affected by user selections in the other states.
        A session alternate state is not persisted and is not included in the StateNames array in the AppLayout.
        You can use the optional second parameter to choose any other state to get the initial selection on the new state from


        qStateName: str
          Name of the alternate state.

        qSourceStateName: str
          Name of existing state to copy the initial selections from

        """
        params = {}
        params["qStateName"] = qStateName
        if qSourceStateName is not None:
            params["qSourceStateName"] = qSourceStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AddSessionAlternateState", handle, **params)
        return response

    def remove_session_alternate_state(self, qStateName: str) -> bool:
        """
        Removes an session alternate state in the app.
        The operation is successful if qSuccess is set to true.


        qStateName: str
          Name of the alternate state.

        """
        params = {}
        params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("RemoveSessionAlternateState", handle, **params)[
            "qSuccess"
        ]
        return response

    def create_bookmark(self, qProp: GenericBookmarkProperties) -> object:
        """
        Creates a bookmark.


        qProp: GenericBookmarkProperties
          Properties for the object.

        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateBookmark", handle, **params)
        return response

    def destroy_bookmark(self, qId: str) -> bool:
        """
        Removes a bookmark.
        The operation is successful if qSuccess is set to true.


        qId: str
          Identifier of the bookmark.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyBookmark", handle, **params)["qSuccess"]
        return response

    def get_bookmark(self, qId: str) -> GenericBookmark:
        """
        Returns the handle of a bookmark.


        qId: str
          Identifier of the bookmark.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetBookmark", handle, **params)["qReturn"]
        obj = GenericBookmark(**response)
        obj._session = self._session
        return obj

    def apply_bookmark(self, qId: str) -> bool:
        """
        Applies a bookmark.
        The operation is successful if qSuccess is set to true.


        qId: str
          Identifier of the bookmark.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyBookmark", handle, **params)["qSuccess"]
        return response

    def clone_bookmark(self, qId: str) -> str:
        """
        Clones a bookmark.
        The identifier is set by the engine.


        qId: str
          Identifier of the object to clone.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CloneBookmark", handle, **params)["qCloneId"]
        return response

    def add_field_from_expression(self, qName: str, qExpr: str) -> bool:
        """
        Adds a field on the fly.
        The expression of a field on the fly is persisted but not its values.

        The operation is successful if qSuccess is set to true.


        qName: str
          Name of the field.

        qExpr: str
          Expression value.
          It is not possible to use all aggregation functions. For example, you cannot add a field on the fly with an expression that uses the Sum or Count aggregation functions.

        """
        params = {}
        params["qName"] = qName
        params["qExpr"] = qExpr
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AddFieldFromExpression", handle, **params)[
            "qSuccess"
        ]
        return response

    def get_field_on_the_fly_by_name(self, qReadableName: str) -> str:
        """
        Find the field-on-the-fly by passing its readable name.


        qReadableName: str
          Readable name of the field-on-the-fly.

        """
        params = {}
        params["qReadableName"] = qReadableName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFieldOnTheFlyByName", handle, **params)[
            "qName"
        ]
        return response

    def get_all_infos(self) -> list[NxInfo]:
        """
        Returns the identifier and the type of any generic object in the app.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAllInfos", handle)["qInfos"]
        return [NxInfo(e) for e in response]

    def resume(self) -> object:
        """
        Resumes the app as the user left it.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Resume", handle)
        return response

    def abort_modal(self, qAccept: bool) -> object:
        """
        Aborts any selection mode in an app. For more information about selection mode, see BeginSelections method.


        qAccept: bool
          Set this parameter to true to accept the selections before exiting the selection mode.

        """
        params = {}
        params["qAccept"] = qAccept
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AbortModal", handle, **params)
        return response

    def get_matching_fields(
        self, qTags: list[str], qMatchingFieldMode: str = None
    ) -> list[NxMatchingFieldInfo]:
        """
        Retrieves any fields that match all of the specified tags or just one of them in the data model of an app.
        Tags set by Qlik Sense are prefixed by the $ sign.


        qTags: list[str]
          List of tags.
          The GetMatchingFields method looks for fields that match one or all of the tags in this list, depending on the value of qMatchingFieldMode .

        qMatchingFieldMode: str
          Matching field mode.
          The default value is MATCHINGFIELDMODE_MATCH_ALL.

          One of:

          • MATCHINGFIELDMODE_MATCH_ALL

          • MATCHINGFIELDMODE_MATCH_ONE

        """
        params = {}
        params["qTags"] = qTags
        if qMatchingFieldMode is not None:
            params["qMatchingFieldMode"] = qMatchingFieldMode
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetMatchingFields", handle, **params)[
            "qFieldNames"
        ]
        return [NxMatchingFieldInfo(e) for e in response]

    def find_matching_fields(
        self, qFieldName: str, qTags: list[str]
    ) -> list[NxMatchingFieldInfo]:
        """
        Retrieves any fields that belong to the same archipelago as the specified field and that match at least one of the specified tags.
        Tags set by Qlik Sense are prefixed by the $ sign.


        qFieldName: str
          Name of the field.
          This method looks for fields that belong to the same archipelago as this specified field.

        qTags: list[str]
          List of tags.
          This method looks for fields that match at least one of the tags in this list.

        """
        params = {}
        params["qFieldName"] = qFieldName
        params["qTags"] = qTags
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("FindMatchingFields", handle, **params)[
            "qFieldNames"
        ]
        return [NxMatchingFieldInfo(e) for e in response]

    def scramble(self, qFieldName: str) -> object:
        """
        Scrambles a field so the data is not recognizable. Some properties are retained to help debugging. For example, special characters are not changed, and small numbers are scrambled to another small number.
        Update access is required to use the function in Qlik Sense Enterprise.


        qFieldName: str
          Name of the field to scramble.

        """
        params = {}
        params["qFieldName"] = qFieldName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Scramble", handle, **params)
        return response

    def save_objects(self) -> object:
        """
        Saves all objects that were modified in the app.
        Data from the data model are not saved.
        This operation is possible only in Qlik Sense Enterprise.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SaveObjects", handle)
        return response

    def get_association_scores(
        self, qTable1: str, qTable2: str
    ) -> list[AssociationScore]:
        """
        Computes a set of association scores for each pair of fields between two given tables that have been loaded in an app.
        When a table contains some synthetic keys, all fields in the synthetic key tables are analyzed against fields in other tables. To denote that a field is a synthetic key, the field name is prefixed by [Synthetic Key]: .


        qTable1: str
          Name of the first table.

        qTable2: str
          Name of the second table.

        """
        params = {}
        params["qTable1"] = qTable1
        params["qTable2"] = qTable2
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAssociationScores", handle, **params)[
            "qScore"
        ]
        return [AssociationScore(e) for e in response]

    def get_media_list(self) -> object:
        """
        Deprecated
        Lists the media files.


        """
        warnings.warn("GetMediaList is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetMediaList", handle)
        return response

    def get_content_libraries(self) -> ContentLibraryList:
        """
        Lists the content libraries.
        To differentiate a global content library from an app specific content library, you can check the property qAppSpecific . If this property is set to true, it means that the content library is app specific.
        There is always one specific content library per app.

        Qlik Sense:

        Returns the global content libraries and the app specific content library.
        When using Qlik Sense, you can have more than one global content library. The global content libraries are common to all apps in the Qlik Sense repository.
        By default, there is one global content library named Default .

        Qlik Sense Desktop:

        Returns the global content library and the app specific content library from the disk.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetContentLibraries", handle)["qList"]
        obj = ContentLibraryList(**response)
        obj._session = self._session
        return obj

    def get_library_content(self, qName: str) -> StaticContentList:
        """
        Returns the content of a library.

        Global content library:

        In Qlik Sense Desktop, the content files are retrieved from:
        _%userprofile%\Documents\Qlik\Sense\Content\Default_
        In Qlik Sense Enterprise, the content files are retrieved from the Qlik Sense repository.

        App specific content library:

        The embedded files are returned.


        qName: str
          Name of the content library.
          It corresponds to the property qContentLibraryListItem/qName returned by the GetContentLibraries method.

        """
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLibraryContent", handle, **params)["qList"]
        obj = StaticContentList(**response)
        obj._session = self._session
        return obj

    def do_reload_ex(self, qParams: DoReloadExParams = None) -> DoReloadExResult:
        """
        Reloads the script that is set in an app and returns the path to the script log file.
        A log file is created per reload.

        Logs:

        When this method is called, audit activity logs are produced to track the user activity.
        In the case of errors, both audit activity logs and system services logs are produced.
        The log files are named as follows:

          +--------------------------+--------------------------+
          |    AUDIT ACTIVITY LOG    |    SYSTEM SERVICE LOG    |
          +--------------------------+--------------------------+
          | < MachineName>           | < MachineName> Service   |
          | AuditActivity Engine.txt | Engine.txt in Qlik       |
          | in Qlik Sense Enterprise | Sense Enterprise  <      |
          |  < MachineName>          | MachineName> Service     |
          | AuditActivity Engine.log | Engine.log in Qlik Sense |
          | in Qlik Sense Desktop    | Desktop                  |
          +--------------------------+--------------------------+

        Where to find the log files:

        The location of the log files depends on whether you have installed Qlik Sense Enterprise or Qlik Sense Desktop.

          +-------------------------------------+----------------------------------------+
          |        QLIK SENSE ENTERPRISE        |           QLIK SENSE DESKTOP           |
          +-------------------------------------+----------------------------------------+
          | %ProgramData%/Qlik/Sense/Log/Engine | %UserProfile%/Documents/Qlik/Sense/Log |
          +-------------------------------------+----------------------------------------+

        DoReloadExParams:

          +----------+--------------------------------+---------+
          |   NAME   |          DESCRIPTION           |  TYPE   |
          +----------+--------------------------------+---------+
          | qMode    | Error handling mode  One of:   | Integer |
          |          |    * 0: for default mode.  *   |         |
          |          | 1: for ABEND; the reload of    |         |
          |          | the script ends if an error    |         |
          |          | occurs.  * 2: for ignore; the  |         |
          |          | reload of the script continues |         |
          |          | even if an error is detected   |         |
          |          | in the script.                 |         |
          | qPartial | Set to true for partial        | Boolean |
          |          | reload.  The default value is  |         |
          |          | false.                         |         |
          | qDebug   | Set to true if debug           | Boolean |
          |          | breakpoints are to be honored. |         |
          |          | The execution of the script    |         |
          |          | will be in debug mode.  The    |         |
          |          | default value is false.        |         |
          +----------+--------------------------------+---------+

        DoReloadExResult:

          +----------------+--------------------------------+---------+
          |      NAME      |          DESCRIPTION           |  TYPE   |
          +----------------+--------------------------------+---------+
          | qSuccess       | The operation is successful if | Boolean |
          |                | qSuccess is set to True.       |         |
          | qScriptLogFile | Path to the script log file.   | String  |
          +----------------+--------------------------------+---------+

        If the data load has successfully finished, no matter how the indexing behaves, true is returned. This happens even if there is a timeout, a memory limit is reached or any other error occurs during the indexing.


        qParams: DoReloadExParams


        """
        params = {}
        if qParams is not None:
            params["qParams"] = qParams
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DoReloadEx", handle, **params)["qResult"]
        obj = DoReloadExResult(**response)
        obj._session = self._session
        return obj

    def back_count(self) -> int:
        """
        Returns the number of entries on the back stack.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("BackCount", handle)["qReturn"]
        return response

    def forward_count(self) -> int:
        """
        Returns the number of entries on the Forward stack.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ForwardCount", handle)["qReturn"]
        return response

    def export_reduced_data(self, qOptions: NxDownloadOptions = None) -> NxDownloadInfo:
        """
        Applies a bookmark to reduce (slice) the data on. Returns a url and file size to the reduced application. Section Access is always applied.
        This API is only available on Sense Enterprise on Windows


        qOptions: NxDownloadOptions
          BookmarkId used to reduced the app on and an expire time.

        """
        params = {}
        if qOptions is not None:
            params["qOptions"] = qOptions
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ExportReducedData", handle, **params)[
            "qDownloadInfo"
        ]
        obj = NxDownloadInfo(**response)
        obj._session = self._session
        return obj

    def get_set_analysis(self, qStateName: str = None, qBookmarkId: str = None) -> str:
        """
        Returns a set analysis expression from active selections or from a saved bookmark. Fields on the fly and Calculated dimensions will not be included in the generated expressions, instead a message indicating 'missing fields' will provided within the expression.
          | | BookmarkId empty | BookmarkId set |
          |-----------------------|--------------------------------------|----------------------------------------------------|
          |StateName empty (or $) | Default selections state is returned.| Default state ($) in bookmark with id is returned. |
          |StateName set | State selections is returned. | State in bookmark with id is returned. |


        qStateName: str
          Optional. The name of the state to get set analysis expression for. If left empty, the default state will be retrieved.

        qBookmarkId: str
          Optional. The Id of the bookmark to get the set analysis expression for. If left empty, the current selection will be retrieved.

        """
        params = {}
        if qStateName is not None:
            params["qStateName"] = qStateName
        if qBookmarkId is not None:
            params["qBookmarkId"] = qBookmarkId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetSetAnalysis", handle, **params)[
            "qSetExpression"
        ]
        return response

    def set_script(self, qScript: str) -> object:
        """
        Sets values in script.


        qScript: str
          Script content.

        """
        params = {}
        params["qScript"] = qScript
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetScript", handle, **params)
        return response

    def check_script_syntax(self) -> list[ScriptSyntaxError]:
        """
        Checks the syntax of a script.

        Example:

        "result": { "qErrors": [ { "qErrLen": 3, "qTabIx": 0, "qLineInTab": 0, "qColInLine": 0, "qTextPos": 0 }, { "qErrLen": 5, "qTabIx": 0, "qLineInTab": 0, "qColInLine": 1, "qTextPos": 4, "qSecondaryFailure": true } ] }
        The first area is the primary error area, the second area is the secondary error area. The second area is optional and is shown only if qSecondaryFailure is set to true. The second area ends when the next statement in the script begins.

        The list of syntax errors in the script.
        If there are no errors, the engine returns:
        If there are errors, the engine returns the following properties in the response:

          +-------------------+--------------------------------+---------+
          |       NAME        |          DESCRIPTION           |  TYPE   |
          +-------------------+--------------------------------+---------+
          | qErrLen           | Length of the word where the   | Integer |
          |                   | error is located.              |         |
          | qTabIx            | Number of the faulty section.  | Integer |
          | qLineInTab        | Line number in the section     | Integer |
          |                   | where the error is located.    |         |
          | qColInLine        | Position of the erroneous      | Integer |
          |                   | text from the beginning of the |         |
          |                   | line.                          |         |
          | qTextPos          | Position of the erroneous      | Integer |
          |                   | text from the beginning of the |         |
          |                   | script.                        |         |
          | qSecondaryFailure | The default value is false.    | Boolean |
          +-------------------+--------------------------------+---------+


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CheckScriptSyntax", handle)["qErrors"]
        return [ScriptSyntaxError(e) for e in response]

    def get_favorite_variables(self) -> list[str]:
        """
        Retrieves the variables that are tagged as favorite.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFavoriteVariables", handle)["qNames"]
        return response

    def set_favorite_variables(self, qNames: list[str]) -> object:
        """
        Set some variables as favorite.


        qNames: list[str]
          Variables to set as favorite.

        """
        params = {}
        params["qNames"] = qNames
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetFavoriteVariables", handle, **params)
        return response

    def get_include_file_content(self, qPath: str) -> str:
        """
        Gets the content of a file.


        qPath: str
          ["lib://CONNECTION_NAME\\\<the name of the file you want to use>.txt"]
          OR
          ["lib://Connection_Name\\\<Folder under your connection>\\\<the name of the file you want to use>.txt"]
          [ ] should be used when the first variable contains a lib reference.

        """
        params = {}
        params["qPath"] = qPath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetIncludeFileContent", handle, **params)[
            "qContent"
        ]
        return response

    def create_connection(self, qConnection: Connection) -> str:
        """
        Creates a connection.
        A connection indicates from which data source the data should be taken.


        qConnection: Connection
          Information about the connection.

        """
        params = {}
        params["qConnection"] = qConnection
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateConnection", handle, **params)[
            "qConnectionId"
        ]
        return response

    def modify_connection(
        self,
        qConnectionId: str,
        qConnection: Connection,
        qOverrideCredentials: bool = None,
    ) -> object:
        """
        Updates a connection.
        The identifier of a connection cannot be updated. qType cannot be modified with the ModifyConnection method.


        qConnectionId: str
          Identifier of the connection.

        qConnection: Connection
          Information about the connection.
          Properties that can be updated.

        qOverrideCredentials: bool
          Set this parameter to true to override the user name and password.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        params["qConnection"] = qConnection
        if qOverrideCredentials is not None:
            params["qOverrideCredentials"] = qOverrideCredentials
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ModifyConnection", handle, **params)
        return response

    def delete_connection(self, qConnectionId: str) -> object:
        """
        Deletes a connection.
        In Qlik Sense Enterprise, there is an additional file connection named AttachedFiles . The AttachedFiles connection can only be removed by the administrator of the system.


        qConnectionId: str
          Identifier of the connection to remove.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DeleteConnection", handle, **params)
        return response

    def get_connection(self, qConnectionId: str) -> Connection:
        """
        Retrieves a connection and returns:

        • The creation time of the connection.

        • The identifier of the connection.

        • The type of the connection.

        • The name of the connection.

        • The connection string.


        qConnectionId: str
          Identifier of the connection.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetConnection", handle, **params)["qConnection"]
        obj = Connection(**response)
        obj._session = self._session
        return obj

    def get_connections(self) -> list[Connection]:
        """
        Lists the connections in an app.
        In Qlik Sense Enterprise, there is an additional file connection named AttachedFiles . This connection is stored in the Qlik Sense repository.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetConnections", handle)["qConnections"]
        return [Connection(e) for e in response]

    def get_database_info(self, qConnectionId: str) -> DatabaseInfo:
        """
        Gives information about an ODBC, OLEDB or CUSTOM connection. See Outputs for more details.


        qConnectionId: str
          Name of the connection.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDatabaseInfo", handle, **params)["qInfo"]
        obj = DatabaseInfo(**response)
        obj._session = self._session
        return obj

    def get_databases(self, qConnectionId: str) -> list[Database]:
        """
        Lists the databases inside a ODBC, OLEDB or CUSTOM data source.


        qConnectionId: str
          Identifier of the connection.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDatabases", handle, **params)["qDatabases"]
        return [Database(e) for e in response]

    def get_database_owners(
        self, qConnectionId: str, qDatabase: str = None
    ) -> list[DatabaseOwner]:
        """
        Lists the owners of a database for a ODBC, OLEDB or CUSTOM connection.


        qConnectionId: str
          Identifier of the connection.

        qDatabase: str
          Name of the database.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qDatabase is not None:
            params["qDatabase"] = qDatabase
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDatabaseOwners", handle, **params)["qOwners"]
        return [DatabaseOwner(e) for e in response]

    def get_database_tables(
        self, qConnectionId: str, qDatabase: str = None, qOwner: str = None
    ) -> list[DataTable]:
        """
        Lists the tables inside a database for a ODBC, OLEDB or CUSTOM connection.


        qConnectionId: str
          Identifier of the connection.

        qDatabase: str
          Name of the database.
          If qDatabase is not set then qOwner must be set.

        qOwner: str
          Owner of the database.
          If qOwner is not set then qDatabase must be set.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qDatabase is not None:
            params["qDatabase"] = qDatabase
        if qOwner is not None:
            params["qOwner"] = qOwner
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDatabaseTables", handle, **params)["qTables"]
        return [DataTable(e) for e in response]

    def get_database_table_fields(
        self, qConnectionId: str, qDatabase: str, qOwner: str, qTable: str
    ) -> list[DataField]:
        """
        Lists the fields inside a table of a database for a ODBC, OLEDB or CUSTOM connection.


        qConnectionId: str
          Identifier of the connection.

        qDatabase: str
          Name of the database.
          If qDatabase is not set then qOwner must be set.

        qOwner: str
          Owner of the database.
          If qOwner is not set then qDatabase must be set.

        qTable: str
          Name of the table.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qDatabase is not None:
            params["qDatabase"] = qDatabase
        if qOwner is not None:
            params["qOwner"] = qOwner
        params["qTable"] = qTable
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDatabaseTableFields", handle, **params)[
            "qFields"
        ]
        return [DataField(e) for e in response]

    def get_database_table_preview(
        self,
        qConnectionId: str,
        qDatabase: str,
        qOwner: str,
        qTable: str,
        qConditions: FilterInfo,
    ) -> object:
        """
        Retrieves the values of the specified table of a database for a ODBC, OLEDB or CUSTOM connection.


        qConnectionId: str
          Identifier of the connection.

        qDatabase: str
          Name of the database.
          If qDatabase is not set then qOwner must be set.

        qOwner: str
          Owner of the database.
          If qOwner is not set then qDatabase must be set.

        qTable: str
          Name of the table.

        qConditions: FilterInfo


        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qDatabase is not None:
            params["qDatabase"] = qDatabase
        if qOwner is not None:
            params["qOwner"] = qOwner
        params["qTable"] = qTable
        if qConditions is not None:
            params["qConditions"] = qConditions
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDatabaseTablePreview", handle, **params)
        return response

    def get_folder_items_for_connection(
        self, qConnectionId: str, qRelativePath: str = None
    ) -> list[FolderItem]:
        """
        Lists the items for a folder connection.


        qConnectionId: str
          Identifier of the connection.

        qRelativePath: str
          Relative path of the connection.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qRelativePath is not None:
            params["qRelativePath"] = qRelativePath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFolderItemsForConnection", handle, **params)[
            "qFolderItems"
        ]
        return [FolderItem(e) for e in response]

    def guess_file_type(
        self, qConnectionId: str, qRelativePath: str = None
    ) -> FileDataFormat:
        """
        Guesses the data format for a given file.
        Recognized file formats are:

        • CSV for Delimited

        • FIX for Fixed Record

        • DIF for Data Interchange Format

        • EXCELBIFF_ for Microsoft Excel (XLS)

        • EXCELOOXML_ for Microsoft Excel (XLSX)

        • HTML for HTML

        • QVD for QVD file

        • XML for XML

        • QVX for QVX file

        • JSON for JSON format

        • KML for KML file

        FileType:

        Recognized file formats are:

        • CSV for Delimited

        • FIX for Fixed Record

        • DIF for Data Interchange Format

        • EXCELBIFF_ for Microsoft Excel (XLS)

        • EXCELOOXML_ for Microsoft Excel (XLSX)

        • HTML for HTML

        • QVD for QVD file

        • XML for XML

        • QVX for QVX file

        • JSON for JSON format

        • KML for KML file


        qConnectionId: str
          Identifier of the connection file.

        qRelativePath: str
          Path of the connection file.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qRelativePath is not None:
            params["qRelativePath"] = qRelativePath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GuessFileType", handle, **params)["qDataFormat"]
        obj = FileDataFormat(**response)
        obj._session = self._session
        return obj

    def get_file_tables(
        self, qConnectionId: str, qRelativePath: str, qDataFormat: FileDataFormat
    ) -> list[DataTable]:
        """
        Lists the tables for a folder connection.

        FileType:

        Recognized file formats are:

        • CSV for Delimited

        • FIX for Fixed Record

        • DIF for Data Interchange Format

        • EXCELBIFF_ for Microsoft Excel (XLS)

        • EXCELOOXML_ for Microsoft Excel (XLSX)

        • HTML for HTML

        • QVD for QVD file

        • XML for XML

        • QVX for QVX file

        • JSON for JSON format

        • KML for KML file


        qConnectionId: str
          Identifier of the connection.

        qRelativePath: str
          Path of the connection file.

        qDataFormat: FileDataFormat
          Type of the file.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qRelativePath is not None:
            params["qRelativePath"] = qRelativePath
        params["qDataFormat"] = qDataFormat
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFileTables", handle, **params)["qTables"]
        return [DataTable(e) for e in response]

    def get_file_table_fields(
        self,
        qConnectionId: str,
        qRelativePath: str,
        qDataFormat: FileDataFormat,
        qTable: str,
    ) -> object:
        """
        Lists the fields of a table for a folder connection.

        FileType:

        Recognized file formats are:

        • CSV for Delimited

        • FIX for Fixed Record

        • DIF for Data Interchange Format

        • EXCELBIFF_ for Microsoft Excel (XLS)

        • EXCELOOXML_ for Microsoft Excel (XLSX)

        • HTML for HTML

        • QVD for QVD file

        • XML for XML

        • QVX for QVX file

        • JSON for JSON format

        • KML for KML file


        qConnectionId: str
          Identifier of the connection.

        qRelativePath: str
          Path of the connection file.

        qDataFormat: FileDataFormat
          Type of the file.

        qTable: str
          Name of the table.
          This parameter must be set for XLS , XLSX , HTML   and XML files.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qRelativePath is not None:
            params["qRelativePath"] = qRelativePath
        params["qDataFormat"] = qDataFormat
        params["qTable"] = qTable
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFileTableFields", handle, **params)
        return response

    def get_file_table_preview(
        self,
        qConnectionId: str,
        qRelativePath: str,
        qDataFormat: FileDataFormat,
        qTable: str,
    ) -> object:
        """
        Lists the values in a table for a folder connection.

        FileType:

        Recognized file formats are:

        • CSV for Delimited

        • FIX for Fixed Record

        • DIF for Data Interchange Format

        • EXCELBIFF_ for Microsoft Excel (XLS)

        • EXCELOOXML_ for Microsoft Excel (XLSX)

        • HTML for HTML

        • QVD for QVD file

        • XML for XML

        • QVX for QVX file

        • JSON for JSON format

        • KML for KML file


        qConnectionId: str
          Identifier of the connection.

        qRelativePath: str
          Path of the connection file.

        qDataFormat: FileDataFormat
          Type of the file.

        qTable: str
          Name of the table.
          This parameter must be set for XLS , XLSX , HTML   and XML files.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qRelativePath is not None:
            params["qRelativePath"] = qRelativePath
        params["qDataFormat"] = qDataFormat
        params["qTable"] = qTable
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFileTablePreview", handle, **params)
        return response

    def get_file_tables_ex(
        self, qConnectionId: str, qRelativePath: str, qDataFormat: FileDataFormat
    ) -> list[DataTableEx]:
        """
        Lists the tables and fields of a JSON or XML file for a folder connection.


        qConnectionId: str
          Identifier of the connection.

        qRelativePath: str
          Path of the connection file.

        qDataFormat: FileDataFormat
          Type of the file.

        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qRelativePath is not None:
            params["qRelativePath"] = qRelativePath
        params["qDataFormat"] = qDataFormat
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFileTablesEx", handle, **params)["qTables"]
        return [DataTableEx(e) for e in response]

    def send_generic_command_to_custom_connector(
        self,
        qProvider: str,
        qCommand: str,
        qMethod: str,
        qParameters: list[str],
        qAppendConnection: str,
    ) -> str:
        """
        Sends a generic command to a custom connector.
        For more information on the commands that can be sent to a custom connector, see the QVX SDK help.


        qProvider: str
          Connector file name.
          Command to be executed by the connector.

        qCommand: str
          One of:

          • JsonRequest

          • GetCustomCaption

          • IsConnected

          • DisableQlikViewSelectButton

          • HaveStarField

        qMethod: str
          Method name to be used within the command.
          The available methods depend on the chosen connector.

        qParameters: list[str]
          Parameters of the command.
          No parameters are required.

        qAppendConnection: str
          Name of the connection.

        """
        params = {}
        params["qProvider"] = qProvider
        params["qCommand"] = qCommand
        params["qMethod"] = qMethod
        params["qParameters"] = qParameters
        params["qAppendConnection"] = qAppendConnection
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send(
            "SendGenericCommandToCustomConnector", handle, **params
        )["qResult"]
        return response

    def search_suggest(
        self, qOptions: SearchCombinationOptions, qTerms: list[str]
    ) -> SearchSuggestionResult:
        """
        Returns search terms suggestions.


        qOptions: SearchCombinationOptions
          Information about the search combinations.

        qTerms: list[str]
          Terms to search for.

        """
        params = {}
        params["qOptions"] = qOptions
        params["qTerms"] = qTerms
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SearchSuggest", handle, **params)["qResult"]
        obj = SearchSuggestionResult(**response)
        obj._session = self._session
        return obj

    def search_associations(
        self, qOptions: SearchCombinationOptions, qTerms: list[str], qPage: SearchPage
    ) -> SearchAssociationResult:
        """
        Deprecated
        Returns the search matches for one or more search terms.
        The search results depend on the search context.
        _SearchCombinationOptions_

        SearchMatchCombinations:

          +--------------------------+-------------------------------+------------------------+
          |           NAME           |          DESCRIPTION          |          TYPE          |
          +--------------------------+-------------------------------+------------------------+
          | qSearchMatchCombinations | Array of search combinations. | Array of               |
          |                          |                               | SearchMatchCombination |
          |                          |                               |                        |
          +--------------------------+-------------------------------+------------------------+


        qOptions: SearchCombinationOptions
          Information about the search fields and the search context.

        qTerms: list[str]
          List of terms to search for.

        qPage: SearchPage
          Array of pages to retrieve.

        """
        warnings.warn(
            "SearchAssociations is deprecated", DeprecationWarning, stacklevel=2
        )
        params = {}
        params["qOptions"] = qOptions
        params["qTerms"] = qTerms
        params["qPage"] = qPage
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SearchAssociations", handle, **params)[
            "qResults"
        ]
        obj = SearchAssociationResult(**response)
        obj._session = self._session
        return obj

    def select_associations(
        self,
        qOptions: SearchCombinationOptions,
        qTerms: list[str],
        qMatchIx: int,
        qSoftLock: bool = None,
    ) -> object:
        """
        Selects all search hits for a specified group.
        The results depend on the search context.
        _SearchCombinationOptions_.


        qOptions: SearchCombinationOptions
          Information about the search fields and the search context.

        qTerms: list[str]
          List of terms to search for.

        qMatchIx: int
          Index (value of qId ) of the search result to select.

        qSoftLock: bool
          This parameter is deprecated and should not be set.

        """
        params = {}
        params["qOptions"] = qOptions
        params["qTerms"] = qTerms
        params["qMatchIx"] = qMatchIx
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectAssociations", handle, **params)
        return response

    def search_results(
        self, qOptions: SearchCombinationOptions, qTerms: list[str], qPage: SearchPage
    ) -> SearchResult:
        """
        Returns the search matches for one or more search terms.
        Search results are organized in search groups. The type of search group indicates where the search matches come from (from data for example).
        Each search group contains search results that correspond to a combination of search terms.
        For example, if the search terms are organic , pasta , and America , the possible combination of search groups are:

        • organic

        • pasta

        • America

        • organic, pasta, America

        • organic, pasta

        • organic, America

        • pasta, America

        For every search group, there are one or more search group items. Each subgroup item contains results that correspond to an item type (for example a field).
        For every search group item, there are one or several search matches. The position of the match in each search result is given.


        qOptions: SearchCombinationOptions
          Information about the search combinations.

        qTerms: list[str]
          Terms to search for.

        qPage: SearchPage
          Array of pages to retrieve.

        """
        params = {}
        params["qOptions"] = qOptions
        params["qTerms"] = qTerms
        params["qPage"] = qPage
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SearchResults", handle, **params)["qResult"]
        obj = SearchResult(**response)
        obj._session = self._session
        return obj

    def search_objects(
        self, qOptions: SearchObjectOptions, qTerms: list[str], qPage: SearchPage
    ) -> SearchResult:
        """
        Returns the generic objects corresponding to one or more search terms. The search is performed within the title, subtitle, footnote and type. In addition, associated dimension values are also searched in. For example, if the country “Japan” is selected and the object contains the dimension City, the object will appear in the results for “Osaka” but not for “Johannesburg”. The generic objects with the following types will never appear in the results: slideitem , sheet , story , slide , masterobject , snapshot , LoadModel , appprops and searchhistory .


        qOptions: SearchObjectOptions
          Information about attributes.

        qTerms: list[str]
          Terms to search for.

        qPage: SearchPage
          Array of pages to retrieve.

        """
        params = {}
        params["qOptions"] = qOptions
        params["qTerms"] = qTerms
        params["qPage"] = qPage
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SearchObjects", handle, **params)["qResult"]
        obj = SearchResult(**response)
        obj._session = self._session
        return obj

    def get_field_and_column_samples(
        self,
        qFieldsOrColumnsWithWildcards: list[FieldOrColumn],
        qMaxNumberOfValues: int,
        qRandSeed: int = None,
    ) -> list[SampleResult]:
        """
        Get sample values from either a column in a table or from a field.
        Supports wildcard matches in tables or field names:
        - '*' for zero or more characters.
        - '?' for one character.


        qFieldsOrColumnsWithWildcards: list[FieldOrColumn]
          Pairs of table (optionally) and field names. Support wildcard matches.

        qMaxNumberOfValues: int
          Max number of sample values returned. Depending on the column or field size the number of returned samples can be less than MaxNumberOfValues. If MaxNumberOfValues is negative all sample values are returned.

        qRandSeed: int
          Optional. Sets the random number seed. Should only be set for test purposes.

        """
        params = {}
        params["qFieldsOrColumnsWithWildcards"] = qFieldsOrColumnsWithWildcards
        params["qMaxNumberOfValues"] = qMaxNumberOfValues
        if qRandSeed is not None:
            params["qRandSeed"] = qRandSeed
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFieldAndColumnSamples", handle, **params)[
            "qResult"
        ]
        return [SampleResult(e) for e in response]

    def get_script_ex(self) -> AppScript:
        """
        Gets script and script meta-data.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetScriptEx", handle)["qScript"]
        obj = AppScript(**response)
        obj._session = self._session
        return obj

    def get_variables(self, qListDef: VariableListDef) -> list[NxVariableListItem]:
        """


        qListDef: VariableListDef


        """
        params = {}
        params["qListDef"] = qListDef
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetVariables", handle, **params)["qList"]
        return [NxVariableListItem(e) for e in response]

    def expand_expression(self, qExpression: str) -> str:
        """
        Expands the expression.


        qExpression: str
          The expression string to expand.

        """
        params = {}
        params["qExpression"] = qExpression
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ExpandExpression", handle, **params)[
            "qExpandedExpression"
        ]
        return response

    def destroy_session_variable_by_id(self, qId: str) -> bool:
        """
        Removes a transient variable.


        •*qSuccess** is set to true if the operation is successful.


        qId: str
          Identifier of the variable.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroySessionVariableById", handle, **params)[
            "qSuccess"
        ]
        return response

    def destroy_session_variable_by_name(self, qName: str) -> bool:
        """
        Removes a transient variable.


        •*qSuccess** is set to true if the operation is successful.


        qName: str
          Name of the variable.

        """
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroySessionVariableByName", handle, **params)[
            "qSuccess"
        ]
        return response

    def create_bookmark_ex(
        self, qProp: GenericBookmarkProperties, qObjectIdsToPatch: list[str] = None
    ) -> object:
        """
        Experimental
        Creates a bookmark with softpatches.


        qProp: GenericBookmarkProperties
          Properties for the object.

        qObjectIdsToPatch: list[str]
          Add softpatches for this objects if available. If empty all softpatches are added to the bookmark.

        """
        warnings.warn("CreateBookmarkEx is experimental", UserWarning, stacklevel=2)
        params = {}
        params["qProp"] = qProp
        if qObjectIdsToPatch is not None:
            params["qObjectIdsToPatch"] = qObjectIdsToPatch
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateBookmarkEx", handle, **params)
        return response

    def save_as(self, qNewAppName: str) -> str:
        """
        Save a copy of an app with a different name.
        Can be used to save a session app as an ordinary app.


        qNewAppName: str
          <Name of the saved app>

        """
        params = {}
        params["qNewAppName"] = qNewAppName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SaveAs", handle, **params)["qNewAppId"]
        return response

    def store_temp_selection_state(self, qTTLOfTempState: int = None) -> object:
        """
        Store current selection state temporarily.
        The temporary selection state will be stored for 30min by default if TTL parameter is not present or positive.

        StoreTempSelectionState method is only supported in SaaS Editions of Qlik Sense.


        qTTLOfTempState: int
          Time to live in seconds for stored selection state

        """
        params = {}
        if qTTLOfTempState is not None:
            params["qTTLOfTempState"] = qTTLOfTempState
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("StoreTempSelectionState", handle, **params)
        return response

    def restore_temp_selection_state(self, qId: str) -> bool:
        """
        Restore a temporary selection state identified by Id.
        RestoreTempSelectionState method is only supported in SaaS Editions of Qlik Sense.


        qId: str
          Identifier of the temporary selection state

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("RestoreTempSelectionState", handle, **params)[
            "qReturn"
        ]
        return response

    def change_session_app_owner(self, qNewOwnerId: str) -> bool:
        """
        Experimental
        Change the owner of a session app.
        Can be used by a privileged user when creating a session app to be consumed by another user.
        Only useful in environments where it is possible to reconnect to a session app, currently only in cloud deployments.


        qNewOwnerId: str
          Identifier of the new app owner.

        """
        warnings.warn(
            "ChangeSessionAppOwner is experimental", UserWarning, stacklevel=2
        )
        params = {}
        params["qNewOwnerId"] = qNewOwnerId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ChangeSessionAppOwner", handle, **params)[
            "qSuccess"
        ]
        return response

    def change_session_app_space(self, qSpaceId: str) -> bool:
        """
        Experimental
        Add a session app to a space.
        Can be used by a privileged user when creating a session app to be consumed by other users.
        Only useful in environments where it is possible to reconnect to a session app, currently only in cloud deployments.


        qSpaceId: str
          Identifier of the new space.

        """
        warnings.warn(
            "ChangeSessionAppSpace is experimental", UserWarning, stacklevel=2
        )
        params = {}
        params["qSpaceId"] = qSpaceId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ChangeSessionAppSpace", handle, **params)[
            "qSuccess"
        ]
        return response

    def get_table_profile_data(self, qTableName: str) -> TableProfilingData:
        """
        Experimental
        Returns profile data for a given table.


        qTableName: str
          Name of the table

        """
        warnings.warn("GetTableProfileData is experimental", UserWarning, stacklevel=2)
        params = {}
        params["qTableName"] = qTableName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetTableProfileData", handle, **params)[
            "qProfiling"
        ]
        obj = TableProfilingData(**response)
        obj._session = self._session
        return obj

    def get_measure_with_label(self, qLabel: str) -> GenericMeasure:
        """
        Returns the handle of a measure with a label.
        If multiple measures has the same label the first is returned.


        qLabel: str
          is the label of the measure to be returned.

        """
        params = {}
        params["qLabel"] = qLabel
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetMeasureWithLabel", handle, **params)[
            "qReturn"
        ]
        obj = GenericMeasure(**response)
        obj._session = self._session
        return obj

    def search_values(
        self, qOptions: SearchValueOptions, qTerms: list[str], qPage: SearchValuePage
    ) -> SearchValueResult:
        """
        Experimental


        qOptions: SearchValueOptions


        qTerms: list[str]


        qPage: SearchValuePage


        """
        warnings.warn("SearchValues is experimental", UserWarning, stacklevel=2)
        params = {}
        params["qOptions"] = qOptions
        params["qTerms"] = qTerms
        params["qPage"] = qPage
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SearchValues", handle, **params)["qResult"]
        obj = SearchValueResult(**response)
        obj._session = self._session
        return obj

    def get_fields_from_expression(self, qExpr: str) -> list[str]:
        """
        Retrives any fields from an expression.


        qExpr: str
          Expression to get fields from.

        """
        params = {}
        params["qExpr"] = qExpr
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFieldsFromExpression", handle, **params)[
            "qFieldNames"
        ]
        return response

    def get_fields_resource_ids(
        self, qFieldNames: list[str]
    ) -> list[NxFieldResourceId]:
        """
        Returns a list of resource ids (QRI) for fields that belongs to the datamodel.
        Key fields (that belongs to multiple tables), returns one resource identifier per table.
        GetFieldsResourceIds method is only supported in SaaS Editions of Qlik Sense.


        qFieldNames: list[str]
          List of fields names that resource ids should be returned from.

        """
        params = {}
        params["qFieldNames"] = qFieldNames
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFieldsResourceIds", handle, **params)[
            "qFields"
        ]
        return [NxFieldResourceId(e) for e in response]

    def get_expression_bnf(self) -> object:
        """
        Experimental
        Gets the current Backus-Naur Form (BNF) grammar of the Qlik chart expressions supported within a given App.


        """
        warnings.warn("GetExpressionBNF is experimental", UserWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetExpressionBNF", handle)
        return response

    def get_expression_bnf_hash(self) -> str:
        """
        Experimental
        Gets a string hash calculated from the current Backus-Naur Form (BNF) grammar of the Qlik chart expressions supported within a given App.


        """
        warnings.warn("GetExpressionBNFHash is experimental", UserWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetExpressionBNFHash", handle)["qBnfHash"]
        return response

    def set_prohibit_binary_load(self, qProhibit: bool) -> object:
        """
        Prohibit binary load of this app.
        An app with prohibit binary load set cannot be loaded binary. For the setting to have effect a save is required.


        qProhibit: bool
          True or false.

        """
        params = {}
        params["qProhibit"] = qProhibit
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetProhibitBinaryLoad", handle, **params)
        return response

    def open(self, qNoData: bool = None) -> RpcSession:
        if not hasattr(self, "_session"):
            self._session = self.auth.rpc(self.attributes.id)
        session = self._session.open()
        params = {"qDocName": self.attributes.id}
        if qNoData is not None:
            params["qNoData"] = qNoData
        response = self._session.send("OpenDoc", -1, **params)["qReturn"]
        self.qGenericType = response["qType"]
        self.qGenericId = response["qGenericId"]
        self.qHandle = response["qHandle"]
        self.Global = Qix()
        self.Global._session = session
        return session

    def close(self) -> None:
        self._session.close()


@dataclass
class DocListEntry:
    """

    Attributes
    ----------
    qDocName: str
      Name of the app.
    qConnectedUsers: int
      Not used.
    qFileTime: float
      Last modified time stamp of the app.
      This property is used only with Qlik Sense Desktop.
      It is set to 0 for Qlik Sense Enterprise.
    qFileSize: float
      Size of remote app.
      This property is used only with Qlik Sense Desktop.
      It is set to 0 for Qlik Sense Enterprise.
    qDocId: str
      Identifier of the app.

      • In Qlik Sense Desktop, the identifier is the path and name of the app.

      • In Qlik Sense Enterprise, the identifier is the app's GUID.
    qMeta: NxMeta
      Meta data related to the app.
    qLastReloadTime: str
      Last reload time of the app.
    qReadOnly: bool
      If set to true, the app is read-only.
    qTitle: str
      Title of the app.
    qThumbnail: StaticContentUrl
      Thumbnail of the app.
    qHasSectionAccess: bool
      If true the app has section access configured.
    qIsDirectQueryMode: bool
      Is the app a Direct Query app?
    """

    qDocName: str = None
    qConnectedUsers: int = None
    qFileTime: float = None
    qFileSize: float = None
    qDocId: str = None
    qMeta: NxMeta = None
    qLastReloadTime: str = None
    qReadOnly: bool = None
    qTitle: str = None
    qThumbnail: StaticContentUrl = None
    qHasSectionAccess: bool = None
    qIsDirectQueryMode: bool = None

    def __init__(self_, **kvargs):
        if "qDocName" in kvargs:
            if type(kvargs["qDocName"]).__name__ is self_.__annotations__["qDocName"]:
                self_.qDocName = kvargs["qDocName"]
            else:
                self_.qDocName = kvargs["qDocName"]
        if "qConnectedUsers" in kvargs:
            if (
                type(kvargs["qConnectedUsers"]).__name__
                is self_.__annotations__["qConnectedUsers"]
            ):
                self_.qConnectedUsers = kvargs["qConnectedUsers"]
            else:
                self_.qConnectedUsers = kvargs["qConnectedUsers"]
        if "qFileTime" in kvargs:
            if type(kvargs["qFileTime"]).__name__ is self_.__annotations__["qFileTime"]:
                self_.qFileTime = kvargs["qFileTime"]
            else:
                self_.qFileTime = kvargs["qFileTime"]
        if "qFileSize" in kvargs:
            if type(kvargs["qFileSize"]).__name__ is self_.__annotations__["qFileSize"]:
                self_.qFileSize = kvargs["qFileSize"]
            else:
                self_.qFileSize = kvargs["qFileSize"]
        if "qDocId" in kvargs:
            if type(kvargs["qDocId"]).__name__ is self_.__annotations__["qDocId"]:
                self_.qDocId = kvargs["qDocId"]
            else:
                self_.qDocId = kvargs["qDocId"]
        if "qMeta" in kvargs:
            if type(kvargs["qMeta"]).__name__ is self_.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(**kvargs["qMeta"])
        if "qLastReloadTime" in kvargs:
            if (
                type(kvargs["qLastReloadTime"]).__name__
                is self_.__annotations__["qLastReloadTime"]
            ):
                self_.qLastReloadTime = kvargs["qLastReloadTime"]
            else:
                self_.qLastReloadTime = kvargs["qLastReloadTime"]
        if "qReadOnly" in kvargs:
            if type(kvargs["qReadOnly"]).__name__ is self_.__annotations__["qReadOnly"]:
                self_.qReadOnly = kvargs["qReadOnly"]
            else:
                self_.qReadOnly = kvargs["qReadOnly"]
        if "qTitle" in kvargs:
            if type(kvargs["qTitle"]).__name__ is self_.__annotations__["qTitle"]:
                self_.qTitle = kvargs["qTitle"]
            else:
                self_.qTitle = kvargs["qTitle"]
        if "qThumbnail" in kvargs:
            if (
                type(kvargs["qThumbnail"]).__name__
                is self_.__annotations__["qThumbnail"]
            ):
                self_.qThumbnail = kvargs["qThumbnail"]
            else:
                self_.qThumbnail = StaticContentUrl(**kvargs["qThumbnail"])
        if "qHasSectionAccess" in kvargs:
            if (
                type(kvargs["qHasSectionAccess"]).__name__
                is self_.__annotations__["qHasSectionAccess"]
            ):
                self_.qHasSectionAccess = kvargs["qHasSectionAccess"]
            else:
                self_.qHasSectionAccess = kvargs["qHasSectionAccess"]
        if "qIsDirectQueryMode" in kvargs:
            if (
                type(kvargs["qIsDirectQueryMode"]).__name__
                is self_.__annotations__["qIsDirectQueryMode"]
            ):
                self_.qIsDirectQueryMode = kvargs["qIsDirectQueryMode"]
            else:
                self_.qIsDirectQueryMode = kvargs["qIsDirectQueryMode"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DriveInfo:
    """

  Attributes
  ----------
  qDrive: str
    Value of the drive.
    Examples:
    C:\\\, E:\\\
  qType: str
    Type of the drive.
    _Fixed_ means physical drive.
  qName: str
    Name of the drive.
  qTypeIdentifier: str
    Information about the drive type.
    
    One of:
    
    • REMOVABLE
    
    • FIXED
    
    • NETWORK
    
    • CD_ROM
    
    • RAM
    
    • UNKNOWN_TYPE
  qUnnamedDrive: bool
  """

    qDrive: str = None
    qType: str = None
    qName: str = None
    qTypeIdentifier: str = None
    qUnnamedDrive: bool = None

    def __init__(self_, **kvargs):
        if "qDrive" in kvargs:
            if type(kvargs["qDrive"]).__name__ is self_.__annotations__["qDrive"]:
                self_.qDrive = kvargs["qDrive"]
            else:
                self_.qDrive = kvargs["qDrive"]
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qTypeIdentifier" in kvargs:
            if (
                type(kvargs["qTypeIdentifier"]).__name__
                is self_.__annotations__["qTypeIdentifier"]
            ):
                self_.qTypeIdentifier = kvargs["qTypeIdentifier"]
            else:
                self_.qTypeIdentifier = kvargs["qTypeIdentifier"]
        if "qUnnamedDrive" in kvargs:
            if (
                type(kvargs["qUnnamedDrive"]).__name__
                is self_.__annotations__["qUnnamedDrive"]
            ):
                self_.qUnnamedDrive = kvargs["qUnnamedDrive"]
            else:
                self_.qUnnamedDrive = kvargs["qUnnamedDrive"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ErrorData:
    """

    Attributes
    ----------
    qErrorString: str
      Detailed information about the error message.
    qLineEnd: str
      Line termination characters.
    qLine: str
      Script statement where the error occurs.
    qErrorDataCode: str
      Type of the error messages.

      One of:

      • EDC_ERROR

      • EDC_WARNING

      • EDC_CIRCULAR_REFERENCE
    qMessage: ProgressMessage
    """

    qErrorString: str = None
    qLineEnd: str = None
    qLine: str = None
    qErrorDataCode: str = None
    qMessage: ProgressMessage = None

    def __init__(self_, **kvargs):
        if "qErrorString" in kvargs:
            if (
                type(kvargs["qErrorString"]).__name__
                is self_.__annotations__["qErrorString"]
            ):
                self_.qErrorString = kvargs["qErrorString"]
            else:
                self_.qErrorString = kvargs["qErrorString"]
        if "qLineEnd" in kvargs:
            if type(kvargs["qLineEnd"]).__name__ is self_.__annotations__["qLineEnd"]:
                self_.qLineEnd = kvargs["qLineEnd"]
            else:
                self_.qLineEnd = kvargs["qLineEnd"]
        if "qLine" in kvargs:
            if type(kvargs["qLine"]).__name__ is self_.__annotations__["qLine"]:
                self_.qLine = kvargs["qLine"]
            else:
                self_.qLine = kvargs["qLine"]
        if "qErrorDataCode" in kvargs:
            if (
                type(kvargs["qErrorDataCode"]).__name__
                is self_.__annotations__["qErrorDataCode"]
            ):
                self_.qErrorDataCode = kvargs["qErrorDataCode"]
            else:
                self_.qErrorDataCode = kvargs["qErrorDataCode"]
        if "qMessage" in kvargs:
            if type(kvargs["qMessage"]).__name__ is self_.__annotations__["qMessage"]:
                self_.qMessage = kvargs["qMessage"]
            else:
                self_.qMessage = ProgressMessage(**kvargs["qMessage"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ExpansionData:
    """

    Attributes
    ----------
    qExcludeList: bool
    qPos: PositionMark
    """

    qExcludeList: bool = None
    qPos: PositionMark = None

    def __init__(self_, **kvargs):
        if "qExcludeList" in kvargs:
            if (
                type(kvargs["qExcludeList"]).__name__
                is self_.__annotations__["qExcludeList"]
            ):
                self_.qExcludeList = kvargs["qExcludeList"]
            else:
                self_.qExcludeList = kvargs["qExcludeList"]
        if "qPos" in kvargs:
            if type(kvargs["qPos"]).__name__ is self_.__annotations__["qPos"]:
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = PositionMark(**kvargs["qPos"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ExtendedLayoutBookmarkData:
    """

    Attributes
    ----------
    qId: str
    qActive: bool
    qShowMode: int
    qScrollPos: ScrollPosition
    qExpansionInfo: list[ExpansionData]
    qLeftCollapsed: bool
    qTopCollapsed: bool
    qSortData: list[InterFieldSortData]
    qDimensionGroupPos: list[GroupStateInfo]
    qExpressionGroupPos: list[GroupStateInfo]
    qUseGraphMode: bool
    qGraphMode: str
      One of:

      • GRAPH_MODE_BAR

      • GRAPH_MODE_PIE

      • GRAPH_MODE_PIVOTTABLE

      • GRAPH_MODE_SCATTER

      • GRAPH_MODE_LINE

      • GRAPH_MODE_STRAIGHTTABLE

      • GRAPH_MODE_COMBO

      • GRAPH_MODE_RADAR

      • GRAPH_MODE_GAUGE

      • GRAPH_MODE_GRID

      • GRAPH_MODE_BLOCK

      • GRAPH_MODE_FUNNEL

      • GRAPH_MODE_MEKKO

      • GRAPH_MODE_LAST
    qActiveContainerChildObjectId: str
    qExtendedPivotState: ExtendedPivotStateData
    """

    qId: str = None
    qActive: bool = None
    qShowMode: int = None
    qScrollPos: ScrollPosition = None
    qExpansionInfo: list[ExpansionData] = None
    qLeftCollapsed: bool = None
    qTopCollapsed: bool = None
    qSortData: list[InterFieldSortData] = None
    qDimensionGroupPos: list[GroupStateInfo] = None
    qExpressionGroupPos: list[GroupStateInfo] = None
    qUseGraphMode: bool = None
    qGraphMode: str = None
    qActiveContainerChildObjectId: str = None
    qExtendedPivotState: ExtendedPivotStateData = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs:
            if type(kvargs["qId"]).__name__ is self_.__annotations__["qId"]:
                self_.qId = kvargs["qId"]
            else:
                self_.qId = kvargs["qId"]
        if "qActive" in kvargs:
            if type(kvargs["qActive"]).__name__ is self_.__annotations__["qActive"]:
                self_.qActive = kvargs["qActive"]
            else:
                self_.qActive = kvargs["qActive"]
        if "qShowMode" in kvargs:
            if type(kvargs["qShowMode"]).__name__ is self_.__annotations__["qShowMode"]:
                self_.qShowMode = kvargs["qShowMode"]
            else:
                self_.qShowMode = kvargs["qShowMode"]
        if "qScrollPos" in kvargs:
            if (
                type(kvargs["qScrollPos"]).__name__
                is self_.__annotations__["qScrollPos"]
            ):
                self_.qScrollPos = kvargs["qScrollPos"]
            else:
                self_.qScrollPos = ScrollPosition(**kvargs["qScrollPos"])
        if "qExpansionInfo" in kvargs:
            if (
                type(kvargs["qExpansionInfo"]).__name__
                is self_.__annotations__["qExpansionInfo"]
            ):
                self_.qExpansionInfo = kvargs["qExpansionInfo"]
            else:
                self_.qExpansionInfo = [
                    ExpansionData(**e) for e in kvargs["qExpansionInfo"]
                ]
        if "qLeftCollapsed" in kvargs:
            if (
                type(kvargs["qLeftCollapsed"]).__name__
                is self_.__annotations__["qLeftCollapsed"]
            ):
                self_.qLeftCollapsed = kvargs["qLeftCollapsed"]
            else:
                self_.qLeftCollapsed = kvargs["qLeftCollapsed"]
        if "qTopCollapsed" in kvargs:
            if (
                type(kvargs["qTopCollapsed"]).__name__
                is self_.__annotations__["qTopCollapsed"]
            ):
                self_.qTopCollapsed = kvargs["qTopCollapsed"]
            else:
                self_.qTopCollapsed = kvargs["qTopCollapsed"]
        if "qSortData" in kvargs:
            if type(kvargs["qSortData"]).__name__ is self_.__annotations__["qSortData"]:
                self_.qSortData = kvargs["qSortData"]
            else:
                self_.qSortData = [InterFieldSortData(**e) for e in kvargs["qSortData"]]
        if "qDimensionGroupPos" in kvargs:
            if (
                type(kvargs["qDimensionGroupPos"]).__name__
                is self_.__annotations__["qDimensionGroupPos"]
            ):
                self_.qDimensionGroupPos = kvargs["qDimensionGroupPos"]
            else:
                self_.qDimensionGroupPos = [
                    GroupStateInfo(**e) for e in kvargs["qDimensionGroupPos"]
                ]
        if "qExpressionGroupPos" in kvargs:
            if (
                type(kvargs["qExpressionGroupPos"]).__name__
                is self_.__annotations__["qExpressionGroupPos"]
            ):
                self_.qExpressionGroupPos = kvargs["qExpressionGroupPos"]
            else:
                self_.qExpressionGroupPos = [
                    GroupStateInfo(**e) for e in kvargs["qExpressionGroupPos"]
                ]
        if "qUseGraphMode" in kvargs:
            if (
                type(kvargs["qUseGraphMode"]).__name__
                is self_.__annotations__["qUseGraphMode"]
            ):
                self_.qUseGraphMode = kvargs["qUseGraphMode"]
            else:
                self_.qUseGraphMode = kvargs["qUseGraphMode"]
        if "qGraphMode" in kvargs:
            if (
                type(kvargs["qGraphMode"]).__name__
                is self_.__annotations__["qGraphMode"]
            ):
                self_.qGraphMode = kvargs["qGraphMode"]
            else:
                self_.qGraphMode = kvargs["qGraphMode"]
        if "qActiveContainerChildObjectId" in kvargs:
            if (
                type(kvargs["qActiveContainerChildObjectId"]).__name__
                is self_.__annotations__["qActiveContainerChildObjectId"]
            ):
                self_.qActiveContainerChildObjectId = kvargs[
                    "qActiveContainerChildObjectId"
                ]
            else:
                self_.qActiveContainerChildObjectId = kvargs[
                    "qActiveContainerChildObjectId"
                ]
        if "qExtendedPivotState" in kvargs:
            if (
                type(kvargs["qExtendedPivotState"]).__name__
                is self_.__annotations__["qExtendedPivotState"]
            ):
                self_.qExtendedPivotState = kvargs["qExtendedPivotState"]
            else:
                self_.qExtendedPivotState = ExtendedPivotStateData(
                    **kvargs["qExtendedPivotState"]
                )
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Field:
    """

    Attributes
    ----------
    qType: str
      The native type of the object.
    qHandle: int
      The handle used to connect to object.
    qGenericType: str
      The type of the object.
    qGenericId: str
      Object ID.
    """

    qType: str = None
    qHandle: int = None
    qGenericType: str = None
    qGenericId: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qHandle" in kvargs:
            if type(kvargs["qHandle"]).__name__ is self_.__annotations__["qHandle"]:
                self_.qHandle = kvargs["qHandle"]
            else:
                self_.qHandle = kvargs["qHandle"]
        if "qGenericType" in kvargs:
            if (
                type(kvargs["qGenericType"]).__name__
                is self_.__annotations__["qGenericType"]
            ):
                self_.qGenericType = kvargs["qGenericType"]
            else:
                self_.qGenericType = kvargs["qGenericType"]
        if "qGenericId" in kvargs:
            if (
                type(kvargs["qGenericId"]).__name__
                is self_.__annotations__["qGenericId"]
            ):
                self_.qGenericId = kvargs["qGenericId"]
            else:
                self_.qGenericId = kvargs["qGenericId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_cardinal(self) -> int:
        """
        Retrieves the number of distinct values in a field.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetCardinal", handle)["qReturn"]
        return response

    def get_and_mode(self) -> bool:
        """
        Returns the AND mode status of a field.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAndMode", handle)["qReturn"]
        return response

    def select_values(
        self,
        qFieldValues: list[FieldValue],
        qToggleMode: bool = None,
        qSoftLock: bool = None,
    ) -> bool:
        """
        Selects some values in a field, by entering the values to select.


        qFieldValues: list[FieldValue]
          List of the values to select.

        qToggleMode: bool
          The default value is false.

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        params["qFieldValues"] = qFieldValues
        if qToggleMode is not None:
            params["qToggleMode"] = qToggleMode
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectValues", handle, **params)["qReturn"]
        return response

    def select(
        self, qMatch: str, qSoftLock: bool = None, qExcludedValuesMode: int = None
    ) -> bool:
        """
        Selects field values matching a search string.


        qMatch: str
          String to search for.
          Can contain wild cards or numeric search criteria.

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        qExcludedValuesMode: int
          Include excluded values in search.

        """
        params = {}
        params["qMatch"] = qMatch
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        if qExcludedValuesMode is not None:
            params["qExcludedValuesMode"] = qExcludedValuesMode
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Select", handle, **params)["qReturn"]
        return response

    def toggle_select(
        self, qMatch: str, qSoftLock: bool = None, qExcludedValuesMode: int = None
    ) -> bool:
        """
        Toggle selects field values matching a search string.


        qMatch: str
          String to search for.
          Can contain wild cards or numeric search criteria.

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        qExcludedValuesMode: int
          Include excluded values in search.

        """
        params = {}
        params["qMatch"] = qMatch
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        if qExcludedValuesMode is not None:
            params["qExcludedValuesMode"] = qExcludedValuesMode
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ToggleSelect", handle, **params)["qReturn"]
        return response

    def clear_all_but_this(self, qSoftLock: bool = None) -> bool:
        """
        Maintains the selections in the current field while clearing the selections in the other fields.


        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ClearAllButThis", handle, **params)["qReturn"]
        return response

    def select_possible(self, qSoftLock: bool = None) -> bool:
        """
        Selects all possible values in a specific field.


        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectPossible", handle, **params)["qReturn"]
        return response

    def select_excluded(self, qSoftLock: bool = None) -> bool:
        """
        Inverts the current selections.


        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectExcluded", handle, **params)["qReturn"]
        return response

    def select_all(self, qSoftLock: bool = None) -> bool:
        """
        Selects all values of a field. Excluded values are also selected.


        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectAll", handle, **params)["qReturn"]
        return response

    def lock(self) -> bool:
        """
        Locks all selected values of a specific field.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Lock", handle)["qReturn"]
        return response

    def unlock(self) -> bool:
        """
        Unlocks all selected values of a specific field if the target (or handle ) is a field.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Unlock", handle)["qReturn"]
        return response

    def get_nx_properties(self) -> NxFieldProperties:
        """
        Gets the properties of a field.

        The property OneAndOnlyOne is set to true if one and only value has been selected in the field prior setting the property.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetNxProperties", handle)["qProperties"]
        obj = NxFieldProperties(**response)
        obj._session = self._session
        return obj

    def set_nx_properties(self, qProperties: NxFieldProperties) -> object:
        """
        Sets some properties to a field.


        qProperties: NxFieldProperties
          Information about the properties of the field.

        """
        params = {}
        params["qProperties"] = qProperties
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetNxProperties", handle, **params)
        return response

    def set_and_mode(self, qAndMode: bool) -> object:
        """
        Sets a field in the AND mode.


        qAndMode: bool
          Specifies if the AND mode applies to the field.
          Set this parameter to true to enter the AND mode.

        """
        params = {}
        params["qAndMode"] = qAndMode
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetAndMode", handle, **params)
        return response

    def select_alternative(self, qSoftLock: bool = None) -> bool:
        """
        Selects all alternatives values in a specific field.
        In a field that contains at least one selected value, the values that are neither selected nor excluded are alternatives values.


        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectAlternative", handle, **params)["qReturn"]
        return response

    def low_level_select(
        self, qValues: list[int], qToggleMode: bool, qSoftLock: bool = None
    ) -> bool:
        """
        Selects some values in a field, by entering the element numbers related to the values to select.


        qValues: list[int]
          Indexes (or element numbers) of the values to select.

        qToggleMode: bool
          Set to true to keep any selections present in the list object.
          If this parameter is set to false, selections made before accepting the list object search become alternative.

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        params["qValues"] = qValues
        params["qToggleMode"] = qToggleMode
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("LowLevelSelect", handle, **params)["qReturn"]
        return response

    def clear(self) -> bool:
        """
        Clears the selections in a specific field.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Clear", handle)["qReturn"]
        return response


@dataclass
class FieldDefEx:
    """

    Attributes
    ----------
    qName: str
      Name of the field.
    qType: str
      Type of data entity.

      One of:

      • NOT_PRESENT

      • PRESENT

      • IS_CYCLIC_GROUP

      • IS_DRILL_GROUP

      • IS_VAR

      • IS_EXPR

      • IS_IMPLICIT

      • IS_DETAIL
    """

    qName: str = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldInTableData:
    """

    Attributes
    ----------
    qName: str
      Name of the field.
    qOriginalFields: list[str]
      Is shown for fixed records.
      _qOriginalFieldName_ and qName are identical if no field names are used in the file.
      _qOriginalFieldName_ differs from qName if embedded file names are used in the file.
    qPresent: bool
    qHasNull: bool
      This property is set to true if the field contains some Null values.
    qHasWild: bool
    qHasDuplicates: bool
      This property is set to true if the field contains some duplicate values.
    qIsSynthetic: bool
      This property is set to true if the field contains a synthetic key.
    qInformationDensity: float
      Number of records that have values (for example, not NULL) in the field as compared to the total number of records in the table.
    qnNonNulls: int
      Number of values that are non Null.
    qnRows: int
      Number of rows in the field.
    qSubsetRatio: float
      Number of distinct values in the field (in the current table) as compared to the total number of distinct values of this field (in all tables).
    qnTotalDistinctValues: int
      Number of distinct values in the field.
    qnPresentDistinctValues: int
    qKeyType: str
      Tells if the field is a key field.

      One of:

      • NOT_KEY

      • ANY_KEY

      • PRIMARY_KEY

      • PERFECT_KEY
    qComment: str
      Comment related to the field.
    qTags: list[str]
      List of tags related to the field.
    qDerivedFields: list[DerivedFieldsInTableData]
      List of the derived fields.
    qIsFieldOnTheFly: bool
    qReadableName: str
    """

    qName: str = None
    qOriginalFields: list[str] = None
    qPresent: bool = None
    qHasNull: bool = None
    qHasWild: bool = None
    qHasDuplicates: bool = None
    qIsSynthetic: bool = None
    qInformationDensity: float = None
    qnNonNulls: int = None
    qnRows: int = None
    qSubsetRatio: float = None
    qnTotalDistinctValues: int = None
    qnPresentDistinctValues: int = None
    qKeyType: str = None
    qComment: str = None
    qTags: list[str] = None
    qDerivedFields: list[DerivedFieldsInTableData] = None
    qIsFieldOnTheFly: bool = None
    qReadableName: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qOriginalFields" in kvargs:
            if (
                type(kvargs["qOriginalFields"]).__name__
                is self_.__annotations__["qOriginalFields"]
            ):
                self_.qOriginalFields = kvargs["qOriginalFields"]
            else:
                self_.qOriginalFields = kvargs["qOriginalFields"]
        if "qPresent" in kvargs:
            if type(kvargs["qPresent"]).__name__ is self_.__annotations__["qPresent"]:
                self_.qPresent = kvargs["qPresent"]
            else:
                self_.qPresent = kvargs["qPresent"]
        if "qHasNull" in kvargs:
            if type(kvargs["qHasNull"]).__name__ is self_.__annotations__["qHasNull"]:
                self_.qHasNull = kvargs["qHasNull"]
            else:
                self_.qHasNull = kvargs["qHasNull"]
        if "qHasWild" in kvargs:
            if type(kvargs["qHasWild"]).__name__ is self_.__annotations__["qHasWild"]:
                self_.qHasWild = kvargs["qHasWild"]
            else:
                self_.qHasWild = kvargs["qHasWild"]
        if "qHasDuplicates" in kvargs:
            if (
                type(kvargs["qHasDuplicates"]).__name__
                is self_.__annotations__["qHasDuplicates"]
            ):
                self_.qHasDuplicates = kvargs["qHasDuplicates"]
            else:
                self_.qHasDuplicates = kvargs["qHasDuplicates"]
        if "qIsSynthetic" in kvargs:
            if (
                type(kvargs["qIsSynthetic"]).__name__
                is self_.__annotations__["qIsSynthetic"]
            ):
                self_.qIsSynthetic = kvargs["qIsSynthetic"]
            else:
                self_.qIsSynthetic = kvargs["qIsSynthetic"]
        if "qInformationDensity" in kvargs:
            if (
                type(kvargs["qInformationDensity"]).__name__
                is self_.__annotations__["qInformationDensity"]
            ):
                self_.qInformationDensity = kvargs["qInformationDensity"]
            else:
                self_.qInformationDensity = kvargs["qInformationDensity"]
        if "qnNonNulls" in kvargs:
            if (
                type(kvargs["qnNonNulls"]).__name__
                is self_.__annotations__["qnNonNulls"]
            ):
                self_.qnNonNulls = kvargs["qnNonNulls"]
            else:
                self_.qnNonNulls = kvargs["qnNonNulls"]
        if "qnRows" in kvargs:
            if type(kvargs["qnRows"]).__name__ is self_.__annotations__["qnRows"]:
                self_.qnRows = kvargs["qnRows"]
            else:
                self_.qnRows = kvargs["qnRows"]
        if "qSubsetRatio" in kvargs:
            if (
                type(kvargs["qSubsetRatio"]).__name__
                is self_.__annotations__["qSubsetRatio"]
            ):
                self_.qSubsetRatio = kvargs["qSubsetRatio"]
            else:
                self_.qSubsetRatio = kvargs["qSubsetRatio"]
        if "qnTotalDistinctValues" in kvargs:
            if (
                type(kvargs["qnTotalDistinctValues"]).__name__
                is self_.__annotations__["qnTotalDistinctValues"]
            ):
                self_.qnTotalDistinctValues = kvargs["qnTotalDistinctValues"]
            else:
                self_.qnTotalDistinctValues = kvargs["qnTotalDistinctValues"]
        if "qnPresentDistinctValues" in kvargs:
            if (
                type(kvargs["qnPresentDistinctValues"]).__name__
                is self_.__annotations__["qnPresentDistinctValues"]
            ):
                self_.qnPresentDistinctValues = kvargs["qnPresentDistinctValues"]
            else:
                self_.qnPresentDistinctValues = kvargs["qnPresentDistinctValues"]
        if "qKeyType" in kvargs:
            if type(kvargs["qKeyType"]).__name__ is self_.__annotations__["qKeyType"]:
                self_.qKeyType = kvargs["qKeyType"]
            else:
                self_.qKeyType = kvargs["qKeyType"]
        if "qComment" in kvargs:
            if type(kvargs["qComment"]).__name__ is self_.__annotations__["qComment"]:
                self_.qComment = kvargs["qComment"]
            else:
                self_.qComment = kvargs["qComment"]
        if "qTags" in kvargs:
            if type(kvargs["qTags"]).__name__ is self_.__annotations__["qTags"]:
                self_.qTags = kvargs["qTags"]
            else:
                self_.qTags = kvargs["qTags"]
        if "qDerivedFields" in kvargs:
            if (
                type(kvargs["qDerivedFields"]).__name__
                is self_.__annotations__["qDerivedFields"]
            ):
                self_.qDerivedFields = kvargs["qDerivedFields"]
            else:
                self_.qDerivedFields = [
                    DerivedFieldsInTableData(**e) for e in kvargs["qDerivedFields"]
                ]
        if "qIsFieldOnTheFly" in kvargs:
            if (
                type(kvargs["qIsFieldOnTheFly"]).__name__
                is self_.__annotations__["qIsFieldOnTheFly"]
            ):
                self_.qIsFieldOnTheFly = kvargs["qIsFieldOnTheFly"]
            else:
                self_.qIsFieldOnTheFly = kvargs["qIsFieldOnTheFly"]
        if "qReadableName" in kvargs:
            if (
                type(kvargs["qReadableName"]).__name__
                is self_.__annotations__["qReadableName"]
            ):
                self_.qReadableName = kvargs["qReadableName"]
            else:
                self_.qReadableName = kvargs["qReadableName"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FileDataFormat:
    """
    FileType:

    Recognized file formats are:

    • CSV for Delimited

    • FIX for Fixed Record

    • DIF for Data Interchange Format

    • EXCELBIFF_ for Microsoft Excel (XLS)

    • EXCELOOXML_ for Microsoft Excel (XLSX)

    • HTML for HTML

    • QVD for QVD file

    • XML for XML

    • QVX for QVX file

    • JSON for JSON format

    • KML for KML file

    Attributes
    ----------
    qType: str
      Type of the file.

      One of:

      • CSV or FILE_TYPE_CSV

      • FIX or FILE_TYPE_FIX

      • DIF or FILE_TYPE_DIF

      • EXCEL_BIFF or FILE_TYPE_EXCEL_BIFF

      • EXCEL_OOXML or FILE_TYPE_EXCEL_OOXML

      • HTML or FILE_TYPE_HTML

      • QVD or FILE_TYPE_QVD

      • XML or FILE_TYPE_XML

      • QVX or FILE_TYPE_QVX

      • JSON or FILE_TYPE_JSON

      • KML or FILE_TYPE_KML
    qLabel: str
      One of:

      • Embedded labels (field names are present in the file)

      • No labels

      • Explicit labels (for DIFfiles)
    qQuote: str
      One of:

      • None (no quotes)

      • MSQ (Modern Style Quoting)

      • Standard (quotes " " or ' ' can be used, but only if they are the first and last non blank characters of a field value)

      This property is used for delimited files.
    qComment: str
      String that marks the beginning of the comment line.
      Example: “

      ” or “//”:

      The engine ignores the commented lines during the data load.
      This property is only used for delimited files.
    qDelimiter: DelimiterInfo
      Information about the delimiter.
      This property is used for delimited files.
    qCodePage: int
      Character set used in the file.
    qHeaderSize: int
      Size of the header.
      Example: If the header size is 2, the first two rows in the file are considered as header and not as data. The header can contain the field names.
    qRecordSize: int
      Record length.
      Each record (row of data) contains a number of columns with a fixed field size.
      This property is used for fixed record data files.
    qTabSize: int
      Number of spaces that one tab character represents in the table file.
      This property is used for fixed record data files.
    qIgnoreEOF: bool
      Is set to true, the end-of-file character is not taken into account during reload.
      This property is used for delimited files and fixed record data files.
    qFixedWidthDelimiters: str
      Positions of the field breaks in the table.
      This property is used for fixed record data files.
    """

    qType: str = None
    qLabel: str = None
    qQuote: str = None
    qComment: str = None
    qDelimiter: DelimiterInfo = None
    qCodePage: int = None
    qHeaderSize: int = None
    qRecordSize: int = None
    qTabSize: int = None
    qIgnoreEOF: bool = None
    qFixedWidthDelimiters: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qLabel" in kvargs:
            if type(kvargs["qLabel"]).__name__ is self_.__annotations__["qLabel"]:
                self_.qLabel = kvargs["qLabel"]
            else:
                self_.qLabel = kvargs["qLabel"]
        if "qQuote" in kvargs:
            if type(kvargs["qQuote"]).__name__ is self_.__annotations__["qQuote"]:
                self_.qQuote = kvargs["qQuote"]
            else:
                self_.qQuote = kvargs["qQuote"]
        if "qComment" in kvargs:
            if type(kvargs["qComment"]).__name__ is self_.__annotations__["qComment"]:
                self_.qComment = kvargs["qComment"]
            else:
                self_.qComment = kvargs["qComment"]
        if "qDelimiter" in kvargs:
            if (
                type(kvargs["qDelimiter"]).__name__
                is self_.__annotations__["qDelimiter"]
            ):
                self_.qDelimiter = kvargs["qDelimiter"]
            else:
                self_.qDelimiter = DelimiterInfo(**kvargs["qDelimiter"])
        if "qCodePage" in kvargs:
            if type(kvargs["qCodePage"]).__name__ is self_.__annotations__["qCodePage"]:
                self_.qCodePage = kvargs["qCodePage"]
            else:
                self_.qCodePage = kvargs["qCodePage"]
        if "qHeaderSize" in kvargs:
            if (
                type(kvargs["qHeaderSize"]).__name__
                is self_.__annotations__["qHeaderSize"]
            ):
                self_.qHeaderSize = kvargs["qHeaderSize"]
            else:
                self_.qHeaderSize = kvargs["qHeaderSize"]
        if "qRecordSize" in kvargs:
            if (
                type(kvargs["qRecordSize"]).__name__
                is self_.__annotations__["qRecordSize"]
            ):
                self_.qRecordSize = kvargs["qRecordSize"]
            else:
                self_.qRecordSize = kvargs["qRecordSize"]
        if "qTabSize" in kvargs:
            if type(kvargs["qTabSize"]).__name__ is self_.__annotations__["qTabSize"]:
                self_.qTabSize = kvargs["qTabSize"]
            else:
                self_.qTabSize = kvargs["qTabSize"]
        if "qIgnoreEOF" in kvargs:
            if (
                type(kvargs["qIgnoreEOF"]).__name__
                is self_.__annotations__["qIgnoreEOF"]
            ):
                self_.qIgnoreEOF = kvargs["qIgnoreEOF"]
            else:
                self_.qIgnoreEOF = kvargs["qIgnoreEOF"]
        if "qFixedWidthDelimiters" in kvargs:
            if (
                type(kvargs["qFixedWidthDelimiters"]).__name__
                is self_.__annotations__["qFixedWidthDelimiters"]
            ):
                self_.qFixedWidthDelimiters = kvargs["qFixedWidthDelimiters"]
            else:
                self_.qFixedWidthDelimiters = kvargs["qFixedWidthDelimiters"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FilterInfo:
    """

    Attributes
    ----------
    qType: str
      One of:

      • NONE or FILTER_TYPE_NONE

      • RAW or FILTER_TYPE_RAW
    qWherePredicate: str
    """

    qType: str = None
    qWherePredicate: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qWherePredicate" in kvargs:
            if (
                type(kvargs["qWherePredicate"]).__name__
                is self_.__annotations__["qWherePredicate"]
            ):
                self_.qWherePredicate = kvargs["qWherePredicate"]
            else:
                self_.qWherePredicate = kvargs["qWherePredicate"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FolderItem:
    """

    Attributes
    ----------
    qName: str
      Name of the folder item.
    qType: str
      Type of the folder item.

      One of:

      • FOLDER or FOLDER_ITEM_FOLDER

      • FILE or FOLDER_ITEM_FILE

      • OTHER or FOLDER_ITEM_OTHER
    """

    qName: str = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Function:
    """

    Attributes
    ----------
    qName: str
      Name of the script function.
    qGroup: str
      Group of the script function.

      One of:

      • ALL or FUNC_GROUP_ALL

      • U or FUNC_GROUP_UNKNOWN

      • NONE or FUNC_GROUP_NONE

      • AGGR or FUNC_GROUP_AGGR

      • NUM or FUNC_GROUP_NUMERIC

      • RNG or FUNC_GROUP_RANGE

      • EXP or FUNC_GROUP_EXPONENTIAL_AND_LOGARITHMIC

      • TRIG or FUNC_GROUP_TRIGONOMETRIC_AND_HYPERBOLIC

      • FIN or FUNC_GROUP_FINANCIAL

      • MATH or FUNC_GROUP_MATH_CONSTANT_AND_PARAM_FREE

      • COUNT or FUNC_GROUP_COUNTER

      • STR or FUNC_GROUP_STRING

      • MAPP or FUNC_GROUP_MAPPING

      • RCRD or FUNC_GROUP_INTER_RECORD

      • CND or FUNC_GROUP_CONDITIONAL

      • LOG or FUNC_GROUP_LOGICAL

      • NULL or FUNC_GROUP_NULL

      • SYS or FUNC_GROUP_SYSTEM

      • FILE or FUNC_GROUP_FILE

      • TBL or FUNC_GROUP_TABLE

      • DATE or FUNC_GROUP_DATE_AND_TIME

      • NUMI or FUNC_GROUP_NUMBER_INTERPRET

      • FRMT or FUNC_GROUP_FORMATTING

      • CLR or FUNC_GROUP_COLOR

      • RNK or FUNC_GROUP_RANKING

      • GEO or FUNC_GROUP_GEO

      • EXT or FUNC_GROUP_EXTERNAL

      • PROB or FUNC_GROUP_PROBABILITY

      • ARRAY or FUNC_GROUP_ARRAY

      • LEG or FUNC_GROUP_LEGACY
    qSignature: str
      Signature of the script function.
      Gives general information about the function.
    """

    qName: str = None
    qGroup: str = None
    qSignature: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qGroup" in kvargs:
            if type(kvargs["qGroup"]).__name__ is self_.__annotations__["qGroup"]:
                self_.qGroup = kvargs["qGroup"]
            else:
                self_.qGroup = kvargs["qGroup"]
        if "qSignature" in kvargs:
            if (
                type(kvargs["qSignature"]).__name__
                is self_.__annotations__["qSignature"]
            ):
                self_.qSignature = kvargs["qSignature"]
            else:
                self_.qSignature = kvargs["qSignature"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericBookmark:
    """

    Attributes
    ----------
    qType: str
      The native type of the object.
    qHandle: int
      The handle used to connect to object.
    qGenericType: str
      The type of the object.
    qGenericId: str
      Object ID.
    """

    qType: str = None
    qHandle: int = None
    qGenericType: str = None
    qGenericId: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qHandle" in kvargs:
            if type(kvargs["qHandle"]).__name__ is self_.__annotations__["qHandle"]:
                self_.qHandle = kvargs["qHandle"]
            else:
                self_.qHandle = kvargs["qHandle"]
        if "qGenericType" in kvargs:
            if (
                type(kvargs["qGenericType"]).__name__
                is self_.__annotations__["qGenericType"]
            ):
                self_.qGenericType = kvargs["qGenericType"]
            else:
                self_.qGenericType = kvargs["qGenericType"]
        if "qGenericId" in kvargs:
            if (
                type(kvargs["qGenericId"]).__name__
                is self_.__annotations__["qGenericId"]
            ):
                self_.qGenericId = kvargs["qGenericId"]
            else:
                self_.qGenericId = kvargs["qGenericId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_field_values(
        self, qField: str, qGetExcludedValues: bool, qDataPage: BookmarkFieldPage
    ) -> list[FieldValue]:
        """
        Retrieves the values of a field.

        Fieldvalue:

          +------------+--------------------------------+---------+
          |    NAME    |          DESCRIPTION           |  TYPE   |
          +------------+--------------------------------+---------+
          | qText      | Text related to the field      | String  |
          |            | value.                         |         |
          | qIsNumeric | Is set to true if the value is | Boolean |
          |            | a numeric.  Default is false.  |         |
          | qNumber    | Numeric value of the field.    | Double  |
          |            | This parameter is displayed if |         |
          |            | qIsNumeric is set to true.     |         |
          +------------+--------------------------------+---------+


        qField: str
          Name of the field.

        qGetExcludedValues: bool
          If set to true, only excluded values are returned.

        qDataPage: BookmarkFieldPage
          Range of returned values.

        """
        params = {}
        params["qField"] = qField
        params["qGetExcludedValues"] = qGetExcludedValues
        params["qDataPage"] = qDataPage
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFieldValues", handle, **params)[
            "qFieldValues"
        ]
        return [FieldValue(e) for e in response]

    def get_layout(self) -> GenericBookmarkLayout:
        """
        Evaluates an object and displays its properties including the dynamic properties.
        If the member delta is set to true in the request object, only the delta is evaluated.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLayout", handle)["qLayout"]
        obj = GenericBookmarkLayout(**response)
        obj._session = self._session
        return obj

    def apply_patches(self, qPatches: list[NxPatch]) -> object:
        """
        Applies a patch to the properties of an object. Allows an update to some of the properties. It should not be possible to patch "/qInfo/qId",
        and it will be forbidden in the near future.
        Applying a patch takes less time than resetting all the properties.


        qPatches: list[NxPatch]
          Array of patches.

        """
        params = {}
        params["qPatches"] = qPatches
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyPatches", handle, **params)
        return response

    def set_properties(self, qProp: GenericBookmarkProperties) -> object:
        """
        Sets some properties for a bookmark.


        qProp: GenericBookmarkProperties
          Information about the bookmark.

        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetProperties", handle, **params)
        return response

    def get_properties(self) -> GenericBookmarkProperties:
        """
        Shows the properties of an object.
        If the member delta is set to true in the request object, only the delta is retrieved.

        The following is always returned in the output:


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetProperties", handle)["qProp"]
        obj = GenericBookmarkProperties(**response)
        obj._session = self._session
        return obj

    def get_info(self) -> NxInfo:
        """
        Returns:

        • The type of the object.

        • The identifier of the object.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetInfo", handle)["qInfo"]
        obj = NxInfo(**response)
        obj._session = self._session
        return obj

    def apply(self) -> bool:
        """
        Applies a bookmark.

        The operation is successful if qSuccess is set to true.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Apply", handle)["qSuccess"]
        return response

    def publish(self) -> object:
        """
        Publishes a bookmark.
        This operation is not applicable for Qlik Sense Desktop.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Publish", handle)
        return response

    def un_publish(self) -> object:
        """
        Unpublishes a bookmark.
        This operation is not applicable for Qlik Sense Desktop.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnPublish", handle)
        return response

    def approve(self) -> object:
        """
        Adds the generic bookmark to the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Approve", handle)
        return response

    def un_approve(self) -> object:
        """
        Removes the generic bookmark from the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnApprove", handle)
        return response


@dataclass
class GenericBookmarkProperties:
    """

    Attributes
    ----------
    qInfo: NxInfo
      Information about the bookmark.
      This parameter is mandatory.
    qMetaDef: NxMetaDef
      Definition of the dynamic properties.
    """

    qInfo: NxInfo = None
    qMetaDef: NxMetaDef = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        if "qMetaDef" in kvargs:
            if type(kvargs["qMetaDef"]).__name__ is self_.__annotations__["qMetaDef"]:
                self_.qMetaDef = kvargs["qMetaDef"]
            else:
                self_.qMetaDef = NxMetaDef(**kvargs["qMetaDef"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericDimension:
    """

    Attributes
    ----------
    qType: str
      The native type of the object.
    qHandle: int
      The handle used to connect to object.
    qGenericType: str
      The type of the object.
    qGenericId: str
      Object ID.
    """

    qType: str = None
    qHandle: int = None
    qGenericType: str = None
    qGenericId: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qHandle" in kvargs:
            if type(kvargs["qHandle"]).__name__ is self_.__annotations__["qHandle"]:
                self_.qHandle = kvargs["qHandle"]
            else:
                self_.qHandle = kvargs["qHandle"]
        if "qGenericType" in kvargs:
            if (
                type(kvargs["qGenericType"]).__name__
                is self_.__annotations__["qGenericType"]
            ):
                self_.qGenericType = kvargs["qGenericType"]
            else:
                self_.qGenericType = kvargs["qGenericType"]
        if "qGenericId" in kvargs:
            if (
                type(kvargs["qGenericId"]).__name__
                is self_.__annotations__["qGenericId"]
            ):
                self_.qGenericId = kvargs["qGenericId"]
            else:
                self_.qGenericId = kvargs["qGenericId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_layout(self) -> GenericDimensionLayout:
        """
        Evaluates a dimension and displays its properties, including the dynamic properties.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLayout", handle)["qLayout"]
        obj = GenericDimensionLayout(**response)
        obj._session = self._session
        return obj

    def apply_patches(self, qPatches: list[NxPatch]) -> object:
        """
        Applies a patch to the properties of an object. Allows an update to some of the properties. It should not be possible to patch "/qInfo/qId",
        and it will be forbidden in the near future.
        Applying a patch takes less time than resetting all the properties.


        qPatches: list[NxPatch]
          Array of patches.

        """
        params = {}
        params["qPatches"] = qPatches
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyPatches", handle, **params)
        return response

    def set_properties(self, qProp: GenericDimensionProperties) -> object:
        """
        Sets some properties for a dimension.


        qProp: GenericDimensionProperties
          Information about the dimension.

        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetProperties", handle, **params)
        return response

    def get_properties(self) -> GenericDimensionProperties:
        """
        Shows the properties of an object.
        Returns the identifier and the definition of the dimension.
        If the member delta is set to true in the request object, only the delta is retrieved.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetProperties", handle)["qProp"]
        obj = GenericDimensionProperties(**response)
        obj._session = self._session
        return obj

    def get_info(self) -> NxInfo:
        """
        Returns the type and identifier of the object.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetInfo", handle)["qInfo"]
        obj = NxInfo(**response)
        obj._session = self._session
        return obj

    def get_dimension(self) -> NxLibraryDimensionDef:
        """
        Returns the definition of a dimension.

        The definition of the dimension is returned.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDimension", handle)["qDim"]
        obj = NxLibraryDimensionDef(**response)
        obj._session = self._session
        return obj

    def get_linked_objects(self) -> list[NxLinkedObjectInfo]:
        """
        Lists the linked objects to a generic object, a dimension or a measure.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLinkedObjects", handle)["qItems"]
        return [NxLinkedObjectInfo(e) for e in response]

    def publish(self) -> object:
        """
        Publishes a dimension.
        This operation is not applicable for Qlik Sense Desktop.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Publish", handle)
        return response

    def un_publish(self) -> object:
        """
        Unpublishes a dimension.
        This operation is not applicable for Qlik Sense Desktop.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnPublish", handle)
        return response

    def approve(self) -> object:
        """
        Adds the generic dimension to the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Approve", handle)
        return response

    def un_approve(self) -> object:
        """
        Removes the generic dimension from the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnApprove", handle)
        return response


@dataclass
class GenericDimensionLayout:
    """
    Is the layout for GenericDimensionProperties.

    Attributes
    ----------
    qInfo: NxInfo
      Identifier and type of the dimension.
    qMeta: NxMeta
      Information about publishing and permissions.
    qDim: NxLibraryDimension
      Name and label of the dimension, information about grouping.
    qDimInfos: list[GenericDimensionInfo]
      Cardinal and tags related to the dimension.
      Length of the longest value in the field.
    """

    qInfo: NxInfo = None
    qMeta: NxMeta = None
    qDim: NxLibraryDimension = None
    qDimInfos: list[GenericDimensionInfo] = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        if "qMeta" in kvargs:
            if type(kvargs["qMeta"]).__name__ is self_.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(**kvargs["qMeta"])
        if "qDim" in kvargs:
            if type(kvargs["qDim"]).__name__ is self_.__annotations__["qDim"]:
                self_.qDim = kvargs["qDim"]
            else:
                self_.qDim = NxLibraryDimension(**kvargs["qDim"])
        if "qDimInfos" in kvargs:
            if type(kvargs["qDimInfos"]).__name__ is self_.__annotations__["qDimInfos"]:
                self_.qDimInfos = kvargs["qDimInfos"]
            else:
                self_.qDimInfos = [
                    GenericDimensionInfo(**e) for e in kvargs["qDimInfos"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericDimensionProperties:
    """

    Attributes
    ----------
    qInfo: NxInfo
      Identifier and type of the dimension.
      This parameter is mandatory.
    qDim: NxLibraryDimensionDef
      Definition of the dimension.
      This parameter is mandatory.
    qMetaDef: NxMetaDef
      Definition of the dynamic properties.
    """

    qInfo: NxInfo = None
    qDim: NxLibraryDimensionDef = None
    qMetaDef: NxMetaDef = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        if "qDim" in kvargs:
            if type(kvargs["qDim"]).__name__ is self_.__annotations__["qDim"]:
                self_.qDim = kvargs["qDim"]
            else:
                self_.qDim = NxLibraryDimensionDef(**kvargs["qDim"])
        if "qMetaDef" in kvargs:
            if type(kvargs["qMetaDef"]).__name__ is self_.__annotations__["qMetaDef"]:
                self_.qMetaDef = kvargs["qMetaDef"]
            else:
                self_.qMetaDef = NxMetaDef(**kvargs["qMetaDef"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericMeasure:
    """

    Attributes
    ----------
    qType: str
      The native type of the object.
    qHandle: int
      The handle used to connect to object.
    qGenericType: str
      The type of the object.
    qGenericId: str
      Object ID.
    """

    qType: str = None
    qHandle: int = None
    qGenericType: str = None
    qGenericId: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qHandle" in kvargs:
            if type(kvargs["qHandle"]).__name__ is self_.__annotations__["qHandle"]:
                self_.qHandle = kvargs["qHandle"]
            else:
                self_.qHandle = kvargs["qHandle"]
        if "qGenericType" in kvargs:
            if (
                type(kvargs["qGenericType"]).__name__
                is self_.__annotations__["qGenericType"]
            ):
                self_.qGenericType = kvargs["qGenericType"]
            else:
                self_.qGenericType = kvargs["qGenericType"]
        if "qGenericId" in kvargs:
            if (
                type(kvargs["qGenericId"]).__name__
                is self_.__annotations__["qGenericId"]
            ):
                self_.qGenericId = kvargs["qGenericId"]
            else:
                self_.qGenericId = kvargs["qGenericId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_layout(self) -> GenericMeasureLayout:
        """
        Evaluates a measure and displays its properties, including the dynamic properties.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLayout", handle)["qLayout"]
        obj = GenericMeasureLayout(**response)
        obj._session = self._session
        return obj

    def apply_patches(self, qPatches: list[NxPatch]) -> object:
        """
        Applies a patch to the properties of an object. Allows an update to some of the properties. It should not be possible to patch "/qInfo/qId",
        and it will be forbidden in the near future.
        Applying a patch takes less time than resetting all the properties.


        qPatches: list[NxPatch]
          Array of patches.

        """
        params = {}
        params["qPatches"] = qPatches
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyPatches", handle, **params)
        return response

    def set_properties(self, qProp: GenericMeasureProperties) -> object:
        """
        Sets some properties for a measure.


        qProp: GenericMeasureProperties
          Information about the measure.

        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetProperties", handle, **params)
        return response

    def get_properties(self) -> GenericMeasureProperties:
        """
        Shows the properties of an object.
        Returns the identifier and the definition of the measure.
        If the member delta is set to true in the request object, only the delta is retrieved.

        The following is always returned in the output:


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetProperties", handle)["qProp"]
        obj = GenericMeasureProperties(**response)
        obj._session = self._session
        return obj

    def get_info(self) -> NxInfo:
        """
        Returns the type and identifier of the object.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetInfo", handle)["qInfo"]
        obj = NxInfo(**response)
        obj._session = self._session
        return obj

    def get_measure(self) -> NxLibraryMeasureDef:
        """
        Returns the definition of a measure.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetMeasure", handle)["qMeasure"]
        obj = NxLibraryMeasureDef(**response)
        obj._session = self._session
        return obj

    def get_linked_objects(self) -> list[NxLinkedObjectInfo]:
        """
        Lists the linked objects to a generic object, a dimension or a measure.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLinkedObjects", handle)["qItems"]
        return [NxLinkedObjectInfo(e) for e in response]

    def publish(self) -> object:
        """
        Publishes a measure.
        This operation is not applicable for Qlik Sense Desktop.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Publish", handle)
        return response

    def un_publish(self) -> object:
        """
        Unpublishes a measure.
        This operation is not applicable for Qlik Sense Desktop.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnPublish", handle)
        return response

    def approve(self) -> object:
        """
        Adds the generic measure to the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Approve", handle)
        return response

    def un_approve(self) -> object:
        """
        Removes the generic measure from the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnApprove", handle)
        return response


@dataclass
class GenericMeasureLayout:
    """
    Is the layout for GenericMeasureProperties.

    Attributes
    ----------
    qInfo: NxInfo
      Information about the object.
    qMeasure: NxLibraryMeasure
      Information about the measure.
    qMeta: NxMeta
      Information on publishing and permissions.
    """

    qInfo: NxInfo = None
    qMeasure: NxLibraryMeasure = None
    qMeta: NxMeta = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        if "qMeasure" in kvargs:
            if type(kvargs["qMeasure"]).__name__ is self_.__annotations__["qMeasure"]:
                self_.qMeasure = kvargs["qMeasure"]
            else:
                self_.qMeasure = NxLibraryMeasure(**kvargs["qMeasure"])
        if "qMeta" in kvargs:
            if type(kvargs["qMeta"]).__name__ is self_.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(**kvargs["qMeta"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericMeasureProperties:
    """

    Attributes
    ----------
    qInfo: NxInfo
      Information about the measure.
      This parameter is mandatory.
    qMeasure: NxLibraryMeasureDef
      Definition of the measure.
      This parameter is mandatory.
    qMetaDef: NxMetaDef
      Definition of the dynamic properties.
    """

    qInfo: NxInfo = None
    qMeasure: NxLibraryMeasureDef = None
    qMetaDef: NxMetaDef = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        if "qMeasure" in kvargs:
            if type(kvargs["qMeasure"]).__name__ is self_.__annotations__["qMeasure"]:
                self_.qMeasure = kvargs["qMeasure"]
            else:
                self_.qMeasure = NxLibraryMeasureDef(**kvargs["qMeasure"])
        if "qMetaDef" in kvargs:
            if type(kvargs["qMetaDef"]).__name__ is self_.__annotations__["qMetaDef"]:
                self_.qMetaDef = kvargs["qMetaDef"]
            else:
                self_.qMetaDef = NxMetaDef(**kvargs["qMetaDef"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericObject:
    """

    Attributes
    ----------
    qType: str
      The native type of the object.
    qHandle: int
      The handle used to connect to object.
    qGenericType: str
      The type of the object.
    qGenericId: str
      Object ID.
    """

    qType: str = None
    qHandle: int = None
    qGenericType: str = None
    qGenericId: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qHandle" in kvargs:
            if type(kvargs["qHandle"]).__name__ is self_.__annotations__["qHandle"]:
                self_.qHandle = kvargs["qHandle"]
            else:
                self_.qHandle = kvargs["qHandle"]
        if "qGenericType" in kvargs:
            if (
                type(kvargs["qGenericType"]).__name__
                is self_.__annotations__["qGenericType"]
            ):
                self_.qGenericType = kvargs["qGenericType"]
            else:
                self_.qGenericType = kvargs["qGenericType"]
        if "qGenericId" in kvargs:
            if (
                type(kvargs["qGenericId"]).__name__
                is self_.__annotations__["qGenericId"]
            ):
                self_.qGenericId = kvargs["qGenericId"]
            else:
                self_.qGenericId = kvargs["qGenericId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_layout(self) -> GenericObjectLayout:
        """
        Evaluates an object and displays its properties including the dynamic properties.
        If the member delta is set to true in the request object, only the delta is evaluated. A GetLayout call on a generic object, returns up to one level down in the hierarchy.

        Example::

        _A_ is a generic object and is the parent of the objects B and C. B is the parent of the objects D and E.

        ![](images/dr_gen_QVCPMethodGetLayoutHierarchy.png)

        A GetLayout call on A returns information on the objects A, B and C.
        A GetLayout call on B returns information on the objects B, D and E.
        A  GetLayout call on C returns information on the object C.

        In addition to the parameters displayed above, the GetLayout method can return other properties according to what is defined in the generic object.
        For example, if qHyperCubeDef is defined in the generic object, the GetLayout method returns the properties described in HyperCube.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLayout", handle)["qLayout"]
        obj = GenericObjectLayout(**response)
        obj._session = self._session
        return obj

    def get_list_object_data(
        self, qPath: str, qPages: list[NxPage]
    ) -> list[NxDataPage]:
        """
        Retrieves the values of a list object.
        A data set is returned.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qListObjectDef .

        qPages: list[NxPage]
          Array of pages you are interested in.

        """
        params = {}
        params["qPath"] = qPath
        params["qPages"] = qPages
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetListObjectData", handle, **params)[
            "qDataPages"
        ]
        return [NxDataPage(e) for e in response]

    def get_hyper_cube_data(self, qPath: str, qPages: list[NxPage]) -> list[NxDataPage]:
        """
        Retrieves the calculated data for a chart, a table, or a scatter plot. It is possible to retrieve specific pages of data.
        This method works for a hypercube in DATA_MODE_STRAIGHT.

        A data set is returned.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .

        qPages: list[NxPage]
          Array of pages to retrieve.

        """
        params = {}
        params["qPath"] = qPath
        params["qPages"] = qPages
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubeData", handle, **params)[
            "qDataPages"
        ]
        return [NxDataPage(e) for e in response]

    def get_hyper_cube_reduced_data(
        self, qPath: str, qPages: list[NxPage], qZoomFactor: int, qReductionMode: str
    ) -> list[NxDataPage]:
        """
        Reduces the data of a bar chart, a line chart or a scatter plot chart and retrieves them.
        The reduction is dependent on the zoom factor (parameter qZoomFactor ) and on the reduction mode.
        This method can be used to create mini charts.

        Bar chart or line chart data reduction:

        For the data reduction to happen, the following conditions must be fulfilled:

        • The values cannot fit in the defined page (parameter qPages ).

        • The zoom factor is not 0 (parameter qZoomFactor ).

        • The reduction mode must be set to D1.

        The reduction algorithm keeps the shape of the visualizations and works whatever the number of dimensions in the chart. The global profile of the chart is reduced, and not only a specific dimension. A visualization that has been reduced contains fewer values but its shape is the same. Data of all types can be reduced. Therefore it is hard to relate the values before and after a reduction especially when reducing string values.

        Example:

        If you have a chart with 1 million data, and you have set the zoom factor to 5, the GetHyperCubeReducedData method reduces the chart and retrieves 200 000 data.

        Scatter plot chart data reduction:

        The reduction mode must be set to C.
        This reduction mechanism follows the 2D K-Means algorithm. Data are reduced into a number of clusters. Each data is assigned to a specific centroid.
        The number of centroids can be defined in the parameter qZoomFactor.

        Scatter plot chart resolution reduction:

        The reduction mode must be set to S.
        The resolution is reduced according to the zoom factor (parameter qZoomFactor ).

        Example:

        If you have a scatter plot chart and the zoom factor is set to 2, the scatter plot chart resolution is reduced by 4.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .

        qPages: list[NxPage]
          Array of pages.

        qZoomFactor: int
          Defines the zoom factor.
          If set to -1, the engine decides of the zoom factor.

          • If the reduction mode is D1 or S , the zoom factor is 2ⁿ. If the zoom factor is 5, the data are reduced by a factor 32.

          • If the reduction mode is C , the zoom factor defines the number of centroids.

        qReductionMode: str
          Defines the reduction mode.

          One of:

          • N or DATA_REDUCTION_NONE

          • D1 or DATA_REDUCTION_ONEDIM

          • S or DATA_REDUCTION_SCATTERED

          • C or DATA_REDUCTION_CLUSTERED

          • ST or DATA_REDUCTION_STACKED

        """
        params = {}
        params["qPath"] = qPath
        params["qPages"] = qPages
        params["qZoomFactor"] = qZoomFactor
        params["qReductionMode"] = qReductionMode
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubeReducedData", handle, **params)[
            "qDataPages"
        ]
        return [NxDataPage(e) for e in response]

    def get_hyper_cube_pivot_data(
        self, qPath: str, qPages: list[NxPage]
    ) -> list[NxPivotPage]:
        """
        Retrieves the values of a pivot table. It is possible to retrieve specific pages of data.
        This method works for a hypercube in DATA_MODE_PIVOT.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .

        qPages: list[NxPage]
          Array of pages to retrieve.

        """
        params = {}
        params["qPath"] = qPath
        params["qPages"] = qPages
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubePivotData", handle, **params)[
            "qDataPages"
        ]
        return [NxPivotPage(e) for e in response]

    def get_hyper_cube_stack_data(
        self, qPath: str, qPages: list[NxPage], qMaxNbrCells: int = None
    ) -> list[NxStackPage]:
        """
        Retrieves the values of a stacked pivot table. It is possible to retrieve specific pages of data.
        This method works for a hypercube in DATA_MODE_PIVOT_STACK.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .

        qPages: list[NxPage]
          Array of pages to retrieve.

        qMaxNbrCells: int
          Maximum number of cells at outer level.
          The default value is 10 000.

        """
        params = {}
        params["qPath"] = qPath
        params["qPages"] = qPages
        if qMaxNbrCells is not None:
            params["qMaxNbrCells"] = qMaxNbrCells
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubeStackData", handle, **params)[
            "qDataPages"
        ]
        return [NxStackPage(e) for e in response]

    def get_hyper_cube_continuous_data(
        self, qPath: str, qOptions: NxContinuousDataOptions, qReverseSort: bool = None
    ) -> object:
        """
        Retrieves and packs compressed hypercube and axis data. It is possible to retrieve specific pages of data.
        Binning is done on the time stamp data as well as the date. This means that you can zoom in to a level of granularity as low as seconds.


        qPath: str
          Path to the definition of the object.
          For example, /qHyperCubeDef .

        qOptions: NxContinuousDataOptions
          Defines the data to return.

        qReverseSort: bool
          If set to true the returned data pages are reverse sorted.
          Optional.

        """
        params = {}
        params["qPath"] = qPath
        params["qOptions"] = qOptions
        if qReverseSort is not None:
            params["qReverseSort"] = qReverseSort
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubeContinuousData", handle, **params)
        return response

    def get_hyper_cube_tree_data(
        self, qPath: str, qNodeOptions: NxTreeDataOption = None
    ) -> list[NxTreeNode]:
        """
        Retrieves data for nodes in a tree structure. It is possible to retrieve specific pages of data.
        This method works for a treedata object or a hypercube in DATA_MODE_TREE.


        qPath: str
          Path to the definition of the object to be selected.

        qNodeOptions: NxTreeDataOption
          Specifies all the paging filters needed to define the tree to be fetched. If left out the complete tree is returned.

        """
        params = {}
        params["qPath"] = qPath
        if qNodeOptions is not None:
            params["qNodeOptions"] = qNodeOptions
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubeTreeData", handle, **params)[
            "qNodes"
        ]
        return [NxTreeNode(e) for e in response]

    def get_hyper_cube_binned_data(
        self,
        qPath: str,
        qPages: list[NxPage],
        qViewport: NxViewPort,
        qDataRanges: list[NxDataAreaPage],
        qMaxNbrCells: int,
        qQueryLevel: int,
        qBinningMethod: int,
    ) -> list[NxDataPage]:
        """
        This method supports data binning.
        When a generic object with two or three measures and one dimension contains a lot of data, groups of points (for example, cells) can be rendered instead of points.
        A zone of interest can be refined (for zooming in) up to a maximum refinement level (set in the qQueryLevel parameter) or coarsened (for zoom out).
        The grid of cells is adaptive (not static), meaning that it adapts to different length scales.
        The GetHyperCubeBinnedData method gives information about the adaptive grid and the values of the generic object.
        The number of points in a cell and the coordinates (expressed in the measure range) of each cell are returned.
        Dimension values and measure values are rendered at point level (highest detailed level).
        The generic object should contain two or three measures and one dimension. When the refinement is high, the first two measures are represented on the x-axis and on the y-axis, while the third measure is visualized as color or point size.

        Adaptive Grid:

        More details about the properties of the adaptive grid are given in this paragraph.
        When the refinement is not the highest (cells are rendered), information about the adaptive grid is returned through several arrays.
        The first array contains the following properties:

          +-------------+--------------------------------+----------------------------+
          |    NAME     |          DESCRIPTION           |            TYPE            |
          +-------------+--------------------------------+----------------------------+
          | qNum        | Maximum number of points that  | String                     |
          |             | a cell can contain.            |                            |
          | qElemNumber | Is set to 0.                   | Boolean                    |
          | qState      | The default value is L.        | One of:   * L for Locked   |
          |             |                                |  * S for Selected  *       |
          |             |                                | O for Optional  * D        |
          |             |                                | for Deselected  * A        |
          |             |                                | for Alternative  * X       |
          |             |                                | for eXcluded  * XS for     |
          |             |                                | eXcluded Selected  * XL    |
          |             |                                | for eXcluded Locked        |
          +-------------+--------------------------------+----------------------------+

        The next arrays give the coordinates of each cell in the page.
        Each array contains the following properties:

          +-------------+--------------------------------+--------------------------------+
          |    NAME     |          DESCRIPTION           |              TYPE              |
          +-------------+--------------------------------+--------------------------------+
          | qText       | Coordinates of a cell in       | String                         |
          |             | the measure range.  “qText”:   |                                |
          |             | “[[<left>, <top>, <right>,     |                                |
          |             | <bottom>], [<left>, <top>,     |                                |
          |             | <right>, <bottom>], ....       |                                |
          |             | [<left>, <top>, <right>,       |                                |
          |             | <bottom>]]  Where:  < left     |                                |
          |             | >, < top >, < right > and <    |                                |
          |             | bottom > are the coordinates   |                                |
          |             | of the cell in the measure     |                                |
          |             | range.                         |                                |
          | qNum        | Number of points in the cell.  | Double precision floating      |
          |             |                                | point                          |
          | qElemNumber | Unique identifier for each     | Integer                        |
          |             | cell, calculated by the engine |                                |
          |             | during the construction of     |                                |
          |             | the grid.  This element number |                                |
          |             | is not stored in the database  |                                |
          |             | and can have a positive or a   |                                |
          |             | negative value.                |                                |
          | qState      | The default value is L.        | One of:   * L for Locked       |
          |             |                                |  * S for Selected  *           |
          |             |                                | O for Optional  * D            |
          |             |                                | for Deselected  * A            |
          |             |                                | for Alternative  * X           |
          |             |                                | for eXcluded  * XS for         |
          |             |                                | eXcluded Selected  * XL        |
          |             |                                | for eXcluded Locked            |
          +-------------+--------------------------------+--------------------------------+

        Cells are represented as rectangles.

        Dimension values and measures values:

        More details about the properties, when dimension and measure values are returned, are given in this paragraph.
        When the refinement is high, points are rendered (not cells) and dimension and measure values for each cell are returned.
        The first array is empty because no information on the adaptive grid is needed.
        The next arrays bring information about the dimension and the measure values.

          +-------------+--------------------------------+--------------------------------+
          |    NAME     |          DESCRIPTION           |              TYPE              |
          +-------------+--------------------------------+--------------------------------+
          | qText       | Text value of the dimension or | String                         |
          |             | the measure.                   |                                |
          | qNum        | Numerical value of the         | Double precision floating      |
          |             | dimension or the measure.  Is  | point                          |
          |             | set to 0 if the value is only  |                                |
          |             | text.                          |                                |
          | qElemNumber | Unique identifier for each     | Integer                        |
          |             | cell, calculated by the engine |                                |
          |             | during the construction of     |                                |
          |             | the grid.  This element number |                                |
          |             | is not stored in the database  |                                |
          |             | and can have a positive or a   |                                |
          |             | negative value.                |                                |
          | qState      | The default value is L.        | One of:   * L for Locked       |
          |             |                                |  * S for Selected  *           |
          |             |                                | O for Optional  * D            |
          |             |                                | for Deselected  * A            |
          |             |                                | for Alternative  * X           |
          |             |                                | for eXcluded  * XS for         |
          |             |                                | eXcluded Selected  * XL        |
          |             |                                | for eXcluded Locked            |
          +-------------+--------------------------------+--------------------------------+


        qPath: str
          Path to the definition of the object.
          For example, /qHyperCubeDef .

        qPages: list[NxPage]
          Array of pages to retrieve.
          Since the generic object contains two measures and one dimension, qWidth should be set to 3.
          If the value of a measure is Null, the value cannot be rendered. Therefore, the number of elements rendered in a page can be less than the number defined in the property qHeight .

        qViewport: NxViewPort
          Defines the canvas and the zoom level.
          This parameter is not yet used and is optional.

        qDataRanges: list[NxDataAreaPage]
          Range of the data to render.
          This range applies to the measure values.
          The lowest and highest values of a measure can be retrieved by using the GetLayout method (in /qHyperCube/qMeasureInfo ).

        qMaxNbrCells: int
          Maximum number of cells in the grid.

        qQueryLevel: int
          Level of details. The higher the level, the more detailed information you get (zoom-in).
          When the number of points to render falls below a certain threshold, the values are no longer rendered as cells but as points.
          The query level should be no greater than 20.

        qBinningMethod: int
          Selects the algorithm.
          The default value is 0.
          One of:

          • 0: Adaptive grid

          • 1: Hexagonal grid

          • 2: Uniform grid

        """
        params = {}
        params["qPath"] = qPath
        params["qPages"] = qPages
        params["qViewport"] = qViewport
        params["qDataRanges"] = qDataRanges
        params["qMaxNbrCells"] = qMaxNbrCells
        params["qQueryLevel"] = qQueryLevel
        params["qBinningMethod"] = qBinningMethod
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubeBinnedData", handle, **params)[
            "qDataPages"
        ]
        return [NxDataPage(e) for e in response]

    def apply_patches(self, qPatches: list[NxPatch], qSoftPatch: bool = None) -> object:
        """
        Applies a patch to the properties of an object. Allows an update to some of the properties.
        It is possible to apply a patch to the properties of a generic object, that is not persistent. Such a patch is called a soft patch.
        In that case, the result of the operation on the properties (add, remove or delete) is not shown when doing GetProperties , and only a GetLayout call shows the result of the operation.
        Properties that are not persistent are called soft properties. Once the engine session is over, soft properties are cleared. It should not be possible to patch "/qInfo/qId",
        and it will be forbidden in the near future.
        Soft properties apply only to generic objects.


        qPatches: list[NxPatch]
          Array of patches.

        qSoftPatch: bool
          If set to true, it means that the properties to be applied are not persistent. The patch is a soft patch.
          The default value is false.

        """
        params = {}
        params["qPatches"] = qPatches
        if qSoftPatch is not None:
            params["qSoftPatch"] = qSoftPatch
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyPatches", handle, **params)
        return response

    def clear_soft_patches(self) -> object:
        """
        Clears the soft properties of a generic object.
        For more information on how to add soft properties to a generic object, see ApplyPatches Method.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ClearSoftPatches", handle)
        return response

    def set_properties(self, qProp: GenericObjectProperties) -> object:
        """
        Sets some properties for a generic object.
        The properties depends on the generic object type, see [properties](genericobject-property.html).


        qProp: GenericObjectProperties
          Information about the generic object.

        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetProperties", handle, **params)
        return response

    def get_properties(self) -> GenericObjectProperties:
        """
        Returns the identifier, the type and the properties of the object.
        Because it is not mandatory to set all properties when you define an object, the GetProperties method may show properties that were not set. In that case, default values are given.
        If the object contains some soft properties, the soft properties are not returned by the GetProperties method. Use the GetEffectiveProperties method instead.
        If the object is linked to another object, the properties of the linking object are not returned by the GetProperties method. Use the GetEffectiveProperties method instead.
        The properties depends on the generic object type, see [properties](genericobject-layout.html).

        If the member delta is set to true in the request object, only the delta is retrieved.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetProperties", handle)["qProp"]
        obj = GenericObjectProperties(**response)
        obj._session = self._session
        return obj

    def get_effective_properties(self) -> GenericObjectProperties:
        """
        Returns the identifier, the type and the properties of the object.
        If the object contains some soft properties, the soft properties are returned.
        If the object is linked to another object, the properties of the linking object are returned.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetEffectiveProperties", handle)["qProp"]
        obj = GenericObjectProperties(**response)
        obj._session = self._session
        return obj

    def set_full_property_tree(self, qPropEntry: GenericObjectEntry) -> object:
        """
        Sets the properties of:

        • A generic object.

        • The children of the generic object.

        • The bookmarks/embedded snapshots of the generic object.

        If the SetFullPropertyTree method is asked to set some properties to a child that does not exist, it creates the child.
        The type of an object cannot be updated.


        qPropEntry: GenericObjectEntry
          Information about the generic object entry.

        """
        params = {}
        params["qPropEntry"] = qPropEntry
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetFullPropertyTree", handle, **params)
        return response

    def get_full_property_tree(self) -> GenericObjectEntry:
        """
        Gets the properties of:

        • A generic object.

        • The children of the generic object.

        • The bookmarks/embedded snapshots of the generic object.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFullPropertyTree", handle)["qPropEntry"]
        obj = GenericObjectEntry(**response)
        obj._session = self._session
        return obj

    def get_info(self) -> NxInfo:
        """
        Returns the type and identifier of the object.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetInfo", handle)["qInfo"]
        obj = NxInfo(**response)
        obj._session = self._session
        return obj

    def clear_selections(self, qPath: str, qColIndices: list[int] = None) -> object:
        """
        Clears the selections in a dimension of a visualization.


        qPath: str
          Path to the definition of the visualization.
          For example, /qListObjectDef .

        qColIndices: list[int]
          Array of dimension numbers or indexes. The selections are cleared in the specified dimensions.
          Dimension numbers/indexes start from 0.
          If this parameter is not set, all dimensions are cleared.

        """
        params = {}
        params["qPath"] = qPath
        if qColIndices is not None:
            params["qColIndices"] = qColIndices
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ClearSelections", handle, **params)
        return response

    def export_data(
        self,
        qFileType: str,
        qPath: str = None,
        qFileName: str = None,
        qExportState: str = None,
        qServeOnce: bool = None,
    ) -> object:
        """
        Exports the data of any generic object to an Excel file or a open XML file. If the object contains excluded values, those excluded values are not exported.
        This API has limited functionality and will not support CSV export from all types of objects. Consider using Excel export instead. Treemap and bar chart are not supported.
        ExportData method is not supported in SaaS Editions of Qlik Sense.

        Default limitations in number of rows and columns:

        The default maximum number of rows and columns in the Excel export file is:

        • 1048566 rows per sheet. For pivot tables: 1048566 column dimensions. 10 rows can be added after the export.

        • 16384 columns per sheet. If the number of columns exceeds the limit, the exported file is truncated and a warning message is sent.

        Default limitation in number of columns:

        The default maximum number of columns in the export file is:

        • 1000 to export to a CSV file

        The exported file is truncated if the number of cells exceeds the limit. A warning message with code 1000 is sent.
        There is an option to export only the possible values ( qExportState is P).

        Default limitation in size:

        If the exported file is larger than the maximum value, then an out-of-memory error with code 13000 is returned.

        Exported files are temporary and are available only for a certain time span and only to the user who created them.


        qFileType: str
          Type of the file to export.

          One of:

          • CSV_C or EXPORT_CSV_C

          • CSV_T or EXPORT_CSV_T

          • OOXML or EXPORT_OOXML

        qPath: str
          Path to the definition of the object to be exported.
          For example, /qHyperCubeDef .
          This parameter is mandatory if the file type is CSVC_ or CSVT_ .

        qFileName: str
          Name of the exported file after download from browser.
          This parameter is optional and only used in Qlik Sense Desktop.

        qExportState: str
          Defines the values to be exported.
          The default value is A.

          One of:

          • P or EXPORT_POSSIBLE

          • A or EXPORT_ALL

        qServeOnce: bool
          If the exported file should be served only once
          This parameter is optional and only used in Qlik Sense Enterprise (Windows)
          Default value: false

        """
        params = {}
        params["qFileType"] = qFileType
        if qPath is not None:
            params["qPath"] = qPath
        if qFileName is not None:
            params["qFileName"] = qFileName
        if qExportState is not None:
            params["qExportState"] = qExportState
        if qServeOnce is not None:
            params["qServeOnce"] = qServeOnce
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ExportData", handle, **params)
        return response

    def select_list_object_values(
        self, qPath: str, qValues: list[int], qToggleMode: bool, qSoftLock: bool = None
    ) -> bool:
        """
        Makes single selections in dimensions.
        This method applies to list objects only.

        The member Change returns the handles of the objects that are updated following the selections.
        _qSuccess_ is set to true if the selections are successful and is set to false in the following cases:

        • The object contains invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qListObjectDef .

        qValues: list[int]
          Element numbers to select.
          You can select multiple values; the separator is the comma.

        qToggleMode: bool
          Set to true to toggle.

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        params["qPath"] = qPath
        params["qValues"] = qValues
        params["qToggleMode"] = qToggleMode
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectListObjectValues", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_list_object_possible(self, qPath: str, qSoftLock: bool = None) -> bool:
        """
        Selects all possible values of a list object.
        This method applies to list objects (objects with one dimension).

        The member Change returns the handles of the objects that are updated following the selections.
        _qSuccess_ is set to true if the selections are successful and is set to false in the following cases:

        • The object contains invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qListObjectDef .

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        params["qPath"] = qPath
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectListObjectPossible", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_list_object_excluded(self, qPath: str, qSoftLock: bool = None) -> bool:
        """
        Inverts the current selections in a specific field.
        This method applies to list objects (objects with one dimension).

        The member Change returns the handles of the objects that are updated following the selections.
        _qSuccess_ is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qListObjectDef .

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        params["qPath"] = qPath
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectListObjectExcluded", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_list_object_alternative(
        self, qPath: str, qSoftLock: bool = None
    ) -> bool:
        """
        Selects all alternative values in a specific field.
        This method applies to list objects (objects with one dimension).
        If a field contains at least one selected value, the values that are neither selected nor excluded are alternatives values.

        The member Change returns the handles of the objects that are updated following the selections.
        _qSuccess_ is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qListObjectDef .

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        params["qPath"] = qPath
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectListObjectAlternative", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_list_object_all(self, qPath: str, qSoftLock: bool = None) -> bool:
        """
        Selects all values of a field.
        This method applies to list objects (objects with one dimension).

        The member Change returns the handles of the objects that are updated following the selections.
        _qSuccess_ is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qListObjectDef .

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        params["qPath"] = qPath
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectListObjectAll", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_list_object_continuous_range(
        self, qPath: str, qRanges: list[Range], qSoftLock: bool = None
    ) -> bool:
        """
        The following is returned in the output:
        The operation is successful if qSuccess is set to true.


        qPath: str
          Path to the definition of the object.
          For example, /qHyperCubeDef .

        qRanges: list[Range]
          Selects ranges in a hypercube in (Ranges[N].Min,Ranges[N].Max) intervals.
          If either Ranges[N].MinInclEq or Ranges[N].MaxInclEq, or both flags are set to true then Min and Max values will be selected.

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        params["qPath"] = qPath
        params["qRanges"] = qRanges
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send(
            "SelectListObjectContinuousRange", handle, **params
        )["qSuccess"]
        return response

    def search_list_object_for(self, qPath: str, qMatch: str) -> bool:
        """
        Searches for a string in a list object.
        This method applies to list objects (objects with one dimension).
        The search results can be displayed using the GetLayout Method.

        The operation is successful if qSuccess is set to true.


        qPath: str
          Path to the definition of the list object.
          For example, /qListObjectDef .

        qMatch: str
          Search string.
          Wild card characters are allowed. The search is not case sensitive.
          Examples:

          • `P*U*`: retrieves only values that start with P and contain U

          • `P U S`: retrieves values that start with P, U or S

        """
        params = {}
        params["qPath"] = qPath
        params["qMatch"] = qMatch
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SearchListObjectFor", handle, **params)[
            "qSuccess"
        ]
        return response

    def abort_list_object_search(self, qPath: str) -> object:
        """
        Aborts the results of a search in a list object.
        This method applies to list objects (objects with one dimension).
        After an abort on a list object search, the GetLayout Method does not return any more search results but it does return the values in the field.


        qPath: str
          Path to the definition of the list object.
          For example, /qListObjectDef .

        """
        params = {}
        params["qPath"] = qPath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AbortListObjectSearch", handle, **params)
        return response

    def accept_list_object_search(
        self, qPath: str, qToggleMode: bool, qSoftLock: bool = None
    ) -> object:
        """
        Accept the results of a search in a list object. The search results become selected in the field.
        This method applies to list objects (objects with one dimension).
        The search results are displayed using the GetLayout Method.


        qPath: str
          Path to the definition of the list object.
          For example, /qListObjectDef .

        qToggleMode: bool
          Set to true to keep any selections present in the list object.
          If this parameter is set to false, selections made before accepting the list object search become alternative.

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        params["qPath"] = qPath
        params["qToggleMode"] = qToggleMode
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AcceptListObjectSearch", handle, **params)
        return response

    def expand_left(self, qPath: str, qRow: int, qCol: int, qAll: bool) -> object:
        """
        Expands the left dimensions of a pivot table. This method applies only to pivot tables that are not always fully expanded.
        In the definition of the hypercube (in HyperCubeDef ), the parameter qAlwaysFullyExpanded must be set to false.


        qPath: str
          Path to the definition of the object to be expanded.
          For example, /qHyperCubeDef .

        qRow: int
          Row index in the data matrix to expand.
          Indexing starts from 0.

        qCol: int
          Column index. The index is based on the left dimension indexes.
          Indexing starts from 0.

        qAll: bool
          If set to true, it expands all cells.
          Parameters qRow and qCol are not used if qAll is set to true, but they need to be set (for example to 0).

        """
        params = {}
        params["qPath"] = qPath
        params["qRow"] = qRow
        params["qCol"] = qCol
        params["qAll"] = qAll
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ExpandLeft", handle, **params)
        return response

    def expand_top(self, qPath: str, qRow: int, qCol: int, qAll: bool) -> object:
        """
        Expands the top dimensions of a pivot table. This method applies only to pivot tables that are not always fully expanded.
        In the definition of the hypercube (in HyperCubeDef ), the parameter qAlwaysFullyExpanded must be set to false.


        qPath: str
          Path to the definition of the object to be expanded.
          For example, /qHyperCubeDef .

        qRow: int
          Row index. The index is based on the top dimension indexes.
          Indexing starts from 0.

        qCol: int
          Column index in the data matrix.
          Indexing starts from 0.

        qAll: bool
          If set to true, it expands all cells.
          Parameters qRow and qCol are not used if qAll is set to true, but they need to be set (for example to 0).

        """
        params = {}
        params["qPath"] = qPath
        params["qRow"] = qRow
        params["qCol"] = qCol
        params["qAll"] = qAll
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ExpandTop", handle, **params)
        return response

    def collapse_left(self, qPath: str, qRow: int, qCol: int, qAll: bool) -> object:
        """
        Collapses the left dimensions of a pivot table. This method applies only to pivot tables that are not always fully expanded.
        In the definition of the hypercube (in HyperCubeDef ), the parameter qAlwaysFullyExpanded must be set to false.


        qPath: str
          Path to the definition of the object to be collapsed.
          For example, /qHyperCubeDef .

        qRow: int
          Row index in the data matrix.
          Indexing starts from 0.

        qCol: int
          Column index. The index is based on the left dimension indexes.
          Indexing starts from 0.

        qAll: bool
          If set to true, it collapses all cells.
          Parameters qRow and qCol are not used if qAll is set to true, but they need to be set (for example to 0).

        """
        params = {}
        params["qPath"] = qPath
        params["qRow"] = qRow
        params["qCol"] = qCol
        params["qAll"] = qAll
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CollapseLeft", handle, **params)
        return response

    def collapse_top(self, qPath: str, qRow: int, qCol: int, qAll: bool) -> object:
        """
        Collapses the top dimensions of a pivot table. This method applies only to pivot tables that are not always fully expanded.
        In the definition of the hypercube (in HyperCubeDef ), the parameter qAlwaysFullyExpanded must be set to false.


        qPath: str
          Path to the definition of the object to be collapsed
          For example, /qHyperCubeDef .

        qRow: int
          Row index. The index is based on the top dimension indexes.
          Indexing starts from 0.

        qCol: int
          Column index in the data matrix.
          Indexing starts from 0.

        qAll: bool
          If set to true, it collapses all cells.
          Parameters qRow and qCol are not used if qAll is set to true, but they need to be set (for example to 0).

        """
        params = {}
        params["qPath"] = qPath
        params["qRow"] = qRow
        params["qCol"] = qCol
        params["qAll"] = qAll
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CollapseTop", handle, **params)
        return response

    def drill_up(self, qPath: str, qDimNo: int, qNbrSteps: int) -> object:
        """
        You can use the drillUp method with any object that contains a drill-down group as a dimension.
        This method allows you to move between different levels of information (from a detailed level to a less detailed level of information). You can go back to previous visualizations up to the highest level of the hierarchy.
        If you try to drill up more steps than there are available levels, the first level of the hierarchy is displayed.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .

        qDimNo: int
          Dimension number or index starting from 0.
          The default value is 0.

        qNbrSteps: int
          Number of steps you want to drill up.
          The default value is 0.

        """
        params = {}
        params["qPath"] = qPath
        params["qDimNo"] = qDimNo
        params["qNbrSteps"] = qNbrSteps
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DrillUp", handle, **params)
        return response

    def lock(self, qPath: str, qColIndices: list[int] = None) -> object:
        """
        Locks the selected values of a generic object.


        qPath: str
          Path to the definition of the object.
          For example, /qListObjectDef .

        qColIndices: list[int]
          Dimension numbers or dimension indexes where the lock should apply.
          Dimension numbers/indexes start from 0.
          If this parameter is not set, the selected values in all dimensions are locked.

        """
        params = {}
        params["qPath"] = qPath
        if qColIndices is not None:
            params["qColIndices"] = qColIndices
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Lock", handle, **params)
        return response

    def unlock(self, qPath: str, qColIndices: list[int] = None) -> object:
        """
        Unlocks the selected values of a generic object if the target (or handle ) is a generic object


        qPath: str
          Path to the definition of the object.
          For example, /qListObjectDef .

        qColIndices: list[int]
          Dimension numbers/indexes where the unlock should apply.
          Dimension numbers/indexes start from 0.
          If this parameter is not set, the locked values in all dimensions are unlocked.

        """
        params = {}
        params["qPath"] = qPath
        if qColIndices is not None:
            params["qColIndices"] = qColIndices
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Unlock", handle, **params)
        return response

    def select_hyper_cube_values(
        self, qPath: str, qDimNo: int, qValues: list[int], qToggleMode: bool
    ) -> bool:
        """
        Selects some values in one dimension.
        The values are identified by their element numbers.
        This method applies to charts, tables and scatter plots.

        The member Change returns the handles of the objects that are updated following the selections.
        _qSuccess_ is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .

        qDimNo: int
          Dimension number or index to select.
          Dimension numbers/index start from 0.

        qValues: list[int]
          Element numbers of the field to select.
          You can select multiple elements; the separator is the comma.

        qToggleMode: bool
          Set to true to toggle.

        """
        params = {}
        params["qPath"] = qPath
        params["qDimNo"] = qDimNo
        params["qValues"] = qValues
        params["qToggleMode"] = qToggleMode
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectHyperCubeValues", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_hyper_cube_cells(
        self,
        qPath: str,
        qRowIndices: list[int],
        qColIndices: list[int],
        qSoftLock: bool = None,
        qDeselectOnlyOneSelected: bool = None,
    ) -> bool:
        """
        Makes selections in multiple dimensions and measures.
        This method applies to hypercubes, such as bar charts, tables and scatter plots.

        The member Change returns the handles of the objects that are updated following the selections.
        _qSuccess_ is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .

        qRowIndices: list[int]
          Array of row indexes to select, starting from 0.
          If the array is empty [ ] , all rows are selected.

        qColIndices: list[int]
          Indexes of the columns to select, starting from 0.
          A column corresponds to a dimension in the order they are added to the hypercube.
          If a column is hidden it is ignored, qColIndex n refers to the n:th visible column (starting from zero).
          Example:
          If the hypercube has two dimensions:

          • [0] selects the first column (i.e the first dimension).

          • [1] selects the second column (i.e the second dimension).

          If the array is empty [ ] , all columns are selected.

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.

        qDeselectOnlyOneSelected: bool
          Set this parameter to true to unselect the last single selected value. There must be only one selected value in the field.
          The default value is false.

        """
        params = {}
        params["qPath"] = qPath
        params["qRowIndices"] = qRowIndices
        params["qColIndices"] = qColIndices
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        if qDeselectOnlyOneSelected is not None:
            params["qDeselectOnlyOneSelected"] = qDeselectOnlyOneSelected
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectHyperCubeCells", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_pivot_cells(
        self,
        qPath: str,
        qSelections: list[NxSelectionCell],
        qSoftLock: bool = None,
        qDeselectOnlyOneSelected: bool = None,
    ) -> bool:
        """
        This method only applies to hypercubes that are not represented as straight tables. The parameter qMode in HyperCubeDef must be set either to P  or K .

        Pivot table:

        Makes selections in the top or left dimension cells of a pivot table or in the data matrix. Only expanded dimensions can be selected.

        Stacked table:

        Makes selections in the left dimension cells of a stacked table or in the data matrix.
        There is no top dimensions in a stacked table. A stacked table can only contain one measure.

        Example of a pivot table:

        ![](images/ui_gen_ExampleQVCPPivotTableDescription.png)

        In the representation above:

          +-------------------+--------------------------------+
          | Sum(OrderTotal)   | Are pseudo dimensions.         |
          | Count(OrderTotal) |                                |
          | CategoryName      | Is a left dimension.           |
          |                   | Beverages , Condiments ... are |
          |                   | left dimension values.         |
          | ProductName       | Is a top dimension.  Chef      |
          |                   | Anton's Cajun Seasoning is a   |
          |                   | top dimension value.           |
          | Numeric values    | Are calculated values in the   |
          |                   | data matrix.  626291,832 is a  |
          |                   | calculated value.              |
          +-------------------+--------------------------------+

        The member Change returns the handles of the objects that are updated following the selections.
        _qSuccess_ is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.


        qPath: str
          Path to the definition of the object.
          For example, /qHyperCubeDef .

        qSelections: list[NxSelectionCell]
          Information about the selections to perform.

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.

        qDeselectOnlyOneSelected: bool
          Set this parameter to true to unselect the last single selected value. There must be only one selected value in the field.
          The default value is false.

        """
        params = {}
        params["qPath"] = qPath
        params["qSelections"] = qSelections
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        if qDeselectOnlyOneSelected is not None:
            params["qDeselectOnlyOneSelected"] = qDeselectOnlyOneSelected
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectPivotCells", handle, **params)["qSuccess"]
        return response

    def range_select_hyper_cube_values(
        self,
        qPath: str,
        qRanges: list[NxRangeSelectInfo],
        qColumnsToSelect: list[int] = None,
        qOrMode: bool = None,
        qDeselectOnlyOneSelected: bool = None,
    ) -> bool:
        """
        Makes range selections in measures.
        This method applies to hypercubes. For example, bar charts, tables and scatter plots.

        The member Change returns the handles of the objects that are updated following the selections.
        _qSuccess_ is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .

        qRanges: list[NxRangeSelectInfo]
          Ranges of selections.

        qColumnsToSelect: list[int]
          Indicates which dimensions to select.
          The dimensions numbering starts at 0 (first dimension is 0).
          If the array is empty, all dimensions are selected.

        qOrMode: bool
          Applies to hypercubes with multiple measures.
          If set to true, it means that at least one of the measures must be in the range of selections for the group of measures to be selected.
          If set to false, it means that all measures must be in the range of selections for the group of measures to be selected.
          The default value is false.

        qDeselectOnlyOneSelected: bool
          Set this parameter to true to unselect the last single selected value. There must be only one selected value in the field.
          The default value is false.

        """
        params = {}
        params["qPath"] = qPath
        params["qRanges"] = qRanges
        if qColumnsToSelect is not None:
            params["qColumnsToSelect"] = qColumnsToSelect
        if qOrMode is not None:
            params["qOrMode"] = qOrMode
        if qDeselectOnlyOneSelected is not None:
            params["qDeselectOnlyOneSelected"] = qDeselectOnlyOneSelected
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("RangeSelectHyperCubeValues", handle, **params)[
            "qSuccess"
        ]
        return response

    def multi_range_select_hyper_cube_values(
        self,
        qPath: str,
        qRanges: list[NxMultiRangeSelectInfo],
        qOrMode: bool = None,
        qDeselectOnlyOneSelected: bool = None,
    ) -> bool:
        """
        Makes multiple range selections in measures.
        This method applies to hypercubes. For example, bar charts, tables and scatter plots.

        The member Change returns the handles of the objects that are updated following the selections.
        _qSuccess_ is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.


        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .

        qRanges: list[NxMultiRangeSelectInfo]
          Ranges of selections.

        qOrMode: bool
          Applies to hypercubes with multiple measures.
          If set to true, it means that at least one of the measures must be in the range of selections for the group of measures to be selected.
          If set to false, it means that all measures must be in the range of selections for the group of measures to be selected.
          The default value is false.

        qDeselectOnlyOneSelected: bool
          Set this parameter to true to unselect the last single selected value. There must be only one selected value in the field.
          The default value is false.

        """
        params = {}
        params["qPath"] = qPath
        params["qRanges"] = qRanges
        if qOrMode is not None:
            params["qOrMode"] = qOrMode
        if qDeselectOnlyOneSelected is not None:
            params["qDeselectOnlyOneSelected"] = qDeselectOnlyOneSelected
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send(
            "MultiRangeSelectHyperCubeValues", handle, **params
        )["qSuccess"]
        return response

    def multi_range_select_tree_data_values(
        self,
        qPath: str,
        qRanges: list[NxTreeMultiRangeSelectInfo],
        qOrMode: bool = None,
        qDeselectOnlyOneSelected: bool = None,
    ) -> bool:
        """


        qPath: str


        qRanges: list[NxTreeMultiRangeSelectInfo]


        qOrMode: bool


        qDeselectOnlyOneSelected: bool


        """
        params = {}
        params["qPath"] = qPath
        params["qRanges"] = qRanges
        if qOrMode is not None:
            params["qOrMode"] = qOrMode
        if qDeselectOnlyOneSelected is not None:
            params["qDeselectOnlyOneSelected"] = qDeselectOnlyOneSelected
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send(
            "MultiRangeSelectTreeDataValues", handle, **params
        )["qSuccess"]
        return response

    def select_hyper_cube_continuous_range(
        self,
        qPath: str,
        qRanges: list[NxContinuousRangeSelectInfo],
        qSoftLock: bool = None,
    ) -> bool:
        """
        The following is returned in the output:
        The operation is successful if qSuccess is set to true.


        qPath: str
          Path to the definition of the object.
          For example, /qHyperCubeDef .

        qRanges: list[NxContinuousRangeSelectInfo]
          Selects ranges in a hypercube in (Ranges[N].Min,Ranges[N].Max) intervals.
          If either Ranges[N].MinInclEq or Ranges[N].MaxInclEq, or both flags are set to true then Min and Max values will be selected.

        qSoftLock: bool
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.

        """
        params = {}
        params["qPath"] = qPath
        params["qRanges"] = qRanges
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send(
            "SelectHyperCubeContinuousRange", handle, **params
        )["qSuccess"]
        return response

    def get_child(self, qId: str) -> GenericObject:
        """
        Returns the type of the object and the corresponding handle.


        qId: str
          Identifier of the object.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetChild", handle, **params)["qReturn"]
        obj = GenericObject(**response)
        obj._session = self._session
        return obj

    def get_parent(self) -> GenericObject:
        """
        Returns the type of the object and the corresponding handle to the parent object in the hiearchy.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetParent", handle)["qReturn"]
        obj = GenericObject(**response)
        obj._session = self._session
        return obj

    def get_child_infos(self) -> list[NxInfo]:
        """
        Returns the identifier and the type for each child in an app object. If the child contains extra properties in qInfos , these properties are returned.

        Full dynamic properties are optional and are returned if they exist in the definition of the object.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetChildInfos", handle)["qInfos"]
        return [NxInfo(e) for e in response]

    def create_child(
        self,
        qProp: GenericObjectProperties,
        qPropForThis: GenericObjectProperties = None,
    ) -> object:
        """
        Creates a generic object that is a child of another generic object.
        It is possible to update the properties of the child's parent at the same time that the child is created. Both operations are performed by the same call.
        It is possible to create a child that is linked to another generic object. The two objects have the same properties.


        qProp: GenericObjectProperties
          Information about the child.
          It is possible to create a child that is linked to another object.

        qPropForThis: GenericObjectProperties
          Identifier of the parent's object.
          Should be set to update the properties of the parent's object at the same time the child is created.

        """
        params = {}
        params["qProp"] = qProp
        if qPropForThis is not None:
            params["qPropForThis"] = qPropForThis
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateChild", handle, **params)
        return response

    def destroy_child(
        self, qId: str, qPropForThis: GenericObjectProperties = None
    ) -> bool:
        """
        Removes a child object.
        It is possible to update the properties of the child's parent at the same time that the child is removed. Both operations are performed by the same call.
        Removing a linked object, invalidate the linking object.

        The operation is successful if qSuccess is set to true.


        qId: str
          Identifier of the child to remove.

        qPropForThis: GenericObjectProperties
          Identifier of the parent's object and property to update.
          Should be set to update the properties of the parent's object at the same time the child is created.

        """
        params = {}
        params["qId"] = qId
        if qPropForThis is not None:
            params["qPropForThis"] = qPropForThis
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyChild", handle, **params)["qSuccess"]
        return response

    def destroy_all_children(
        self, qPropForThis: GenericObjectProperties = None
    ) -> object:
        """
        Removes all children and all children to the children on an object.


        qPropForThis: GenericObjectProperties
          Identifier of the parent's object and property to update.
          Should be set to update the properties of the parent's object at the same time the child is created.

        """
        params = {}
        if qPropForThis is not None:
            params["qPropForThis"] = qPropForThis
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyAllChildren", handle, **params)
        return response

    def set_child_array_order(self, qIds: list[str]) -> object:
        """
        Sets the order of the children in a generic object.
        To change the order of the children in a generic object, the identifiers of all the children must be included in the list of the identifiers (in qIds ).


        qIds: list[str]
          List of the children identifiers.

        """
        params = {}
        params["qIds"] = qIds
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetChildArrayOrder", handle, **params)
        return response

    def get_linked_objects(self) -> list[NxLinkedObjectInfo]:
        """
        Lists the linked objects to a generic object, a dimension or a measure.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLinkedObjects", handle)["qItems"]
        return [NxLinkedObjectInfo(e) for e in response]

    def copy_from(self, qFromId: str) -> object:
        """
        Copies the properties of a generic object and its children.
        The source object is specified by the parameter qFromId and the destination object is referenced by its handle.
        The identifier of the destination object is the same as before the copy takes place.


        qFromId: str
          Identifier of the object to copy.

        """
        params = {}
        params["qFromId"] = qFromId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CopyFrom", handle, **params)
        return response

    def begin_selections(self, qPaths: list[str]) -> object:
        """
        Begins the selection mode. The app enters the modal state. The specified object enters the selection mode and a modal window is opened. The selection mode can apply to only one object in an app at a time.
        When a visualization is in selection mode, selections can be made in this visualization. The visualization is not sorted until the selection mode is ended. Once the selection mode is ended and if the selections are accepted, the visualization is sorted according to the sort criteria. For more information about:

        • Ending the selection mode, see EndSelections Method.

        • The sort criteria, see ListObjectDef or HyperCubeDef.

        Example:

        A sheet contains a list object and a chart. If the list object is in selection mode then the chart cannot be in selection mode. No selection on the chart can be made until the list object exits the selection mode.


        qPaths: list[str]
          List of the paths to the definition of the objects to enter selection mode.
          For example, /qListObjectDef .

        """
        params = {}
        params["qPaths"] = qPaths
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("BeginSelections", handle, **params)
        return response

    def end_selections(self, qAccept: bool) -> object:
        """
        Ends the selection mode on a visualization. The selections are accepted or aborted when exiting the selection mode, depending on the qAccept parameter value.


        qAccept: bool
          Set this parameter to true to accept the selections before exiting the selection mode.

        """
        params = {}
        params["qAccept"] = qAccept
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("EndSelections", handle, **params)
        return response

    def reset_made_selections(self) -> object:
        """
        Resets all selections made in selection mode.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ResetMadeSelections", handle)
        return response

    def embed_snapshot_object(self, qId: str) -> object:
        """
        Adds a snapshot to a generic object.
        Only one snapshot can be embedded in a generic object.
        If you embed a snapshot in an object that already contains a snapshot, the new snapshot overwrites the previous one.


        qId: str
          Identifier of the bookmark.

        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("EmbedSnapshotObject", handle, **params)
        return response

    def get_snapshot_object(self) -> GenericObject:
        """
        Returns the type of the object and the corresponding handle.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetSnapshotObject", handle)["qReturn"]
        obj = GenericObject(**response)
        obj._session = self._session
        return obj

    def publish(self) -> object:
        """
        Publishes a generic object.
        This operation is not applicable for Qlik Sense Desktop.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Publish", handle)
        return response

    def un_publish(self) -> object:
        """
        Unpublishes a generic object.
        This operation is not applicable for Qlik Sense Desktop.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnPublish", handle)
        return response

    def approve(self) -> object:
        """
        Adds the generic object to the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Approve", handle)
        return response

    def un_approve(self) -> object:
        """
        Removes the generic object from the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnApprove", handle)
        return response


@dataclass
class GenericObjectLayout:
    """
    Is the layout for GenericObjectProperties.

    Attributes
    ----------
    qInfo: NxInfo
      Identifier and type of the generic object.
    qMeta: NxMeta
      Information about publishing and permissions.
      This parameter is optional.
    qExtendsId: str
      Should be set to create an object that is linked to another object. Enter the identifier of the object you want to link to.
      If you do not want to link your object, set this parameter to an empty string.
    qHasSoftPatches: bool
      Is set to true if the generic object contains some properties that are not persistent (a soft patch was applied).
    qError: NxLayoutErrors
      Gives information on the error.
      This parameter is optional.
    qSelectionInfo: NxSelectionInfo
      Information about the selections.
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .

    Additional Attributes
    ---------------------
    qAppObjectList: AppObjectList
      Lists the app objects. Is the layout for AppObjectListDef.
      An app object is a generic object created at app level.
    qBookmarkList: BookmarkList
      Lists the bookmarks. Is the layout for BookmarkListDef.
    qChildList: ChildList
      Lists the children of a generic object. Is the layout for ChildListDef.
      ChildList is used by the GetLayout Method to list the children of a generic object.
    qDimensionList: DimensionList
      Lists the dimensions. Is the layout for DimensionListDef.
    qEmbeddedSnapshot: EmbeddedSnapshot
      Renders the embedded snapshot in an object.
      The following is returned:

      • Any dynamic properties defined in the bookmark

      • Any properties defined in qEmbeddedSnapshot

      Properties:

      "qEmbeddedSnapshot": {}
    qExtensionList: ExtensionList
      Obsolete, use qrs API's to fetch extensions.
    qFieldList: FieldList
      Lists the fields present in the data model viewer. Is the layout for FieldListDef.
    qHyperCube: HyperCube
      Renders the properties of a hypercube. Is the layout for HyperCubeDef.
      For more information about the definition of a hypercube, see Generic object.
      What is returned in HyperCube depends on the type of the hypercube (straight, pivot or stacked table, or tree) and on the method called (GetLayout, GetHyperCubeData, GetHyperCubePivotData, GetHyperCubeStackData, GetHyperCubeTreeData).
    qListObject: ListObject
      Renders the properties of a list object. Is the layout for ListObjectDef.
      For more information about the definition of a list object, see Generic object.
      ListObject is used by the GetLayout Method to display the properties of a list object.
    qMeasureList: MeasureList
      Lists the measures. Is the layout for MeasureListDef.
    qMediaList: MediaList
      Lists the media files. Is the layout for MediaListDef.
      This struct is deprecated.
    qNxLibraryDimension: NxLibraryDimension
    qNxLibraryMeasure: NxLibraryMeasure
      Information about the library measure. Is the layout for NxLibraryMeasureDef.
    qSelectionObject: SelectionObject
      Indicates which selections are currently applied. It gives the current selections. Is the layout for SelectionObjectDef.
    qStaticContentUrl: StaticContentUrl
      In addition, this structure can return dynamic properties.
    qTreeData: TreeData
      Renders the properties of a TreeData object. Is the layout for TreeDataDef.
      For more information about the definition of TreeData, see Generic object.
      To retrieve data from the TreeData object, use the method called GetHyperCubeTreeData.
    qUndoInfo: UndoInfo
      Displays information about the number of possible undos and redos. Is the layout for UndoInfoDef.
    qVariableList: VariableList
      Lists the variables in an app. Is the layout for VariableListDef.
    """

    qInfo: NxInfo = None
    qMeta: NxMeta = None
    qExtendsId: str = None
    qHasSoftPatches: bool = None
    qError: NxLayoutErrors = None
    qSelectionInfo: NxSelectionInfo = None
    qStateName: str = None
    qAppObjectList: AppObjectList = None
    qBookmarkList: BookmarkList = None
    qChildList: ChildList = None
    qDimensionList: DimensionList = None
    qEmbeddedSnapshot: EmbeddedSnapshot = None
    qExtensionList: ExtensionList = None
    qFieldList: FieldList = None
    qHyperCube: HyperCube = None
    qListObject: ListObject = None
    qMeasureList: MeasureList = None
    qMediaList: MediaList = None
    qNxLibraryDimension: NxLibraryDimension = None
    qNxLibraryMeasure: NxLibraryMeasure = None
    qSelectionObject: SelectionObject = None
    qStaticContentUrl: StaticContentUrl = None
    qTreeData: TreeData = None
    qUndoInfo: UndoInfo = None
    qVariableList: VariableList = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        if "qMeta" in kvargs:
            if type(kvargs["qMeta"]).__name__ is self_.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(**kvargs["qMeta"])
        if "qExtendsId" in kvargs:
            if (
                type(kvargs["qExtendsId"]).__name__
                is self_.__annotations__["qExtendsId"]
            ):
                self_.qExtendsId = kvargs["qExtendsId"]
            else:
                self_.qExtendsId = kvargs["qExtendsId"]
        if "qHasSoftPatches" in kvargs:
            if (
                type(kvargs["qHasSoftPatches"]).__name__
                is self_.__annotations__["qHasSoftPatches"]
            ):
                self_.qHasSoftPatches = kvargs["qHasSoftPatches"]
            else:
                self_.qHasSoftPatches = kvargs["qHasSoftPatches"]
        if "qError" in kvargs:
            if type(kvargs["qError"]).__name__ is self_.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxLayoutErrors(**kvargs["qError"])
        if "qSelectionInfo" in kvargs:
            if (
                type(kvargs["qSelectionInfo"]).__name__
                is self_.__annotations__["qSelectionInfo"]
            ):
                self_.qSelectionInfo = kvargs["qSelectionInfo"]
            else:
                self_.qSelectionInfo = NxSelectionInfo(**kvargs["qSelectionInfo"])
        if "qStateName" in kvargs:
            if (
                type(kvargs["qStateName"]).__name__
                is self_.__annotations__["qStateName"]
            ):
                self_.qStateName = kvargs["qStateName"]
            else:
                self_.qStateName = kvargs["qStateName"]
        if "qAppObjectList" in kvargs:
            if (
                type(kvargs["qAppObjectList"]).__name__
                is self_.__annotations__["qAppObjectList"]
            ):
                self_.qAppObjectList = kvargs["qAppObjectList"]
            else:
                self_.qAppObjectList = AppObjectList(**kvargs["qAppObjectList"])
        if "qBookmarkList" in kvargs:
            if (
                type(kvargs["qBookmarkList"]).__name__
                is self_.__annotations__["qBookmarkList"]
            ):
                self_.qBookmarkList = kvargs["qBookmarkList"]
            else:
                self_.qBookmarkList = BookmarkList(**kvargs["qBookmarkList"])
        if "qChildList" in kvargs:
            if (
                type(kvargs["qChildList"]).__name__
                is self_.__annotations__["qChildList"]
            ):
                self_.qChildList = kvargs["qChildList"]
            else:
                self_.qChildList = ChildList(**kvargs["qChildList"])
        if "qDimensionList" in kvargs:
            if (
                type(kvargs["qDimensionList"]).__name__
                is self_.__annotations__["qDimensionList"]
            ):
                self_.qDimensionList = kvargs["qDimensionList"]
            else:
                self_.qDimensionList = DimensionList(**kvargs["qDimensionList"])
        if "qEmbeddedSnapshot" in kvargs:
            if (
                type(kvargs["qEmbeddedSnapshot"]).__name__
                is self_.__annotations__["qEmbeddedSnapshot"]
            ):
                self_.qEmbeddedSnapshot = kvargs["qEmbeddedSnapshot"]
            else:
                self_.qEmbeddedSnapshot = EmbeddedSnapshot(
                    **kvargs["qEmbeddedSnapshot"]
                )
        if "qExtensionList" in kvargs:
            if (
                type(kvargs["qExtensionList"]).__name__
                is self_.__annotations__["qExtensionList"]
            ):
                self_.qExtensionList = kvargs["qExtensionList"]
            else:
                self_.qExtensionList = ExtensionList(**kvargs["qExtensionList"])
        if "qFieldList" in kvargs:
            if (
                type(kvargs["qFieldList"]).__name__
                is self_.__annotations__["qFieldList"]
            ):
                self_.qFieldList = kvargs["qFieldList"]
            else:
                self_.qFieldList = FieldList(**kvargs["qFieldList"])
        if "qHyperCube" in kvargs:
            if (
                type(kvargs["qHyperCube"]).__name__
                is self_.__annotations__["qHyperCube"]
            ):
                self_.qHyperCube = kvargs["qHyperCube"]
            else:
                self_.qHyperCube = HyperCube(**kvargs["qHyperCube"])
        if "qListObject" in kvargs:
            if (
                type(kvargs["qListObject"]).__name__
                is self_.__annotations__["qListObject"]
            ):
                self_.qListObject = kvargs["qListObject"]
            else:
                self_.qListObject = ListObject(**kvargs["qListObject"])
        if "qMeasureList" in kvargs:
            if (
                type(kvargs["qMeasureList"]).__name__
                is self_.__annotations__["qMeasureList"]
            ):
                self_.qMeasureList = kvargs["qMeasureList"]
            else:
                self_.qMeasureList = MeasureList(**kvargs["qMeasureList"])
        if "qMediaList" in kvargs:
            if (
                type(kvargs["qMediaList"]).__name__
                is self_.__annotations__["qMediaList"]
            ):
                self_.qMediaList = kvargs["qMediaList"]
            else:
                self_.qMediaList = MediaList(**kvargs["qMediaList"])
        if "qNxLibraryDimension" in kvargs:
            if (
                type(kvargs["qNxLibraryDimension"]).__name__
                is self_.__annotations__["qNxLibraryDimension"]
            ):
                self_.qNxLibraryDimension = kvargs["qNxLibraryDimension"]
            else:
                self_.qNxLibraryDimension = NxLibraryDimension(
                    **kvargs["qNxLibraryDimension"]
                )
        if "qNxLibraryMeasure" in kvargs:
            if (
                type(kvargs["qNxLibraryMeasure"]).__name__
                is self_.__annotations__["qNxLibraryMeasure"]
            ):
                self_.qNxLibraryMeasure = kvargs["qNxLibraryMeasure"]
            else:
                self_.qNxLibraryMeasure = NxLibraryMeasure(
                    **kvargs["qNxLibraryMeasure"]
                )
        if "qSelectionObject" in kvargs:
            if (
                type(kvargs["qSelectionObject"]).__name__
                is self_.__annotations__["qSelectionObject"]
            ):
                self_.qSelectionObject = kvargs["qSelectionObject"]
            else:
                self_.qSelectionObject = SelectionObject(**kvargs["qSelectionObject"])
        if "qStaticContentUrl" in kvargs:
            if (
                type(kvargs["qStaticContentUrl"]).__name__
                is self_.__annotations__["qStaticContentUrl"]
            ):
                self_.qStaticContentUrl = kvargs["qStaticContentUrl"]
            else:
                self_.qStaticContentUrl = StaticContentUrl(
                    **kvargs["qStaticContentUrl"]
                )
        if "qTreeData" in kvargs:
            if type(kvargs["qTreeData"]).__name__ is self_.__annotations__["qTreeData"]:
                self_.qTreeData = kvargs["qTreeData"]
            else:
                self_.qTreeData = TreeData(**kvargs["qTreeData"])
        if "qUndoInfo" in kvargs:
            if type(kvargs["qUndoInfo"]).__name__ is self_.__annotations__["qUndoInfo"]:
                self_.qUndoInfo = kvargs["qUndoInfo"]
            else:
                self_.qUndoInfo = UndoInfo(**kvargs["qUndoInfo"])
        if "qVariableList" in kvargs:
            if (
                type(kvargs["qVariableList"]).__name__
                is self_.__annotations__["qVariableList"]
            ):
                self_.qVariableList = kvargs["qVariableList"]
            else:
                self_.qVariableList = VariableList(**kvargs["qVariableList"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericObjectProperties:
    """

    Attributes
    ----------
    qInfo: NxInfo
      Identifier and type of the object.
      This parameter is mandatory.
    qExtendsId: str
      Should be set to create an object that is linked to another object. Enter the identifier of the linking object (i.e the object you want to link to).
      If you do not want to link your object, set this parameter to an empty string.
    qMetaDef: NxMetaDef
      Definition of the dynamic properties.
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .

    Additional Attributes
    ---------------------
    qAppObjectListDef: AppObjectListDef
      Defines the list of objects in an app.
      An app object is a generic object created at app level.
    qBookmarkListDef: BookmarkListDef
      Defines the list of bookmarks.
    qChildListDef: ChildListDef
      Defines the list of children of a generic object.
      What is defined in ChildListDef has an impact on what the GetLayout method returns. See Example for more information.
    qDimensionListDef: DimensionListDef
      Defines the lists of dimensions.
    qEmbeddedSnapshotDef: EmbeddedSnapshotDef
      Defines the embedded snapshot in a generic object.

      Properties:

      "EmbeddedSnapshotDef": {}
    qExtensionListDef: ExtensionListDef
      Obsolete, use qrs API's to fetch extensions.
    qFieldListDef: FieldListDef
      Defines the fields to show.
    qHyperCubeDef: HyperCubeDef
      Defines the properties of a hypercube.
      For more information about the definition of a hypercube, see Generic object.
    qLayoutExclude: LayoutExclude
      Contains JSON to be excluded from validation.
    qListObjectDef: ListObjectDef
      Defines the properties of a list object.
      For more information about the definition of a list object, see Generic object.
    qMeasureListDef: MeasureListDef
      Defines the list of measures.
    qMediaListDef: MediaListDef
      Defines the list of media files.
      This struct is deprecated.

      Properties:

      "qMediaListDef": {}
      _qMediaListDef_ has an empty structure. No properties need to be set.
    qNxLibraryDimensionDef: NxLibraryDimensionDef
    qNxLibraryMeasureDef: NxLibraryMeasureDef
    qSelectionObjectDef: SelectionObjectDef
      To display the current selections.
      Can be added to any generic object but is particularly meaningful when using session objects to monitor an app.

      Properties:

      "qSelectionObjectDef": {}
    qStaticContentUrlDef: StaticContentUrlDef
      In addition, this structure can contain dynamic properties.
    qStringExpression: StringExpression
      Properties:

      Abbreviated syntax:
      "qStringExpression":"=<expression>"
      Extended object syntax:
      "qStringExpression":{"qExpr":"=<expression>"}
      Where:

      • < expression > is a string

      The "=" sign in the string expression is not mandatory. Even if the "=" sign is not given, the expression is evaluated.
      A string expression is not evaluated, if the expression is surrounded by simple quotes.

      The result of the evaluation of the expression can be of any type, as it is returned as a JSON (quoted) string.
    qTreeDataDef: TreeDataDef
      Defines the properties of a TreeData object.
      For more information about the definition of a TreeData object, see Generic object.
    qUndoInfoDef: UndoInfoDef
      Defines if an object should contain information on the number of possible undo and redo.

      Properties:

      "qUndoInfoDef": {}
      The numbers of undos and redos are empty when an object is created. The number of possible undos is increased every time an action (for example, create a child, set some properties) on the object is performed. The number of possible redos is increased every time an undo action is performed.
    qValueExpression: ValueExpression
      Properties:

      Abbreviated syntax:
      "qValueExpression":"=<expression>"
      Extended object syntax:
      "qValueExpression":{"qExpr":"=<expression>"}
      Where:

      • < expression > is a string.

      The "=" sign in the value expression is not mandatory. Even if the "=" sign is not given, the expression is evaluated.

      The expression is evaluated as a numeric.
    qVariableListDef: VariableListDef
      Defines the list of variables in an app.
    """

    qInfo: NxInfo = None
    qExtendsId: str = None
    qMetaDef: NxMetaDef = None
    qStateName: str = None
    qAppObjectListDef: AppObjectListDef = None
    qBookmarkListDef: BookmarkListDef = None
    qChildListDef: ChildListDef = None
    qDimensionListDef: DimensionListDef = None
    qEmbeddedSnapshotDef: EmbeddedSnapshotDef = None
    qExtensionListDef: ExtensionListDef = None
    qFieldListDef: FieldListDef = None
    qHyperCubeDef: HyperCubeDef = None
    qLayoutExclude: LayoutExclude = None
    qListObjectDef: ListObjectDef = None
    qMeasureListDef: MeasureListDef = None
    qMediaListDef: MediaListDef = None
    qNxLibraryDimensionDef: NxLibraryDimensionDef = None
    qNxLibraryMeasureDef: NxLibraryMeasureDef = None
    qSelectionObjectDef: SelectionObjectDef = None
    qStaticContentUrlDef: StaticContentUrlDef = None
    qStringExpression: StringExpression = None
    qTreeDataDef: TreeDataDef = None
    qUndoInfoDef: UndoInfoDef = None
    qValueExpression: ValueExpression = None
    qVariableListDef: VariableListDef = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        if "qExtendsId" in kvargs:
            if (
                type(kvargs["qExtendsId"]).__name__
                is self_.__annotations__["qExtendsId"]
            ):
                self_.qExtendsId = kvargs["qExtendsId"]
            else:
                self_.qExtendsId = kvargs["qExtendsId"]
        if "qMetaDef" in kvargs:
            if type(kvargs["qMetaDef"]).__name__ is self_.__annotations__["qMetaDef"]:
                self_.qMetaDef = kvargs["qMetaDef"]
            else:
                self_.qMetaDef = NxMetaDef(**kvargs["qMetaDef"])
        if "qStateName" in kvargs:
            if (
                type(kvargs["qStateName"]).__name__
                is self_.__annotations__["qStateName"]
            ):
                self_.qStateName = kvargs["qStateName"]
            else:
                self_.qStateName = kvargs["qStateName"]
        if "qAppObjectListDef" in kvargs:
            if (
                type(kvargs["qAppObjectListDef"]).__name__
                is self_.__annotations__["qAppObjectListDef"]
            ):
                self_.qAppObjectListDef = kvargs["qAppObjectListDef"]
            else:
                self_.qAppObjectListDef = AppObjectListDef(
                    **kvargs["qAppObjectListDef"]
                )
        if "qBookmarkListDef" in kvargs:
            if (
                type(kvargs["qBookmarkListDef"]).__name__
                is self_.__annotations__["qBookmarkListDef"]
            ):
                self_.qBookmarkListDef = kvargs["qBookmarkListDef"]
            else:
                self_.qBookmarkListDef = BookmarkListDef(**kvargs["qBookmarkListDef"])
        if "qChildListDef" in kvargs:
            if (
                type(kvargs["qChildListDef"]).__name__
                is self_.__annotations__["qChildListDef"]
            ):
                self_.qChildListDef = kvargs["qChildListDef"]
            else:
                self_.qChildListDef = ChildListDef(**kvargs["qChildListDef"])
        if "qDimensionListDef" in kvargs:
            if (
                type(kvargs["qDimensionListDef"]).__name__
                is self_.__annotations__["qDimensionListDef"]
            ):
                self_.qDimensionListDef = kvargs["qDimensionListDef"]
            else:
                self_.qDimensionListDef = DimensionListDef(
                    **kvargs["qDimensionListDef"]
                )
        if "qEmbeddedSnapshotDef" in kvargs:
            if (
                type(kvargs["qEmbeddedSnapshotDef"]).__name__
                is self_.__annotations__["qEmbeddedSnapshotDef"]
            ):
                self_.qEmbeddedSnapshotDef = kvargs["qEmbeddedSnapshotDef"]
            else:
                self_.qEmbeddedSnapshotDef = EmbeddedSnapshotDef(
                    **kvargs["qEmbeddedSnapshotDef"]
                )
        if "qExtensionListDef" in kvargs:
            if (
                type(kvargs["qExtensionListDef"]).__name__
                is self_.__annotations__["qExtensionListDef"]
            ):
                self_.qExtensionListDef = kvargs["qExtensionListDef"]
            else:
                self_.qExtensionListDef = ExtensionListDef(
                    **kvargs["qExtensionListDef"]
                )
        if "qFieldListDef" in kvargs:
            if (
                type(kvargs["qFieldListDef"]).__name__
                is self_.__annotations__["qFieldListDef"]
            ):
                self_.qFieldListDef = kvargs["qFieldListDef"]
            else:
                self_.qFieldListDef = FieldListDef(**kvargs["qFieldListDef"])
        if "qHyperCubeDef" in kvargs:
            if (
                type(kvargs["qHyperCubeDef"]).__name__
                is self_.__annotations__["qHyperCubeDef"]
            ):
                self_.qHyperCubeDef = kvargs["qHyperCubeDef"]
            else:
                self_.qHyperCubeDef = HyperCubeDef(**kvargs["qHyperCubeDef"])
        if "qLayoutExclude" in kvargs:
            if (
                type(kvargs["qLayoutExclude"]).__name__
                is self_.__annotations__["qLayoutExclude"]
            ):
                self_.qLayoutExclude = kvargs["qLayoutExclude"]
            else:
                self_.qLayoutExclude = LayoutExclude(**kvargs["qLayoutExclude"])
        if "qListObjectDef" in kvargs:
            if (
                type(kvargs["qListObjectDef"]).__name__
                is self_.__annotations__["qListObjectDef"]
            ):
                self_.qListObjectDef = kvargs["qListObjectDef"]
            else:
                self_.qListObjectDef = ListObjectDef(**kvargs["qListObjectDef"])
        if "qMeasureListDef" in kvargs:
            if (
                type(kvargs["qMeasureListDef"]).__name__
                is self_.__annotations__["qMeasureListDef"]
            ):
                self_.qMeasureListDef = kvargs["qMeasureListDef"]
            else:
                self_.qMeasureListDef = MeasureListDef(**kvargs["qMeasureListDef"])
        if "qMediaListDef" in kvargs:
            if (
                type(kvargs["qMediaListDef"]).__name__
                is self_.__annotations__["qMediaListDef"]
            ):
                self_.qMediaListDef = kvargs["qMediaListDef"]
            else:
                self_.qMediaListDef = MediaListDef(**kvargs["qMediaListDef"])
        if "qNxLibraryDimensionDef" in kvargs:
            if (
                type(kvargs["qNxLibraryDimensionDef"]).__name__
                is self_.__annotations__["qNxLibraryDimensionDef"]
            ):
                self_.qNxLibraryDimensionDef = kvargs["qNxLibraryDimensionDef"]
            else:
                self_.qNxLibraryDimensionDef = NxLibraryDimensionDef(
                    **kvargs["qNxLibraryDimensionDef"]
                )
        if "qNxLibraryMeasureDef" in kvargs:
            if (
                type(kvargs["qNxLibraryMeasureDef"]).__name__
                is self_.__annotations__["qNxLibraryMeasureDef"]
            ):
                self_.qNxLibraryMeasureDef = kvargs["qNxLibraryMeasureDef"]
            else:
                self_.qNxLibraryMeasureDef = NxLibraryMeasureDef(
                    **kvargs["qNxLibraryMeasureDef"]
                )
        if "qSelectionObjectDef" in kvargs:
            if (
                type(kvargs["qSelectionObjectDef"]).__name__
                is self_.__annotations__["qSelectionObjectDef"]
            ):
                self_.qSelectionObjectDef = kvargs["qSelectionObjectDef"]
            else:
                self_.qSelectionObjectDef = SelectionObjectDef(
                    **kvargs["qSelectionObjectDef"]
                )
        if "qStaticContentUrlDef" in kvargs:
            if (
                type(kvargs["qStaticContentUrlDef"]).__name__
                is self_.__annotations__["qStaticContentUrlDef"]
            ):
                self_.qStaticContentUrlDef = kvargs["qStaticContentUrlDef"]
            else:
                self_.qStaticContentUrlDef = StaticContentUrlDef(
                    **kvargs["qStaticContentUrlDef"]
                )
        if "qStringExpression" in kvargs:
            if (
                type(kvargs["qStringExpression"]).__name__
                is self_.__annotations__["qStringExpression"]
            ):
                self_.qStringExpression = kvargs["qStringExpression"]
            else:
                self_.qStringExpression = StringExpression(
                    **kvargs["qStringExpression"]
                )
        if "qTreeDataDef" in kvargs:
            if (
                type(kvargs["qTreeDataDef"]).__name__
                is self_.__annotations__["qTreeDataDef"]
            ):
                self_.qTreeDataDef = kvargs["qTreeDataDef"]
            else:
                self_.qTreeDataDef = TreeDataDef(**kvargs["qTreeDataDef"])
        if "qUndoInfoDef" in kvargs:
            if (
                type(kvargs["qUndoInfoDef"]).__name__
                is self_.__annotations__["qUndoInfoDef"]
            ):
                self_.qUndoInfoDef = kvargs["qUndoInfoDef"]
            else:
                self_.qUndoInfoDef = UndoInfoDef(**kvargs["qUndoInfoDef"])
        if "qValueExpression" in kvargs:
            if (
                type(kvargs["qValueExpression"]).__name__
                is self_.__annotations__["qValueExpression"]
            ):
                self_.qValueExpression = kvargs["qValueExpression"]
            else:
                self_.qValueExpression = ValueExpression(**kvargs["qValueExpression"])
        if "qVariableListDef" in kvargs:
            if (
                type(kvargs["qVariableListDef"]).__name__
                is self_.__annotations__["qVariableListDef"]
            ):
                self_.qVariableListDef = kvargs["qVariableListDef"]
            else:
                self_.qVariableListDef = VariableListDef(**kvargs["qVariableListDef"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericVariable:
    """

    Attributes
    ----------
    qType: str
      The native type of the object.
    qHandle: int
      The handle used to connect to object.
    qGenericType: str
      The type of the object.
    qGenericId: str
      Object ID.
    """

    qType: str = None
    qHandle: int = None
    qGenericType: str = None
    qGenericId: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qHandle" in kvargs:
            if type(kvargs["qHandle"]).__name__ is self_.__annotations__["qHandle"]:
                self_.qHandle = kvargs["qHandle"]
            else:
                self_.qHandle = kvargs["qHandle"]
        if "qGenericType" in kvargs:
            if (
                type(kvargs["qGenericType"]).__name__
                is self_.__annotations__["qGenericType"]
            ):
                self_.qGenericType = kvargs["qGenericType"]
            else:
                self_.qGenericType = kvargs["qGenericType"]
        if "qGenericId" in kvargs:
            if (
                type(kvargs["qGenericId"]).__name__
                is self_.__annotations__["qGenericId"]
            ):
                self_.qGenericId = kvargs["qGenericId"]
            else:
                self_.qGenericId = kvargs["qGenericId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_layout(self) -> GenericVariableLayout:
        """
        Evaluates an object and displays its properties including the dynamic properties.
        If the member delta is set to true in the request object, only the delta is evaluated.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLayout", handle)["qLayout"]
        obj = GenericVariableLayout(**response)
        obj._session = self._session
        return obj

    def apply_patches(self, qPatches: list[NxPatch]) -> object:
        """
        Applies a patch to the properties of a variable. Allows an update to some of the properties. It should not be possible to patch "/qInfo/qId",
        and it will be forbidden in the near future.
        Applying a patch takes less time than resetting all the properties.


        qPatches: list[NxPatch]
          Array of patches.

        """
        params = {}
        params["qPatches"] = qPatches
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyPatches", handle, **params)
        return response

    def set_properties(self, qProp: GenericVariableProperties) -> object:
        """
        Sets some properties for a variable.
        The identifier of a variable cannot be modified.
        You cannot update the properties of a script-defined variable using the SetProperties method.


        qProp: GenericVariableProperties
          Information about the variable.

        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetProperties", handle, **params)
        return response

    def get_properties(self) -> GenericVariableProperties:
        """
        Shows the properties of an object.
        If the member delta is set to true in the request, only the delta is retrieved.

        The following is always returned in the output:


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetProperties", handle)["qProp"]
        obj = GenericVariableProperties(**response)
        obj._session = self._session
        return obj

    def get_info(self) -> NxInfo:
        """
        Returns the type and identifier of the object.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetInfo", handle)["qInfo"]
        obj = NxInfo(**response)
        obj._session = self._session
        return obj

    def set_string_value(self, qVal: str) -> object:
        """
        Sets a string value to a variable.
        These changes are not persistent. They only last the duration of the engine session.


        qVal: str
          Value of the variable. The string can contain an expression.

        """
        params = {}
        params["qVal"] = qVal
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetStringValue", handle, **params)
        return response

    def set_num_value(self, qVal: float) -> object:
        """
        Sets a numerical value to a variable.
        These changes are not persistent. They only last the duration of the engine session.


        qVal: float
          Value of the variable.

        """
        params = {}
        params["qVal"] = qVal
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetNumValue", handle, **params)
        return response

    def set_dual_value(self, qText: str, qNum: float) -> object:
        """
        Sets the value of a dual variable.
        These changes are not persistent. They only last the duration of the engine session.


        qText: str
          String representation of a dual value. Set this parameter to "", if the string representation is to be Null.

        qNum: float
          Numeric representation of a dual value.

        """
        params = {}
        params["qText"] = qText
        params["qNum"] = qNum
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetDualValue", handle, **params)
        return response

    def get_raw_content(self) -> str:
        """
        Returns the raw value of a variable.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetRawContent", handle)["qReturn"]
        return response


@dataclass
class GenericVariableLayout:
    """
    Is the layout for GenericVariableProperties.

    Attributes
    ----------
    qInfo: NxInfo
      Identifier and type of the object.
      This parameter is mandatory.
    qMeta: NxMeta
      Information about publishing and permissions.
      This parameter is optional.
    qText: str
      Some text.
    qNum: float
      A value.
    qIsScriptCreated: bool
      If set to true, it means that the variable was defined via script.
    """

    qInfo: NxInfo = None
    qMeta: NxMeta = None
    qText: str = None
    qNum: float = None
    qIsScriptCreated: bool = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        if "qMeta" in kvargs:
            if type(kvargs["qMeta"]).__name__ is self_.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(**kvargs["qMeta"])
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qNum" in kvargs:
            if type(kvargs["qNum"]).__name__ is self_.__annotations__["qNum"]:
                self_.qNum = kvargs["qNum"]
            else:
                self_.qNum = kvargs["qNum"]
        if "qIsScriptCreated" in kvargs:
            if (
                type(kvargs["qIsScriptCreated"]).__name__
                is self_.__annotations__["qIsScriptCreated"]
            ):
                self_.qIsScriptCreated = kvargs["qIsScriptCreated"]
            else:
                self_.qIsScriptCreated = kvargs["qIsScriptCreated"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericVariableProperties:
    """

    Attributes
    ----------
    qInfo: NxInfo
      Identifier and type of the object.
      This parameter is mandatory.
    qMetaDef: NxMetaDef
      Meta data.
    qName: str
      Name of the variable.
      The name must be unique.
      This parameter is mandatory.
    qComment: str
      Comment related to the variable.
      This parameter is optional.
    qNumberPresentation: FieldAttributes
      Defines the format of the value.
      This parameter is optional.
    qIncludeInBookmark: bool
      Set this property to true to update the variable when applying a bookmark. The variable value will be persisted in the bookmark.
      The value of a variable can affect the state of the selections.
      Script variables cannot be persisted in the bookmark.
      The default value is false.
    qDefinition: str
      Definition of the variable.
    """

    qInfo: NxInfo = None
    qMetaDef: NxMetaDef = None
    qName: str = None
    qComment: str = None
    qNumberPresentation: FieldAttributes = None
    qIncludeInBookmark: bool = None
    qDefinition: str = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        if "qMetaDef" in kvargs:
            if type(kvargs["qMetaDef"]).__name__ is self_.__annotations__["qMetaDef"]:
                self_.qMetaDef = kvargs["qMetaDef"]
            else:
                self_.qMetaDef = NxMetaDef(**kvargs["qMetaDef"])
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qComment" in kvargs:
            if type(kvargs["qComment"]).__name__ is self_.__annotations__["qComment"]:
                self_.qComment = kvargs["qComment"]
            else:
                self_.qComment = kvargs["qComment"]
        if "qNumberPresentation" in kvargs:
            if (
                type(kvargs["qNumberPresentation"]).__name__
                is self_.__annotations__["qNumberPresentation"]
            ):
                self_.qNumberPresentation = kvargs["qNumberPresentation"]
            else:
                self_.qNumberPresentation = FieldAttributes(
                    **kvargs["qNumberPresentation"]
                )
        if "qIncludeInBookmark" in kvargs:
            if (
                type(kvargs["qIncludeInBookmark"]).__name__
                is self_.__annotations__["qIncludeInBookmark"]
            ):
                self_.qIncludeInBookmark = kvargs["qIncludeInBookmark"]
            else:
                self_.qIncludeInBookmark = kvargs["qIncludeInBookmark"]
        if "qDefinition" in kvargs:
            if (
                type(kvargs["qDefinition"]).__name__
                is self_.__annotations__["qDefinition"]
            ):
                self_.qDefinition = kvargs["qDefinition"]
            else:
                self_.qDefinition = kvargs["qDefinition"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Global:
    """

    Attributes
    ----------
    qType: str
      The native type of the object.
    qHandle: int
      The handle used to connect to object.
    qGenericType: str
      The type of the object.
    qGenericId: str
      Object ID.
    """

    qType: str = None
    qHandle: int = None
    qGenericType: str = None
    qGenericId: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qHandle" in kvargs:
            if type(kvargs["qHandle"]).__name__ is self_.__annotations__["qHandle"]:
                self_.qHandle = kvargs["qHandle"]
            else:
                self_.qHandle = kvargs["qHandle"]
        if "qGenericType" in kvargs:
            if (
                type(kvargs["qGenericType"]).__name__
                is self_.__annotations__["qGenericType"]
            ):
                self_.qGenericType = kvargs["qGenericType"]
            else:
                self_.qGenericType = kvargs["qGenericType"]
        if "qGenericId" in kvargs:
            if (
                type(kvargs["qGenericId"]).__name__
                is self_.__annotations__["qGenericId"]
            ):
                self_.qGenericId = kvargs["qGenericId"]
            else:
                self_.qGenericId = kvargs["qGenericId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class InteractDef:
    """

    Attributes
    ----------
    qType: str
      Interaction type.

      One of:

      • IT_MSGBOX

      • IT_SCRIPTLINE

      • IT_BREAK

      • IT_INPUT

      • IT_END

      • IT_PASSWD

      • IT_USERNAME
    qTitle: str
      Title used in the message box dialog.
      This property is relevant if qType is *IT_MSGBOX*.
    qMsg: str
      Message used in the message box dialog.
      This property is relevant if qType is *IT_MSGBOX*.
    qButtons: int
      Buttons displayed in the message box dialog.
      This property is relevant if qType is *IT_MSGBOX*.
      One of:

      • 0 means that the qButtons property is not relevant.

      • 17 means that the message box contains the OK and Cancel buttons or the stop -sign icon.
    qLine: str
      Next script statement to be executed.
      This property is used if the type of interaction is *IT_SCRIPTLINE*.
    qOldLineNr: int
      First line number of the previously executed statement.
      This property is used if the type of interaction is *IT_SCRIPTLINE*.
    qNewLineNr: int
      First line number of the next statement to be executed.
      This property is used if the type of interaction is *IT_SCRIPTLINE*.
    qPath: str
      Path specified by the Include script variable.
      This property is used if the type of interaction is *IT_SCRIPTLINE*.
      Example of an Include variable:
      _$(Include=lib:\\\MyDataFiles\abc.txt);_
    qHidden: bool
      This property is set to true if the returned statement is an hidden script statement.
    qResult: int
      Not relevant for describing the requested user interaction.
    qInput: str
      Is not used in Qlik Sense.
    """

    qType: str = None
    qTitle: str = None
    qMsg: str = None
    qButtons: int = None
    qLine: str = None
    qOldLineNr: int = None
    qNewLineNr: int = None
    qPath: str = None
    qHidden: bool = None
    qResult: int = None
    qInput: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qTitle" in kvargs:
            if type(kvargs["qTitle"]).__name__ is self_.__annotations__["qTitle"]:
                self_.qTitle = kvargs["qTitle"]
            else:
                self_.qTitle = kvargs["qTitle"]
        if "qMsg" in kvargs:
            if type(kvargs["qMsg"]).__name__ is self_.__annotations__["qMsg"]:
                self_.qMsg = kvargs["qMsg"]
            else:
                self_.qMsg = kvargs["qMsg"]
        if "qButtons" in kvargs:
            if type(kvargs["qButtons"]).__name__ is self_.__annotations__["qButtons"]:
                self_.qButtons = kvargs["qButtons"]
            else:
                self_.qButtons = kvargs["qButtons"]
        if "qLine" in kvargs:
            if type(kvargs["qLine"]).__name__ is self_.__annotations__["qLine"]:
                self_.qLine = kvargs["qLine"]
            else:
                self_.qLine = kvargs["qLine"]
        if "qOldLineNr" in kvargs:
            if (
                type(kvargs["qOldLineNr"]).__name__
                is self_.__annotations__["qOldLineNr"]
            ):
                self_.qOldLineNr = kvargs["qOldLineNr"]
            else:
                self_.qOldLineNr = kvargs["qOldLineNr"]
        if "qNewLineNr" in kvargs:
            if (
                type(kvargs["qNewLineNr"]).__name__
                is self_.__annotations__["qNewLineNr"]
            ):
                self_.qNewLineNr = kvargs["qNewLineNr"]
            else:
                self_.qNewLineNr = kvargs["qNewLineNr"]
        if "qPath" in kvargs:
            if type(kvargs["qPath"]).__name__ is self_.__annotations__["qPath"]:
                self_.qPath = kvargs["qPath"]
            else:
                self_.qPath = kvargs["qPath"]
        if "qHidden" in kvargs:
            if type(kvargs["qHidden"]).__name__ is self_.__annotations__["qHidden"]:
                self_.qHidden = kvargs["qHidden"]
            else:
                self_.qHidden = kvargs["qHidden"]
        if "qResult" in kvargs:
            if type(kvargs["qResult"]).__name__ is self_.__annotations__["qResult"]:
                self_.qResult = kvargs["qResult"]
            else:
                self_.qResult = kvargs["qResult"]
        if "qInput" in kvargs:
            if type(kvargs["qInput"]).__name__ is self_.__annotations__["qInput"]:
                self_.qInput = kvargs["qInput"]
            else:
                self_.qInput = kvargs["qInput"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LayoutBookmarkData:
    """

    Attributes
    ----------
    qId: str
    qActive: bool
    qShowMode: int
    qScrollPos: ScrollPosition
    """

    qId: str = None
    qActive: bool = None
    qShowMode: int = None
    qScrollPos: ScrollPosition = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs:
            if type(kvargs["qId"]).__name__ is self_.__annotations__["qId"]:
                self_.qId = kvargs["qId"]
            else:
                self_.qId = kvargs["qId"]
        if "qActive" in kvargs:
            if type(kvargs["qActive"]).__name__ is self_.__annotations__["qActive"]:
                self_.qActive = kvargs["qActive"]
            else:
                self_.qActive = kvargs["qActive"]
        if "qShowMode" in kvargs:
            if type(kvargs["qShowMode"]).__name__ is self_.__annotations__["qShowMode"]:
                self_.qShowMode = kvargs["qShowMode"]
            else:
                self_.qShowMode = kvargs["qShowMode"]
        if "qScrollPos" in kvargs:
            if (
                type(kvargs["qScrollPos"]).__name__
                is self_.__annotations__["qScrollPos"]
            ):
                self_.qScrollPos = kvargs["qScrollPos"]
            else:
                self_.qScrollPos = ScrollPosition(**kvargs["qScrollPos"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MediaList:
    """
    Lists the media files. Is the layout for MediaListDef.
    This struct is deprecated.

    Attributes
    ----------
    qItems: list[MediaListItem]
      Information about the list of media files.
      In Qlik Sense Desktop, the media files are retrieved from:
      _%userprofile%\Documents\Qlik\Sense\Content\Default_
      In Qlik Sense Enterprise, the media files are retrieved from:
      <installation_directory>\Qlik\Sense\Repository\Content\Default
      The default installation directory is ProgramData .
    """

    qItems: list[MediaListItem] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs:
            if type(kvargs["qItems"]).__name__ is self_.__annotations__["qItems"]:
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [MediaListItem(**e) for e in kvargs["qItems"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAppLayout:
    """
    Qlik Sense Desktop:

    In Qlik Sense Desktop, this structure can contain dynamic properties.

    Qlik Sense Enterprise:

    In Qlik Sense Enterprise, only a few dynamic properties at the app level are persisted.
    The persisted dynamic properties are the following:

    • modifiedDate

    • published

    • publishTime

    • privileges

    • description

    • dynamicColor

    Attributes
    ----------
    qTitle: str
      Title of the app.
    qFileName: str
      In Qlik Sense Enterprise, this property corresponds to the app identifier (GUID).
      In Qlik Sense Desktop, this property corresponds to the full path of the app.
    qLastReloadTime: str
      Date and time of the last reload of the app in ISO format.
    qModified: bool
      Is set to true if the app has been updated since the last save.
    qHasScript: bool
      Is set to true if a script is defined in the app.
    qStateNames: list[str]
      Array of alternate states.
    qMeta: NxMeta
      Information on publishing and permissions.
    qLocaleInfo: LocaleInfo
      Information about the locale.
    qHasData: bool
      Is set to true if the app contains data following a script reload.
    qReadOnly: bool
      If set to true, it means that the app is read-only.
    qIsOpenedWithoutData: bool
      If set to true, it means that the app was opened without loading its data.
    qIsSessionApp: bool
      If set to true, the app is a Session App, i.e. not persistent.
    qThumbnail: StaticContentUrl
      App thumbnail.
    qIsBDILiveMode: bool
      If set to true, the app is in BDI Live Mode.
    qIsDirectQueryMode: bool
      If set to true, the app is in Direct Query Mode.
    qUnsupportedFeatures: list[NxFeature]
      Array of features not supported by the app.
    """

    qTitle: str = None
    qFileName: str = None
    qLastReloadTime: str = None
    qModified: bool = None
    qHasScript: bool = None
    qStateNames: list[str] = None
    qMeta: NxMeta = None
    qLocaleInfo: LocaleInfo = None
    qHasData: bool = None
    qReadOnly: bool = None
    qIsOpenedWithoutData: bool = None
    qIsSessionApp: bool = None
    qThumbnail: StaticContentUrl = None
    qIsBDILiveMode: bool = None
    qIsDirectQueryMode: bool = None
    qUnsupportedFeatures: list[NxFeature] = None

    def __init__(self_, **kvargs):
        if "qTitle" in kvargs:
            if type(kvargs["qTitle"]).__name__ is self_.__annotations__["qTitle"]:
                self_.qTitle = kvargs["qTitle"]
            else:
                self_.qTitle = kvargs["qTitle"]
        if "qFileName" in kvargs:
            if type(kvargs["qFileName"]).__name__ is self_.__annotations__["qFileName"]:
                self_.qFileName = kvargs["qFileName"]
            else:
                self_.qFileName = kvargs["qFileName"]
        if "qLastReloadTime" in kvargs:
            if (
                type(kvargs["qLastReloadTime"]).__name__
                is self_.__annotations__["qLastReloadTime"]
            ):
                self_.qLastReloadTime = kvargs["qLastReloadTime"]
            else:
                self_.qLastReloadTime = kvargs["qLastReloadTime"]
        if "qModified" in kvargs:
            if type(kvargs["qModified"]).__name__ is self_.__annotations__["qModified"]:
                self_.qModified = kvargs["qModified"]
            else:
                self_.qModified = kvargs["qModified"]
        if "qHasScript" in kvargs:
            if (
                type(kvargs["qHasScript"]).__name__
                is self_.__annotations__["qHasScript"]
            ):
                self_.qHasScript = kvargs["qHasScript"]
            else:
                self_.qHasScript = kvargs["qHasScript"]
        if "qStateNames" in kvargs:
            if (
                type(kvargs["qStateNames"]).__name__
                is self_.__annotations__["qStateNames"]
            ):
                self_.qStateNames = kvargs["qStateNames"]
            else:
                self_.qStateNames = kvargs["qStateNames"]
        if "qMeta" in kvargs:
            if type(kvargs["qMeta"]).__name__ is self_.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(**kvargs["qMeta"])
        if "qLocaleInfo" in kvargs:
            if (
                type(kvargs["qLocaleInfo"]).__name__
                is self_.__annotations__["qLocaleInfo"]
            ):
                self_.qLocaleInfo = kvargs["qLocaleInfo"]
            else:
                self_.qLocaleInfo = LocaleInfo(**kvargs["qLocaleInfo"])
        if "qHasData" in kvargs:
            if type(kvargs["qHasData"]).__name__ is self_.__annotations__["qHasData"]:
                self_.qHasData = kvargs["qHasData"]
            else:
                self_.qHasData = kvargs["qHasData"]
        if "qReadOnly" in kvargs:
            if type(kvargs["qReadOnly"]).__name__ is self_.__annotations__["qReadOnly"]:
                self_.qReadOnly = kvargs["qReadOnly"]
            else:
                self_.qReadOnly = kvargs["qReadOnly"]
        if "qIsOpenedWithoutData" in kvargs:
            if (
                type(kvargs["qIsOpenedWithoutData"]).__name__
                is self_.__annotations__["qIsOpenedWithoutData"]
            ):
                self_.qIsOpenedWithoutData = kvargs["qIsOpenedWithoutData"]
            else:
                self_.qIsOpenedWithoutData = kvargs["qIsOpenedWithoutData"]
        if "qIsSessionApp" in kvargs:
            if (
                type(kvargs["qIsSessionApp"]).__name__
                is self_.__annotations__["qIsSessionApp"]
            ):
                self_.qIsSessionApp = kvargs["qIsSessionApp"]
            else:
                self_.qIsSessionApp = kvargs["qIsSessionApp"]
        if "qThumbnail" in kvargs:
            if (
                type(kvargs["qThumbnail"]).__name__
                is self_.__annotations__["qThumbnail"]
            ):
                self_.qThumbnail = kvargs["qThumbnail"]
            else:
                self_.qThumbnail = StaticContentUrl(**kvargs["qThumbnail"])
        if "qIsBDILiveMode" in kvargs:
            if (
                type(kvargs["qIsBDILiveMode"]).__name__
                is self_.__annotations__["qIsBDILiveMode"]
            ):
                self_.qIsBDILiveMode = kvargs["qIsBDILiveMode"]
            else:
                self_.qIsBDILiveMode = kvargs["qIsBDILiveMode"]
        if "qIsDirectQueryMode" in kvargs:
            if (
                type(kvargs["qIsDirectQueryMode"]).__name__
                is self_.__annotations__["qIsDirectQueryMode"]
            ):
                self_.qIsDirectQueryMode = kvargs["qIsDirectQueryMode"]
            else:
                self_.qIsDirectQueryMode = kvargs["qIsDirectQueryMode"]
        if "qUnsupportedFeatures" in kvargs:
            if (
                type(kvargs["qUnsupportedFeatures"]).__name__
                is self_.__annotations__["qUnsupportedFeatures"]
            ):
                self_.qUnsupportedFeatures = kvargs["qUnsupportedFeatures"]
            else:
                self_.qUnsupportedFeatures = [
                    NxFeature(**e) for e in kvargs["qUnsupportedFeatures"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAppProperties:
    """
    Qlik Sense Desktop:

    In Qlik Sense Desktop, this structure can contain dynamic properties.

    Qlik Sense Enterprise:

    In Qlik Sense Enterprise, only a few dynamic properties at the app level are persisted.
    The persisted dynamic properties are the following:

    • modifiedDate

    • published

    • publishTime

    • privileges

    • description

    • dynamicColor

    Attributes
    ----------
    qTitle: str
      App title.
    qLastReloadTime: str
      Last reload time of the app.
    qMigrationHash: str
      Internal property reserved for app migration.
      Patch version of the app.
      Do not update.
    qSavedInProductVersion: str
      Internal property reserved for app migration.
      The app is saved in this version of the product.
      Do not update.
    qThumbnail: StaticContentUrlDef
      App thumbnail.
    qHasSectionAccess: bool
      If true the app has section access configured.
    """

    qTitle: str = None
    qLastReloadTime: str = None
    qMigrationHash: str = None
    qSavedInProductVersion: str = None
    qThumbnail: StaticContentUrlDef = None
    qHasSectionAccess: bool = None

    def __init__(self_, **kvargs):
        if "qTitle" in kvargs:
            if type(kvargs["qTitle"]).__name__ is self_.__annotations__["qTitle"]:
                self_.qTitle = kvargs["qTitle"]
            else:
                self_.qTitle = kvargs["qTitle"]
        if "qLastReloadTime" in kvargs:
            if (
                type(kvargs["qLastReloadTime"]).__name__
                is self_.__annotations__["qLastReloadTime"]
            ):
                self_.qLastReloadTime = kvargs["qLastReloadTime"]
            else:
                self_.qLastReloadTime = kvargs["qLastReloadTime"]
        if "qMigrationHash" in kvargs:
            if (
                type(kvargs["qMigrationHash"]).__name__
                is self_.__annotations__["qMigrationHash"]
            ):
                self_.qMigrationHash = kvargs["qMigrationHash"]
            else:
                self_.qMigrationHash = kvargs["qMigrationHash"]
        if "qSavedInProductVersion" in kvargs:
            if (
                type(kvargs["qSavedInProductVersion"]).__name__
                is self_.__annotations__["qSavedInProductVersion"]
            ):
                self_.qSavedInProductVersion = kvargs["qSavedInProductVersion"]
            else:
                self_.qSavedInProductVersion = kvargs["qSavedInProductVersion"]
        if "qThumbnail" in kvargs:
            if (
                type(kvargs["qThumbnail"]).__name__
                is self_.__annotations__["qThumbnail"]
            ):
                self_.qThumbnail = kvargs["qThumbnail"]
            else:
                self_.qThumbnail = StaticContentUrlDef(**kvargs["qThumbnail"])
        if "qHasSectionAccess" in kvargs:
            if (
                type(kvargs["qHasSectionAccess"]).__name__
                is self_.__annotations__["qHasSectionAccess"]
            ):
                self_.qHasSectionAccess = kvargs["qHasSectionAccess"]
            else:
                self_.qHasSectionAccess = kvargs["qHasSectionAccess"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttrDimInfo:
    """
    Layout for NxAttrDimDef.

    Attributes
    ----------
    qCardinal: int
      Cardinality of the attribute expression.
    qSize: Size
      Number of rows.
    qFallbackTitle: str
      The title for the attribute dimension.
    qLocked: bool
      The Locked value of the dimension.
    qError: NxValidationError
      Validation error.
    qIsCalculated: bool
      True if this is a calculated dimension.
    """

    qCardinal: int = None
    qSize: Size = None
    qFallbackTitle: str = None
    qLocked: bool = None
    qError: NxValidationError = None
    qIsCalculated: bool = None

    def __init__(self_, **kvargs):
        if "qCardinal" in kvargs:
            if type(kvargs["qCardinal"]).__name__ is self_.__annotations__["qCardinal"]:
                self_.qCardinal = kvargs["qCardinal"]
            else:
                self_.qCardinal = kvargs["qCardinal"]
        if "qSize" in kvargs:
            if type(kvargs["qSize"]).__name__ is self_.__annotations__["qSize"]:
                self_.qSize = kvargs["qSize"]
            else:
                self_.qSize = Size(**kvargs["qSize"])
        if "qFallbackTitle" in kvargs:
            if (
                type(kvargs["qFallbackTitle"]).__name__
                is self_.__annotations__["qFallbackTitle"]
            ):
                self_.qFallbackTitle = kvargs["qFallbackTitle"]
            else:
                self_.qFallbackTitle = kvargs["qFallbackTitle"]
        if "qLocked" in kvargs:
            if type(kvargs["qLocked"]).__name__ is self_.__annotations__["qLocked"]:
                self_.qLocked = kvargs["qLocked"]
            else:
                self_.qLocked = kvargs["qLocked"]
        if "qError" in kvargs:
            if type(kvargs["qError"]).__name__ is self_.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(**kvargs["qError"])
        if "qIsCalculated" in kvargs:
            if (
                type(kvargs["qIsCalculated"]).__name__
                is self_.__annotations__["qIsCalculated"]
            ):
                self_.qIsCalculated = kvargs["qIsCalculated"]
            else:
                self_.qIsCalculated = kvargs["qIsCalculated"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttributeDimValues:
    """

    Attributes
    ----------
    qValues: list[NxSimpleDimValue]
      List of values.
    """

    qValues: list[NxSimpleDimValue] = None

    def __init__(self_, **kvargs):
        if "qValues" in kvargs:
            if type(kvargs["qValues"]).__name__ is self_.__annotations__["qValues"]:
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [NxSimpleDimValue(**e) for e in kvargs["qValues"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttributeExpressionValues:
    """

    Attributes
    ----------
    qValues: list[NxSimpleValue]
      List of attribute expressions values.
    """

    qValues: list[NxSimpleValue] = None

    def __init__(self_, **kvargs):
        if "qValues" in kvargs:
            if type(kvargs["qValues"]).__name__ is self_.__annotations__["qValues"]:
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [NxSimpleValue(**e) for e in kvargs["qValues"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAxisTicks:
    """

    Attributes
    ----------
    qName: str
      Name of the derived definition.
    qTags: list[str]
      List of tags.
    qTicks: list[NxTickCell]
      List of ticks.
    """

    qName: str = None
    qTags: list[str] = None
    qTicks: list[NxTickCell] = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qTags" in kvargs:
            if type(kvargs["qTags"]).__name__ is self_.__annotations__["qTags"]:
                self_.qTags = kvargs["qTags"]
            else:
                self_.qTags = kvargs["qTags"]
        if "qTicks" in kvargs:
            if type(kvargs["qTicks"]).__name__ is self_.__annotations__["qTicks"]:
                self_.qTicks = kvargs["qTicks"]
            else:
                self_.qTicks = [NxTickCell(**e) for e in kvargs["qTicks"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxCalcCond:
    """

    Attributes
    ----------
    qCond: ValueExpr
      Condition for calculating an hypercube, dimension or measure.
    qMsg: StringExpr
      Evaluated if Cond is not fullfilled.
    """

    qCond: ValueExpr = None
    qMsg: StringExpr = None

    def __init__(self_, **kvargs):
        if "qCond" in kvargs:
            if type(kvargs["qCond"]).__name__ is self_.__annotations__["qCond"]:
                self_.qCond = kvargs["qCond"]
            else:
                self_.qCond = ValueExpr(**kvargs["qCond"])
        if "qMsg" in kvargs:
            if type(kvargs["qMsg"]).__name__ is self_.__annotations__["qMsg"]:
                self_.qMsg = kvargs["qMsg"]
            else:
                self_.qMsg = StringExpr(**kvargs["qMsg"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxContainerEntry:
    """

    Attributes
    ----------
    qInfo: NxInfo
      Information about the object.
    qMeta: NxMeta
      Information on publishing and permissions.
    qData: JsonObject
      Set of data.
    """

    qInfo: NxInfo = None
    qMeta: NxMeta = None
    qData: JsonObject = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        if "qMeta" in kvargs:
            if type(kvargs["qMeta"]).__name__ is self_.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(**kvargs["qMeta"])
        if "qData" in kvargs:
            if type(kvargs["qData"]).__name__ is self_.__annotations__["qData"]:
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(**kvargs["qData"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxContinuousRangeSelectInfo:
    """

    Attributes
    ----------
    qRange: Range
      Range information.
    qDimIx: int
      Dimension index.
    """

    qRange: Range = None
    qDimIx: int = None

    def __init__(self_, **kvargs):
        if "qRange" in kvargs:
            if type(kvargs["qRange"]).__name__ is self_.__annotations__["qRange"]:
                self_.qRange = kvargs["qRange"]
            else:
                self_.qRange = Range(**kvargs["qRange"])
        if "qDimIx" in kvargs:
            if type(kvargs["qDimIx"]).__name__ is self_.__annotations__["qDimIx"]:
                self_.qDimIx = kvargs["qDimIx"]
            else:
                self_.qDimIx = kvargs["qDimIx"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDerivedGroup:
    """

    Attributes
    ----------
    qId: str
      Identifier of the group.
    qName: str
      Name of the derived group.
    qGrouping: str
      Grouping type.
      The grouping should be either H or C (Grouping is mandatory for derived definitions).
      The parameter is mandatory.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qFieldDefs: list[str]
      List of the derived fields in the group.
    """

    qId: str = None
    qName: str = None
    qGrouping: str = None
    qFieldDefs: list[str] = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs:
            if type(kvargs["qId"]).__name__ is self_.__annotations__["qId"]:
                self_.qId = kvargs["qId"]
            else:
                self_.qId = kvargs["qId"]
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qGrouping" in kvargs:
            if type(kvargs["qGrouping"]).__name__ is self_.__annotations__["qGrouping"]:
                self_.qGrouping = kvargs["qGrouping"]
            else:
                self_.qGrouping = kvargs["qGrouping"]
        if "qFieldDefs" in kvargs:
            if (
                type(kvargs["qFieldDefs"]).__name__
                is self_.__annotations__["qFieldDefs"]
            ):
                self_.qFieldDefs = kvargs["qFieldDefs"]
            else:
                self_.qFieldDefs = kvargs["qFieldDefs"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDimensionInfo:
    """

    Attributes
    ----------
    qFallbackTitle: str
      Corresponds to the label of the dimension that is selected.
      If the label is not defined then the field name is used.
    qApprMaxGlyphCount: int
      Length of the longest value in the field.
    qCardinal: int
      Number of distinct field values.
    qLocked: bool
      Is set to true if the field is locked.
    qSortIndicator: str
      Sort indicator.
      The default value is no sorting.
      This parameter is optional.

      One of:

      • N or NX_SORT_INDICATE_NONE

      • A or NX_SORT_INDICATE_ASC

      • D or NX_SORT_INDICATE_DESC
    qGroupFallbackTitles: list[str]
      Array of dimension labels.
      Contains the labels of all dimensions in a hierarchy group (for example the labels of all dimensions in a drill down group).
    qGroupPos: int
      Index of the dimension that is currently in use.
      _qGroupPos_ is set to 0 if there are no hierarchical groups (drill-down groups) or cycle groups.
    qStateCounts: NxStateCounts
      Number of values in a particular state.
    qTags: list[str]
      Gives information on a field. For example, it can return the type of the field.
      Examples: key, text, ASCII
    qError: NxValidationError
      This parameter is optional.
      Gives information on the error.
    qDimensionType: str
      Binary format of the field.

      One of:

      • D or NX_DIMENSION_TYPE_DISCRETE

      • N or NX_DIMENSION_TYPE_NUMERIC

      • T or NX_DIMENSION_TYPE_TIME
    qReverseSort: bool
      If set to true, it inverts the sort criteria in the field.
    qGrouping: str
      Defines the grouping.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qIsSemantic: bool
      If set to true, it means that the field is a semantic.
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    qIsAutoFormat: bool
      This parameter is set to true if qNumFormat is set to U (unknown). The engine guesses the type of the field based on the field's definition.
    qGroupFieldDefs: list[str]
      Array of field names.
    qMin: float
      Minimum value.
    qMax: float
      Maximum value.
    qContinuousAxes: bool
      Is continuous axis used.
    qIsCyclic: bool
      Is a cyclic dimension used.
    qDerivedField: bool
      Is derived field is used as a dimension.
    qAttrExprInfo: list[NxAttrExprInfo]
      Array of attribute expressions.
    qAttrDimInfo: list[NxAttrDimInfo]
      Array of attribute dimensions.
    qCalcCondMsg: str
      The message displayed if calculation condition is not fulfilled.
    qIsCalculated: bool
      True if this is a calculated dimension.
    qIsOneAndOnlyOne: bool
      If set to true, it means that the field always has one and only one selected value.
    qCardinalities: NxCardinalities
      Dimension Cardinalities
    qLibraryId: str
      Refers to a dimension stored in the library.
    """

    qFallbackTitle: str = None
    qApprMaxGlyphCount: int = None
    qCardinal: int = None
    qLocked: bool = None
    qSortIndicator: str = None
    qGroupFallbackTitles: list[str] = None
    qGroupPos: int = None
    qStateCounts: NxStateCounts = None
    qTags: list[str] = None
    qError: NxValidationError = None
    qDimensionType: str = None
    qReverseSort: bool = None
    qGrouping: str = None
    qIsSemantic: bool = None
    qNumFormat: FieldAttributes = None
    qIsAutoFormat: bool = None
    qGroupFieldDefs: list[str] = None
    qMin: float = None
    qMax: float = None
    qContinuousAxes: bool = None
    qIsCyclic: bool = None
    qDerivedField: bool = None
    qAttrExprInfo: list[NxAttrExprInfo] = None
    qAttrDimInfo: list[NxAttrDimInfo] = None
    qCalcCondMsg: str = None
    qIsCalculated: bool = None
    qIsOneAndOnlyOne: bool = None
    qCardinalities: NxCardinalities = None
    qLibraryId: str = None

    def __init__(self_, **kvargs):
        if "qFallbackTitle" in kvargs:
            if (
                type(kvargs["qFallbackTitle"]).__name__
                is self_.__annotations__["qFallbackTitle"]
            ):
                self_.qFallbackTitle = kvargs["qFallbackTitle"]
            else:
                self_.qFallbackTitle = kvargs["qFallbackTitle"]
        if "qApprMaxGlyphCount" in kvargs:
            if (
                type(kvargs["qApprMaxGlyphCount"]).__name__
                is self_.__annotations__["qApprMaxGlyphCount"]
            ):
                self_.qApprMaxGlyphCount = kvargs["qApprMaxGlyphCount"]
            else:
                self_.qApprMaxGlyphCount = kvargs["qApprMaxGlyphCount"]
        if "qCardinal" in kvargs:
            if type(kvargs["qCardinal"]).__name__ is self_.__annotations__["qCardinal"]:
                self_.qCardinal = kvargs["qCardinal"]
            else:
                self_.qCardinal = kvargs["qCardinal"]
        if "qLocked" in kvargs:
            if type(kvargs["qLocked"]).__name__ is self_.__annotations__["qLocked"]:
                self_.qLocked = kvargs["qLocked"]
            else:
                self_.qLocked = kvargs["qLocked"]
        if "qSortIndicator" in kvargs:
            if (
                type(kvargs["qSortIndicator"]).__name__
                is self_.__annotations__["qSortIndicator"]
            ):
                self_.qSortIndicator = kvargs["qSortIndicator"]
            else:
                self_.qSortIndicator = kvargs["qSortIndicator"]
        if "qGroupFallbackTitles" in kvargs:
            if (
                type(kvargs["qGroupFallbackTitles"]).__name__
                is self_.__annotations__["qGroupFallbackTitles"]
            ):
                self_.qGroupFallbackTitles = kvargs["qGroupFallbackTitles"]
            else:
                self_.qGroupFallbackTitles = kvargs["qGroupFallbackTitles"]
        if "qGroupPos" in kvargs:
            if type(kvargs["qGroupPos"]).__name__ is self_.__annotations__["qGroupPos"]:
                self_.qGroupPos = kvargs["qGroupPos"]
            else:
                self_.qGroupPos = kvargs["qGroupPos"]
        if "qStateCounts" in kvargs:
            if (
                type(kvargs["qStateCounts"]).__name__
                is self_.__annotations__["qStateCounts"]
            ):
                self_.qStateCounts = kvargs["qStateCounts"]
            else:
                self_.qStateCounts = NxStateCounts(**kvargs["qStateCounts"])
        if "qTags" in kvargs:
            if type(kvargs["qTags"]).__name__ is self_.__annotations__["qTags"]:
                self_.qTags = kvargs["qTags"]
            else:
                self_.qTags = kvargs["qTags"]
        if "qError" in kvargs:
            if type(kvargs["qError"]).__name__ is self_.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(**kvargs["qError"])
        if "qDimensionType" in kvargs:
            if (
                type(kvargs["qDimensionType"]).__name__
                is self_.__annotations__["qDimensionType"]
            ):
                self_.qDimensionType = kvargs["qDimensionType"]
            else:
                self_.qDimensionType = kvargs["qDimensionType"]
        if "qReverseSort" in kvargs:
            if (
                type(kvargs["qReverseSort"]).__name__
                is self_.__annotations__["qReverseSort"]
            ):
                self_.qReverseSort = kvargs["qReverseSort"]
            else:
                self_.qReverseSort = kvargs["qReverseSort"]
        if "qGrouping" in kvargs:
            if type(kvargs["qGrouping"]).__name__ is self_.__annotations__["qGrouping"]:
                self_.qGrouping = kvargs["qGrouping"]
            else:
                self_.qGrouping = kvargs["qGrouping"]
        if "qIsSemantic" in kvargs:
            if (
                type(kvargs["qIsSemantic"]).__name__
                is self_.__annotations__["qIsSemantic"]
            ):
                self_.qIsSemantic = kvargs["qIsSemantic"]
            else:
                self_.qIsSemantic = kvargs["qIsSemantic"]
        if "qNumFormat" in kvargs:
            if (
                type(kvargs["qNumFormat"]).__name__
                is self_.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(**kvargs["qNumFormat"])
        if "qIsAutoFormat" in kvargs:
            if (
                type(kvargs["qIsAutoFormat"]).__name__
                is self_.__annotations__["qIsAutoFormat"]
            ):
                self_.qIsAutoFormat = kvargs["qIsAutoFormat"]
            else:
                self_.qIsAutoFormat = kvargs["qIsAutoFormat"]
        if "qGroupFieldDefs" in kvargs:
            if (
                type(kvargs["qGroupFieldDefs"]).__name__
                is self_.__annotations__["qGroupFieldDefs"]
            ):
                self_.qGroupFieldDefs = kvargs["qGroupFieldDefs"]
            else:
                self_.qGroupFieldDefs = kvargs["qGroupFieldDefs"]
        if "qMin" in kvargs:
            if type(kvargs["qMin"]).__name__ is self_.__annotations__["qMin"]:
                self_.qMin = kvargs["qMin"]
            else:
                self_.qMin = kvargs["qMin"]
        if "qMax" in kvargs:
            if type(kvargs["qMax"]).__name__ is self_.__annotations__["qMax"]:
                self_.qMax = kvargs["qMax"]
            else:
                self_.qMax = kvargs["qMax"]
        if "qContinuousAxes" in kvargs:
            if (
                type(kvargs["qContinuousAxes"]).__name__
                is self_.__annotations__["qContinuousAxes"]
            ):
                self_.qContinuousAxes = kvargs["qContinuousAxes"]
            else:
                self_.qContinuousAxes = kvargs["qContinuousAxes"]
        if "qIsCyclic" in kvargs:
            if type(kvargs["qIsCyclic"]).__name__ is self_.__annotations__["qIsCyclic"]:
                self_.qIsCyclic = kvargs["qIsCyclic"]
            else:
                self_.qIsCyclic = kvargs["qIsCyclic"]
        if "qDerivedField" in kvargs:
            if (
                type(kvargs["qDerivedField"]).__name__
                is self_.__annotations__["qDerivedField"]
            ):
                self_.qDerivedField = kvargs["qDerivedField"]
            else:
                self_.qDerivedField = kvargs["qDerivedField"]
        if "qAttrExprInfo" in kvargs:
            if (
                type(kvargs["qAttrExprInfo"]).__name__
                is self_.__annotations__["qAttrExprInfo"]
            ):
                self_.qAttrExprInfo = kvargs["qAttrExprInfo"]
            else:
                self_.qAttrExprInfo = [
                    NxAttrExprInfo(**e) for e in kvargs["qAttrExprInfo"]
                ]
        if "qAttrDimInfo" in kvargs:
            if (
                type(kvargs["qAttrDimInfo"]).__name__
                is self_.__annotations__["qAttrDimInfo"]
            ):
                self_.qAttrDimInfo = kvargs["qAttrDimInfo"]
            else:
                self_.qAttrDimInfo = [
                    NxAttrDimInfo(**e) for e in kvargs["qAttrDimInfo"]
                ]
        if "qCalcCondMsg" in kvargs:
            if (
                type(kvargs["qCalcCondMsg"]).__name__
                is self_.__annotations__["qCalcCondMsg"]
            ):
                self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
            else:
                self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
        if "qIsCalculated" in kvargs:
            if (
                type(kvargs["qIsCalculated"]).__name__
                is self_.__annotations__["qIsCalculated"]
            ):
                self_.qIsCalculated = kvargs["qIsCalculated"]
            else:
                self_.qIsCalculated = kvargs["qIsCalculated"]
        if "qIsOneAndOnlyOne" in kvargs:
            if (
                type(kvargs["qIsOneAndOnlyOne"]).__name__
                is self_.__annotations__["qIsOneAndOnlyOne"]
            ):
                self_.qIsOneAndOnlyOne = kvargs["qIsOneAndOnlyOne"]
            else:
                self_.qIsOneAndOnlyOne = kvargs["qIsOneAndOnlyOne"]
        if "qCardinalities" in kvargs:
            if (
                type(kvargs["qCardinalities"]).__name__
                is self_.__annotations__["qCardinalities"]
            ):
                self_.qCardinalities = kvargs["qCardinalities"]
            else:
                self_.qCardinalities = NxCardinalities(**kvargs["qCardinalities"])
        if "qLibraryId" in kvargs:
            if (
                type(kvargs["qLibraryId"]).__name__
                is self_.__annotations__["qLibraryId"]
            ):
                self_.qLibraryId = kvargs["qLibraryId"]
            else:
                self_.qLibraryId = kvargs["qLibraryId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFieldResourceId:
    """

    Attributes
    ----------
    qName: str
      Name of the field to get the resource id for.
    qResourceIds: list[NxFieldTableResourceId]
      Field level resource Id per table that the field is part of
    """

    qName: str = None
    qResourceIds: list[NxFieldTableResourceId] = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qResourceIds" in kvargs:
            if (
                type(kvargs["qResourceIds"]).__name__
                is self_.__annotations__["qResourceIds"]
            ):
                self_.qResourceIds = kvargs["qResourceIds"]
            else:
                self_.qResourceIds = [
                    NxFieldTableResourceId(**e) for e in kvargs["qResourceIds"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFieldSelectionInfo:
    """

    Attributes
    ----------
    qName: str
      Name of the field.
    qFieldSelectionMode: str
      Selection mode.

      Properties:

      One of:

      • NORMAL for a selection in normal mode.

      • AND for a selection in AND mode.

      • NOT for a selection NOT in AND mode.
      One of:

      • NORMAL or SELECTION_MODE_NORMAL

      • AND or SELECTION_MODE_AND

      • NOT or SELECTION_MODE_NOT
    """

    qName: str = None
    qFieldSelectionMode: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qFieldSelectionMode" in kvargs:
            if (
                type(kvargs["qFieldSelectionMode"]).__name__
                is self_.__annotations__["qFieldSelectionMode"]
            ):
                self_.qFieldSelectionMode = kvargs["qFieldSelectionMode"]
            else:
                self_.qFieldSelectionMode = kvargs["qFieldSelectionMode"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMiniChart:
    """

    Attributes
    ----------
    qYMin: float
    qYMax: float
    qXMin: float
    qXMax: float
    qAttrExprInfo: list[NxAttrExprInfo]
      List of attribute expressions.
    qError: NxValidationError
      This parameter is optional and is displayed in case of error.
    """

    qYMin: float = None
    qYMax: float = None
    qXMin: float = None
    qXMax: float = None
    qAttrExprInfo: list[NxAttrExprInfo] = None
    qError: NxValidationError = None

    def __init__(self_, **kvargs):
        if "qYMin" in kvargs:
            if type(kvargs["qYMin"]).__name__ is self_.__annotations__["qYMin"]:
                self_.qYMin = kvargs["qYMin"]
            else:
                self_.qYMin = kvargs["qYMin"]
        if "qYMax" in kvargs:
            if type(kvargs["qYMax"]).__name__ is self_.__annotations__["qYMax"]:
                self_.qYMax = kvargs["qYMax"]
            else:
                self_.qYMax = kvargs["qYMax"]
        if "qXMin" in kvargs:
            if type(kvargs["qXMin"]).__name__ is self_.__annotations__["qXMin"]:
                self_.qXMin = kvargs["qXMin"]
            else:
                self_.qXMin = kvargs["qXMin"]
        if "qXMax" in kvargs:
            if type(kvargs["qXMax"]).__name__ is self_.__annotations__["qXMax"]:
                self_.qXMax = kvargs["qXMax"]
            else:
                self_.qXMax = kvargs["qXMax"]
        if "qAttrExprInfo" in kvargs:
            if (
                type(kvargs["qAttrExprInfo"]).__name__
                is self_.__annotations__["qAttrExprInfo"]
            ):
                self_.qAttrExprInfo = kvargs["qAttrExprInfo"]
            else:
                self_.qAttrExprInfo = [
                    NxAttrExprInfo(**e) for e in kvargs["qAttrExprInfo"]
                ]
        if "qError" in kvargs:
            if type(kvargs["qError"]).__name__ is self_.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(**kvargs["qError"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMiniChartCell:
    """

    Attributes
    ----------
    qText: str
      Some text.
    qNum: float
      A value.
      This parameter is optional.
    qElemNumber: int
      Rank number of the value, starting from 0.
      If the element number is a negative number, it means that the returned value is not an element number.
      You can get the following negative values:

      • -1: the cell is a Total cell. It shows a total.

      • -2: the cell is a Null cell.

      • -3: the cell belongs to the group Others .

      • -4: the cell is empty. Applies to pivot tables.
    qAttrExps: NxAttributeExpressionValues
      Attribute expressions values.
    """

    qText: str = None
    qNum: float = None
    qElemNumber: int = None
    qAttrExps: NxAttributeExpressionValues = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qNum" in kvargs:
            if type(kvargs["qNum"]).__name__ is self_.__annotations__["qNum"]:
                self_.qNum = kvargs["qNum"]
            else:
                self_.qNum = kvargs["qNum"]
        if "qElemNumber" in kvargs:
            if (
                type(kvargs["qElemNumber"]).__name__
                is self_.__annotations__["qElemNumber"]
            ):
                self_.qElemNumber = kvargs["qElemNumber"]
            else:
                self_.qElemNumber = kvargs["qElemNumber"]
        if "qAttrExps" in kvargs:
            if type(kvargs["qAttrExps"]).__name__ is self_.__annotations__["qAttrExps"]:
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(**kvargs["qAttrExps"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMiniChartRows:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPageTreeNode:
    """
    Defines an area of the tree to be fetched.

    Attributes
    ----------
    qArea: Rect
      The area of the tree to be fetched. If no area is defined on a dimension, all existing nodes are included.
    qAllValues: bool
      When set to true, generated nodes (based on current selection) will be inserted into the returned tree even when there is no actual value. For example, suppose you are looking for hybrid car sales at all car dealerships. Normally, only dealerships where hybrid cars are sold would be part of the returned tree but with qAllValues set to true, all available dealerships will be included regardless if they sold any hybrid cars or not.
    """

    qArea: Rect = None
    qAllValues: bool = None

    def __init__(self_, **kvargs):
        if "qArea" in kvargs:
            if type(kvargs["qArea"]).__name__ is self_.__annotations__["qArea"]:
                self_.qArea = kvargs["qArea"]
            else:
                self_.qArea = Rect(**kvargs["qArea"])
        if "qAllValues" in kvargs:
            if (
                type(kvargs["qAllValues"]).__name__
                is self_.__annotations__["qAllValues"]
            ):
                self_.qAllValues = kvargs["qAllValues"]
            else:
                self_.qAllValues = kvargs["qAllValues"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPatch:
    """

    Attributes
    ----------
    qOp: str
      Operation to perform.

      One of:

      • add or Add

      • remove or Remove

      • replace or Replace
    qPath: str
      Path to the property to add, remove or replace.
    qValue: str
      This parameter is not used in a remove operation.
      Corresponds to the value of the property to add or to the new value of the property to update.
      Examples:
      "false", "2", "\"New title\""
    """

    qOp: str = None
    qPath: str = None
    qValue: str = None

    def __init__(self_, **kvargs):
        if "qOp" in kvargs:
            if type(kvargs["qOp"]).__name__ is self_.__annotations__["qOp"]:
                self_.qOp = kvargs["qOp"]
            else:
                self_.qOp = kvargs["qOp"]
        if "qPath" in kvargs:
            if type(kvargs["qPath"]).__name__ is self_.__annotations__["qPath"]:
                self_.qPath = kvargs["qPath"]
            else:
                self_.qPath = kvargs["qPath"]
        if "qValue" in kvargs:
            if type(kvargs["qValue"]).__name__ is self_.__annotations__["qValue"]:
                self_.qValue = kvargs["qValue"]
            else:
                self_.qValue = kvargs["qValue"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPatches:
    """

    Attributes
    ----------
    qInfo: NxInfo
      Identifier and type of the object.
    qPatches: list[NxPatch]
      Array with patches.
    qChildren: list[NxPatches]
      Array with child objects and their patches.
    """

    qInfo: NxInfo = None
    qPatches: list[NxPatch] = None
    qChildren: list[NxPatches] = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        if "qPatches" in kvargs:
            if type(kvargs["qPatches"]).__name__ is self_.__annotations__["qPatches"]:
                self_.qPatches = kvargs["qPatches"]
            else:
                self_.qPatches = [NxPatch(**e) for e in kvargs["qPatches"]]
        if "qChildren" in kvargs:
            if type(kvargs["qChildren"]).__name__ is self_.__annotations__["qChildren"]:
                self_.qChildren = kvargs["qChildren"]
            else:
                self_.qChildren = [NxPatches(**e) for e in kvargs["qChildren"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPivotDimensionCell:
    """

    Attributes
    ----------
    qText: str
      Some text.
    qElemNo: int
      Rank number of the value.
      If set to -1, it means that the value is not an element number.
    qValue: float
      Value of the cell.
      Is set to NaN , if the value is not a number.
    qCanExpand: bool
      If set to true, it means that the cell can be expanded.
      This parameter is not returned if it is set to false.
    qCanCollapse: bool
      If set to true, it means that the cell can be collapsed.
      This parameter is not returned if it is set to false.
    qType: str
      Type of the cell.

      One of:

      • V or NX_DIM_CELL_VALUE

      • E or NX_DIM_CELL_EMPTY

      • N or NX_DIM_CELL_NORMAL

      • T or NX_DIM_CELL_TOTAL

      • O or NX_DIM_CELL_OTHER

      • A or NX_DIM_CELL_AGGR

      • P or NX_DIM_CELL_PSEUDO

      • R or NX_DIM_CELL_ROOT

      • U or NX_DIM_CELL_NULL

      • G or NX_DIM_CELL_GENERATED
    qUp: int
      Number of elements that are part of the previous tail.
      This number depends on the paging, more particularly it depends on the values defined in qTop and qHeight .
    qDown: int
      Number of elements that are part of the next tail.
      This number depends on the paging, more particularly it depends on the values defined in qTop and qHeight .
    qSubNodes: list[NxPivotDimensionCell]
      Information about sub nodes (or sub cells).
      The array is empty [ ] when there is no sub nodes.
    qAttrExps: NxAttributeExpressionValues
      Information about attribute expressions.
      The array is empty [ ] when there is no attribute expressions.
    qAttrDims: NxAttributeDimValues
      Information about attribute dimensions.
    """

    qText: str = None
    qElemNo: int = None
    qValue: float = None
    qCanExpand: bool = None
    qCanCollapse: bool = None
    qType: str = None
    qUp: int = None
    qDown: int = None
    qSubNodes: list[NxPivotDimensionCell] = None
    qAttrExps: NxAttributeExpressionValues = None
    qAttrDims: NxAttributeDimValues = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qElemNo" in kvargs:
            if type(kvargs["qElemNo"]).__name__ is self_.__annotations__["qElemNo"]:
                self_.qElemNo = kvargs["qElemNo"]
            else:
                self_.qElemNo = kvargs["qElemNo"]
        if "qValue" in kvargs:
            if type(kvargs["qValue"]).__name__ is self_.__annotations__["qValue"]:
                self_.qValue = kvargs["qValue"]
            else:
                self_.qValue = kvargs["qValue"]
        if "qCanExpand" in kvargs:
            if (
                type(kvargs["qCanExpand"]).__name__
                is self_.__annotations__["qCanExpand"]
            ):
                self_.qCanExpand = kvargs["qCanExpand"]
            else:
                self_.qCanExpand = kvargs["qCanExpand"]
        if "qCanCollapse" in kvargs:
            if (
                type(kvargs["qCanCollapse"]).__name__
                is self_.__annotations__["qCanCollapse"]
            ):
                self_.qCanCollapse = kvargs["qCanCollapse"]
            else:
                self_.qCanCollapse = kvargs["qCanCollapse"]
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qUp" in kvargs:
            if type(kvargs["qUp"]).__name__ is self_.__annotations__["qUp"]:
                self_.qUp = kvargs["qUp"]
            else:
                self_.qUp = kvargs["qUp"]
        if "qDown" in kvargs:
            if type(kvargs["qDown"]).__name__ is self_.__annotations__["qDown"]:
                self_.qDown = kvargs["qDown"]
            else:
                self_.qDown = kvargs["qDown"]
        if "qSubNodes" in kvargs:
            if type(kvargs["qSubNodes"]).__name__ is self_.__annotations__["qSubNodes"]:
                self_.qSubNodes = kvargs["qSubNodes"]
            else:
                self_.qSubNodes = [
                    NxPivotDimensionCell(**e) for e in kvargs["qSubNodes"]
                ]
        if "qAttrExps" in kvargs:
            if type(kvargs["qAttrExps"]).__name__ is self_.__annotations__["qAttrExps"]:
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(**kvargs["qAttrExps"])
        if "qAttrDims" in kvargs:
            if type(kvargs["qAttrDims"]).__name__ is self_.__annotations__["qAttrDims"]:
                self_.qAttrDims = kvargs["qAttrDims"]
            else:
                self_.qAttrDims = NxAttributeDimValues(**kvargs["qAttrDims"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPivotValuePoint:
    """

    Attributes
    ----------
    qLabel: str
      Label of the cell.
      This parameter is optional.
    qText: str
      Some text related to the cell.
    qNum: float
      Value of the cell.
    qType: str
      Type of the cell.

      One of:

      • V or NX_DIM_CELL_VALUE

      • E or NX_DIM_CELL_EMPTY

      • N or NX_DIM_CELL_NORMAL

      • T or NX_DIM_CELL_TOTAL

      • O or NX_DIM_CELL_OTHER

      • A or NX_DIM_CELL_AGGR

      • P or NX_DIM_CELL_PSEUDO

      • R or NX_DIM_CELL_ROOT

      • U or NX_DIM_CELL_NULL

      • G or NX_DIM_CELL_GENERATED
    qAttrExps: NxAttributeExpressionValues
      Attribute expressions values.
    qAttrDims: NxAttributeDimValues
    """

    qLabel: str = None
    qText: str = None
    qNum: float = None
    qType: str = None
    qAttrExps: NxAttributeExpressionValues = None
    qAttrDims: NxAttributeDimValues = None

    def __init__(self_, **kvargs):
        if "qLabel" in kvargs:
            if type(kvargs["qLabel"]).__name__ is self_.__annotations__["qLabel"]:
                self_.qLabel = kvargs["qLabel"]
            else:
                self_.qLabel = kvargs["qLabel"]
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qNum" in kvargs:
            if type(kvargs["qNum"]).__name__ is self_.__annotations__["qNum"]:
                self_.qNum = kvargs["qNum"]
            else:
                self_.qNum = kvargs["qNum"]
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qAttrExps" in kvargs:
            if type(kvargs["qAttrExps"]).__name__ is self_.__annotations__["qAttrExps"]:
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(**kvargs["qAttrExps"])
        if "qAttrDims" in kvargs:
            if type(kvargs["qAttrDims"]).__name__ is self_.__annotations__["qAttrDims"]:
                self_.qAttrDims = kvargs["qAttrDims"]
            else:
                self_.qAttrDims = NxAttributeDimValues(**kvargs["qAttrDims"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxRangeSelectInfo:
    """

    Attributes
    ----------
    qRange: Range
      Range of values.
    qMeasureIx: int
      Number of the measure to select.
      Numbering starts from 0.
    """

    qRange: Range = None
    qMeasureIx: int = None

    def __init__(self_, **kvargs):
        if "qRange" in kvargs:
            if type(kvargs["qRange"]).__name__ is self_.__annotations__["qRange"]:
                self_.qRange = kvargs["qRange"]
            else:
                self_.qRange = Range(**kvargs["qRange"])
        if "qMeasureIx" in kvargs:
            if (
                type(kvargs["qMeasureIx"]).__name__
                is self_.__annotations__["qMeasureIx"]
            ):
                self_.qMeasureIx = kvargs["qMeasureIx"]
            else:
                self_.qMeasureIx = kvargs["qMeasureIx"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxSelectionCell:
    """

    Attributes
    ----------
    qType: str
      Type of cells to select.

      One of:

      • D or NX_CELL_DATA

      • T or NX_CELL_TOP

      • L or NX_CELL_LEFT
    qCol: int
      Column index to select.
      Indexing starts from 0.
      If the cell's type is:

      • D, the index is based on the data matrix.

      • T, the index is based on the data matrix.

      • L, the index is based on the left dimensions indexes.
    qRow: int
      Row index to select.
      Indexing starts from 0.
      If the cell's type is:

      • D, the index is based on the data matrix.

      • T, the index is based on the top dimensions indexes.

      • L, the index is based on the data matrix.
    """

    qType: str = None
    qCol: int = None
    qRow: int = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qCol" in kvargs:
            if type(kvargs["qCol"]).__name__ is self_.__annotations__["qCol"]:
                self_.qCol = kvargs["qCol"]
            else:
                self_.qCol = kvargs["qCol"]
        if "qRow" in kvargs:
            if type(kvargs["qRow"]).__name__ is self_.__annotations__["qRow"]:
                self_.qRow = kvargs["qRow"]
            else:
                self_.qRow = kvargs["qRow"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxStackedPivotCell:
    """

    Attributes
    ----------
    qText: str
      Some text.
    qElemNo: int
      Rank number of the value.
      If set to -1, it means that the value is not an element number.
    qValue: float
      Value of the cell.
      Is set to NaN , if the value is not a number.
    qCanExpand: bool
      If set to true, it means that the cell can be expanded.
      This parameter is not returned if it is set to false.
    qCanCollapse: bool
      If set to true, it means that the cell can be collapsed.
      This parameter is not returned if it is set to false.
    qType: str
      Type of the cell.

      One of:

      • V or NX_DIM_CELL_VALUE

      • E or NX_DIM_CELL_EMPTY

      • N or NX_DIM_CELL_NORMAL

      • T or NX_DIM_CELL_TOTAL

      • O or NX_DIM_CELL_OTHER

      • A or NX_DIM_CELL_AGGR

      • P or NX_DIM_CELL_PSEUDO

      • R or NX_DIM_CELL_ROOT

      • U or NX_DIM_CELL_NULL

      • G or NX_DIM_CELL_GENERATED
    qMaxPos: float
      Total of the positive values in the current group of cells.
    qMinNeg: float
      Total of the negative values in the current group of cells.
    qUp: int
      Number of elements that are part of the previous tail.
    qDown: int
      Number of elements that are part of the next tail.
    qRow: int
      Row index in the data matrix.
      The indexing starts from 0.
    qSubNodes: list[NxStackedPivotCell]
      Information about sub nodes (or sub cells).
      The array is empty [ ] when there are no sub nodes.
    qAttrExps: NxAttributeExpressionValues
      Attribute expressions values.
    qAttrDims: NxAttributeDimValues
      Attribute dimensions values.
    """

    qText: str = None
    qElemNo: int = None
    qValue: float = None
    qCanExpand: bool = None
    qCanCollapse: bool = None
    qType: str = None
    qMaxPos: float = None
    qMinNeg: float = None
    qUp: int = None
    qDown: int = None
    qRow: int = None
    qSubNodes: list[NxStackedPivotCell] = None
    qAttrExps: NxAttributeExpressionValues = None
    qAttrDims: NxAttributeDimValues = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qElemNo" in kvargs:
            if type(kvargs["qElemNo"]).__name__ is self_.__annotations__["qElemNo"]:
                self_.qElemNo = kvargs["qElemNo"]
            else:
                self_.qElemNo = kvargs["qElemNo"]
        if "qValue" in kvargs:
            if type(kvargs["qValue"]).__name__ is self_.__annotations__["qValue"]:
                self_.qValue = kvargs["qValue"]
            else:
                self_.qValue = kvargs["qValue"]
        if "qCanExpand" in kvargs:
            if (
                type(kvargs["qCanExpand"]).__name__
                is self_.__annotations__["qCanExpand"]
            ):
                self_.qCanExpand = kvargs["qCanExpand"]
            else:
                self_.qCanExpand = kvargs["qCanExpand"]
        if "qCanCollapse" in kvargs:
            if (
                type(kvargs["qCanCollapse"]).__name__
                is self_.__annotations__["qCanCollapse"]
            ):
                self_.qCanCollapse = kvargs["qCanCollapse"]
            else:
                self_.qCanCollapse = kvargs["qCanCollapse"]
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qMaxPos" in kvargs:
            if type(kvargs["qMaxPos"]).__name__ is self_.__annotations__["qMaxPos"]:
                self_.qMaxPos = kvargs["qMaxPos"]
            else:
                self_.qMaxPos = kvargs["qMaxPos"]
        if "qMinNeg" in kvargs:
            if type(kvargs["qMinNeg"]).__name__ is self_.__annotations__["qMinNeg"]:
                self_.qMinNeg = kvargs["qMinNeg"]
            else:
                self_.qMinNeg = kvargs["qMinNeg"]
        if "qUp" in kvargs:
            if type(kvargs["qUp"]).__name__ is self_.__annotations__["qUp"]:
                self_.qUp = kvargs["qUp"]
            else:
                self_.qUp = kvargs["qUp"]
        if "qDown" in kvargs:
            if type(kvargs["qDown"]).__name__ is self_.__annotations__["qDown"]:
                self_.qDown = kvargs["qDown"]
            else:
                self_.qDown = kvargs["qDown"]
        if "qRow" in kvargs:
            if type(kvargs["qRow"]).__name__ is self_.__annotations__["qRow"]:
                self_.qRow = kvargs["qRow"]
            else:
                self_.qRow = kvargs["qRow"]
        if "qSubNodes" in kvargs:
            if type(kvargs["qSubNodes"]).__name__ is self_.__annotations__["qSubNodes"]:
                self_.qSubNodes = kvargs["qSubNodes"]
            else:
                self_.qSubNodes = [NxStackedPivotCell(**e) for e in kvargs["qSubNodes"]]
        if "qAttrExps" in kvargs:
            if type(kvargs["qAttrExps"]).__name__ is self_.__annotations__["qAttrExps"]:
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(**kvargs["qAttrExps"])
        if "qAttrDims" in kvargs:
            if type(kvargs["qAttrDims"]).__name__ is self_.__annotations__["qAttrDims"]:
                self_.qAttrDims = kvargs["qAttrDims"]
            else:
                self_.qAttrDims = NxAttributeDimValues(**kvargs["qAttrDims"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeDataOption:
    """
    Specifies all the paging filters needed to define the tree to be fetched.

    Attributes
    ----------
    qMaxNbrOfNodes: int
      Maximum number of nodes in the tree. If this limit is exceeded, no nodes are returned. All nodes are counted.
    qTreeNodes: list[NxPageTreeNode]
      Defines areas of the tree to be fetched. Areas must be defined left to right.
    qTreeLevels: NxPageTreeLevel
      Filters out complete dimensions from the fetched tree.
    """

    qMaxNbrOfNodes: int = None
    qTreeNodes: list[NxPageTreeNode] = None
    qTreeLevels: NxPageTreeLevel = None

    def __init__(self_, **kvargs):
        if "qMaxNbrOfNodes" in kvargs:
            if (
                type(kvargs["qMaxNbrOfNodes"]).__name__
                is self_.__annotations__["qMaxNbrOfNodes"]
            ):
                self_.qMaxNbrOfNodes = kvargs["qMaxNbrOfNodes"]
            else:
                self_.qMaxNbrOfNodes = kvargs["qMaxNbrOfNodes"]
        if "qTreeNodes" in kvargs:
            if (
                type(kvargs["qTreeNodes"]).__name__
                is self_.__annotations__["qTreeNodes"]
            ):
                self_.qTreeNodes = kvargs["qTreeNodes"]
            else:
                self_.qTreeNodes = [NxPageTreeNode(**e) for e in kvargs["qTreeNodes"]]
        if "qTreeLevels" in kvargs:
            if (
                type(kvargs["qTreeLevels"]).__name__
                is self_.__annotations__["qTreeLevels"]
            ):
                self_.qTreeLevels = kvargs["qTreeLevels"]
            else:
                self_.qTreeLevels = NxPageTreeLevel(**kvargs["qTreeLevels"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeRangeSelectInfo:
    """

    Attributes
    ----------
    qRange: Range
      Range of values.
    qMeasureIx: int
      Number of the measure to select.
      Numbering starts from 0.
    qDimensionIx: int
      Number of the dimension to select
      measure from. Numbering starts from 0.
    """

    qRange: Range = None
    qMeasureIx: int = None
    qDimensionIx: int = None

    def __init__(self_, **kvargs):
        if "qRange" in kvargs:
            if type(kvargs["qRange"]).__name__ is self_.__annotations__["qRange"]:
                self_.qRange = kvargs["qRange"]
            else:
                self_.qRange = Range(**kvargs["qRange"])
        if "qMeasureIx" in kvargs:
            if (
                type(kvargs["qMeasureIx"]).__name__
                is self_.__annotations__["qMeasureIx"]
            ):
                self_.qMeasureIx = kvargs["qMeasureIx"]
            else:
                self_.qMeasureIx = kvargs["qMeasureIx"]
        if "qDimensionIx" in kvargs:
            if (
                type(kvargs["qDimensionIx"]).__name__
                is self_.__annotations__["qDimensionIx"]
            ):
                self_.qDimensionIx = kvargs["qDimensionIx"]
            else:
                self_.qDimensionIx = kvargs["qDimensionIx"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeValue:
    """
    Represents a measure.

    Attributes
    ----------
    qText: str
      The text version of the value, if available.
    qValue: float
      Value of the cell.
      Is set to NaN , if the value is not a number.
    qAttrExps: NxAttributeExpressionValues
      Attribute expression values.
    qAttrDims: NxAttributeDimValues
      Attribute dimension values.
    """

    qText: str = None
    qValue: float = None
    qAttrExps: NxAttributeExpressionValues = None
    qAttrDims: NxAttributeDimValues = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qValue" in kvargs:
            if type(kvargs["qValue"]).__name__ is self_.__annotations__["qValue"]:
                self_.qValue = kvargs["qValue"]
            else:
                self_.qValue = kvargs["qValue"]
        if "qAttrExps" in kvargs:
            if type(kvargs["qAttrExps"]).__name__ is self_.__annotations__["qAttrExps"]:
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(**kvargs["qAttrExps"])
        if "qAttrDims" in kvargs:
            if type(kvargs["qAttrDims"]).__name__ is self_.__annotations__["qAttrDims"]:
                self_.qAttrDims = kvargs["qAttrDims"]
            else:
                self_.qAttrDims = NxAttributeDimValues(**kvargs["qAttrDims"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTrendline:
    """
    Information about the calculated trendline.

    Attributes
    ----------
    qType: str
      Type of trendline

      One of:

      • AVERAGE or Average

      • LINEAR or Linear

      • POLYNOMIAL2 or Polynomial2

      • POLYNOMIAL3 or Polynomial3

      • POLYNOMIAL4 or Polynomial4

      • EXPONENTIAL or Exponential

      • POWER or Power

      • LOG or Logarithmic
    qError: NxValidationError
      This parameter is optional and is displayed in case of error.
    qCoeff: list[float]
      Coefficent c0..cN depending on the trendline type.
    qR2: float
      R2 score. Value between 0..1 that shows the correlation between the trendline and the data. Higher value means higher correlation.
    qExpression: str
      Trendline expression
    qElemNo: int
      Inner Dim elem no
    """

    qType: str = None
    qError: NxValidationError = None
    qCoeff: list[float] = None
    qR2: float = None
    qExpression: str = None
    qElemNo: int = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qError" in kvargs:
            if type(kvargs["qError"]).__name__ is self_.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(**kvargs["qError"])
        if "qCoeff" in kvargs:
            if type(kvargs["qCoeff"]).__name__ is self_.__annotations__["qCoeff"]:
                self_.qCoeff = kvargs["qCoeff"]
            else:
                self_.qCoeff = kvargs["qCoeff"]
        if "qR2" in kvargs:
            if type(kvargs["qR2"]).__name__ is self_.__annotations__["qR2"]:
                self_.qR2 = kvargs["qR2"]
            else:
                self_.qR2 = kvargs["qR2"]
        if "qExpression" in kvargs:
            if (
                type(kvargs["qExpression"]).__name__
                is self_.__annotations__["qExpression"]
            ):
                self_.qExpression = kvargs["qExpression"]
            else:
                self_.qExpression = kvargs["qExpression"]
        if "qElemNo" in kvargs:
            if type(kvargs["qElemNo"]).__name__ is self_.__annotations__["qElemNo"]:
                self_.qElemNo = kvargs["qElemNo"]
            else:
                self_.qElemNo = kvargs["qElemNo"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTrendlineDef:
    """
    Trendline input definition

    Attributes
    ----------
    qType: str
      The type of trendline to calculate

      One of:

      • AVERAGE or Average

      • LINEAR or Linear

      • POLYNOMIAL2 or Polynomial2

      • POLYNOMIAL3 or Polynomial3

      • POLYNOMIAL4 or Polynomial4

      • EXPONENTIAL or Exponential

      • POWER or Power

      • LOG or Logarithmic
    qXColIx: int
      The column in the hypercube to be used as x axis. Can point to either a dimension (numeric or text) or a measure
    qCalcR2: bool
      Set to true to calulatate the R2 score
    qContinuousXAxis: str
      Set if the numerical value of x axis dimension should be used

      One of:

      • Never or CONTINUOUS_NEVER

      • Possible or CONTINUOUS_IF_POSSIBLE

      • Time or CONTINUOUS_IF_TIME
    qMultiDimMode: str
      If you have a hypercube with two dimensions and qXColIx refers to a dimension
      This determines if you get one trendline of each value in the other dimension or
      Or trendline based on the sum of the value in the other dimension
      The sum variant is only supported when qXColIx is 0 and qMode (on the hypercube) is K or T

      One of:

      • Multi or TRENDLINE_MULTILINE

      • Sum or TRENDLINE_SUM
    """

    qType: str = None
    qXColIx: int = -1
    qCalcR2: bool = None
    qContinuousXAxis: str = "CONTINUOUS_NEVER"
    qMultiDimMode: str = "TRENDLINE_MULTILINE"

    def __init__(self_, **kvargs):
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qXColIx" in kvargs:
            if type(kvargs["qXColIx"]).__name__ is self_.__annotations__["qXColIx"]:
                self_.qXColIx = kvargs["qXColIx"]
            else:
                self_.qXColIx = kvargs["qXColIx"]
        if "qCalcR2" in kvargs:
            if type(kvargs["qCalcR2"]).__name__ is self_.__annotations__["qCalcR2"]:
                self_.qCalcR2 = kvargs["qCalcR2"]
            else:
                self_.qCalcR2 = kvargs["qCalcR2"]
        if "qContinuousXAxis" in kvargs:
            if (
                type(kvargs["qContinuousXAxis"]).__name__
                is self_.__annotations__["qContinuousXAxis"]
            ):
                self_.qContinuousXAxis = kvargs["qContinuousXAxis"]
            else:
                self_.qContinuousXAxis = kvargs["qContinuousXAxis"]
        if "qMultiDimMode" in kvargs:
            if (
                type(kvargs["qMultiDimMode"]).__name__
                is self_.__annotations__["qMultiDimMode"]
            ):
                self_.qMultiDimMode = kvargs["qMultiDimMode"]
            else:
                self_.qMultiDimMode = kvargs["qMultiDimMode"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class OtherTotalSpecProp:
    """

    Attributes
    ----------
    qOtherMode: str
      Determines how many dimension values are displayed.
      The default value is OTHEROFF_ .

      One of:

      • OTHER_OFF

      • OTHER_COUNTED

      • OTHER_ABS_LIMITED

      • OTHER_ABS_ACC_TARGET

      • OTHER_REL_LIMITED

      • OTHER_REL_ACC_TARGET
    qOtherCounted: ValueExpr
      Number of values to display. The number of values can be entered as a calculated formula.
      This parameter is used when qOtherMode is set to OTHERCOUNTED_ .
    qOtherLimit: ValueExpr
      Value used to limit the dimension values. The limit can be entered as a calculated formula.
      This parameter is used when qOtherMode is set to:

      • OTHER_ABS_LIMITED

      • OTHER_REL_LIMITED

      • OTHER_ABS_ACC_TARGET
      OTHER_REL_ACC_TARGET
    qOtherLimitMode: str
      Sets the limit for the Others mode.
      This parameter is used when qOtherMode is set to:

      • OTHER_ABS_LIMITED

      • OTHER_REL_LIMITED

      • OTHER_ABS_ACC_TARGET
      OTHER_REL_ACC_TARGET

      One of:

      • OTHER_GE_LIMIT

      • OTHER_LE_LIMIT

      • OTHER_GT_LIMIT

      • OTHER_LT_LIMIT
    qSuppressOther: bool
      If set to true, the group Others is not displayed as a dimension value.
      The default value is false.
    qForceBadValueKeeping: bool
      This parameter is used when qOtherMode is set to:

      • OTHER_ABS_LIMITED

      • OTHER_REL_LIMITED

      • OTHER_ABS_ACC_TARGET
      OTHER_REL_ACC_TARGET

      and when the dimension values include not numeric values.
      Set this parameter to true to include text values in the returned values.
      The default value is true.
    qApplyEvenWhenPossiblyWrongResult: bool
      Set this parameter to true to allow the calculation of Others even if the engine detects some potential mistakes.
      For example the country Russia is part of the continent Europe and Asia. If you have an hypercube with two dimensions Country and Continent and one measure Population, the engine can detect that the population of Russia is included in both the continent Asia and Europe.
      The default value is true.
    qGlobalOtherGrouping: bool
      This parameter applies to inner dimensions.
      If this parameter is set to true, the restrictions are calculated on the selected dimension only. All previous dimensions are ignored.
      The default value is false.
    qOtherCollapseInnerDimensions: bool
      If set to true, it collapses the inner dimensions (if any) in the group Others .
      The default value is false.
    qOtherSortMode: str
      Defines the sort order of the dimension values.
      The default value is OTHERSORT_DESCENDING_ .

      One of:

      • OTHER_SORT_DEFAULT

      • OTHER_SORT_DESCENDING

      • OTHER_SORT_ASCENDING
    qTotalMode: str
      If set to TOTALEXPR_ , the total of the dimension values is returned.
      The default value is TOTALOFF_ .

      One of:

      • TOTAL_OFF

      • TOTAL_EXPR
    qReferencedExpression: StringExpr
      This parameter applies when there are several measures.
      Name of the measure to use for the calculation of Others for a specific dimension.
    """

    qOtherMode: str = "OTHER_OFF"
    qOtherCounted: ValueExpr = None
    qOtherLimit: ValueExpr = None
    qOtherLimitMode: str = "OTHER_GT_LIMIT"
    qSuppressOther: bool = None
    qForceBadValueKeeping: bool = True
    qApplyEvenWhenPossiblyWrongResult: bool = True
    qGlobalOtherGrouping: bool = None
    qOtherCollapseInnerDimensions: bool = None
    qOtherSortMode: str = "OTHER_SORT_DESCENDING"
    qTotalMode: str = "TOTAL_OFF"
    qReferencedExpression: StringExpr = None

    def __init__(self_, **kvargs):
        if "qOtherMode" in kvargs:
            if (
                type(kvargs["qOtherMode"]).__name__
                is self_.__annotations__["qOtherMode"]
            ):
                self_.qOtherMode = kvargs["qOtherMode"]
            else:
                self_.qOtherMode = kvargs["qOtherMode"]
        if "qOtherCounted" in kvargs:
            if (
                type(kvargs["qOtherCounted"]).__name__
                is self_.__annotations__["qOtherCounted"]
            ):
                self_.qOtherCounted = kvargs["qOtherCounted"]
            else:
                self_.qOtherCounted = ValueExpr(**kvargs["qOtherCounted"])
        if "qOtherLimit" in kvargs:
            if (
                type(kvargs["qOtherLimit"]).__name__
                is self_.__annotations__["qOtherLimit"]
            ):
                self_.qOtherLimit = kvargs["qOtherLimit"]
            else:
                self_.qOtherLimit = ValueExpr(**kvargs["qOtherLimit"])
        if "qOtherLimitMode" in kvargs:
            if (
                type(kvargs["qOtherLimitMode"]).__name__
                is self_.__annotations__["qOtherLimitMode"]
            ):
                self_.qOtherLimitMode = kvargs["qOtherLimitMode"]
            else:
                self_.qOtherLimitMode = kvargs["qOtherLimitMode"]
        if "qSuppressOther" in kvargs:
            if (
                type(kvargs["qSuppressOther"]).__name__
                is self_.__annotations__["qSuppressOther"]
            ):
                self_.qSuppressOther = kvargs["qSuppressOther"]
            else:
                self_.qSuppressOther = kvargs["qSuppressOther"]
        if "qForceBadValueKeeping" in kvargs:
            if (
                type(kvargs["qForceBadValueKeeping"]).__name__
                is self_.__annotations__["qForceBadValueKeeping"]
            ):
                self_.qForceBadValueKeeping = kvargs["qForceBadValueKeeping"]
            else:
                self_.qForceBadValueKeeping = kvargs["qForceBadValueKeeping"]
        if "qApplyEvenWhenPossiblyWrongResult" in kvargs:
            if (
                type(kvargs["qApplyEvenWhenPossiblyWrongResult"]).__name__
                is self_.__annotations__["qApplyEvenWhenPossiblyWrongResult"]
            ):
                self_.qApplyEvenWhenPossiblyWrongResult = kvargs[
                    "qApplyEvenWhenPossiblyWrongResult"
                ]
            else:
                self_.qApplyEvenWhenPossiblyWrongResult = kvargs[
                    "qApplyEvenWhenPossiblyWrongResult"
                ]
        if "qGlobalOtherGrouping" in kvargs:
            if (
                type(kvargs["qGlobalOtherGrouping"]).__name__
                is self_.__annotations__["qGlobalOtherGrouping"]
            ):
                self_.qGlobalOtherGrouping = kvargs["qGlobalOtherGrouping"]
            else:
                self_.qGlobalOtherGrouping = kvargs["qGlobalOtherGrouping"]
        if "qOtherCollapseInnerDimensions" in kvargs:
            if (
                type(kvargs["qOtherCollapseInnerDimensions"]).__name__
                is self_.__annotations__["qOtherCollapseInnerDimensions"]
            ):
                self_.qOtherCollapseInnerDimensions = kvargs[
                    "qOtherCollapseInnerDimensions"
                ]
            else:
                self_.qOtherCollapseInnerDimensions = kvargs[
                    "qOtherCollapseInnerDimensions"
                ]
        if "qOtherSortMode" in kvargs:
            if (
                type(kvargs["qOtherSortMode"]).__name__
                is self_.__annotations__["qOtherSortMode"]
            ):
                self_.qOtherSortMode = kvargs["qOtherSortMode"]
            else:
                self_.qOtherSortMode = kvargs["qOtherSortMode"]
        if "qTotalMode" in kvargs:
            if (
                type(kvargs["qTotalMode"]).__name__
                is self_.__annotations__["qTotalMode"]
            ):
                self_.qTotalMode = kvargs["qTotalMode"]
            else:
                self_.qTotalMode = kvargs["qTotalMode"]
        if "qReferencedExpression" in kvargs:
            if (
                type(kvargs["qReferencedExpression"]).__name__
                is self_.__annotations__["qReferencedExpression"]
            ):
                self_.qReferencedExpression = kvargs["qReferencedExpression"]
            else:
                self_.qReferencedExpression = StringExpr(
                    **kvargs["qReferencedExpression"]
                )
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ProgressData:
    """

    Attributes
    ----------
    qStarted: bool
      True if the request is started.
    qFinished: bool
      True if the request is finished.
    qCompleted: int
      This property is not used.
    qTotal: int
      This property is not used.
    qKB: int
      This property is not used.
    qMillisecs: int
      Request duration in milliseconds.
    qUserInteractionWanted: bool
      True when the engine pauses the script execution and waits for a user interaction.
    qPersistentProgress: str
      A progress message is persistent when it informs about the start or end of a statement. For example, it can inform about the total number of lines fetched from a data source or tell that the app was saved. All persistent progress messages between two *GetProgress* calls are summarized in this string. Contrarily to *qPersistentProgressMessages*, the content of the localized message string is displayed (not its message code).
    qTransientProgress: str
      A progress message is transient when it informs about the progress of an ongoing statement. For example, it can tell how many lines are currently fetched from a data source. All transient progress messages between two *GetProgress* calls are summarized in this string. Contrarily to *qTransientProgressMessage*, the content of the localized message string is displayed (not its message code).
    qErrorData: list[ErrorData]
      Information about the error messages that occur during the script execution.
    qPersistentProgressMessages: list[ProgressMessage]
      List of persistent progress messages.
    qTransientProgressMessage: ProgressMessage
      Transient progress message.
    """

    qStarted: bool = None
    qFinished: bool = None
    qCompleted: int = None
    qTotal: int = None
    qKB: int = None
    qMillisecs: int = None
    qUserInteractionWanted: bool = None
    qPersistentProgress: str = None
    qTransientProgress: str = None
    qErrorData: list[ErrorData] = None
    qPersistentProgressMessages: list[ProgressMessage] = None
    qTransientProgressMessage: ProgressMessage = None

    def __init__(self_, **kvargs):
        if "qStarted" in kvargs:
            if type(kvargs["qStarted"]).__name__ is self_.__annotations__["qStarted"]:
                self_.qStarted = kvargs["qStarted"]
            else:
                self_.qStarted = kvargs["qStarted"]
        if "qFinished" in kvargs:
            if type(kvargs["qFinished"]).__name__ is self_.__annotations__["qFinished"]:
                self_.qFinished = kvargs["qFinished"]
            else:
                self_.qFinished = kvargs["qFinished"]
        if "qCompleted" in kvargs:
            if (
                type(kvargs["qCompleted"]).__name__
                is self_.__annotations__["qCompleted"]
            ):
                self_.qCompleted = kvargs["qCompleted"]
            else:
                self_.qCompleted = kvargs["qCompleted"]
        if "qTotal" in kvargs:
            if type(kvargs["qTotal"]).__name__ is self_.__annotations__["qTotal"]:
                self_.qTotal = kvargs["qTotal"]
            else:
                self_.qTotal = kvargs["qTotal"]
        if "qKB" in kvargs:
            if type(kvargs["qKB"]).__name__ is self_.__annotations__["qKB"]:
                self_.qKB = kvargs["qKB"]
            else:
                self_.qKB = kvargs["qKB"]
        if "qMillisecs" in kvargs:
            if (
                type(kvargs["qMillisecs"]).__name__
                is self_.__annotations__["qMillisecs"]
            ):
                self_.qMillisecs = kvargs["qMillisecs"]
            else:
                self_.qMillisecs = kvargs["qMillisecs"]
        if "qUserInteractionWanted" in kvargs:
            if (
                type(kvargs["qUserInteractionWanted"]).__name__
                is self_.__annotations__["qUserInteractionWanted"]
            ):
                self_.qUserInteractionWanted = kvargs["qUserInteractionWanted"]
            else:
                self_.qUserInteractionWanted = kvargs["qUserInteractionWanted"]
        if "qPersistentProgress" in kvargs:
            if (
                type(kvargs["qPersistentProgress"]).__name__
                is self_.__annotations__["qPersistentProgress"]
            ):
                self_.qPersistentProgress = kvargs["qPersistentProgress"]
            else:
                self_.qPersistentProgress = kvargs["qPersistentProgress"]
        if "qTransientProgress" in kvargs:
            if (
                type(kvargs["qTransientProgress"]).__name__
                is self_.__annotations__["qTransientProgress"]
            ):
                self_.qTransientProgress = kvargs["qTransientProgress"]
            else:
                self_.qTransientProgress = kvargs["qTransientProgress"]
        if "qErrorData" in kvargs:
            if (
                type(kvargs["qErrorData"]).__name__
                is self_.__annotations__["qErrorData"]
            ):
                self_.qErrorData = kvargs["qErrorData"]
            else:
                self_.qErrorData = [ErrorData(**e) for e in kvargs["qErrorData"]]
        if "qPersistentProgressMessages" in kvargs:
            if (
                type(kvargs["qPersistentProgressMessages"]).__name__
                is self_.__annotations__["qPersistentProgressMessages"]
            ):
                self_.qPersistentProgressMessages = kvargs[
                    "qPersistentProgressMessages"
                ]
            else:
                self_.qPersistentProgressMessages = [
                    ProgressMessage(**e) for e in kvargs["qPersistentProgressMessages"]
                ]
        if "qTransientProgressMessage" in kvargs:
            if (
                type(kvargs["qTransientProgressMessage"]).__name__
                is self_.__annotations__["qTransientProgressMessage"]
            ):
                self_.qTransientProgressMessage = kvargs["qTransientProgressMessage"]
            else:
                self_.qTransientProgressMessage = ProgressMessage(
                    **kvargs["qTransientProgressMessage"]
                )
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchCombinationOptions:
    """

    Attributes
    ----------
    qSearchFields: list[str]
      List of the search fields.
      If empty, the search is performed in all fields of the app.
    qContext: str
      Search context.
      The default value is LockedFieldsOnly .

      One of:

      • Cleared or CONTEXT_CLEARED

      • LockedFieldsOnly or CONTEXT_LOCKED_FIELDS_ONLY

      • CurrentSelections or CONTEXT_CURRENT_SELECTIONS
    qCharEncoding: str
      Encoding used to compute qRanges of type SearchCharRange.
      Only affects the computation of the ranges. It does not impact the encoding of the text.

      One of:

      • Utf8 or CHAR_ENCODING_UTF8

      • Utf16 or CHAR_ENCODING_UTF16
    qAttributes: list[str]
      Optional.

      • For SearchSuggest method, this array is empty.

      • For SearchObjects method, this array is empty or contain qProperty .

      • For SearchResults method, this array is empty, or contains qNum and/or qElemNum . It allows the user to request details in the outputted SearchGroupItemMatch . For more information, see SearchGroupItemMatch.
    """

    qSearchFields: list[str] = None
    qContext: str = "CONTEXT_LOCKED_FIELDS_ONLY"
    qCharEncoding: str = "CHAR_ENCODING_UTF8"
    qAttributes: list[str] = None

    def __init__(self_, **kvargs):
        if "qSearchFields" in kvargs:
            if (
                type(kvargs["qSearchFields"]).__name__
                is self_.__annotations__["qSearchFields"]
            ):
                self_.qSearchFields = kvargs["qSearchFields"]
            else:
                self_.qSearchFields = kvargs["qSearchFields"]
        if "qContext" in kvargs:
            if type(kvargs["qContext"]).__name__ is self_.__annotations__["qContext"]:
                self_.qContext = kvargs["qContext"]
            else:
                self_.qContext = kvargs["qContext"]
        if "qCharEncoding" in kvargs:
            if (
                type(kvargs["qCharEncoding"]).__name__
                is self_.__annotations__["qCharEncoding"]
            ):
                self_.qCharEncoding = kvargs["qCharEncoding"]
            else:
                self_.qCharEncoding = kvargs["qCharEncoding"]
        if "qAttributes" in kvargs:
            if (
                type(kvargs["qAttributes"]).__name__
                is self_.__annotations__["qAttributes"]
            ):
                self_.qAttributes = kvargs["qAttributes"]
            else:
                self_.qAttributes = kvargs["qAttributes"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchFieldDictionary:
    """

    Attributes
    ----------
    qField: int
      Position of the field in the list of fields, starting from 0.
      The list of fields is defined in qResults/qFieldNames and contains the search associations.
    qResult: list[SearchTermResult]
      List of the matching values.
      The maximum number of values in this list is set by qMaxNbrFieldMatches .
    """

    qField: int = None
    qResult: list[SearchTermResult] = None

    def __init__(self_, **kvargs):
        if "qField" in kvargs:
            if type(kvargs["qField"]).__name__ is self_.__annotations__["qField"]:
                self_.qField = kvargs["qField"]
            else:
                self_.qField = kvargs["qField"]
        if "qResult" in kvargs:
            if type(kvargs["qResult"]).__name__ is self_.__annotations__["qResult"]:
                self_.qResult = kvargs["qResult"]
            else:
                self_.qResult = [SearchTermResult(**e) for e in kvargs["qResult"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroupItem:
    """

    Attributes
    ----------
    qItemType: str
      Type of the group item.

      One of:

      • Field or FIELD

      • GenericObject or GENERIC_OBJECT
    qTotalNumberOfMatches: int
      Total number of distinct matches in the search group item.
    qIdentifier: str
      Identifier of the item.
      It corresponds to:

      • The name of the field, if the type of the search group is data set.

      • The id of the generic object if the type of the search group is generic object.
    qItemMatches: list[SearchGroupItemMatch]
      List of matches in the search group item.
      The group item matches are numbered from the value of SearchGroupItemOptions.qOffset to the value of SearchGroupItemOptions.qOffset \+ SearchGroupItemOptions.qCount .
    qSearchTermsMatched: list[int]
      Indexes of the search terms that are included in the group item. These search terms are related to the list of terms defined in SearchResult.qSearchTerms .
    """

    qItemType: str = None
    qTotalNumberOfMatches: int = None
    qIdentifier: str = None
    qItemMatches: list[SearchGroupItemMatch] = None
    qSearchTermsMatched: list[int] = None

    def __init__(self_, **kvargs):
        if "qItemType" in kvargs:
            if type(kvargs["qItemType"]).__name__ is self_.__annotations__["qItemType"]:
                self_.qItemType = kvargs["qItemType"]
            else:
                self_.qItemType = kvargs["qItemType"]
        if "qTotalNumberOfMatches" in kvargs:
            if (
                type(kvargs["qTotalNumberOfMatches"]).__name__
                is self_.__annotations__["qTotalNumberOfMatches"]
            ):
                self_.qTotalNumberOfMatches = kvargs["qTotalNumberOfMatches"]
            else:
                self_.qTotalNumberOfMatches = kvargs["qTotalNumberOfMatches"]
        if "qIdentifier" in kvargs:
            if (
                type(kvargs["qIdentifier"]).__name__
                is self_.__annotations__["qIdentifier"]
            ):
                self_.qIdentifier = kvargs["qIdentifier"]
            else:
                self_.qIdentifier = kvargs["qIdentifier"]
        if "qItemMatches" in kvargs:
            if (
                type(kvargs["qItemMatches"]).__name__
                is self_.__annotations__["qItemMatches"]
            ):
                self_.qItemMatches = kvargs["qItemMatches"]
            else:
                self_.qItemMatches = [
                    SearchGroupItemMatch(**e) for e in kvargs["qItemMatches"]
                ]
        if "qSearchTermsMatched" in kvargs:
            if (
                type(kvargs["qSearchTermsMatched"]).__name__
                is self_.__annotations__["qSearchTermsMatched"]
            ):
                self_.qSearchTermsMatched = kvargs["qSearchTermsMatched"]
            else:
                self_.qSearchTermsMatched = kvargs["qSearchTermsMatched"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroupItemOptions:
    """

    Attributes
    ----------
    qGroupItemType: str
      Type of the group item. Can be:

      • GenericObject: the type of the search group item is a generic object. Group items have this type when you are calling SearchObjects .

      • Field: the type of the search group item is a field. Group items have this type when you are calling SearchResults .

      One of:

      • Field or FIELD

      • GenericObject or GENERIC_OBJECT
    qOffset: int
      Position starting from 0.
      The default value is 0.
    qCount: int
      Maximum number of matches per item (in qItemMatches[ ] ).
      The default value is -1: all values are returned.
    """

    qGroupItemType: str = None
    qOffset: int = None
    qCount: int = -1

    def __init__(self_, **kvargs):
        if "qGroupItemType" in kvargs:
            if (
                type(kvargs["qGroupItemType"]).__name__
                is self_.__annotations__["qGroupItemType"]
            ):
                self_.qGroupItemType = kvargs["qGroupItemType"]
            else:
                self_.qGroupItemType = kvargs["qGroupItemType"]
        if "qOffset" in kvargs:
            if type(kvargs["qOffset"]).__name__ is self_.__annotations__["qOffset"]:
                self_.qOffset = kvargs["qOffset"]
            else:
                self_.qOffset = kvargs["qOffset"]
        if "qCount" in kvargs:
            if type(kvargs["qCount"]).__name__ is self_.__annotations__["qCount"]:
                self_.qCount = kvargs["qCount"]
            else:
                self_.qCount = kvargs["qCount"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroupOptions:
    """

    Attributes
    ----------
    qGroupType: str
      Type of the group. Can be:

      • GenericObjectType: the type of the search group item is a generic object. Groups have this type when you are calling SearchObjects .

      • DatasetType: type of the search group item is a dataset association. Groups have this type when you are calling SearchResults .

      One of:

      • DatasetType or DATASET_GROUP

      • GenericObjectsType or GENERIC_OBJECTS_GROUP
    qOffset: int
      Position starting from 0.
      The default value is 0.
    qCount: int
      Maximum number of items per group (in qItems[ ] ).
      The default value is -1; all values are returned.
    """

    qGroupType: str = None
    qOffset: int = None
    qCount: int = -1

    def __init__(self_, **kvargs):
        if "qGroupType" in kvargs:
            if (
                type(kvargs["qGroupType"]).__name__
                is self_.__annotations__["qGroupType"]
            ):
                self_.qGroupType = kvargs["qGroupType"]
            else:
                self_.qGroupType = kvargs["qGroupType"]
        if "qOffset" in kvargs:
            if type(kvargs["qOffset"]).__name__ is self_.__annotations__["qOffset"]:
                self_.qOffset = kvargs["qOffset"]
            else:
                self_.qOffset = kvargs["qOffset"]
        if "qCount" in kvargs:
            if type(kvargs["qCount"]).__name__ is self_.__annotations__["qCount"]:
                self_.qCount = kvargs["qCount"]
            else:
                self_.qCount = kvargs["qCount"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchPage:
    """

    Attributes
    ----------
    qOffset: int
      Position from the top, starting from 0.
      If the offset is set to 0, the first search result to be returned is at position 0.
    qCount: int
      Number of search groups to return (in qSearchGroupArray ).
    qMaxNbrFieldMatches: int
      Maximum number of matching values to return per search result.
      The default value is -1; all values are returned.
      This property is to be used with the SearchAssociations method.
    qGroupOptions: list[SearchGroupOptions]
      Options of the search groups.
      If this property is not set, all values are returned.
      This property is to be used with the SearchResults method or the SearchObjects method.
    qGroupItemOptions: list[SearchGroupItemOptions]
      Options of the search group items.
      If this property is not set, all values are returned.
      This property is to be used with the SearchResults method or the SearchObjects method.
    """

    qOffset: int = None
    qCount: int = None
    qMaxNbrFieldMatches: int = -1
    qGroupOptions: list[SearchGroupOptions] = None
    qGroupItemOptions: list[SearchGroupItemOptions] = None

    def __init__(self_, **kvargs):
        if "qOffset" in kvargs:
            if type(kvargs["qOffset"]).__name__ is self_.__annotations__["qOffset"]:
                self_.qOffset = kvargs["qOffset"]
            else:
                self_.qOffset = kvargs["qOffset"]
        if "qCount" in kvargs:
            if type(kvargs["qCount"]).__name__ is self_.__annotations__["qCount"]:
                self_.qCount = kvargs["qCount"]
            else:
                self_.qCount = kvargs["qCount"]
        if "qMaxNbrFieldMatches" in kvargs:
            if (
                type(kvargs["qMaxNbrFieldMatches"]).__name__
                is self_.__annotations__["qMaxNbrFieldMatches"]
            ):
                self_.qMaxNbrFieldMatches = kvargs["qMaxNbrFieldMatches"]
            else:
                self_.qMaxNbrFieldMatches = kvargs["qMaxNbrFieldMatches"]
        if "qGroupOptions" in kvargs:
            if (
                type(kvargs["qGroupOptions"]).__name__
                is self_.__annotations__["qGroupOptions"]
            ):
                self_.qGroupOptions = kvargs["qGroupOptions"]
            else:
                self_.qGroupOptions = [
                    SearchGroupOptions(**e) for e in kvargs["qGroupOptions"]
                ]
        if "qGroupItemOptions" in kvargs:
            if (
                type(kvargs["qGroupItemOptions"]).__name__
                is self_.__annotations__["qGroupItemOptions"]
            ):
                self_.qGroupItemOptions = kvargs["qGroupItemOptions"]
            else:
                self_.qGroupItemOptions = [
                    SearchGroupItemOptions(**e) for e in kvargs["qGroupItemOptions"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SortCriteria:
    """

    Attributes
    ----------
    qSortByState: int
      Sorts the field values according to their logical state (selected, optional, alternative or excluded).
    qSortByFrequency: int
      Sorts the field values by frequency (number of occurrences in the field).
    qSortByNumeric: int
      Sorts the field values by numeric value.
    qSortByAscii: int
      Sorts the field by alphabetical order.
    qSortByLoadOrder: int
      Sorts the field values by the initial load order.
    qSortByExpression: int
      Sorts the field by expression.
    qExpression: ValueExpr
      Sort by expression.
    qSortByGreyness: int
    """

    qSortByState: int = None
    qSortByFrequency: int = None
    qSortByNumeric: int = None
    qSortByAscii: int = None
    qSortByLoadOrder: int = None
    qSortByExpression: int = None
    qExpression: ValueExpr = None
    qSortByGreyness: int = None

    def __init__(self_, **kvargs):
        if "qSortByState" in kvargs:
            if (
                type(kvargs["qSortByState"]).__name__
                is self_.__annotations__["qSortByState"]
            ):
                self_.qSortByState = kvargs["qSortByState"]
            else:
                self_.qSortByState = kvargs["qSortByState"]
        if "qSortByFrequency" in kvargs:
            if (
                type(kvargs["qSortByFrequency"]).__name__
                is self_.__annotations__["qSortByFrequency"]
            ):
                self_.qSortByFrequency = kvargs["qSortByFrequency"]
            else:
                self_.qSortByFrequency = kvargs["qSortByFrequency"]
        if "qSortByNumeric" in kvargs:
            if (
                type(kvargs["qSortByNumeric"]).__name__
                is self_.__annotations__["qSortByNumeric"]
            ):
                self_.qSortByNumeric = kvargs["qSortByNumeric"]
            else:
                self_.qSortByNumeric = kvargs["qSortByNumeric"]
        if "qSortByAscii" in kvargs:
            if (
                type(kvargs["qSortByAscii"]).__name__
                is self_.__annotations__["qSortByAscii"]
            ):
                self_.qSortByAscii = kvargs["qSortByAscii"]
            else:
                self_.qSortByAscii = kvargs["qSortByAscii"]
        if "qSortByLoadOrder" in kvargs:
            if (
                type(kvargs["qSortByLoadOrder"]).__name__
                is self_.__annotations__["qSortByLoadOrder"]
            ):
                self_.qSortByLoadOrder = kvargs["qSortByLoadOrder"]
            else:
                self_.qSortByLoadOrder = kvargs["qSortByLoadOrder"]
        if "qSortByExpression" in kvargs:
            if (
                type(kvargs["qSortByExpression"]).__name__
                is self_.__annotations__["qSortByExpression"]
            ):
                self_.qSortByExpression = kvargs["qSortByExpression"]
            else:
                self_.qSortByExpression = kvargs["qSortByExpression"]
        if "qExpression" in kvargs:
            if (
                type(kvargs["qExpression"]).__name__
                is self_.__annotations__["qExpression"]
            ):
                self_.qExpression = kvargs["qExpression"]
            else:
                self_.qExpression = ValueExpr(**kvargs["qExpression"])
        if "qSortByGreyness" in kvargs:
            if (
                type(kvargs["qSortByGreyness"]).__name__
                is self_.__annotations__["qSortByGreyness"]
            ):
                self_.qSortByGreyness = kvargs["qSortByGreyness"]
            else:
                self_.qSortByGreyness = kvargs["qSortByGreyness"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StaticContentList:
    """

    Attributes
    ----------
    qItems: list[StaticContentListItem]
      Information about the list of content files.
    """

    qItems: list[StaticContentListItem] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs:
            if type(kvargs["qItems"]).__name__ is self_.__annotations__["qItems"]:
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [StaticContentListItem(**e) for e in kvargs["qItems"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SymbolFrequency:
    """

    Attributes
    ----------
    qSymbol: SymbolValue
      Symbol. Either string and NaN or number alone
    qFrequency: int
      Frequency of the above symbol in the field
    """

    qSymbol: SymbolValue = None
    qFrequency: int = None

    def __init__(self_, **kvargs):
        if "qSymbol" in kvargs:
            if type(kvargs["qSymbol"]).__name__ is self_.__annotations__["qSymbol"]:
                self_.qSymbol = kvargs["qSymbol"]
            else:
                self_.qSymbol = SymbolValue(**kvargs["qSymbol"])
        if "qFrequency" in kvargs:
            if (
                type(kvargs["qFrequency"]).__name__
                is self_.__annotations__["qFrequency"]
            ):
                self_.qFrequency = kvargs["qFrequency"]
            else:
                self_.qFrequency = kvargs["qFrequency"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableViewSaveInfo:
    """

    Attributes
    ----------
    qTables: list[TableViewTableWinSaveInfo]
      List of the tables in the database model viewer.
    qBroomPoints: list[TableViewBroomPointSaveInfo]
      List of the broom points in the database model viewer.
      Not used in Qlik Sense.
    qConnectionPoints: list[TableViewConnectionPointSaveInfo]
      List of connection points in the database model viewer.
      Not used in Qlik Sense.
    qZoomFactor: float
      Zoom factor in the database model viewer.
      The default value is 1.0.
    """

    qTables: list[TableViewTableWinSaveInfo] = None
    qBroomPoints: list[TableViewBroomPointSaveInfo] = None
    qConnectionPoints: list[TableViewConnectionPointSaveInfo] = None
    qZoomFactor: float = 1

    def __init__(self_, **kvargs):
        if "qTables" in kvargs:
            if type(kvargs["qTables"]).__name__ is self_.__annotations__["qTables"]:
                self_.qTables = kvargs["qTables"]
            else:
                self_.qTables = [
                    TableViewTableWinSaveInfo(**e) for e in kvargs["qTables"]
                ]
        if "qBroomPoints" in kvargs:
            if (
                type(kvargs["qBroomPoints"]).__name__
                is self_.__annotations__["qBroomPoints"]
            ):
                self_.qBroomPoints = kvargs["qBroomPoints"]
            else:
                self_.qBroomPoints = [
                    TableViewBroomPointSaveInfo(**e) for e in kvargs["qBroomPoints"]
                ]
        if "qConnectionPoints" in kvargs:
            if (
                type(kvargs["qConnectionPoints"]).__name__
                is self_.__annotations__["qConnectionPoints"]
            ):
                self_.qConnectionPoints = kvargs["qConnectionPoints"]
            else:
                self_.qConnectionPoints = [
                    TableViewConnectionPointSaveInfo(**e)
                    for e in kvargs["qConnectionPoints"]
                ]
        if "qZoomFactor" in kvargs:
            if (
                type(kvargs["qZoomFactor"]).__name__
                is self_.__annotations__["qZoomFactor"]
            ):
                self_.qZoomFactor = kvargs["qZoomFactor"]
            else:
                self_.qZoomFactor = kvargs["qZoomFactor"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppObjectList:
    """
    Lists the app objects. Is the layout for AppObjectListDef.
    An app object is a generic object created at app level.

    Attributes
    ----------
    qItems: list[NxContainerEntry]
      Information about the list of dimensions.
    """

    qItems: list[NxContainerEntry] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs:
            if type(kvargs["qItems"]).__name__ is self_.__annotations__["qItems"]:
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [NxContainerEntry(**e) for e in kvargs["qItems"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ArrayOfNxValuePoint:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BookmarkFieldItem:
    """

    Attributes
    ----------
    qDef: FieldDefEx
      Name and type of the field.
    qLocked: bool
      Indicates if the field is locked.
      Default is false.
    qSelectInfo: SelectInfo
      Information on the selections criteria.
    qValues: list[FieldValue]
    qExcludedValues: list[FieldValue]
      List of excluded values.
      Either the list of selected values or the list of excluded values is displayed.
    qAndMode: bool
      If set to true, selections within a list object are made in AND mode; If you have a list object that lists all customers, by selecting Customer 1 and Customer 2 while in and-mode, all records that are associated with Customer 1 and Customer 2 are selected.
      The default value is false; selections within a list object are made in OR mode. If you have a list object that lists all customers, by selecting Customer 1 and Customer 2 while in or-mode, all records that are associated with either Customer 1 or Customer 2 are selected.
      This parameter is not returned if set to false.
    qOneAndOnlyOne: bool
      If set to true, the field has always one selection (not 0 and not more than 1). If another value is selected, the previous one is unselected.
      The default value is false. This parameter is not returned if set to false.
    """

    qDef: FieldDefEx = None
    qLocked: bool = None
    qSelectInfo: SelectInfo = None
    qValues: list[FieldValue] = None
    qExcludedValues: list[FieldValue] = None
    qAndMode: bool = None
    qOneAndOnlyOne: bool = None

    def __init__(self_, **kvargs):
        if "qDef" in kvargs:
            if type(kvargs["qDef"]).__name__ is self_.__annotations__["qDef"]:
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = FieldDefEx(**kvargs["qDef"])
        if "qLocked" in kvargs:
            if type(kvargs["qLocked"]).__name__ is self_.__annotations__["qLocked"]:
                self_.qLocked = kvargs["qLocked"]
            else:
                self_.qLocked = kvargs["qLocked"]
        if "qSelectInfo" in kvargs:
            if (
                type(kvargs["qSelectInfo"]).__name__
                is self_.__annotations__["qSelectInfo"]
            ):
                self_.qSelectInfo = kvargs["qSelectInfo"]
            else:
                self_.qSelectInfo = SelectInfo(**kvargs["qSelectInfo"])
        if "qValues" in kvargs:
            if type(kvargs["qValues"]).__name__ is self_.__annotations__["qValues"]:
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [FieldValue(**e) for e in kvargs["qValues"]]
        if "qExcludedValues" in kvargs:
            if (
                type(kvargs["qExcludedValues"]).__name__
                is self_.__annotations__["qExcludedValues"]
            ):
                self_.qExcludedValues = kvargs["qExcludedValues"]
            else:
                self_.qExcludedValues = [
                    FieldValue(**e) for e in kvargs["qExcludedValues"]
                ]
        if "qAndMode" in kvargs:
            if type(kvargs["qAndMode"]).__name__ is self_.__annotations__["qAndMode"]:
                self_.qAndMode = kvargs["qAndMode"]
            else:
                self_.qAndMode = kvargs["qAndMode"]
        if "qOneAndOnlyOne" in kvargs:
            if (
                type(kvargs["qOneAndOnlyOne"]).__name__
                is self_.__annotations__["qOneAndOnlyOne"]
            ):
                self_.qOneAndOnlyOne = kvargs["qOneAndOnlyOne"]
            else:
                self_.qOneAndOnlyOne = kvargs["qOneAndOnlyOne"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BookmarkList:
    """
    Lists the bookmarks. Is the layout for BookmarkListDef.

    Attributes
    ----------
    qItems: list[NxContainerEntry]
      Information about the list of bookmarks.
    """

    qItems: list[NxContainerEntry] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs:
            if type(kvargs["qItems"]).__name__ is self_.__annotations__["qItems"]:
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [NxContainerEntry(**e) for e in kvargs["qItems"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ChildList:
    """
    Lists the children of a generic object. Is the layout for ChildListDef.
    ChildList is used by the GetLayout Method to list the children of a generic object.

    Attributes
    ----------
    qItems: list[NxContainerEntry]
      Information about the items in the app object.
    """

    qItems: list[NxContainerEntry] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs:
            if type(kvargs["qItems"]).__name__ is self_.__annotations__["qItems"]:
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [NxContainerEntry(**e) for e in kvargs["qItems"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ContentLibraryList:
    """

    Attributes
    ----------
    qItems: list[ContentLibraryListItem]
      Information about the content library.
    """

    qItems: list[ContentLibraryListItem] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs:
            if type(kvargs["qItems"]).__name__ is self_.__annotations__["qItems"]:
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [ContentLibraryListItem(**e) for e in kvargs["qItems"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DimensionList:
    """
    Lists the dimensions. Is the layout for DimensionListDef.

    Attributes
    ----------
    qItems: list[NxContainerEntry]
      Information about the list of dimensions.
    """

    qItems: list[NxContainerEntry] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs:
            if type(kvargs["qItems"]).__name__ is self_.__annotations__["qItems"]:
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [NxContainerEntry(**e) for e in kvargs["qItems"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldInTableProfilingData:
    """

    Attributes
    ----------
    qName: str
      Name of the field.
    qFieldTags: list[str]
      List of tags related to the field.
    qNumberFormat: FieldAttributes
    qDistinctValues: int
      Number of distinct values
    qDistinctNumericValues: int
      Number of distinct numeric values
    qDistinctTextValues: int
      Number of distinct text values
    qNumericValues: int
      Number of numeric values
    qNullValues: int
      Number of null values
    qTextValues: int
      Number of textual values
    qNegValues: int
      Number of negative values
    qPosValues: int
      Number of positive values
    qZeroValues: int
      Number of zero values for numerical values
    qSum: float
      Sum of all numerical values. NaN otherwise.
    qSum2: float
      Squared sum of all numerical values. NaN otherwise.
    qAverage: float
      Average of all numerical values. NaN otherwise.
    qMedian: float
      Median of all numerical values. NaN otherwise.
    qStd: float
      Standard deviation of numerical values. NaN otherwise.
    qMin: float
      Minimum value of numerical values. NaN otherwise.
    qMax: float
      Maximum value of numerical values. NaN otherwise.
    qSkewness: float
      Skewness of the numerical values. NaN otherwise.
    qKurtosis: float
      Kurtosis of the numerical values. NaN otherwise.
    qFractiles: list[float]
      The .01, .05, .1, .25, .5, .75, .9, .95, .99 fractiles. Array of NaN otherwise.
    qEmptyStrings: int
      Number of empty strings
    qMaxStringLen: int
      Maximum string length of textual values. 0 otherwise.
    qMinStringLen: int
      Minimum string length of textual values. 0 otherwise.
    qSumStringLen: int
      Sum of all characters in strings in the field
    qAvgStringLen: float
      Average string length of textual values. 0 otherwise.
    qFirstSorted: str
      For textual values the first sorted string.
    qLastSorted: str
      For textual values the last sorted string.
    qMostFrequent: list[SymbolFrequency]
      Three most frequent values and their frequencies
    qFrequencyDistribution: FrequencyDistributionData
      Frequency Distribution for numeric fields.
    """

    qName: str = None
    qFieldTags: list[str] = None
    qNumberFormat: FieldAttributes = None
    qDistinctValues: int = None
    qDistinctNumericValues: int = None
    qDistinctTextValues: int = None
    qNumericValues: int = None
    qNullValues: int = None
    qTextValues: int = None
    qNegValues: int = None
    qPosValues: int = None
    qZeroValues: int = None
    qSum: float = None
    qSum2: float = None
    qAverage: float = None
    qMedian: float = None
    qStd: float = None
    qMin: float = None
    qMax: float = None
    qSkewness: float = None
    qKurtosis: float = None
    qFractiles: list[float] = None
    qEmptyStrings: int = None
    qMaxStringLen: int = None
    qMinStringLen: int = None
    qSumStringLen: int = None
    qAvgStringLen: float = None
    qFirstSorted: str = None
    qLastSorted: str = None
    qMostFrequent: list[SymbolFrequency] = None
    qFrequencyDistribution: FrequencyDistributionData = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qFieldTags" in kvargs:
            if (
                type(kvargs["qFieldTags"]).__name__
                is self_.__annotations__["qFieldTags"]
            ):
                self_.qFieldTags = kvargs["qFieldTags"]
            else:
                self_.qFieldTags = kvargs["qFieldTags"]
        if "qNumberFormat" in kvargs:
            if (
                type(kvargs["qNumberFormat"]).__name__
                is self_.__annotations__["qNumberFormat"]
            ):
                self_.qNumberFormat = kvargs["qNumberFormat"]
            else:
                self_.qNumberFormat = FieldAttributes(**kvargs["qNumberFormat"])
        if "qDistinctValues" in kvargs:
            if (
                type(kvargs["qDistinctValues"]).__name__
                is self_.__annotations__["qDistinctValues"]
            ):
                self_.qDistinctValues = kvargs["qDistinctValues"]
            else:
                self_.qDistinctValues = kvargs["qDistinctValues"]
        if "qDistinctNumericValues" in kvargs:
            if (
                type(kvargs["qDistinctNumericValues"]).__name__
                is self_.__annotations__["qDistinctNumericValues"]
            ):
                self_.qDistinctNumericValues = kvargs["qDistinctNumericValues"]
            else:
                self_.qDistinctNumericValues = kvargs["qDistinctNumericValues"]
        if "qDistinctTextValues" in kvargs:
            if (
                type(kvargs["qDistinctTextValues"]).__name__
                is self_.__annotations__["qDistinctTextValues"]
            ):
                self_.qDistinctTextValues = kvargs["qDistinctTextValues"]
            else:
                self_.qDistinctTextValues = kvargs["qDistinctTextValues"]
        if "qNumericValues" in kvargs:
            if (
                type(kvargs["qNumericValues"]).__name__
                is self_.__annotations__["qNumericValues"]
            ):
                self_.qNumericValues = kvargs["qNumericValues"]
            else:
                self_.qNumericValues = kvargs["qNumericValues"]
        if "qNullValues" in kvargs:
            if (
                type(kvargs["qNullValues"]).__name__
                is self_.__annotations__["qNullValues"]
            ):
                self_.qNullValues = kvargs["qNullValues"]
            else:
                self_.qNullValues = kvargs["qNullValues"]
        if "qTextValues" in kvargs:
            if (
                type(kvargs["qTextValues"]).__name__
                is self_.__annotations__["qTextValues"]
            ):
                self_.qTextValues = kvargs["qTextValues"]
            else:
                self_.qTextValues = kvargs["qTextValues"]
        if "qNegValues" in kvargs:
            if (
                type(kvargs["qNegValues"]).__name__
                is self_.__annotations__["qNegValues"]
            ):
                self_.qNegValues = kvargs["qNegValues"]
            else:
                self_.qNegValues = kvargs["qNegValues"]
        if "qPosValues" in kvargs:
            if (
                type(kvargs["qPosValues"]).__name__
                is self_.__annotations__["qPosValues"]
            ):
                self_.qPosValues = kvargs["qPosValues"]
            else:
                self_.qPosValues = kvargs["qPosValues"]
        if "qZeroValues" in kvargs:
            if (
                type(kvargs["qZeroValues"]).__name__
                is self_.__annotations__["qZeroValues"]
            ):
                self_.qZeroValues = kvargs["qZeroValues"]
            else:
                self_.qZeroValues = kvargs["qZeroValues"]
        if "qSum" in kvargs:
            if type(kvargs["qSum"]).__name__ is self_.__annotations__["qSum"]:
                self_.qSum = kvargs["qSum"]
            else:
                self_.qSum = kvargs["qSum"]
        if "qSum2" in kvargs:
            if type(kvargs["qSum2"]).__name__ is self_.__annotations__["qSum2"]:
                self_.qSum2 = kvargs["qSum2"]
            else:
                self_.qSum2 = kvargs["qSum2"]
        if "qAverage" in kvargs:
            if type(kvargs["qAverage"]).__name__ is self_.__annotations__["qAverage"]:
                self_.qAverage = kvargs["qAverage"]
            else:
                self_.qAverage = kvargs["qAverage"]
        if "qMedian" in kvargs:
            if type(kvargs["qMedian"]).__name__ is self_.__annotations__["qMedian"]:
                self_.qMedian = kvargs["qMedian"]
            else:
                self_.qMedian = kvargs["qMedian"]
        if "qStd" in kvargs:
            if type(kvargs["qStd"]).__name__ is self_.__annotations__["qStd"]:
                self_.qStd = kvargs["qStd"]
            else:
                self_.qStd = kvargs["qStd"]
        if "qMin" in kvargs:
            if type(kvargs["qMin"]).__name__ is self_.__annotations__["qMin"]:
                self_.qMin = kvargs["qMin"]
            else:
                self_.qMin = kvargs["qMin"]
        if "qMax" in kvargs:
            if type(kvargs["qMax"]).__name__ is self_.__annotations__["qMax"]:
                self_.qMax = kvargs["qMax"]
            else:
                self_.qMax = kvargs["qMax"]
        if "qSkewness" in kvargs:
            if type(kvargs["qSkewness"]).__name__ is self_.__annotations__["qSkewness"]:
                self_.qSkewness = kvargs["qSkewness"]
            else:
                self_.qSkewness = kvargs["qSkewness"]
        if "qKurtosis" in kvargs:
            if type(kvargs["qKurtosis"]).__name__ is self_.__annotations__["qKurtosis"]:
                self_.qKurtosis = kvargs["qKurtosis"]
            else:
                self_.qKurtosis = kvargs["qKurtosis"]
        if "qFractiles" in kvargs:
            if (
                type(kvargs["qFractiles"]).__name__
                is self_.__annotations__["qFractiles"]
            ):
                self_.qFractiles = kvargs["qFractiles"]
            else:
                self_.qFractiles = kvargs["qFractiles"]
        if "qEmptyStrings" in kvargs:
            if (
                type(kvargs["qEmptyStrings"]).__name__
                is self_.__annotations__["qEmptyStrings"]
            ):
                self_.qEmptyStrings = kvargs["qEmptyStrings"]
            else:
                self_.qEmptyStrings = kvargs["qEmptyStrings"]
        if "qMaxStringLen" in kvargs:
            if (
                type(kvargs["qMaxStringLen"]).__name__
                is self_.__annotations__["qMaxStringLen"]
            ):
                self_.qMaxStringLen = kvargs["qMaxStringLen"]
            else:
                self_.qMaxStringLen = kvargs["qMaxStringLen"]
        if "qMinStringLen" in kvargs:
            if (
                type(kvargs["qMinStringLen"]).__name__
                is self_.__annotations__["qMinStringLen"]
            ):
                self_.qMinStringLen = kvargs["qMinStringLen"]
            else:
                self_.qMinStringLen = kvargs["qMinStringLen"]
        if "qSumStringLen" in kvargs:
            if (
                type(kvargs["qSumStringLen"]).__name__
                is self_.__annotations__["qSumStringLen"]
            ):
                self_.qSumStringLen = kvargs["qSumStringLen"]
            else:
                self_.qSumStringLen = kvargs["qSumStringLen"]
        if "qAvgStringLen" in kvargs:
            if (
                type(kvargs["qAvgStringLen"]).__name__
                is self_.__annotations__["qAvgStringLen"]
            ):
                self_.qAvgStringLen = kvargs["qAvgStringLen"]
            else:
                self_.qAvgStringLen = kvargs["qAvgStringLen"]
        if "qFirstSorted" in kvargs:
            if (
                type(kvargs["qFirstSorted"]).__name__
                is self_.__annotations__["qFirstSorted"]
            ):
                self_.qFirstSorted = kvargs["qFirstSorted"]
            else:
                self_.qFirstSorted = kvargs["qFirstSorted"]
        if "qLastSorted" in kvargs:
            if (
                type(kvargs["qLastSorted"]).__name__
                is self_.__annotations__["qLastSorted"]
            ):
                self_.qLastSorted = kvargs["qLastSorted"]
            else:
                self_.qLastSorted = kvargs["qLastSorted"]
        if "qMostFrequent" in kvargs:
            if (
                type(kvargs["qMostFrequent"]).__name__
                is self_.__annotations__["qMostFrequent"]
            ):
                self_.qMostFrequent = kvargs["qMostFrequent"]
            else:
                self_.qMostFrequent = [
                    SymbolFrequency(**e) for e in kvargs["qMostFrequent"]
                ]
        if "qFrequencyDistribution" in kvargs:
            if (
                type(kvargs["qFrequencyDistribution"]).__name__
                is self_.__annotations__["qFrequencyDistribution"]
            ):
                self_.qFrequencyDistribution = kvargs["qFrequencyDistribution"]
            else:
                self_.qFrequencyDistribution = FrequencyDistributionData(
                    **kvargs["qFrequencyDistribution"]
                )
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MeasureList:
    """
    Lists the measures. Is the layout for MeasureListDef.

    Attributes
    ----------
    qItems: list[NxContainerEntry]
      Information about the list of measures.
    """

    qItems: list[NxContainerEntry] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs:
            if type(kvargs["qItems"]).__name__ is self_.__annotations__["qItems"]:
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [NxContainerEntry(**e) for e in kvargs["qItems"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttrDimDef:
    """
    Layout for NxAttrDimDef.

    Attributes
    ----------
    qDef: str
      Expression or field name.
    qLibraryId: str
      LibraryId for dimension.
    qSortBy: SortCriteria
      Sorting.
    qAttribute: bool
      If set to true, this attribute will not affect the number of rows in the cube.
    """

    qDef: str = None
    qLibraryId: str = None
    qSortBy: SortCriteria = None
    qAttribute: bool = None

    def __init__(self_, **kvargs):
        if "qDef" in kvargs:
            if type(kvargs["qDef"]).__name__ is self_.__annotations__["qDef"]:
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = kvargs["qDef"]
        if "qLibraryId" in kvargs:
            if (
                type(kvargs["qLibraryId"]).__name__
                is self_.__annotations__["qLibraryId"]
            ):
                self_.qLibraryId = kvargs["qLibraryId"]
            else:
                self_.qLibraryId = kvargs["qLibraryId"]
        if "qSortBy" in kvargs:
            if type(kvargs["qSortBy"]).__name__ is self_.__annotations__["qSortBy"]:
                self_.qSortBy = kvargs["qSortBy"]
            else:
                self_.qSortBy = SortCriteria(**kvargs["qSortBy"])
        if "qAttribute" in kvargs:
            if (
                type(kvargs["qAttribute"]).__name__
                is self_.__annotations__["qAttribute"]
            ):
                self_.qAttribute = kvargs["qAttribute"]
            else:
                self_.qAttribute = kvargs["qAttribute"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAxisData:
    """

    Attributes
    ----------
    qAxis: list[NxAxisTicks]
      List of axis data.
    """

    qAxis: list[NxAxisTicks] = None

    def __init__(self_, **kvargs):
        if "qAxis" in kvargs:
            if type(kvargs["qAxis"]).__name__ is self_.__annotations__["qAxis"]:
                self_.qAxis = kvargs["qAxis"]
            else:
                self_.qAxis = [NxAxisTicks(**e) for e in kvargs["qAxis"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxCurrentSelectionItem:
    """

    Attributes
    ----------
    qTotal: int
      Number of values in the field.
    qIsNum: bool
      This parameter is displayed if its value is true.
      Is set to true if the field is a numeric.
      This parameter is optional.
    qField: str
      Name of the field that is selected.
    qLocked: bool
      This parameter is displayed if its value is true.
      Is set to true if the field is locked.
      This parameter is optional.
    qOneAndOnlyOne: bool
      This parameter is displayed if its value is true.
      Property that is set to a field. Is set to true if the field cannot be unselected.
      This parameter is optional.
    qTextSearch: str
      Text that was used for the search. This parameter is filled when searching for a value and selecting it.
      This parameter is optional.
    qSelectedCount: int
      Number of values that are selected.
    qSelected: str
      Values that are selected.
    qRangeInfo: list[RangeSelectInfo]
      Information about the range of selected values.
      Is empty if there is no range of selected values.
    qSortIndex: int
      Sort index of the field. Indexing starts from 0.
    qStateCounts: NxStateCounts
      Number of values in a particular state.
    qSelectedFieldSelectionInfo: list[NxFieldSelectionInfo]
      Information about the fields that are selected.
    qNotSelectedFieldSelectionInfo: list[NxFieldSelectionInfo]
      Information about the fields that are not selected.
    qSelectionThreshold: int
      Maximum values to show in the current selections.
      The default value is 6.
    qReadableName: str
      Label that, if defined, is displayed in current selections instead of the actual expression.
    qIsHidden: bool
      Optional parameter. Indicates if the selection is to be hidden in the Selections bar.
      Is set to true if the current selection is hidden.
    """

    qTotal: int = None
    qIsNum: bool = None
    qField: str = None
    qLocked: bool = None
    qOneAndOnlyOne: bool = None
    qTextSearch: str = None
    qSelectedCount: int = None
    qSelected: str = None
    qRangeInfo: list[RangeSelectInfo] = None
    qSortIndex: int = None
    qStateCounts: NxStateCounts = None
    qSelectedFieldSelectionInfo: list[NxFieldSelectionInfo] = None
    qNotSelectedFieldSelectionInfo: list[NxFieldSelectionInfo] = None
    qSelectionThreshold: int = None
    qReadableName: str = None
    qIsHidden: bool = None

    def __init__(self_, **kvargs):
        if "qTotal" in kvargs:
            if type(kvargs["qTotal"]).__name__ is self_.__annotations__["qTotal"]:
                self_.qTotal = kvargs["qTotal"]
            else:
                self_.qTotal = kvargs["qTotal"]
        if "qIsNum" in kvargs:
            if type(kvargs["qIsNum"]).__name__ is self_.__annotations__["qIsNum"]:
                self_.qIsNum = kvargs["qIsNum"]
            else:
                self_.qIsNum = kvargs["qIsNum"]
        if "qField" in kvargs:
            if type(kvargs["qField"]).__name__ is self_.__annotations__["qField"]:
                self_.qField = kvargs["qField"]
            else:
                self_.qField = kvargs["qField"]
        if "qLocked" in kvargs:
            if type(kvargs["qLocked"]).__name__ is self_.__annotations__["qLocked"]:
                self_.qLocked = kvargs["qLocked"]
            else:
                self_.qLocked = kvargs["qLocked"]
        if "qOneAndOnlyOne" in kvargs:
            if (
                type(kvargs["qOneAndOnlyOne"]).__name__
                is self_.__annotations__["qOneAndOnlyOne"]
            ):
                self_.qOneAndOnlyOne = kvargs["qOneAndOnlyOne"]
            else:
                self_.qOneAndOnlyOne = kvargs["qOneAndOnlyOne"]
        if "qTextSearch" in kvargs:
            if (
                type(kvargs["qTextSearch"]).__name__
                is self_.__annotations__["qTextSearch"]
            ):
                self_.qTextSearch = kvargs["qTextSearch"]
            else:
                self_.qTextSearch = kvargs["qTextSearch"]
        if "qSelectedCount" in kvargs:
            if (
                type(kvargs["qSelectedCount"]).__name__
                is self_.__annotations__["qSelectedCount"]
            ):
                self_.qSelectedCount = kvargs["qSelectedCount"]
            else:
                self_.qSelectedCount = kvargs["qSelectedCount"]
        if "qSelected" in kvargs:
            if type(kvargs["qSelected"]).__name__ is self_.__annotations__["qSelected"]:
                self_.qSelected = kvargs["qSelected"]
            else:
                self_.qSelected = kvargs["qSelected"]
        if "qRangeInfo" in kvargs:
            if (
                type(kvargs["qRangeInfo"]).__name__
                is self_.__annotations__["qRangeInfo"]
            ):
                self_.qRangeInfo = kvargs["qRangeInfo"]
            else:
                self_.qRangeInfo = [RangeSelectInfo(**e) for e in kvargs["qRangeInfo"]]
        if "qSortIndex" in kvargs:
            if (
                type(kvargs["qSortIndex"]).__name__
                is self_.__annotations__["qSortIndex"]
            ):
                self_.qSortIndex = kvargs["qSortIndex"]
            else:
                self_.qSortIndex = kvargs["qSortIndex"]
        if "qStateCounts" in kvargs:
            if (
                type(kvargs["qStateCounts"]).__name__
                is self_.__annotations__["qStateCounts"]
            ):
                self_.qStateCounts = kvargs["qStateCounts"]
            else:
                self_.qStateCounts = NxStateCounts(**kvargs["qStateCounts"])
        if "qSelectedFieldSelectionInfo" in kvargs:
            if (
                type(kvargs["qSelectedFieldSelectionInfo"]).__name__
                is self_.__annotations__["qSelectedFieldSelectionInfo"]
            ):
                self_.qSelectedFieldSelectionInfo = kvargs[
                    "qSelectedFieldSelectionInfo"
                ]
            else:
                self_.qSelectedFieldSelectionInfo = [
                    NxFieldSelectionInfo(**e)
                    for e in kvargs["qSelectedFieldSelectionInfo"]
                ]
        if "qNotSelectedFieldSelectionInfo" in kvargs:
            if (
                type(kvargs["qNotSelectedFieldSelectionInfo"]).__name__
                is self_.__annotations__["qNotSelectedFieldSelectionInfo"]
            ):
                self_.qNotSelectedFieldSelectionInfo = kvargs[
                    "qNotSelectedFieldSelectionInfo"
                ]
            else:
                self_.qNotSelectedFieldSelectionInfo = [
                    NxFieldSelectionInfo(**e)
                    for e in kvargs["qNotSelectedFieldSelectionInfo"]
                ]
        if "qSelectionThreshold" in kvargs:
            if (
                type(kvargs["qSelectionThreshold"]).__name__
                is self_.__annotations__["qSelectionThreshold"]
            ):
                self_.qSelectionThreshold = kvargs["qSelectionThreshold"]
            else:
                self_.qSelectionThreshold = kvargs["qSelectionThreshold"]
        if "qReadableName" in kvargs:
            if (
                type(kvargs["qReadableName"]).__name__
                is self_.__annotations__["qReadableName"]
            ):
                self_.qReadableName = kvargs["qReadableName"]
            else:
                self_.qReadableName = kvargs["qReadableName"]
        if "qIsHidden" in kvargs:
            if type(kvargs["qIsHidden"]).__name__ is self_.__annotations__["qIsHidden"]:
                self_.qIsHidden = kvargs["qIsHidden"]
            else:
                self_.qIsHidden = kvargs["qIsHidden"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDerivedFieldsData:
    """

    Attributes
    ----------
    qDerivedDefinitionName: str
      Name of the derived definition.
    qFieldDefs: list[NxDerivedField]
      List of the derived fields.
    qGroupDefs: list[NxDerivedGroup]
      List of the derived groups.
    qTags: list[str]
      List of tags on the derived fields.
    """

    qDerivedDefinitionName: str = None
    qFieldDefs: list[NxDerivedField] = None
    qGroupDefs: list[NxDerivedGroup] = None
    qTags: list[str] = None

    def __init__(self_, **kvargs):
        if "qDerivedDefinitionName" in kvargs:
            if (
                type(kvargs["qDerivedDefinitionName"]).__name__
                is self_.__annotations__["qDerivedDefinitionName"]
            ):
                self_.qDerivedDefinitionName = kvargs["qDerivedDefinitionName"]
            else:
                self_.qDerivedDefinitionName = kvargs["qDerivedDefinitionName"]
        if "qFieldDefs" in kvargs:
            if (
                type(kvargs["qFieldDefs"]).__name__
                is self_.__annotations__["qFieldDefs"]
            ):
                self_.qFieldDefs = kvargs["qFieldDefs"]
            else:
                self_.qFieldDefs = [NxDerivedField(**e) for e in kvargs["qFieldDefs"]]
        if "qGroupDefs" in kvargs:
            if (
                type(kvargs["qGroupDefs"]).__name__
                is self_.__annotations__["qGroupDefs"]
            ):
                self_.qGroupDefs = kvargs["qGroupDefs"]
            else:
                self_.qGroupDefs = [NxDerivedGroup(**e) for e in kvargs["qGroupDefs"]]
        if "qTags" in kvargs:
            if type(kvargs["qTags"]).__name__ is self_.__annotations__["qTags"]:
                self_.qTags = kvargs["qTags"]
            else:
                self_.qTags = kvargs["qTags"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxInlineDimensionDef:
    """

    Attributes
    ----------
    qGrouping: str
      Used to define a cyclic group or drill-down group.
      Default value is no grouping.
      This parameter is optional.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qFieldDefs: list[str]
      Array of field names.
      When creating a grouped dimension, more than one field name is defined.
      This parameter is optional.
    qFieldLabels: list[str]
      Array of field labels.
      This parameter is optional.
    qSortCriterias: list[SortCriteria]
      Defines the sorting criteria in the field.
      Default is to sort by alphabetical order, ascending.
      This parameter is optional.
    qNumberPresentations: list[FieldAttributes]
      Defines the format of the value.
      This parameter is optional.
    qReverseSort: bool
      If set to true, it inverts the sort criteria in the field.
    qActiveField: int
      Index of the active field in a cyclic dimension.
      This parameter is optional. The default value is 0.
      This parameter is used in case of cyclic dimensions ( qGrouping is C).
    qLabelExpression: str
      Label expression.
      This parameter is optional.
    """

    qGrouping: str = None
    qFieldDefs: list[str] = None
    qFieldLabels: list[str] = None
    qSortCriterias: list[SortCriteria] = None
    qNumberPresentations: list[FieldAttributes] = None
    qReverseSort: bool = None
    qActiveField: int = None
    qLabelExpression: str = None

    def __init__(self_, **kvargs):
        if "qGrouping" in kvargs:
            if type(kvargs["qGrouping"]).__name__ is self_.__annotations__["qGrouping"]:
                self_.qGrouping = kvargs["qGrouping"]
            else:
                self_.qGrouping = kvargs["qGrouping"]
        if "qFieldDefs" in kvargs:
            if (
                type(kvargs["qFieldDefs"]).__name__
                is self_.__annotations__["qFieldDefs"]
            ):
                self_.qFieldDefs = kvargs["qFieldDefs"]
            else:
                self_.qFieldDefs = kvargs["qFieldDefs"]
        if "qFieldLabels" in kvargs:
            if (
                type(kvargs["qFieldLabels"]).__name__
                is self_.__annotations__["qFieldLabels"]
            ):
                self_.qFieldLabels = kvargs["qFieldLabels"]
            else:
                self_.qFieldLabels = kvargs["qFieldLabels"]
        if "qSortCriterias" in kvargs:
            if (
                type(kvargs["qSortCriterias"]).__name__
                is self_.__annotations__["qSortCriterias"]
            ):
                self_.qSortCriterias = kvargs["qSortCriterias"]
            else:
                self_.qSortCriterias = [
                    SortCriteria(**e) for e in kvargs["qSortCriterias"]
                ]
        if "qNumberPresentations" in kvargs:
            if (
                type(kvargs["qNumberPresentations"]).__name__
                is self_.__annotations__["qNumberPresentations"]
            ):
                self_.qNumberPresentations = kvargs["qNumberPresentations"]
            else:
                self_.qNumberPresentations = [
                    FieldAttributes(**e) for e in kvargs["qNumberPresentations"]
                ]
        if "qReverseSort" in kvargs:
            if (
                type(kvargs["qReverseSort"]).__name__
                is self_.__annotations__["qReverseSort"]
            ):
                self_.qReverseSort = kvargs["qReverseSort"]
            else:
                self_.qReverseSort = kvargs["qReverseSort"]
        if "qActiveField" in kvargs:
            if (
                type(kvargs["qActiveField"]).__name__
                is self_.__annotations__["qActiveField"]
            ):
                self_.qActiveField = kvargs["qActiveField"]
            else:
                self_.qActiveField = kvargs["qActiveField"]
        if "qLabelExpression" in kvargs:
            if (
                type(kvargs["qLabelExpression"]).__name__
                is self_.__annotations__["qLabelExpression"]
            ):
                self_.qLabelExpression = kvargs["qLabelExpression"]
            else:
                self_.qLabelExpression = kvargs["qLabelExpression"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMeasureInfo:
    """
    Layout for NxInlineMeasureDef.

    Attributes
    ----------
    qFallbackTitle: str
      Corresponds to the label of the measure.
      If the label is not defined then the measure name is used.
    qApprMaxGlyphCount: int
      Length of the longest value in the field.
    qCardinal: int
      Number of distinct field values.
    qSortIndicator: str
      Sort indicator.
      The default value is no sorting.
      This parameter is optional.

      One of:

      • N or NX_SORT_INDICATE_NONE

      • A or NX_SORT_INDICATE_ASC

      • D or NX_SORT_INDICATE_DESC
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    qMin: float
      Lowest value in the range.
    qMax: float
      Highest value in the range.
    qError: NxValidationError
      This parameter is optional.
      Gives information on the error.
    qReverseSort: bool
      If set to true, it inverts the sort criteria in the field.
    qIsAutoFormat: bool
      This parameter is set to true if qNumFormat is set to U (unknown). The engine guesses the type of the field based on the field's expression.
    qAttrExprInfo: list[NxAttrExprInfo]
      List of attribute expressions.
    qAttrDimInfo: list[NxAttrDimInfo]
      List of attribute dimensions.
    qCalcCondMsg: str
      The message displayed if calculation condition is not fulfilled.
    qLibraryId: str
      Refers to a dimension stored in the library.
    qTrendLines: list[NxTrendline]
      Calculated trendlines
    qMiniChart: NxMiniChart
    """

    qFallbackTitle: str = None
    qApprMaxGlyphCount: int = None
    qCardinal: int = None
    qSortIndicator: str = None
    qNumFormat: FieldAttributes = None
    qMin: float = None
    qMax: float = None
    qError: NxValidationError = None
    qReverseSort: bool = None
    qIsAutoFormat: bool = None
    qAttrExprInfo: list[NxAttrExprInfo] = None
    qAttrDimInfo: list[NxAttrDimInfo] = None
    qCalcCondMsg: str = None
    qLibraryId: str = None
    qTrendLines: list[NxTrendline] = None
    qMiniChart: NxMiniChart = None

    def __init__(self_, **kvargs):
        if "qFallbackTitle" in kvargs:
            if (
                type(kvargs["qFallbackTitle"]).__name__
                is self_.__annotations__["qFallbackTitle"]
            ):
                self_.qFallbackTitle = kvargs["qFallbackTitle"]
            else:
                self_.qFallbackTitle = kvargs["qFallbackTitle"]
        if "qApprMaxGlyphCount" in kvargs:
            if (
                type(kvargs["qApprMaxGlyphCount"]).__name__
                is self_.__annotations__["qApprMaxGlyphCount"]
            ):
                self_.qApprMaxGlyphCount = kvargs["qApprMaxGlyphCount"]
            else:
                self_.qApprMaxGlyphCount = kvargs["qApprMaxGlyphCount"]
        if "qCardinal" in kvargs:
            if type(kvargs["qCardinal"]).__name__ is self_.__annotations__["qCardinal"]:
                self_.qCardinal = kvargs["qCardinal"]
            else:
                self_.qCardinal = kvargs["qCardinal"]
        if "qSortIndicator" in kvargs:
            if (
                type(kvargs["qSortIndicator"]).__name__
                is self_.__annotations__["qSortIndicator"]
            ):
                self_.qSortIndicator = kvargs["qSortIndicator"]
            else:
                self_.qSortIndicator = kvargs["qSortIndicator"]
        if "qNumFormat" in kvargs:
            if (
                type(kvargs["qNumFormat"]).__name__
                is self_.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(**kvargs["qNumFormat"])
        if "qMin" in kvargs:
            if type(kvargs["qMin"]).__name__ is self_.__annotations__["qMin"]:
                self_.qMin = kvargs["qMin"]
            else:
                self_.qMin = kvargs["qMin"]
        if "qMax" in kvargs:
            if type(kvargs["qMax"]).__name__ is self_.__annotations__["qMax"]:
                self_.qMax = kvargs["qMax"]
            else:
                self_.qMax = kvargs["qMax"]
        if "qError" in kvargs:
            if type(kvargs["qError"]).__name__ is self_.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(**kvargs["qError"])
        if "qReverseSort" in kvargs:
            if (
                type(kvargs["qReverseSort"]).__name__
                is self_.__annotations__["qReverseSort"]
            ):
                self_.qReverseSort = kvargs["qReverseSort"]
            else:
                self_.qReverseSort = kvargs["qReverseSort"]
        if "qIsAutoFormat" in kvargs:
            if (
                type(kvargs["qIsAutoFormat"]).__name__
                is self_.__annotations__["qIsAutoFormat"]
            ):
                self_.qIsAutoFormat = kvargs["qIsAutoFormat"]
            else:
                self_.qIsAutoFormat = kvargs["qIsAutoFormat"]
        if "qAttrExprInfo" in kvargs:
            if (
                type(kvargs["qAttrExprInfo"]).__name__
                is self_.__annotations__["qAttrExprInfo"]
            ):
                self_.qAttrExprInfo = kvargs["qAttrExprInfo"]
            else:
                self_.qAttrExprInfo = [
                    NxAttrExprInfo(**e) for e in kvargs["qAttrExprInfo"]
                ]
        if "qAttrDimInfo" in kvargs:
            if (
                type(kvargs["qAttrDimInfo"]).__name__
                is self_.__annotations__["qAttrDimInfo"]
            ):
                self_.qAttrDimInfo = kvargs["qAttrDimInfo"]
            else:
                self_.qAttrDimInfo = [
                    NxAttrDimInfo(**e) for e in kvargs["qAttrDimInfo"]
                ]
        if "qCalcCondMsg" in kvargs:
            if (
                type(kvargs["qCalcCondMsg"]).__name__
                is self_.__annotations__["qCalcCondMsg"]
            ):
                self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
            else:
                self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
        if "qLibraryId" in kvargs:
            if (
                type(kvargs["qLibraryId"]).__name__
                is self_.__annotations__["qLibraryId"]
            ):
                self_.qLibraryId = kvargs["qLibraryId"]
            else:
                self_.qLibraryId = kvargs["qLibraryId"]
        if "qTrendLines" in kvargs:
            if (
                type(kvargs["qTrendLines"]).__name__
                is self_.__annotations__["qTrendLines"]
            ):
                self_.qTrendLines = kvargs["qTrendLines"]
            else:
                self_.qTrendLines = [NxTrendline(**e) for e in kvargs["qTrendLines"]]
        if "qMiniChart" in kvargs:
            if (
                type(kvargs["qMiniChart"]).__name__
                is self_.__annotations__["qMiniChart"]
            ):
                self_.qMiniChart = kvargs["qMiniChart"]
            else:
                self_.qMiniChart = NxMiniChart(**kvargs["qMiniChart"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMiniChartData:
    """

    Attributes
    ----------
    qMatrix: list[NxMiniChartRows]
      Array of data.
    qMin: float
    qMax: float
    qError: NxValidationError
      This parameter is optional and is displayed in case of error.
    """

    qMatrix: list[NxMiniChartRows] = None
    qMin: float = None
    qMax: float = None
    qError: NxValidationError = None

    def __init__(self_, **kvargs):
        if "qMatrix" in kvargs:
            if type(kvargs["qMatrix"]).__name__ is self_.__annotations__["qMatrix"]:
                self_.qMatrix = kvargs["qMatrix"]
            else:
                self_.qMatrix = [NxMiniChartRows(**e) for e in kvargs["qMatrix"]]
        if "qMin" in kvargs:
            if type(kvargs["qMin"]).__name__ is self_.__annotations__["qMin"]:
                self_.qMin = kvargs["qMin"]
            else:
                self_.qMin = kvargs["qMin"]
        if "qMax" in kvargs:
            if type(kvargs["qMax"]).__name__ is self_.__annotations__["qMax"]:
                self_.qMax = kvargs["qMax"]
            else:
                self_.qMax = kvargs["qMax"]
        if "qError" in kvargs:
            if type(kvargs["qError"]).__name__ is self_.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(**kvargs["qError"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMiniChartDef:
    """

    Attributes
    ----------
    qDef: str
      Expression or field name.
    qLibraryId: str
      LibraryId for dimension.
    qSortBy: SortCriteria
      Sorting.
    qOtherTotalSpec: OtherTotalSpecProp
    qMaxNumberPoints: int
    qAttributeExpressions: list[NxAttrExprDef]
      List of attribute expressions.
    qNullSuppression: bool
      If set to true, no null values are returned.
    """

    qDef: str = None
    qLibraryId: str = None
    qSortBy: SortCriteria = None
    qOtherTotalSpec: OtherTotalSpecProp = None
    qMaxNumberPoints: int = -1
    qAttributeExpressions: list[NxAttrExprDef] = None
    qNullSuppression: bool = None

    def __init__(self_, **kvargs):
        if "qDef" in kvargs:
            if type(kvargs["qDef"]).__name__ is self_.__annotations__["qDef"]:
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = kvargs["qDef"]
        if "qLibraryId" in kvargs:
            if (
                type(kvargs["qLibraryId"]).__name__
                is self_.__annotations__["qLibraryId"]
            ):
                self_.qLibraryId = kvargs["qLibraryId"]
            else:
                self_.qLibraryId = kvargs["qLibraryId"]
        if "qSortBy" in kvargs:
            if type(kvargs["qSortBy"]).__name__ is self_.__annotations__["qSortBy"]:
                self_.qSortBy = kvargs["qSortBy"]
            else:
                self_.qSortBy = SortCriteria(**kvargs["qSortBy"])
        if "qOtherTotalSpec" in kvargs:
            if (
                type(kvargs["qOtherTotalSpec"]).__name__
                is self_.__annotations__["qOtherTotalSpec"]
            ):
                self_.qOtherTotalSpec = kvargs["qOtherTotalSpec"]
            else:
                self_.qOtherTotalSpec = OtherTotalSpecProp(**kvargs["qOtherTotalSpec"])
        if "qMaxNumberPoints" in kvargs:
            if (
                type(kvargs["qMaxNumberPoints"]).__name__
                is self_.__annotations__["qMaxNumberPoints"]
            ):
                self_.qMaxNumberPoints = kvargs["qMaxNumberPoints"]
            else:
                self_.qMaxNumberPoints = kvargs["qMaxNumberPoints"]
        if "qAttributeExpressions" in kvargs:
            if (
                type(kvargs["qAttributeExpressions"]).__name__
                is self_.__annotations__["qAttributeExpressions"]
            ):
                self_.qAttributeExpressions = kvargs["qAttributeExpressions"]
            else:
                self_.qAttributeExpressions = [
                    NxAttrExprDef(**e) for e in kvargs["qAttributeExpressions"]
                ]
        if "qNullSuppression" in kvargs:
            if (
                type(kvargs["qNullSuppression"]).__name__
                is self_.__annotations__["qNullSuppression"]
            ):
                self_.qNullSuppression = kvargs["qNullSuppression"]
            else:
                self_.qNullSuppression = kvargs["qNullSuppression"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMultiRangeSelectInfo:
    """

    Attributes
    ----------
    qRanges: list[NxRangeSelectInfo]
    qColumnsToSelect: list[int]
    """

    qRanges: list[NxRangeSelectInfo] = None
    qColumnsToSelect: list[int] = None

    def __init__(self_, **kvargs):
        if "qRanges" in kvargs:
            if type(kvargs["qRanges"]).__name__ is self_.__annotations__["qRanges"]:
                self_.qRanges = kvargs["qRanges"]
            else:
                self_.qRanges = [NxRangeSelectInfo(**e) for e in kvargs["qRanges"]]
        if "qColumnsToSelect" in kvargs:
            if (
                type(kvargs["qColumnsToSelect"]).__name__
                is self_.__annotations__["qColumnsToSelect"]
            ):
                self_.qColumnsToSelect = kvargs["qColumnsToSelect"]
            else:
                self_.qColumnsToSelect = kvargs["qColumnsToSelect"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPivotPage:
    """

    Attributes
    ----------
    qLeft: list[NxPivotDimensionCell]
      Information about the left dimension values of a pivot table.
    qTop: list[NxPivotDimensionCell]
      Information about the top dimension values of a pivot table. If there is no top dimension in the pivot table, information about the measures are given.
    qData: list[ArrayOfNxValuePoint]
      Array of data.
    qArea: Rect
      Size and offset of the data in the matrix.
    """

    qLeft: list[NxPivotDimensionCell] = None
    qTop: list[NxPivotDimensionCell] = None
    qData: list[ArrayOfNxValuePoint] = None
    qArea: Rect = None

    def __init__(self_, **kvargs):
        if "qLeft" in kvargs:
            if type(kvargs["qLeft"]).__name__ is self_.__annotations__["qLeft"]:
                self_.qLeft = kvargs["qLeft"]
            else:
                self_.qLeft = [NxPivotDimensionCell(**e) for e in kvargs["qLeft"]]
        if "qTop" in kvargs:
            if type(kvargs["qTop"]).__name__ is self_.__annotations__["qTop"]:
                self_.qTop = kvargs["qTop"]
            else:
                self_.qTop = [NxPivotDimensionCell(**e) for e in kvargs["qTop"]]
        if "qData" in kvargs:
            if type(kvargs["qData"]).__name__ is self_.__annotations__["qData"]:
                self_.qData = kvargs["qData"]
            else:
                self_.qData = [ArrayOfNxValuePoint(**e) for e in kvargs["qData"]]
        if "qArea" in kvargs:
            if type(kvargs["qArea"]).__name__ is self_.__annotations__["qArea"]:
                self_.qArea = kvargs["qArea"]
            else:
                self_.qArea = Rect(**kvargs["qArea"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxStackPage:
    """

    Attributes
    ----------
    qData: list[NxStackedPivotCell]
      Array of data.
    qArea: Rect
      Size and offset of the data in the matrix.
    """

    qData: list[NxStackedPivotCell] = None
    qArea: Rect = None

    def __init__(self_, **kvargs):
        if "qData" in kvargs:
            if type(kvargs["qData"]).__name__ is self_.__annotations__["qData"]:
                self_.qData = kvargs["qData"]
            else:
                self_.qData = [NxStackedPivotCell(**e) for e in kvargs["qData"]]
        if "qArea" in kvargs:
            if type(kvargs["qArea"]).__name__ is self_.__annotations__["qArea"]:
                self_.qArea = kvargs["qArea"]
            else:
                self_.qArea = Rect(**kvargs["qArea"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeDimensionInfo:
    """

    Attributes
    ----------
    qFallbackTitle: str
      Corresponds to the label of the dimension that is selected.
      If the label is not defined then the field name is used.
    qApprMaxGlyphCount: int
      Length of the longest value in the field.
    qCardinal: int
      Number of distinct field values.
    qLocked: bool
      Is set to true if the field is locked.
    qSortIndicator: str
      Sort indicator.
      The default value is no sorting.
      This parameter is optional.

      One of:

      • N or NX_SORT_INDICATE_NONE

      • A or NX_SORT_INDICATE_ASC

      • D or NX_SORT_INDICATE_DESC
    qGroupFallbackTitles: list[str]
      Array of dimension labels.
      Contains the labels of all dimensions in a hierarchy group (for example the labels of all dimensions in a drill down group).
    qGroupPos: int
      Index of the dimension that is currently in use.
      _qGroupPos_ is set to 0 if there are no hierarchical groups (drill-down groups) or cycle groups.
    qStateCounts: NxStateCounts
      Number of values in a particular state.
    qTags: list[str]
      Gives information on a field. For example, it can return the type of the field.
      Examples: key, text, ASCII
    qError: NxValidationError
      This parameter is optional.
      Gives information on the error.
    qDimensionType: str
      Binary format of the field.

      One of:

      • D or NX_DIMENSION_TYPE_DISCRETE

      • N or NX_DIMENSION_TYPE_NUMERIC

      • T or NX_DIMENSION_TYPE_TIME
    qReverseSort: bool
      If set to true, it inverts the sort criteria in the field.
    qGrouping: str
      Defines the grouping.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qIsSemantic: bool
      If set to true, it means that the field is a semantic.
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    qIsAutoFormat: bool
      This parameter is set to true if qNumFormat is set to U (unknown). The engine guesses the type of the field based on the field's definition.
    qGroupFieldDefs: list[str]
      Array of field names.
    qMin: float
      Minimum value.
    qMax: float
      Maximum value.
    qContinuousAxes: bool
      Is continuous axis used.
    qIsCyclic: bool
      Is a cyclic dimension used.
    qDerivedField: bool
      Is derived field is used as a dimension.
    qMeasureInfo: list[NxMeasureInfo]
      A List of measures to be calculated on this TreeDimension.
    qAttrExprInfo: list[NxAttrExprInfo]
      List of attribute expressions.
    qAttrDimInfo: list[NxAttrDimInfo]
      List of attribute dimensions.
    qCalcCondMsg: str
      The message displayed if calculation condition is not fulfilled.
    qIsCalculated: bool
      True if this is a calculated dimension.
    qIsOneAndOnlyOne: bool
      If set to true, it means that the field always has one and only one selected value.
    qCardinalities: NxCardinalities
      Dimension Cardinalities
    qLibraryId: str
      Refers to a dimension stored in the library.
    """

    qFallbackTitle: str = None
    qApprMaxGlyphCount: int = None
    qCardinal: int = None
    qLocked: bool = None
    qSortIndicator: str = None
    qGroupFallbackTitles: list[str] = None
    qGroupPos: int = None
    qStateCounts: NxStateCounts = None
    qTags: list[str] = None
    qError: NxValidationError = None
    qDimensionType: str = None
    qReverseSort: bool = None
    qGrouping: str = None
    qIsSemantic: bool = None
    qNumFormat: FieldAttributes = None
    qIsAutoFormat: bool = None
    qGroupFieldDefs: list[str] = None
    qMin: float = None
    qMax: float = None
    qContinuousAxes: bool = None
    qIsCyclic: bool = None
    qDerivedField: bool = None
    qMeasureInfo: list[NxMeasureInfo] = None
    qAttrExprInfo: list[NxAttrExprInfo] = None
    qAttrDimInfo: list[NxAttrDimInfo] = None
    qCalcCondMsg: str = None
    qIsCalculated: bool = None
    qIsOneAndOnlyOne: bool = None
    qCardinalities: NxCardinalities = None
    qLibraryId: str = None

    def __init__(self_, **kvargs):
        if "qFallbackTitle" in kvargs:
            if (
                type(kvargs["qFallbackTitle"]).__name__
                is self_.__annotations__["qFallbackTitle"]
            ):
                self_.qFallbackTitle = kvargs["qFallbackTitle"]
            else:
                self_.qFallbackTitle = kvargs["qFallbackTitle"]
        if "qApprMaxGlyphCount" in kvargs:
            if (
                type(kvargs["qApprMaxGlyphCount"]).__name__
                is self_.__annotations__["qApprMaxGlyphCount"]
            ):
                self_.qApprMaxGlyphCount = kvargs["qApprMaxGlyphCount"]
            else:
                self_.qApprMaxGlyphCount = kvargs["qApprMaxGlyphCount"]
        if "qCardinal" in kvargs:
            if type(kvargs["qCardinal"]).__name__ is self_.__annotations__["qCardinal"]:
                self_.qCardinal = kvargs["qCardinal"]
            else:
                self_.qCardinal = kvargs["qCardinal"]
        if "qLocked" in kvargs:
            if type(kvargs["qLocked"]).__name__ is self_.__annotations__["qLocked"]:
                self_.qLocked = kvargs["qLocked"]
            else:
                self_.qLocked = kvargs["qLocked"]
        if "qSortIndicator" in kvargs:
            if (
                type(kvargs["qSortIndicator"]).__name__
                is self_.__annotations__["qSortIndicator"]
            ):
                self_.qSortIndicator = kvargs["qSortIndicator"]
            else:
                self_.qSortIndicator = kvargs["qSortIndicator"]
        if "qGroupFallbackTitles" in kvargs:
            if (
                type(kvargs["qGroupFallbackTitles"]).__name__
                is self_.__annotations__["qGroupFallbackTitles"]
            ):
                self_.qGroupFallbackTitles = kvargs["qGroupFallbackTitles"]
            else:
                self_.qGroupFallbackTitles = kvargs["qGroupFallbackTitles"]
        if "qGroupPos" in kvargs:
            if type(kvargs["qGroupPos"]).__name__ is self_.__annotations__["qGroupPos"]:
                self_.qGroupPos = kvargs["qGroupPos"]
            else:
                self_.qGroupPos = kvargs["qGroupPos"]
        if "qStateCounts" in kvargs:
            if (
                type(kvargs["qStateCounts"]).__name__
                is self_.__annotations__["qStateCounts"]
            ):
                self_.qStateCounts = kvargs["qStateCounts"]
            else:
                self_.qStateCounts = NxStateCounts(**kvargs["qStateCounts"])
        if "qTags" in kvargs:
            if type(kvargs["qTags"]).__name__ is self_.__annotations__["qTags"]:
                self_.qTags = kvargs["qTags"]
            else:
                self_.qTags = kvargs["qTags"]
        if "qError" in kvargs:
            if type(kvargs["qError"]).__name__ is self_.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(**kvargs["qError"])
        if "qDimensionType" in kvargs:
            if (
                type(kvargs["qDimensionType"]).__name__
                is self_.__annotations__["qDimensionType"]
            ):
                self_.qDimensionType = kvargs["qDimensionType"]
            else:
                self_.qDimensionType = kvargs["qDimensionType"]
        if "qReverseSort" in kvargs:
            if (
                type(kvargs["qReverseSort"]).__name__
                is self_.__annotations__["qReverseSort"]
            ):
                self_.qReverseSort = kvargs["qReverseSort"]
            else:
                self_.qReverseSort = kvargs["qReverseSort"]
        if "qGrouping" in kvargs:
            if type(kvargs["qGrouping"]).__name__ is self_.__annotations__["qGrouping"]:
                self_.qGrouping = kvargs["qGrouping"]
            else:
                self_.qGrouping = kvargs["qGrouping"]
        if "qIsSemantic" in kvargs:
            if (
                type(kvargs["qIsSemantic"]).__name__
                is self_.__annotations__["qIsSemantic"]
            ):
                self_.qIsSemantic = kvargs["qIsSemantic"]
            else:
                self_.qIsSemantic = kvargs["qIsSemantic"]
        if "qNumFormat" in kvargs:
            if (
                type(kvargs["qNumFormat"]).__name__
                is self_.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(**kvargs["qNumFormat"])
        if "qIsAutoFormat" in kvargs:
            if (
                type(kvargs["qIsAutoFormat"]).__name__
                is self_.__annotations__["qIsAutoFormat"]
            ):
                self_.qIsAutoFormat = kvargs["qIsAutoFormat"]
            else:
                self_.qIsAutoFormat = kvargs["qIsAutoFormat"]
        if "qGroupFieldDefs" in kvargs:
            if (
                type(kvargs["qGroupFieldDefs"]).__name__
                is self_.__annotations__["qGroupFieldDefs"]
            ):
                self_.qGroupFieldDefs = kvargs["qGroupFieldDefs"]
            else:
                self_.qGroupFieldDefs = kvargs["qGroupFieldDefs"]
        if "qMin" in kvargs:
            if type(kvargs["qMin"]).__name__ is self_.__annotations__["qMin"]:
                self_.qMin = kvargs["qMin"]
            else:
                self_.qMin = kvargs["qMin"]
        if "qMax" in kvargs:
            if type(kvargs["qMax"]).__name__ is self_.__annotations__["qMax"]:
                self_.qMax = kvargs["qMax"]
            else:
                self_.qMax = kvargs["qMax"]
        if "qContinuousAxes" in kvargs:
            if (
                type(kvargs["qContinuousAxes"]).__name__
                is self_.__annotations__["qContinuousAxes"]
            ):
                self_.qContinuousAxes = kvargs["qContinuousAxes"]
            else:
                self_.qContinuousAxes = kvargs["qContinuousAxes"]
        if "qIsCyclic" in kvargs:
            if type(kvargs["qIsCyclic"]).__name__ is self_.__annotations__["qIsCyclic"]:
                self_.qIsCyclic = kvargs["qIsCyclic"]
            else:
                self_.qIsCyclic = kvargs["qIsCyclic"]
        if "qDerivedField" in kvargs:
            if (
                type(kvargs["qDerivedField"]).__name__
                is self_.__annotations__["qDerivedField"]
            ):
                self_.qDerivedField = kvargs["qDerivedField"]
            else:
                self_.qDerivedField = kvargs["qDerivedField"]
        if "qMeasureInfo" in kvargs:
            if (
                type(kvargs["qMeasureInfo"]).__name__
                is self_.__annotations__["qMeasureInfo"]
            ):
                self_.qMeasureInfo = kvargs["qMeasureInfo"]
            else:
                self_.qMeasureInfo = [
                    NxMeasureInfo(**e) for e in kvargs["qMeasureInfo"]
                ]
        if "qAttrExprInfo" in kvargs:
            if (
                type(kvargs["qAttrExprInfo"]).__name__
                is self_.__annotations__["qAttrExprInfo"]
            ):
                self_.qAttrExprInfo = kvargs["qAttrExprInfo"]
            else:
                self_.qAttrExprInfo = [
                    NxAttrExprInfo(**e) for e in kvargs["qAttrExprInfo"]
                ]
        if "qAttrDimInfo" in kvargs:
            if (
                type(kvargs["qAttrDimInfo"]).__name__
                is self_.__annotations__["qAttrDimInfo"]
            ):
                self_.qAttrDimInfo = kvargs["qAttrDimInfo"]
            else:
                self_.qAttrDimInfo = [
                    NxAttrDimInfo(**e) for e in kvargs["qAttrDimInfo"]
                ]
        if "qCalcCondMsg" in kvargs:
            if (
                type(kvargs["qCalcCondMsg"]).__name__
                is self_.__annotations__["qCalcCondMsg"]
            ):
                self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
            else:
                self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
        if "qIsCalculated" in kvargs:
            if (
                type(kvargs["qIsCalculated"]).__name__
                is self_.__annotations__["qIsCalculated"]
            ):
                self_.qIsCalculated = kvargs["qIsCalculated"]
            else:
                self_.qIsCalculated = kvargs["qIsCalculated"]
        if "qIsOneAndOnlyOne" in kvargs:
            if (
                type(kvargs["qIsOneAndOnlyOne"]).__name__
                is self_.__annotations__["qIsOneAndOnlyOne"]
            ):
                self_.qIsOneAndOnlyOne = kvargs["qIsOneAndOnlyOne"]
            else:
                self_.qIsOneAndOnlyOne = kvargs["qIsOneAndOnlyOne"]
        if "qCardinalities" in kvargs:
            if (
                type(kvargs["qCardinalities"]).__name__
                is self_.__annotations__["qCardinalities"]
            ):
                self_.qCardinalities = kvargs["qCardinalities"]
            else:
                self_.qCardinalities = NxCardinalities(**kvargs["qCardinalities"])
        if "qLibraryId" in kvargs:
            if (
                type(kvargs["qLibraryId"]).__name__
                is self_.__annotations__["qLibraryId"]
            ):
                self_.qLibraryId = kvargs["qLibraryId"]
            else:
                self_.qLibraryId = kvargs["qLibraryId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeMultiRangeSelectInfo:
    """

    Attributes
    ----------
    qRanges: list[NxTreeRangeSelectInfo]
      An array of Ranges.
    """

    qRanges: list[NxTreeRangeSelectInfo] = None

    def __init__(self_, **kvargs):
        if "qRanges" in kvargs:
            if type(kvargs["qRanges"]).__name__ is self_.__annotations__["qRanges"]:
                self_.qRanges = kvargs["qRanges"]
            else:
                self_.qRanges = [NxTreeRangeSelectInfo(**e) for e in kvargs["qRanges"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeNode:
    """
    Represents a dimension in the tree.

    Attributes
    ----------
    qText: str
      The text version of the value, if available.
    qValue: float
      Value of the cell.
      Is set to NaN , if the value is not a number.
    qElemNo: int
      Element number.
    qGroupPos: int
      The position of this node inside it's group in the complete tree, i.e. Not dependant om what part is fetched.
    qGroupSize: int
      Nbr of nodes connected to this node on the next level of the tree. Not dependant on what part is fetched.
    qRow: int
      Row index in the data matrix.
      The indexing starts from 0.
    qType: str
      Type of the cell.

      One of:

      • V or NX_DIM_CELL_VALUE

      • E or NX_DIM_CELL_EMPTY

      • N or NX_DIM_CELL_NORMAL

      • T or NX_DIM_CELL_TOTAL

      • O or NX_DIM_CELL_OTHER

      • A or NX_DIM_CELL_AGGR

      • P or NX_DIM_CELL_PSEUDO

      • R or NX_DIM_CELL_ROOT

      • U or NX_DIM_CELL_NULL

      • G or NX_DIM_CELL_GENERATED
    qValues: list[NxTreeValue]
      The measures for this node.
    qNodes: list[NxTreeNode]
      The children of this node in the fetched tree structure.
    qAttrExps: NxAttributeExpressionValues
      Attribute expression values.
    qAttrDims: NxAttributeDimValues
      Attribute dimension values.
    qMaxPos: list[float]
      Total of the positive values in the current group of cells.
    qMinNeg: list[float]
      Total of the negative values in the current group of cells.
    qCanExpand: bool
      If set to true, it means that the cell can be expanded.
      This parameter is not returned if it is set to false.
    qCanCollapse: bool
      If set to true, it means that the cell can be collapsed.
      This parameter is not returned if it is set to false.
    qState: str
      Selection State of the value.
      The default state for a measure is L(Locked).

      One of:

      • L or LOCKED

      • S or SELECTED

      • O or OPTION

      • D or DESELECTED

      • A or ALTERNATIVE

      • X or EXCLUDED

      • XS or EXCL_SELECTED

      • XL or EXCL_LOCKED

      • NSTATES
    qTreePath: list[int]
      The GroupPos of all prior nodes connected to this one, one position for each level of the tree.
      If this node is attached directly to the root, this array is empty.
    """

    qText: str = None
    qValue: float = None
    qElemNo: int = None
    qGroupPos: int = None
    qGroupSize: int = None
    qRow: int = None
    qType: str = None
    qValues: list[NxTreeValue] = None
    qNodes: list[NxTreeNode] = None
    qAttrExps: NxAttributeExpressionValues = None
    qAttrDims: NxAttributeDimValues = None
    qMaxPos: list[float] = None
    qMinNeg: list[float] = None
    qCanExpand: bool = None
    qCanCollapse: bool = None
    qState: str = None
    qTreePath: list[int] = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qValue" in kvargs:
            if type(kvargs["qValue"]).__name__ is self_.__annotations__["qValue"]:
                self_.qValue = kvargs["qValue"]
            else:
                self_.qValue = kvargs["qValue"]
        if "qElemNo" in kvargs:
            if type(kvargs["qElemNo"]).__name__ is self_.__annotations__["qElemNo"]:
                self_.qElemNo = kvargs["qElemNo"]
            else:
                self_.qElemNo = kvargs["qElemNo"]
        if "qGroupPos" in kvargs:
            if type(kvargs["qGroupPos"]).__name__ is self_.__annotations__["qGroupPos"]:
                self_.qGroupPos = kvargs["qGroupPos"]
            else:
                self_.qGroupPos = kvargs["qGroupPos"]
        if "qGroupSize" in kvargs:
            if (
                type(kvargs["qGroupSize"]).__name__
                is self_.__annotations__["qGroupSize"]
            ):
                self_.qGroupSize = kvargs["qGroupSize"]
            else:
                self_.qGroupSize = kvargs["qGroupSize"]
        if "qRow" in kvargs:
            if type(kvargs["qRow"]).__name__ is self_.__annotations__["qRow"]:
                self_.qRow = kvargs["qRow"]
            else:
                self_.qRow = kvargs["qRow"]
        if "qType" in kvargs:
            if type(kvargs["qType"]).__name__ is self_.__annotations__["qType"]:
                self_.qType = kvargs["qType"]
            else:
                self_.qType = kvargs["qType"]
        if "qValues" in kvargs:
            if type(kvargs["qValues"]).__name__ is self_.__annotations__["qValues"]:
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [NxTreeValue(**e) for e in kvargs["qValues"]]
        if "qNodes" in kvargs:
            if type(kvargs["qNodes"]).__name__ is self_.__annotations__["qNodes"]:
                self_.qNodes = kvargs["qNodes"]
            else:
                self_.qNodes = [NxTreeNode(**e) for e in kvargs["qNodes"]]
        if "qAttrExps" in kvargs:
            if type(kvargs["qAttrExps"]).__name__ is self_.__annotations__["qAttrExps"]:
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(**kvargs["qAttrExps"])
        if "qAttrDims" in kvargs:
            if type(kvargs["qAttrDims"]).__name__ is self_.__annotations__["qAttrDims"]:
                self_.qAttrDims = kvargs["qAttrDims"]
            else:
                self_.qAttrDims = NxAttributeDimValues(**kvargs["qAttrDims"])
        if "qMaxPos" in kvargs:
            if type(kvargs["qMaxPos"]).__name__ is self_.__annotations__["qMaxPos"]:
                self_.qMaxPos = kvargs["qMaxPos"]
            else:
                self_.qMaxPos = kvargs["qMaxPos"]
        if "qMinNeg" in kvargs:
            if type(kvargs["qMinNeg"]).__name__ is self_.__annotations__["qMinNeg"]:
                self_.qMinNeg = kvargs["qMinNeg"]
            else:
                self_.qMinNeg = kvargs["qMinNeg"]
        if "qCanExpand" in kvargs:
            if (
                type(kvargs["qCanExpand"]).__name__
                is self_.__annotations__["qCanExpand"]
            ):
                self_.qCanExpand = kvargs["qCanExpand"]
            else:
                self_.qCanExpand = kvargs["qCanExpand"]
        if "qCanCollapse" in kvargs:
            if (
                type(kvargs["qCanCollapse"]).__name__
                is self_.__annotations__["qCanCollapse"]
            ):
                self_.qCanCollapse = kvargs["qCanCollapse"]
            else:
                self_.qCanCollapse = kvargs["qCanCollapse"]
        if "qState" in kvargs:
            if type(kvargs["qState"]).__name__ is self_.__annotations__["qState"]:
                self_.qState = kvargs["qState"]
            else:
                self_.qState = kvargs["qState"]
        if "qTreePath" in kvargs:
            if type(kvargs["qTreePath"]).__name__ is self_.__annotations__["qTreePath"]:
                self_.qTreePath = kvargs["qTreePath"]
            else:
                self_.qTreePath = kvargs["qTreePath"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchAssociationResult:
    """

    Attributes
    ----------
    qFieldNames: list[str]
      List of the fields that contains search associations.
    qSearchTerms: list[str]
      List of the search terms.
    qFieldDictionaries: list[SearchFieldDictionary]
      Information about the fields containing search hits.
    qSearchTermsMatched: list[SearchMatchCombinations]
      List of search results.
      The maximum number of search results in this list is set by qPage/qCount .
    qTotalSearchResults: int
      Total number of search results.
      This number is not limited by qPage/qCount .
    """

    qFieldNames: list[str] = None
    qSearchTerms: list[str] = None
    qFieldDictionaries: list[SearchFieldDictionary] = None
    qSearchTermsMatched: list[SearchMatchCombinations] = None
    qTotalSearchResults: int = None

    def __init__(self_, **kvargs):
        if "qFieldNames" in kvargs:
            if (
                type(kvargs["qFieldNames"]).__name__
                is self_.__annotations__["qFieldNames"]
            ):
                self_.qFieldNames = kvargs["qFieldNames"]
            else:
                self_.qFieldNames = kvargs["qFieldNames"]
        if "qSearchTerms" in kvargs:
            if (
                type(kvargs["qSearchTerms"]).__name__
                is self_.__annotations__["qSearchTerms"]
            ):
                self_.qSearchTerms = kvargs["qSearchTerms"]
            else:
                self_.qSearchTerms = kvargs["qSearchTerms"]
        if "qFieldDictionaries" in kvargs:
            if (
                type(kvargs["qFieldDictionaries"]).__name__
                is self_.__annotations__["qFieldDictionaries"]
            ):
                self_.qFieldDictionaries = kvargs["qFieldDictionaries"]
            else:
                self_.qFieldDictionaries = [
                    SearchFieldDictionary(**e) for e in kvargs["qFieldDictionaries"]
                ]
        if "qSearchTermsMatched" in kvargs:
            if (
                type(kvargs["qSearchTermsMatched"]).__name__
                is self_.__annotations__["qSearchTermsMatched"]
            ):
                self_.qSearchTermsMatched = kvargs["qSearchTermsMatched"]
            else:
                self_.qSearchTermsMatched = [
                    SearchMatchCombinations(**e) for e in kvargs["qSearchTermsMatched"]
                ]
        if "qTotalSearchResults" in kvargs:
            if (
                type(kvargs["qTotalSearchResults"]).__name__
                is self_.__annotations__["qTotalSearchResults"]
            ):
                self_.qTotalSearchResults = kvargs["qTotalSearchResults"]
            else:
                self_.qTotalSearchResults = kvargs["qTotalSearchResults"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroup:
    """

    Attributes
    ----------
    qId: int
      Identifier of the search group.
    qGroupType: str
      Type of the search group.

      One of:

      • DatasetType or DATASET_GROUP

      • GenericObjectsType or GENERIC_OBJECTS_GROUP
    qSearchTermsMatched: list[int]
      Indexes of the search terms that are included in the group. These search terms are related to the list of terms defined in SearchResult.qSearchTerms .
    qTotalNumberOfItems: int
      Total number of distinct items in the search group.
    qItems: list[SearchGroupItem]
      List of items in the search group.
      The group items are numbered from the value of SearchGroupOptions.qOffset to the value of SearchGroupOptions.qOffset \+ SearchGroupOptions.qCount
    """

    qId: int = None
    qGroupType: str = None
    qSearchTermsMatched: list[int] = None
    qTotalNumberOfItems: int = None
    qItems: list[SearchGroupItem] = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs:
            if type(kvargs["qId"]).__name__ is self_.__annotations__["qId"]:
                self_.qId = kvargs["qId"]
            else:
                self_.qId = kvargs["qId"]
        if "qGroupType" in kvargs:
            if (
                type(kvargs["qGroupType"]).__name__
                is self_.__annotations__["qGroupType"]
            ):
                self_.qGroupType = kvargs["qGroupType"]
            else:
                self_.qGroupType = kvargs["qGroupType"]
        if "qSearchTermsMatched" in kvargs:
            if (
                type(kvargs["qSearchTermsMatched"]).__name__
                is self_.__annotations__["qSearchTermsMatched"]
            ):
                self_.qSearchTermsMatched = kvargs["qSearchTermsMatched"]
            else:
                self_.qSearchTermsMatched = kvargs["qSearchTermsMatched"]
        if "qTotalNumberOfItems" in kvargs:
            if (
                type(kvargs["qTotalNumberOfItems"]).__name__
                is self_.__annotations__["qTotalNumberOfItems"]
            ):
                self_.qTotalNumberOfItems = kvargs["qTotalNumberOfItems"]
            else:
                self_.qTotalNumberOfItems = kvargs["qTotalNumberOfItems"]
        if "qItems" in kvargs:
            if type(kvargs["qItems"]).__name__ is self_.__annotations__["qItems"]:
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [SearchGroupItem(**e) for e in kvargs["qItems"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchResult:
    """

    Attributes
    ----------
    qSearchTerms: list[str]
      List of the search terms.
    qTotalNumberOfGroups: int
      Total number of groups.
    qSearchGroupArray: list[SearchGroup]
      List of search groups.
      The groups are numbered from the value of SearchPage.qOffset to the value of SearchPage.qOffset + SearchPage.qCount .
    """

    qSearchTerms: list[str] = None
    qTotalNumberOfGroups: int = None
    qSearchGroupArray: list[SearchGroup] = None

    def __init__(self_, **kvargs):
        if "qSearchTerms" in kvargs:
            if (
                type(kvargs["qSearchTerms"]).__name__
                is self_.__annotations__["qSearchTerms"]
            ):
                self_.qSearchTerms = kvargs["qSearchTerms"]
            else:
                self_.qSearchTerms = kvargs["qSearchTerms"]
        if "qTotalNumberOfGroups" in kvargs:
            if (
                type(kvargs["qTotalNumberOfGroups"]).__name__
                is self_.__annotations__["qTotalNumberOfGroups"]
            ):
                self_.qTotalNumberOfGroups = kvargs["qTotalNumberOfGroups"]
            else:
                self_.qTotalNumberOfGroups = kvargs["qTotalNumberOfGroups"]
        if "qSearchGroupArray" in kvargs:
            if (
                type(kvargs["qSearchGroupArray"]).__name__
                is self_.__annotations__["qSearchGroupArray"]
            ):
                self_.qSearchGroupArray = kvargs["qSearchGroupArray"]
            else:
                self_.qSearchGroupArray = [
                    SearchGroup(**e) for e in kvargs["qSearchGroupArray"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SelectionObject:
    """
    Indicates which selections are currently applied. It gives the current selections. Is the layout for SelectionObjectDef.

    Attributes
    ----------
    qBackCount: int
      Number of steps back.
    qForwardCount: int
      Number of steps forward.
    qSelections: list[NxCurrentSelectionItem]
      Lists the fields that are selected.
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    """

    qBackCount: int = None
    qForwardCount: int = None
    qSelections: list[NxCurrentSelectionItem] = None
    qStateName: str = None

    def __init__(self_, **kvargs):
        if "qBackCount" in kvargs:
            if (
                type(kvargs["qBackCount"]).__name__
                is self_.__annotations__["qBackCount"]
            ):
                self_.qBackCount = kvargs["qBackCount"]
            else:
                self_.qBackCount = kvargs["qBackCount"]
        if "qForwardCount" in kvargs:
            if (
                type(kvargs["qForwardCount"]).__name__
                is self_.__annotations__["qForwardCount"]
            ):
                self_.qForwardCount = kvargs["qForwardCount"]
            else:
                self_.qForwardCount = kvargs["qForwardCount"]
        if "qSelections" in kvargs:
            if (
                type(kvargs["qSelections"]).__name__
                is self_.__annotations__["qSelections"]
            ):
                self_.qSelections = kvargs["qSelections"]
            else:
                self_.qSelections = [
                    NxCurrentSelectionItem(**e) for e in kvargs["qSelections"]
                ]
        if "qStateName" in kvargs:
            if (
                type(kvargs["qStateName"]).__name__
                is self_.__annotations__["qStateName"]
            ):
                self_.qStateName = kvargs["qStateName"]
            else:
                self_.qStateName = kvargs["qStateName"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableProfilingData:
    """

    Attributes
    ----------
    qNoOfRows: int
      Number of rows in the table.
    qFieldProfiling: list[FieldInTableProfilingData]
      Field values profiling info
    """

    qNoOfRows: int = None
    qFieldProfiling: list[FieldInTableProfilingData] = None

    def __init__(self_, **kvargs):
        if "qNoOfRows" in kvargs:
            if type(kvargs["qNoOfRows"]).__name__ is self_.__annotations__["qNoOfRows"]:
                self_.qNoOfRows = kvargs["qNoOfRows"]
            else:
                self_.qNoOfRows = kvargs["qNoOfRows"]
        if "qFieldProfiling" in kvargs:
            if (
                type(kvargs["qFieldProfiling"]).__name__
                is self_.__annotations__["qFieldProfiling"]
            ):
                self_.qFieldProfiling = kvargs["qFieldProfiling"]
            else:
                self_.qFieldProfiling = [
                    FieldInTableProfilingData(**e) for e in kvargs["qFieldProfiling"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableRecord:
    """

    Attributes
    ----------
    qName: str
      Name of the table.
    qLoose: bool
      This property is set to true if the table is loose.
    qNoOfRows: int
      Number of rows in the table.
    qFields: list[FieldInTableData]
      Information about the fields in the table.
    qPos: Point
      Information about the position of the table.
    qComment: str
      Comment related to the table.
    qIsDirectDiscovery: bool
      If set to true, Direct Discovery is used.
      Direct Discovery fields are not loaded into memory and remain in the external database.
    qIsSynthetic: bool
      This property is set to true if the table contains a synthetic key.
    qTableTags: list[str]
      List of tags related to the table.
    qProfilingData: TableProfilingData
      Profiling information of the table.
    """

    qName: str = None
    qLoose: bool = None
    qNoOfRows: int = None
    qFields: list[FieldInTableData] = None
    qPos: Point = None
    qComment: str = None
    qIsDirectDiscovery: bool = None
    qIsSynthetic: bool = None
    qTableTags: list[str] = None
    qProfilingData: TableProfilingData = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qLoose" in kvargs:
            if type(kvargs["qLoose"]).__name__ is self_.__annotations__["qLoose"]:
                self_.qLoose = kvargs["qLoose"]
            else:
                self_.qLoose = kvargs["qLoose"]
        if "qNoOfRows" in kvargs:
            if type(kvargs["qNoOfRows"]).__name__ is self_.__annotations__["qNoOfRows"]:
                self_.qNoOfRows = kvargs["qNoOfRows"]
            else:
                self_.qNoOfRows = kvargs["qNoOfRows"]
        if "qFields" in kvargs:
            if type(kvargs["qFields"]).__name__ is self_.__annotations__["qFields"]:
                self_.qFields = kvargs["qFields"]
            else:
                self_.qFields = [FieldInTableData(**e) for e in kvargs["qFields"]]
        if "qPos" in kvargs:
            if type(kvargs["qPos"]).__name__ is self_.__annotations__["qPos"]:
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = Point(**kvargs["qPos"])
        if "qComment" in kvargs:
            if type(kvargs["qComment"]).__name__ is self_.__annotations__["qComment"]:
                self_.qComment = kvargs["qComment"]
            else:
                self_.qComment = kvargs["qComment"]
        if "qIsDirectDiscovery" in kvargs:
            if (
                type(kvargs["qIsDirectDiscovery"]).__name__
                is self_.__annotations__["qIsDirectDiscovery"]
            ):
                self_.qIsDirectDiscovery = kvargs["qIsDirectDiscovery"]
            else:
                self_.qIsDirectDiscovery = kvargs["qIsDirectDiscovery"]
        if "qIsSynthetic" in kvargs:
            if (
                type(kvargs["qIsSynthetic"]).__name__
                is self_.__annotations__["qIsSynthetic"]
            ):
                self_.qIsSynthetic = kvargs["qIsSynthetic"]
            else:
                self_.qIsSynthetic = kvargs["qIsSynthetic"]
        if "qTableTags" in kvargs:
            if (
                type(kvargs["qTableTags"]).__name__
                is self_.__annotations__["qTableTags"]
            ):
                self_.qTableTags = kvargs["qTableTags"]
            else:
                self_.qTableTags = kvargs["qTableTags"]
        if "qProfilingData" in kvargs:
            if (
                type(kvargs["qProfilingData"]).__name__
                is self_.__annotations__["qProfilingData"]
            ):
                self_.qProfilingData = kvargs["qProfilingData"]
            else:
                self_.qProfilingData = TableProfilingData(**kvargs["qProfilingData"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableViewCtlSaveInfo:
    """

    Attributes
    ----------
    qInternalView: TableViewSaveInfo
      Internal view mode.
    qSourceView: TableViewSaveInfo
      Source view mode.
    """

    qInternalView: TableViewSaveInfo = None
    qSourceView: TableViewSaveInfo = None

    def __init__(self_, **kvargs):
        if "qInternalView" in kvargs:
            if (
                type(kvargs["qInternalView"]).__name__
                is self_.__annotations__["qInternalView"]
            ):
                self_.qInternalView = kvargs["qInternalView"]
            else:
                self_.qInternalView = TableViewSaveInfo(**kvargs["qInternalView"])
        if "qSourceView" in kvargs:
            if (
                type(kvargs["qSourceView"]).__name__
                is self_.__annotations__["qSourceView"]
            ):
                self_.qSourceView = kvargs["qSourceView"]
            else:
                self_.qSourceView = TableViewSaveInfo(**kvargs["qSourceView"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableViewDlgSaveInfo:
    """

    Attributes
    ----------
    qPos: Rect
      Information about the position of the dialog window.
      Not used in Qlik Sense.
    qCtlInfo: TableViewCtlSaveInfo
      Set of data for internal and source view modes.
    qMode: int
      View mode to display when opening Qlik Sense data model viewer.
      One of:

      • 0 for internal view mode.

      • 1 for source view mode.
    """

    qPos: Rect = None
    qCtlInfo: TableViewCtlSaveInfo = None
    qMode: int = None

    def __init__(self_, **kvargs):
        if "qPos" in kvargs:
            if type(kvargs["qPos"]).__name__ is self_.__annotations__["qPos"]:
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = Rect(**kvargs["qPos"])
        if "qCtlInfo" in kvargs:
            if type(kvargs["qCtlInfo"]).__name__ is self_.__annotations__["qCtlInfo"]:
                self_.qCtlInfo = kvargs["qCtlInfo"]
            else:
                self_.qCtlInfo = TableViewCtlSaveInfo(**kvargs["qCtlInfo"])
        if "qMode" in kvargs:
            if type(kvargs["qMode"]).__name__ is self_.__annotations__["qMode"]:
                self_.qMode = kvargs["qMode"]
            else:
                self_.qMode = kvargs["qMode"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TreeData:
    """
    Renders the properties of a TreeData object. Is the layout for TreeDataDef.
    For more information about the definition of TreeData, see Generic object.
    To retrieve data from the TreeData object, use the method called GetHyperCubeTreeData.

    Attributes
    ----------
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    qNodesOnDim: list[int]
      The total number of nodes on each dimension.
    qError: NxValidationError
      This parameter is optional and is displayed in case of error.
    qDimensionInfo: list[NxTreeDimensionInfo]
      Information on the dimension.
    qEffectiveInterColumnSortOrder: list[int]
      Defines the order of the dimenion levels/columns in the TreeData object.
      Column numbers are separated by a comma.
      Example: [1,0,2] means that the first level in the tree structure is dimension 1, followed by dimension 0 and dimension 2.
    qHasOtherValues: bool
      True if other row exists.
    qTitle: str
      Title of the TreeData object, for example the title of a chart.
    qLastExpandedPos: NxCellPosition
      Position of the last expended cell.
      This property is optional.
    qCalcCondMsg: str
      The message displayed if calculation condition is not fulfilled.
    qTreeDataPages: list[NxTreeNode]
      Set of data.
      Is empty if nothing has been defined in qInitialDataFetch in TreeDataDef.
    qMeasureInfo: list[NxMeasureInfo]
      Information on the measures calculated on the whole tree.
    """

    qStateName: str = None
    qNodesOnDim: list[int] = None
    qError: NxValidationError = None
    qDimensionInfo: list[NxTreeDimensionInfo] = None
    qEffectiveInterColumnSortOrder: list[int] = None
    qHasOtherValues: bool = None
    qTitle: str = None
    qLastExpandedPos: NxCellPosition = None
    qCalcCondMsg: str = None
    qTreeDataPages: list[NxTreeNode] = None
    qMeasureInfo: list[NxMeasureInfo] = None

    def __init__(self_, **kvargs):
        if "qStateName" in kvargs:
            if (
                type(kvargs["qStateName"]).__name__
                is self_.__annotations__["qStateName"]
            ):
                self_.qStateName = kvargs["qStateName"]
            else:
                self_.qStateName = kvargs["qStateName"]
        if "qNodesOnDim" in kvargs:
            if (
                type(kvargs["qNodesOnDim"]).__name__
                is self_.__annotations__["qNodesOnDim"]
            ):
                self_.qNodesOnDim = kvargs["qNodesOnDim"]
            else:
                self_.qNodesOnDim = kvargs["qNodesOnDim"]
        if "qError" in kvargs:
            if type(kvargs["qError"]).__name__ is self_.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(**kvargs["qError"])
        if "qDimensionInfo" in kvargs:
            if (
                type(kvargs["qDimensionInfo"]).__name__
                is self_.__annotations__["qDimensionInfo"]
            ):
                self_.qDimensionInfo = kvargs["qDimensionInfo"]
            else:
                self_.qDimensionInfo = [
                    NxTreeDimensionInfo(**e) for e in kvargs["qDimensionInfo"]
                ]
        if "qEffectiveInterColumnSortOrder" in kvargs:
            if (
                type(kvargs["qEffectiveInterColumnSortOrder"]).__name__
                is self_.__annotations__["qEffectiveInterColumnSortOrder"]
            ):
                self_.qEffectiveInterColumnSortOrder = kvargs[
                    "qEffectiveInterColumnSortOrder"
                ]
            else:
                self_.qEffectiveInterColumnSortOrder = kvargs[
                    "qEffectiveInterColumnSortOrder"
                ]
        if "qHasOtherValues" in kvargs:
            if (
                type(kvargs["qHasOtherValues"]).__name__
                is self_.__annotations__["qHasOtherValues"]
            ):
                self_.qHasOtherValues = kvargs["qHasOtherValues"]
            else:
                self_.qHasOtherValues = kvargs["qHasOtherValues"]
        if "qTitle" in kvargs:
            if type(kvargs["qTitle"]).__name__ is self_.__annotations__["qTitle"]:
                self_.qTitle = kvargs["qTitle"]
            else:
                self_.qTitle = kvargs["qTitle"]
        if "qLastExpandedPos" in kvargs:
            if (
                type(kvargs["qLastExpandedPos"]).__name__
                is self_.__annotations__["qLastExpandedPos"]
            ):
                self_.qLastExpandedPos = kvargs["qLastExpandedPos"]
            else:
                self_.qLastExpandedPos = NxCellPosition(**kvargs["qLastExpandedPos"])
        if "qCalcCondMsg" in kvargs:
            if (
                type(kvargs["qCalcCondMsg"]).__name__
                is self_.__annotations__["qCalcCondMsg"]
            ):
                self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
            else:
                self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
        if "qTreeDataPages" in kvargs:
            if (
                type(kvargs["qTreeDataPages"]).__name__
                is self_.__annotations__["qTreeDataPages"]
            ):
                self_.qTreeDataPages = kvargs["qTreeDataPages"]
            else:
                self_.qTreeDataPages = [
                    NxTreeNode(**e) for e in kvargs["qTreeDataPages"]
                ]
        if "qMeasureInfo" in kvargs:
            if (
                type(kvargs["qMeasureInfo"]).__name__
                is self_.__annotations__["qMeasureInfo"]
            ):
                self_.qMeasureInfo = kvargs["qMeasureInfo"]
            else:
                self_.qMeasureInfo = [
                    NxMeasureInfo(**e) for e in kvargs["qMeasureInfo"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AlternateStateData:
    """

    Attributes
    ----------
    qStateName: str
      Name of the alternate state.
      Default is current selections: $
    qFieldItems: list[BookmarkFieldItem]
      List of the selections.
    """

    qStateName: str = None
    qFieldItems: list[BookmarkFieldItem] = None

    def __init__(self_, **kvargs):
        if "qStateName" in kvargs:
            if (
                type(kvargs["qStateName"]).__name__
                is self_.__annotations__["qStateName"]
            ):
                self_.qStateName = kvargs["qStateName"]
            else:
                self_.qStateName = kvargs["qStateName"]
        if "qFieldItems" in kvargs:
            if (
                type(kvargs["qFieldItems"]).__name__
                is self_.__annotations__["qFieldItems"]
            ):
                self_.qFieldItems = kvargs["qFieldItems"]
            else:
                self_.qFieldItems = [
                    BookmarkFieldItem(**e) for e in kvargs["qFieldItems"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Bookmark:
    """

    Attributes
    ----------
    qId: str
    qName: str
    qUtcModifyTime: float
    qUtcRecallTime: float
    qRecallCount: int
    qApplyAdditive: bool
    qFieldItems: list[BookmarkFieldItem]
    qVariableItems: list[BookmarkVariableItem]
    qSheetId: str
    qObjects: list[LayoutBookmarkData]
    qApplyLayoutState: bool
    qShowPopupInfo: bool
    qInfoText: str
    qOwner: str
    qGroups: list[GroupBookmarkData]
    qShow: CondDef
    qApplyInputFieldValues: bool
    qInputFieldItems: list[InputFieldItem]
    qObjectsLayout: list[ExtendedLayoutBookmarkData]
    qIncludeSelectionState: bool
    qIncludeScrollPosition: bool
    qAlternateStateData: list[AlternateStateData]
    qForAnnotations: bool
    qIncludeAllVariables: bool
    """

    qId: str = None
    qName: str = None
    qUtcModifyTime: float = None
    qUtcRecallTime: float = None
    qRecallCount: int = None
    qApplyAdditive: bool = None
    qFieldItems: list[BookmarkFieldItem] = None
    qVariableItems: list[BookmarkVariableItem] = None
    qSheetId: str = None
    qObjects: list[LayoutBookmarkData] = None
    qApplyLayoutState: bool = None
    qShowPopupInfo: bool = None
    qInfoText: str = None
    qOwner: str = None
    qGroups: list[GroupBookmarkData] = None
    qShow: CondDef = None
    qApplyInputFieldValues: bool = True
    qInputFieldItems: list[InputFieldItem] = None
    qObjectsLayout: list[ExtendedLayoutBookmarkData] = None
    qIncludeSelectionState: bool = True
    qIncludeScrollPosition: bool = None
    qAlternateStateData: list[AlternateStateData] = None
    qForAnnotations: bool = None
    qIncludeAllVariables: bool = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs:
            if type(kvargs["qId"]).__name__ is self_.__annotations__["qId"]:
                self_.qId = kvargs["qId"]
            else:
                self_.qId = kvargs["qId"]
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qUtcModifyTime" in kvargs:
            if (
                type(kvargs["qUtcModifyTime"]).__name__
                is self_.__annotations__["qUtcModifyTime"]
            ):
                self_.qUtcModifyTime = kvargs["qUtcModifyTime"]
            else:
                self_.qUtcModifyTime = kvargs["qUtcModifyTime"]
        if "qUtcRecallTime" in kvargs:
            if (
                type(kvargs["qUtcRecallTime"]).__name__
                is self_.__annotations__["qUtcRecallTime"]
            ):
                self_.qUtcRecallTime = kvargs["qUtcRecallTime"]
            else:
                self_.qUtcRecallTime = kvargs["qUtcRecallTime"]
        if "qRecallCount" in kvargs:
            if (
                type(kvargs["qRecallCount"]).__name__
                is self_.__annotations__["qRecallCount"]
            ):
                self_.qRecallCount = kvargs["qRecallCount"]
            else:
                self_.qRecallCount = kvargs["qRecallCount"]
        if "qApplyAdditive" in kvargs:
            if (
                type(kvargs["qApplyAdditive"]).__name__
                is self_.__annotations__["qApplyAdditive"]
            ):
                self_.qApplyAdditive = kvargs["qApplyAdditive"]
            else:
                self_.qApplyAdditive = kvargs["qApplyAdditive"]
        if "qFieldItems" in kvargs:
            if (
                type(kvargs["qFieldItems"]).__name__
                is self_.__annotations__["qFieldItems"]
            ):
                self_.qFieldItems = kvargs["qFieldItems"]
            else:
                self_.qFieldItems = [
                    BookmarkFieldItem(**e) for e in kvargs["qFieldItems"]
                ]
        if "qVariableItems" in kvargs:
            if (
                type(kvargs["qVariableItems"]).__name__
                is self_.__annotations__["qVariableItems"]
            ):
                self_.qVariableItems = kvargs["qVariableItems"]
            else:
                self_.qVariableItems = [
                    BookmarkVariableItem(**e) for e in kvargs["qVariableItems"]
                ]
        if "qSheetId" in kvargs:
            if type(kvargs["qSheetId"]).__name__ is self_.__annotations__["qSheetId"]:
                self_.qSheetId = kvargs["qSheetId"]
            else:
                self_.qSheetId = kvargs["qSheetId"]
        if "qObjects" in kvargs:
            if type(kvargs["qObjects"]).__name__ is self_.__annotations__["qObjects"]:
                self_.qObjects = kvargs["qObjects"]
            else:
                self_.qObjects = [LayoutBookmarkData(**e) for e in kvargs["qObjects"]]
        if "qApplyLayoutState" in kvargs:
            if (
                type(kvargs["qApplyLayoutState"]).__name__
                is self_.__annotations__["qApplyLayoutState"]
            ):
                self_.qApplyLayoutState = kvargs["qApplyLayoutState"]
            else:
                self_.qApplyLayoutState = kvargs["qApplyLayoutState"]
        if "qShowPopupInfo" in kvargs:
            if (
                type(kvargs["qShowPopupInfo"]).__name__
                is self_.__annotations__["qShowPopupInfo"]
            ):
                self_.qShowPopupInfo = kvargs["qShowPopupInfo"]
            else:
                self_.qShowPopupInfo = kvargs["qShowPopupInfo"]
        if "qInfoText" in kvargs:
            if type(kvargs["qInfoText"]).__name__ is self_.__annotations__["qInfoText"]:
                self_.qInfoText = kvargs["qInfoText"]
            else:
                self_.qInfoText = kvargs["qInfoText"]
        if "qOwner" in kvargs:
            if type(kvargs["qOwner"]).__name__ is self_.__annotations__["qOwner"]:
                self_.qOwner = kvargs["qOwner"]
            else:
                self_.qOwner = kvargs["qOwner"]
        if "qGroups" in kvargs:
            if type(kvargs["qGroups"]).__name__ is self_.__annotations__["qGroups"]:
                self_.qGroups = kvargs["qGroups"]
            else:
                self_.qGroups = [GroupBookmarkData(**e) for e in kvargs["qGroups"]]
        if "qShow" in kvargs:
            if type(kvargs["qShow"]).__name__ is self_.__annotations__["qShow"]:
                self_.qShow = kvargs["qShow"]
            else:
                self_.qShow = CondDef(**kvargs["qShow"])
        if "qApplyInputFieldValues" in kvargs:
            if (
                type(kvargs["qApplyInputFieldValues"]).__name__
                is self_.__annotations__["qApplyInputFieldValues"]
            ):
                self_.qApplyInputFieldValues = kvargs["qApplyInputFieldValues"]
            else:
                self_.qApplyInputFieldValues = kvargs["qApplyInputFieldValues"]
        if "qInputFieldItems" in kvargs:
            if (
                type(kvargs["qInputFieldItems"]).__name__
                is self_.__annotations__["qInputFieldItems"]
            ):
                self_.qInputFieldItems = kvargs["qInputFieldItems"]
            else:
                self_.qInputFieldItems = [
                    InputFieldItem(**e) for e in kvargs["qInputFieldItems"]
                ]
        if "qObjectsLayout" in kvargs:
            if (
                type(kvargs["qObjectsLayout"]).__name__
                is self_.__annotations__["qObjectsLayout"]
            ):
                self_.qObjectsLayout = kvargs["qObjectsLayout"]
            else:
                self_.qObjectsLayout = [
                    ExtendedLayoutBookmarkData(**e) for e in kvargs["qObjectsLayout"]
                ]
        if "qIncludeSelectionState" in kvargs:
            if (
                type(kvargs["qIncludeSelectionState"]).__name__
                is self_.__annotations__["qIncludeSelectionState"]
            ):
                self_.qIncludeSelectionState = kvargs["qIncludeSelectionState"]
            else:
                self_.qIncludeSelectionState = kvargs["qIncludeSelectionState"]
        if "qIncludeScrollPosition" in kvargs:
            if (
                type(kvargs["qIncludeScrollPosition"]).__name__
                is self_.__annotations__["qIncludeScrollPosition"]
            ):
                self_.qIncludeScrollPosition = kvargs["qIncludeScrollPosition"]
            else:
                self_.qIncludeScrollPosition = kvargs["qIncludeScrollPosition"]
        if "qAlternateStateData" in kvargs:
            if (
                type(kvargs["qAlternateStateData"]).__name__
                is self_.__annotations__["qAlternateStateData"]
            ):
                self_.qAlternateStateData = kvargs["qAlternateStateData"]
            else:
                self_.qAlternateStateData = [
                    AlternateStateData(**e) for e in kvargs["qAlternateStateData"]
                ]
        if "qForAnnotations" in kvargs:
            if (
                type(kvargs["qForAnnotations"]).__name__
                is self_.__annotations__["qForAnnotations"]
            ):
                self_.qForAnnotations = kvargs["qForAnnotations"]
            else:
                self_.qForAnnotations = kvargs["qForAnnotations"]
        if "qIncludeAllVariables" in kvargs:
            if (
                type(kvargs["qIncludeAllVariables"]).__name__
                is self_.__annotations__["qIncludeAllVariables"]
            ):
                self_.qIncludeAllVariables = kvargs["qIncludeAllVariables"]
            else:
                self_.qIncludeAllVariables = kvargs["qIncludeAllVariables"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ListObjectDef:
    """
    Defines the properties of a list object.
    For more information about the definition of a list object, see Generic object.

    Attributes
    ----------
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    qLibraryId: str
      Refers to a dimension stored in the library.
    qDef: NxInlineDimensionDef
      Refers to a dimension stored in the list object.
    qAutoSortByState: NxAutoSortByStateDef
      Defines the sorting by state.
    qFrequencyMode: str
      Defines the frequency mode. The frequency mode is used to calculate the frequency of a value in a list object.
      Default is NXFREQUENCY_NONE_ .
      This parameter is optional.

      One of:

      • N or NX_FREQUENCY_NONE

      • V or NX_FREQUENCY_VALUE

      • P or NX_FREQUENCY_PERCENT

      • R or NX_FREQUENCY_RELATIVE
    qShowAlternatives: bool
      If set to true, alternative values are allowed in qData .
      If set to false, no alternative values are displayed in qData . Values are excluded instead.
      The default value is false.
      Note that on the contrary, the qStateCounts parameter counts the excluded values as alternative values.
      This parameter is optional.
    qInitialDataFetch: list[NxPage]
      Fetches an initial data set.
    qExpressions: list[NxListObjectExpressionDef]
      Lists the expressions in the list object.
      This parameter is optional.
    """

    qStateName: str = None
    qLibraryId: str = None
    qDef: NxInlineDimensionDef = None
    qAutoSortByState: NxAutoSortByStateDef = None
    qFrequencyMode: str = "NX_FREQUENCY_NONE"
    qShowAlternatives: bool = None
    qInitialDataFetch: list[NxPage] = None
    qExpressions: list[NxListObjectExpressionDef] = None

    def __init__(self_, **kvargs):
        if "qStateName" in kvargs:
            if (
                type(kvargs["qStateName"]).__name__
                is self_.__annotations__["qStateName"]
            ):
                self_.qStateName = kvargs["qStateName"]
            else:
                self_.qStateName = kvargs["qStateName"]
        if "qLibraryId" in kvargs:
            if (
                type(kvargs["qLibraryId"]).__name__
                is self_.__annotations__["qLibraryId"]
            ):
                self_.qLibraryId = kvargs["qLibraryId"]
            else:
                self_.qLibraryId = kvargs["qLibraryId"]
        if "qDef" in kvargs:
            if type(kvargs["qDef"]).__name__ is self_.__annotations__["qDef"]:
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = NxInlineDimensionDef(**kvargs["qDef"])
        if "qAutoSortByState" in kvargs:
            if (
                type(kvargs["qAutoSortByState"]).__name__
                is self_.__annotations__["qAutoSortByState"]
            ):
                self_.qAutoSortByState = kvargs["qAutoSortByState"]
            else:
                self_.qAutoSortByState = NxAutoSortByStateDef(
                    **kvargs["qAutoSortByState"]
                )
        if "qFrequencyMode" in kvargs:
            if (
                type(kvargs["qFrequencyMode"]).__name__
                is self_.__annotations__["qFrequencyMode"]
            ):
                self_.qFrequencyMode = kvargs["qFrequencyMode"]
            else:
                self_.qFrequencyMode = kvargs["qFrequencyMode"]
        if "qShowAlternatives" in kvargs:
            if (
                type(kvargs["qShowAlternatives"]).__name__
                is self_.__annotations__["qShowAlternatives"]
            ):
                self_.qShowAlternatives = kvargs["qShowAlternatives"]
            else:
                self_.qShowAlternatives = kvargs["qShowAlternatives"]
        if "qInitialDataFetch" in kvargs:
            if (
                type(kvargs["qInitialDataFetch"]).__name__
                is self_.__annotations__["qInitialDataFetch"]
            ):
                self_.qInitialDataFetch = kvargs["qInitialDataFetch"]
            else:
                self_.qInitialDataFetch = [
                    NxPage(**e) for e in kvargs["qInitialDataFetch"]
                ]
        if "qExpressions" in kvargs:
            if (
                type(kvargs["qExpressions"]).__name__
                is self_.__annotations__["qExpressions"]
            ):
                self_.qExpressions = kvargs["qExpressions"]
            else:
                self_.qExpressions = [
                    NxListObjectExpressionDef(**e) for e in kvargs["qExpressions"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxBookmark:
    """

    Attributes
    ----------
    qStateData: list[AlternateStateData]
      List of selections for each state.
    qUtcModifyTime: float
      Time when the bookmark was created.
    qVariableItems: list[BookmarkVariableItem]
      List of the variables in the app at the time the bookmark was created.
    qPatches: list[NxPatches]
      Softpatches to be applied with this bookmark.
    """

    qStateData: list[AlternateStateData] = None
    qUtcModifyTime: float = None
    qVariableItems: list[BookmarkVariableItem] = None
    qPatches: list[NxPatches] = None

    def __init__(self_, **kvargs):
        if "qStateData" in kvargs:
            if (
                type(kvargs["qStateData"]).__name__
                is self_.__annotations__["qStateData"]
            ):
                self_.qStateData = kvargs["qStateData"]
            else:
                self_.qStateData = [
                    AlternateStateData(**e) for e in kvargs["qStateData"]
                ]
        if "qUtcModifyTime" in kvargs:
            if (
                type(kvargs["qUtcModifyTime"]).__name__
                is self_.__annotations__["qUtcModifyTime"]
            ):
                self_.qUtcModifyTime = kvargs["qUtcModifyTime"]
            else:
                self_.qUtcModifyTime = kvargs["qUtcModifyTime"]
        if "qVariableItems" in kvargs:
            if (
                type(kvargs["qVariableItems"]).__name__
                is self_.__annotations__["qVariableItems"]
            ):
                self_.qVariableItems = kvargs["qVariableItems"]
            else:
                self_.qVariableItems = [
                    BookmarkVariableItem(**e) for e in kvargs["qVariableItems"]
                ]
        if "qPatches" in kvargs:
            if type(kvargs["qPatches"]).__name__ is self_.__annotations__["qPatches"]:
                self_.qPatches = kvargs["qPatches"]
            else:
                self_.qPatches = [NxPatches(**e) for e in kvargs["qPatches"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxCell:
    """

    Attributes
    ----------
    qText: str
      Some text.
      This parameter is optional.
    qNum: float
      A value.
      This parameter is optional.
    qElemNumber: int
      Rank number of the value, starting from 0.
      If the element number is a negative number, it means that the returned value is not an element number.
      You can get the following negative values:

      • -1: the cell is a Total cell. It shows a total.

      • -2: the cell is a Null cell.

      • -3: the cell belongs to the group Others .

      • -4: the cell is empty. Applies to pivot tables.
    qState: str
      State of the value.
      The default state for a measure is L.

      One of:

      • L or LOCKED

      • S or SELECTED

      • O or OPTION

      • D or DESELECTED

      • A or ALTERNATIVE

      • X or EXCLUDED

      • XS or EXCL_SELECTED

      • XL or EXCL_LOCKED

      • NSTATES
    qIsEmpty: bool
      Is set to true , if qText and qNum are empty.
      This parameter is optional. The default value is false .
    qIsTotalCell: bool
      Is set to true if a total is displayed in the cell.
      This parameter is optional. The default value is false .
      Not applicable to list objects.
    qIsOtherCell: bool
      Is set to true if the cell belongs to the group Others .
      Dimension values can be set as Others depending on what has been defined in OtherTotalSpecProp .
      This parameter is optional. The default value is false .
      Not applicable to list objects.
    qFrequency: str
      Frequency of the value.
      This parameter is optional.
    qHighlightRanges: NxHighlightRanges
      Search hits.
      The search hits are highlighted.
      This parameter is optional.
    qAttrExps: NxAttributeExpressionValues
      Attribute expression values.
    qAttrDims: NxAttributeDimValues
      Attribute dimensions values.
    qIsNull: bool
      Is set to true if the value is Null.
    qMiniChart: NxMiniChartData
    qInExtRow: bool
    """

    qText: str = None
    qNum: float = None
    qElemNumber: int = None
    qState: str = None
    qIsEmpty: bool = None
    qIsTotalCell: bool = None
    qIsOtherCell: bool = None
    qFrequency: str = None
    qHighlightRanges: NxHighlightRanges = None
    qAttrExps: NxAttributeExpressionValues = None
    qAttrDims: NxAttributeDimValues = None
    qIsNull: bool = None
    qMiniChart: NxMiniChartData = None
    qInExtRow: bool = None

    def __init__(self_, **kvargs):
        if "qText" in kvargs:
            if type(kvargs["qText"]).__name__ is self_.__annotations__["qText"]:
                self_.qText = kvargs["qText"]
            else:
                self_.qText = kvargs["qText"]
        if "qNum" in kvargs:
            if type(kvargs["qNum"]).__name__ is self_.__annotations__["qNum"]:
                self_.qNum = kvargs["qNum"]
            else:
                self_.qNum = kvargs["qNum"]
        if "qElemNumber" in kvargs:
            if (
                type(kvargs["qElemNumber"]).__name__
                is self_.__annotations__["qElemNumber"]
            ):
                self_.qElemNumber = kvargs["qElemNumber"]
            else:
                self_.qElemNumber = kvargs["qElemNumber"]
        if "qState" in kvargs:
            if type(kvargs["qState"]).__name__ is self_.__annotations__["qState"]:
                self_.qState = kvargs["qState"]
            else:
                self_.qState = kvargs["qState"]
        if "qIsEmpty" in kvargs:
            if type(kvargs["qIsEmpty"]).__name__ is self_.__annotations__["qIsEmpty"]:
                self_.qIsEmpty = kvargs["qIsEmpty"]
            else:
                self_.qIsEmpty = kvargs["qIsEmpty"]
        if "qIsTotalCell" in kvargs:
            if (
                type(kvargs["qIsTotalCell"]).__name__
                is self_.__annotations__["qIsTotalCell"]
            ):
                self_.qIsTotalCell = kvargs["qIsTotalCell"]
            else:
                self_.qIsTotalCell = kvargs["qIsTotalCell"]
        if "qIsOtherCell" in kvargs:
            if (
                type(kvargs["qIsOtherCell"]).__name__
                is self_.__annotations__["qIsOtherCell"]
            ):
                self_.qIsOtherCell = kvargs["qIsOtherCell"]
            else:
                self_.qIsOtherCell = kvargs["qIsOtherCell"]
        if "qFrequency" in kvargs:
            if (
                type(kvargs["qFrequency"]).__name__
                is self_.__annotations__["qFrequency"]
            ):
                self_.qFrequency = kvargs["qFrequency"]
            else:
                self_.qFrequency = kvargs["qFrequency"]
        if "qHighlightRanges" in kvargs:
            if (
                type(kvargs["qHighlightRanges"]).__name__
                is self_.__annotations__["qHighlightRanges"]
            ):
                self_.qHighlightRanges = kvargs["qHighlightRanges"]
            else:
                self_.qHighlightRanges = NxHighlightRanges(**kvargs["qHighlightRanges"])
        if "qAttrExps" in kvargs:
            if type(kvargs["qAttrExps"]).__name__ is self_.__annotations__["qAttrExps"]:
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(**kvargs["qAttrExps"])
        if "qAttrDims" in kvargs:
            if type(kvargs["qAttrDims"]).__name__ is self_.__annotations__["qAttrDims"]:
                self_.qAttrDims = kvargs["qAttrDims"]
            else:
                self_.qAttrDims = NxAttributeDimValues(**kvargs["qAttrDims"])
        if "qIsNull" in kvargs:
            if type(kvargs["qIsNull"]).__name__ is self_.__annotations__["qIsNull"]:
                self_.qIsNull = kvargs["qIsNull"]
            else:
                self_.qIsNull = kvargs["qIsNull"]
        if "qMiniChart" in kvargs:
            if (
                type(kvargs["qMiniChart"]).__name__
                is self_.__annotations__["qMiniChart"]
            ):
                self_.qMiniChart = kvargs["qMiniChart"]
            else:
                self_.qMiniChart = NxMiniChartData(**kvargs["qMiniChart"])
        if "qInExtRow" in kvargs:
            if type(kvargs["qInExtRow"]).__name__ is self_.__annotations__["qInExtRow"]:
                self_.qInExtRow = kvargs["qInExtRow"]
            else:
                self_.qInExtRow = kvargs["qInExtRow"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxCellRows:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDataPage:
    """

    Attributes
    ----------
    qMatrix: list[NxCellRows]
      Array of data.
    qTails: list[NxGroupTail]
      Array of tails.
      Is used for hypercube objects with multiple dimensions. It might happen that due to the window size some elements in a group cannot be displayed in the same page as the other elements of the group. Elements of a group of dimensions can be part of the previous or the next tail.
      If there is no tail, the array is empty [ ] .
    qArea: Rect
      Size and offset of the data in the matrix.
    qIsReduced: bool
      Is set to true, if the data have been reduced.
      The default value is false.
    """

    qMatrix: list[NxCellRows] = None
    qTails: list[NxGroupTail] = None
    qArea: Rect = None
    qIsReduced: bool = None

    def __init__(self_, **kvargs):
        if "qMatrix" in kvargs:
            if type(kvargs["qMatrix"]).__name__ is self_.__annotations__["qMatrix"]:
                self_.qMatrix = kvargs["qMatrix"]
            else:
                self_.qMatrix = [NxCellRows(**e) for e in kvargs["qMatrix"]]
        if "qTails" in kvargs:
            if type(kvargs["qTails"]).__name__ is self_.__annotations__["qTails"]:
                self_.qTails = kvargs["qTails"]
            else:
                self_.qTails = [NxGroupTail(**e) for e in kvargs["qTails"]]
        if "qArea" in kvargs:
            if type(kvargs["qArea"]).__name__ is self_.__annotations__["qArea"]:
                self_.qArea = kvargs["qArea"]
            else:
                self_.qArea = Rect(**kvargs["qArea"])
        if "qIsReduced" in kvargs:
            if (
                type(kvargs["qIsReduced"]).__name__
                is self_.__annotations__["qIsReduced"]
            ):
                self_.qIsReduced = kvargs["qIsReduced"]
            else:
                self_.qIsReduced = kvargs["qIsReduced"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDerivedFieldDescriptionList:
    """

    Attributes
    ----------
    qDerivedFieldLists: list[NxDerivedFieldsData]
      Information about the derived fields.
    """

    qDerivedFieldLists: list[NxDerivedFieldsData] = None

    def __init__(self_, **kvargs):
        if "qDerivedFieldLists" in kvargs:
            if (
                type(kvargs["qDerivedFieldLists"]).__name__
                is self_.__annotations__["qDerivedFieldLists"]
            ):
                self_.qDerivedFieldLists = kvargs["qDerivedFieldLists"]
            else:
                self_.qDerivedFieldLists = [
                    NxDerivedFieldsData(**e) for e in kvargs["qDerivedFieldLists"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDimension:
    """
    Either qDef or qLibraryId must be set, but not both.
    If the dimension is set in the hypercube and not in the library, this dimension cannot be shared with other objects.
    A dimension that is set in the library can be used by many objects.

    Attributes
    ----------
    qLibraryId: str
      Refers to a dimension stored in the library.
    qDef: NxInlineDimensionDef
      Refers to a dimension stored in the hypercube.
    qNullSuppression: bool
      If set to true, no null values are returned.
    qIncludeElemValue: bool
    qOtherTotalSpec: OtherTotalSpecProp
      Sets the dimension limits. Each dimension of a hypercube is configured separately.
      Defines if some values (grouped as Others ) should be grouped together in the visualization.
      For example in a pie chart all values lower than 200 could be grouped together.
    qShowTotal: bool
    qShowAll: bool
      If set to true, all dimension values are shown.
    qOtherLabel: StringExpr
      This property is used when some dimension limits are set.
      Label of the Others group. The default label is Others .
      Example:
      _"qOtherLabel":"= <label>"_
      or
      _"qOtherLabel":{"qExpr":"= <label>"}_
      Where:

      • < label > is the label of the Others group.
    qTotalLabel: StringExpr
      If this property is set, the total of the calculated values is returned.
      The default label is Total .
      Example:
      _"qTotalLabel":"= <label>"_
      or
      _"qTotalLabel":{"qExpr":"= <label>"}_
      Where:

      • < label > is the label of the Total group.
    qCalcCond: ValueExpr
      Specifies a calculation condition, which must be fulfilled for the dimension to be calculated.
      If the calculation condition is not met, the dimension is excluded from the calculation.
      By default, there is no calculation condition.
      This property is optional.
    qAttributeExpressions: list[NxAttrExprDef]
      List of attribute expressions.
    qAttributeDimensions: list[NxAttrDimDef]
      List of attribute dimensions.
    qCalcCondition: NxCalcCond
      Specifies a calculation condition object.
      If CalcCondition.Cond is not fulfilled, the dimension is excluded from the calculation and CalcCondition.Msg is evaluated.
      By default, there is no calculation condition.
      This property is optional.
    """

    qLibraryId: str = None
    qDef: NxInlineDimensionDef = None
    qNullSuppression: bool = None
    qIncludeElemValue: bool = None
    qOtherTotalSpec: OtherTotalSpecProp = None
    qShowTotal: bool = None
    qShowAll: bool = None
    qOtherLabel: StringExpr = None
    qTotalLabel: StringExpr = None
    qCalcCond: ValueExpr = None
    qAttributeExpressions: list[NxAttrExprDef] = None
    qAttributeDimensions: list[NxAttrDimDef] = None
    qCalcCondition: NxCalcCond = None

    def __init__(self_, **kvargs):
        if "qLibraryId" in kvargs:
            if (
                type(kvargs["qLibraryId"]).__name__
                is self_.__annotations__["qLibraryId"]
            ):
                self_.qLibraryId = kvargs["qLibraryId"]
            else:
                self_.qLibraryId = kvargs["qLibraryId"]
        if "qDef" in kvargs:
            if type(kvargs["qDef"]).__name__ is self_.__annotations__["qDef"]:
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = NxInlineDimensionDef(**kvargs["qDef"])
        if "qNullSuppression" in kvargs:
            if (
                type(kvargs["qNullSuppression"]).__name__
                is self_.__annotations__["qNullSuppression"]
            ):
                self_.qNullSuppression = kvargs["qNullSuppression"]
            else:
                self_.qNullSuppression = kvargs["qNullSuppression"]
        if "qIncludeElemValue" in kvargs:
            if (
                type(kvargs["qIncludeElemValue"]).__name__
                is self_.__annotations__["qIncludeElemValue"]
            ):
                self_.qIncludeElemValue = kvargs["qIncludeElemValue"]
            else:
                self_.qIncludeElemValue = kvargs["qIncludeElemValue"]
        if "qOtherTotalSpec" in kvargs:
            if (
                type(kvargs["qOtherTotalSpec"]).__name__
                is self_.__annotations__["qOtherTotalSpec"]
            ):
                self_.qOtherTotalSpec = kvargs["qOtherTotalSpec"]
            else:
                self_.qOtherTotalSpec = OtherTotalSpecProp(**kvargs["qOtherTotalSpec"])
        if "qShowTotal" in kvargs:
            if (
                type(kvargs["qShowTotal"]).__name__
                is self_.__annotations__["qShowTotal"]
            ):
                self_.qShowTotal = kvargs["qShowTotal"]
            else:
                self_.qShowTotal = kvargs["qShowTotal"]
        if "qShowAll" in kvargs:
            if type(kvargs["qShowAll"]).__name__ is self_.__annotations__["qShowAll"]:
                self_.qShowAll = kvargs["qShowAll"]
            else:
                self_.qShowAll = kvargs["qShowAll"]
        if "qOtherLabel" in kvargs:
            if (
                type(kvargs["qOtherLabel"]).__name__
                is self_.__annotations__["qOtherLabel"]
            ):
                self_.qOtherLabel = kvargs["qOtherLabel"]
            else:
                self_.qOtherLabel = StringExpr(**kvargs["qOtherLabel"])
        if "qTotalLabel" in kvargs:
            if (
                type(kvargs["qTotalLabel"]).__name__
                is self_.__annotations__["qTotalLabel"]
            ):
                self_.qTotalLabel = kvargs["qTotalLabel"]
            else:
                self_.qTotalLabel = StringExpr(**kvargs["qTotalLabel"])
        if "qCalcCond" in kvargs:
            if type(kvargs["qCalcCond"]).__name__ is self_.__annotations__["qCalcCond"]:
                self_.qCalcCond = kvargs["qCalcCond"]
            else:
                self_.qCalcCond = ValueExpr(**kvargs["qCalcCond"])
        if "qAttributeExpressions" in kvargs:
            if (
                type(kvargs["qAttributeExpressions"]).__name__
                is self_.__annotations__["qAttributeExpressions"]
            ):
                self_.qAttributeExpressions = kvargs["qAttributeExpressions"]
            else:
                self_.qAttributeExpressions = [
                    NxAttrExprDef(**e) for e in kvargs["qAttributeExpressions"]
                ]
        if "qAttributeDimensions" in kvargs:
            if (
                type(kvargs["qAttributeDimensions"]).__name__
                is self_.__annotations__["qAttributeDimensions"]
            ):
                self_.qAttributeDimensions = kvargs["qAttributeDimensions"]
            else:
                self_.qAttributeDimensions = [
                    NxAttrDimDef(**e) for e in kvargs["qAttributeDimensions"]
                ]
        if "qCalcCondition" in kvargs:
            if (
                type(kvargs["qCalcCondition"]).__name__
                is self_.__annotations__["qCalcCondition"]
            ):
                self_.qCalcCondition = kvargs["qCalcCondition"]
            else:
                self_.qCalcCondition = NxCalcCond(**kvargs["qCalcCondition"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFieldDescription:
    """
    NxDerivedFieldsdata:

      +------------------------+--------------------------------+----------------+
      |          NAME          |          DESCRIPTION           |      TYPE      |
      +------------------------+--------------------------------+----------------+
      | qDerivedDefinitionName | Name of the derived            | String         |
      |                        | definition.                    |                |
      | qFieldDefs             | List of the derived fields.    | Array of       |
      |                        |                                | NxDerivedField |
      | qGroupDefs             | List of the derived groups.    | Array of       |
      |                        |                                | NxDerivedGroup |
      | qTags                  | List of tags on the derived    | Array of       |
      |                        | fields.                        | String         |
      +------------------------+--------------------------------+----------------+

    Attributes
    ----------
    qIsSemantic: bool
      If set to true, it means that the field is a semantic.
    qIsHidden: bool
      If set to true, it means that the field is hidden.
    qIsSystem: bool
      If set to true, it means that the field is a system field.
    qAndMode: bool
      If set to true a logical AND (instead of a logical OR) is used when making selections in a field.
      The default value is false.
    qName: str
      Name of the field
    qCardinal: int
      Number of distinct field values
    qTags: list[str]
      Gives information on a field. For example, it can return the type of the field.
      Examples: key, text, ASCII
    qIsDefinitionOnly: bool
      If set to true, it means that the field is a field on the fly.
    qDerivedFieldData: NxDerivedFieldDescriptionList
      Lists the derived fields if any.
    qIsDetail: bool
      Is used for Direct Discovery.
      If set to true, it means that the type of the field is detail.
    qIsImplicit: bool
      Is used for Direct Discovery.
      If set to true, it means that the type of the field is measure.
    qReadableName: str
    """

    qIsSemantic: bool = None
    qIsHidden: bool = None
    qIsSystem: bool = None
    qAndMode: bool = None
    qName: str = None
    qCardinal: int = None
    qTags: list[str] = None
    qIsDefinitionOnly: bool = None
    qDerivedFieldData: NxDerivedFieldDescriptionList = None
    qIsDetail: bool = None
    qIsImplicit: bool = None
    qReadableName: str = None

    def __init__(self_, **kvargs):
        if "qIsSemantic" in kvargs:
            if (
                type(kvargs["qIsSemantic"]).__name__
                is self_.__annotations__["qIsSemantic"]
            ):
                self_.qIsSemantic = kvargs["qIsSemantic"]
            else:
                self_.qIsSemantic = kvargs["qIsSemantic"]
        if "qIsHidden" in kvargs:
            if type(kvargs["qIsHidden"]).__name__ is self_.__annotations__["qIsHidden"]:
                self_.qIsHidden = kvargs["qIsHidden"]
            else:
                self_.qIsHidden = kvargs["qIsHidden"]
        if "qIsSystem" in kvargs:
            if type(kvargs["qIsSystem"]).__name__ is self_.__annotations__["qIsSystem"]:
                self_.qIsSystem = kvargs["qIsSystem"]
            else:
                self_.qIsSystem = kvargs["qIsSystem"]
        if "qAndMode" in kvargs:
            if type(kvargs["qAndMode"]).__name__ is self_.__annotations__["qAndMode"]:
                self_.qAndMode = kvargs["qAndMode"]
            else:
                self_.qAndMode = kvargs["qAndMode"]
        if "qName" in kvargs:
            if type(kvargs["qName"]).__name__ is self_.__annotations__["qName"]:
                self_.qName = kvargs["qName"]
            else:
                self_.qName = kvargs["qName"]
        if "qCardinal" in kvargs:
            if type(kvargs["qCardinal"]).__name__ is self_.__annotations__["qCardinal"]:
                self_.qCardinal = kvargs["qCardinal"]
            else:
                self_.qCardinal = kvargs["qCardinal"]
        if "qTags" in kvargs:
            if type(kvargs["qTags"]).__name__ is self_.__annotations__["qTags"]:
                self_.qTags = kvargs["qTags"]
            else:
                self_.qTags = kvargs["qTags"]
        if "qIsDefinitionOnly" in kvargs:
            if (
                type(kvargs["qIsDefinitionOnly"]).__name__
                is self_.__annotations__["qIsDefinitionOnly"]
            ):
                self_.qIsDefinitionOnly = kvargs["qIsDefinitionOnly"]
            else:
                self_.qIsDefinitionOnly = kvargs["qIsDefinitionOnly"]
        if "qDerivedFieldData" in kvargs:
            if (
                type(kvargs["qDerivedFieldData"]).__name__
                is self_.__annotations__["qDerivedFieldData"]
            ):
                self_.qDerivedFieldData = kvargs["qDerivedFieldData"]
            else:
                self_.qDerivedFieldData = NxDerivedFieldDescriptionList(
                    **kvargs["qDerivedFieldData"]
                )
        if "qIsDetail" in kvargs:
            if type(kvargs["qIsDetail"]).__name__ is self_.__annotations__["qIsDetail"]:
                self_.qIsDetail = kvargs["qIsDetail"]
            else:
                self_.qIsDetail = kvargs["qIsDetail"]
        if "qIsImplicit" in kvargs:
            if (
                type(kvargs["qIsImplicit"]).__name__
                is self_.__annotations__["qIsImplicit"]
            ):
                self_.qIsImplicit = kvargs["qIsImplicit"]
            else:
                self_.qIsImplicit = kvargs["qIsImplicit"]
        if "qReadableName" in kvargs:
            if (
                type(kvargs["qReadableName"]).__name__
                is self_.__annotations__["qReadableName"]
            ):
                self_.qReadableName = kvargs["qReadableName"]
            else:
                self_.qReadableName = kvargs["qReadableName"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMeasure:
    """
    Either qDef or qLibraryId must be set, but not both.
    If the measure is set in the hypercube and not in the library, this measure cannot be shared with other objects.
    A measure that is set in the library can be used by many objects.

    expressions are complementary expressions associated to a measure. For example, you can decide to change the background color of a visualization depending on the values of the measure.
    Attribute expressions do not affect the layout of an object. The sorting order is unchanged.

    Attributes
    ----------
    qLibraryId: str
      Refers to a measure stored in the library.
    qDef: NxInlineMeasureDef
      Refers to a measure stored in the hypercube.
    qSortBy: SortCriteria
      Defines the sort criteria.
      The default value is sort by ascending alphabetic order.
      This property is optional.
    qAttributeExpressions: list[NxAttrExprDef]
      List of attribute expressions.
    qAttributeDimensions: list[NxAttrDimDef]
      List of attribute dimensions.
    qCalcCond: ValueExpr
      Specifies a calculation condition, which must be fulfilled for the measure to be calculated.
      If the calculation condition is not met, the measure is excluded from the calculation.
      By default, there is no calculation condition.
      This property is optional.
    qCalcCondition: NxCalcCond
      Specifies a calculation condition object.
      If CalcCondition.Cond is not fulfilled, the measure is excluded from the calculation and CalcCondition.Msg is evaluated.
      By default, there is no calculation condition.
      This property is optional.
    qTrendLines: list[NxTrendlineDef]
      Specifies trendlines for this measure.
    qMiniChartDef: NxMiniChartDef
    """

    qLibraryId: str = None
    qDef: NxInlineMeasureDef = None
    qSortBy: SortCriteria = None
    qAttributeExpressions: list[NxAttrExprDef] = None
    qAttributeDimensions: list[NxAttrDimDef] = None
    qCalcCond: ValueExpr = None
    qCalcCondition: NxCalcCond = None
    qTrendLines: list[NxTrendlineDef] = None
    qMiniChartDef: NxMiniChartDef = None

    def __init__(self_, **kvargs):
        if "qLibraryId" in kvargs:
            if (
                type(kvargs["qLibraryId"]).__name__
                is self_.__annotations__["qLibraryId"]
            ):
                self_.qLibraryId = kvargs["qLibraryId"]
            else:
                self_.qLibraryId = kvargs["qLibraryId"]
        if "qDef" in kvargs:
            if type(kvargs["qDef"]).__name__ is self_.__annotations__["qDef"]:
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = NxInlineMeasureDef(**kvargs["qDef"])
        if "qSortBy" in kvargs:
            if type(kvargs["qSortBy"]).__name__ is self_.__annotations__["qSortBy"]:
                self_.qSortBy = kvargs["qSortBy"]
            else:
                self_.qSortBy = SortCriteria(**kvargs["qSortBy"])
        if "qAttributeExpressions" in kvargs:
            if (
                type(kvargs["qAttributeExpressions"]).__name__
                is self_.__annotations__["qAttributeExpressions"]
            ):
                self_.qAttributeExpressions = kvargs["qAttributeExpressions"]
            else:
                self_.qAttributeExpressions = [
                    NxAttrExprDef(**e) for e in kvargs["qAttributeExpressions"]
                ]
        if "qAttributeDimensions" in kvargs:
            if (
                type(kvargs["qAttributeDimensions"]).__name__
                is self_.__annotations__["qAttributeDimensions"]
            ):
                self_.qAttributeDimensions = kvargs["qAttributeDimensions"]
            else:
                self_.qAttributeDimensions = [
                    NxAttrDimDef(**e) for e in kvargs["qAttributeDimensions"]
                ]
        if "qCalcCond" in kvargs:
            if type(kvargs["qCalcCond"]).__name__ is self_.__annotations__["qCalcCond"]:
                self_.qCalcCond = kvargs["qCalcCond"]
            else:
                self_.qCalcCond = ValueExpr(**kvargs["qCalcCond"])
        if "qCalcCondition" in kvargs:
            if (
                type(kvargs["qCalcCondition"]).__name__
                is self_.__annotations__["qCalcCondition"]
            ):
                self_.qCalcCondition = kvargs["qCalcCondition"]
            else:
                self_.qCalcCondition = NxCalcCond(**kvargs["qCalcCondition"])
        if "qTrendLines" in kvargs:
            if (
                type(kvargs["qTrendLines"]).__name__
                is self_.__annotations__["qTrendLines"]
            ):
                self_.qTrendLines = kvargs["qTrendLines"]
            else:
                self_.qTrendLines = [NxTrendlineDef(**e) for e in kvargs["qTrendLines"]]
        if "qMiniChartDef" in kvargs:
            if (
                type(kvargs["qMiniChartDef"]).__name__
                is self_.__annotations__["qMiniChartDef"]
            ):
                self_.qMiniChartDef = kvargs["qMiniChartDef"]
            else:
                self_.qMiniChartDef = NxMiniChartDef(**kvargs["qMiniChartDef"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeDimensionDef:
    """

    Attributes
    ----------
    qLibraryId: str
      Refers to a dimension stored in the library.
    qDef: NxInlineDimensionDef
      Refers to a dimension.
    qValueExprs: list[NxMeasure]
      List of measures.
    qNullSuppression: bool
      If set to true, no null values are returned.
    qOtherTotalSpec: OtherTotalSpecProp
      Sets the dimension limits. Each dimension of a hypercube is configured separately.
      Defines if some values (grouped as Others ) should be grouped together in the visualization.
      For example in a pie chart all values lower than 200 could be grouped together.
    qShowAll: bool
      If set to true, all dimension values are shown.
    qOtherLabel: StringExpr
      This property is used when some dimension limits are set.
      Label of the Others group. The default label is Others .
      Example:
      _"qOtherLabel":"= <label>"_
      or
      _"qOtherLabel":{"qExpr":"= <label>"}_
      Where:

      • < label > is the label of the Others group.
    qTotalLabel: StringExpr
      If this property is set, the total of the calculated values is returned.
      The default label is Total .
      Example:
      _"qTotalLabel":"= <label>"_
      or
      _"qTotalLabel":{"qExpr":"= <label>"}_
      Where:

      • < label > is the label of the Total group.
    qCalcCondition: NxCalcCond
      Specifies a calculation condition object.
      If CalcCondition.Cond is not fulfilled, the dimension is excluded from the calculation and CalcCondition.Msg is evaluated.
      By default, there is no calculation condition.
      This property is optional.
    qAttributeExpressions: list[NxAttrExprDef]
      List of attribute expressions.
    qAttributeDimensions: list[NxAttrDimDef]
      List of attribute dimensions.
    """

    qLibraryId: str = None
    qDef: NxInlineDimensionDef = None
    qValueExprs: list[NxMeasure] = None
    qNullSuppression: bool = None
    qOtherTotalSpec: OtherTotalSpecProp = None
    qShowAll: bool = None
    qOtherLabel: StringExpr = None
    qTotalLabel: StringExpr = None
    qCalcCondition: NxCalcCond = None
    qAttributeExpressions: list[NxAttrExprDef] = None
    qAttributeDimensions: list[NxAttrDimDef] = None

    def __init__(self_, **kvargs):
        if "qLibraryId" in kvargs:
            if (
                type(kvargs["qLibraryId"]).__name__
                is self_.__annotations__["qLibraryId"]
            ):
                self_.qLibraryId = kvargs["qLibraryId"]
            else:
                self_.qLibraryId = kvargs["qLibraryId"]
        if "qDef" in kvargs:
            if type(kvargs["qDef"]).__name__ is self_.__annotations__["qDef"]:
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = NxInlineDimensionDef(**kvargs["qDef"])
        if "qValueExprs" in kvargs:
            if (
                type(kvargs["qValueExprs"]).__name__
                is self_.__annotations__["qValueExprs"]
            ):
                self_.qValueExprs = kvargs["qValueExprs"]
            else:
                self_.qValueExprs = [NxMeasure(**e) for e in kvargs["qValueExprs"]]
        if "qNullSuppression" in kvargs:
            if (
                type(kvargs["qNullSuppression"]).__name__
                is self_.__annotations__["qNullSuppression"]
            ):
                self_.qNullSuppression = kvargs["qNullSuppression"]
            else:
                self_.qNullSuppression = kvargs["qNullSuppression"]
        if "qOtherTotalSpec" in kvargs:
            if (
                type(kvargs["qOtherTotalSpec"]).__name__
                is self_.__annotations__["qOtherTotalSpec"]
            ):
                self_.qOtherTotalSpec = kvargs["qOtherTotalSpec"]
            else:
                self_.qOtherTotalSpec = OtherTotalSpecProp(**kvargs["qOtherTotalSpec"])
        if "qShowAll" in kvargs:
            if type(kvargs["qShowAll"]).__name__ is self_.__annotations__["qShowAll"]:
                self_.qShowAll = kvargs["qShowAll"]
            else:
                self_.qShowAll = kvargs["qShowAll"]
        if "qOtherLabel" in kvargs:
            if (
                type(kvargs["qOtherLabel"]).__name__
                is self_.__annotations__["qOtherLabel"]
            ):
                self_.qOtherLabel = kvargs["qOtherLabel"]
            else:
                self_.qOtherLabel = StringExpr(**kvargs["qOtherLabel"])
        if "qTotalLabel" in kvargs:
            if (
                type(kvargs["qTotalLabel"]).__name__
                is self_.__annotations__["qTotalLabel"]
            ):
                self_.qTotalLabel = kvargs["qTotalLabel"]
            else:
                self_.qTotalLabel = StringExpr(**kvargs["qTotalLabel"])
        if "qCalcCondition" in kvargs:
            if (
                type(kvargs["qCalcCondition"]).__name__
                is self_.__annotations__["qCalcCondition"]
            ):
                self_.qCalcCondition = kvargs["qCalcCondition"]
            else:
                self_.qCalcCondition = NxCalcCond(**kvargs["qCalcCondition"])
        if "qAttributeExpressions" in kvargs:
            if (
                type(kvargs["qAttributeExpressions"]).__name__
                is self_.__annotations__["qAttributeExpressions"]
            ):
                self_.qAttributeExpressions = kvargs["qAttributeExpressions"]
            else:
                self_.qAttributeExpressions = [
                    NxAttrExprDef(**e) for e in kvargs["qAttributeExpressions"]
                ]
        if "qAttributeDimensions" in kvargs:
            if (
                type(kvargs["qAttributeDimensions"]).__name__
                is self_.__annotations__["qAttributeDimensions"]
            ):
                self_.qAttributeDimensions = kvargs["qAttributeDimensions"]
            else:
                self_.qAttributeDimensions = [
                    NxAttrDimDef(**e) for e in kvargs["qAttributeDimensions"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TreeDataDef:
    """
    Defines the properties of a TreeData object.
    For more information about the definition of a TreeData object, see Generic object.

    Attributes
    ----------
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    qDimensions: list[NxTreeDimensionDef]
      Array of dimensions.
    qInterColumnSortOrder: list[int]
      Defines the order of the dimension levels/columns in the TreeData object.
      Column numbers are separated by a comma.
      Example: [1,0,2] means that the first level in the tree structure is dimension 1, followed by dimension 0 and dimension 2.
      The default sort order is the order in which the dimensions and measures have been defined in the TreeDataDef.
    qSuppressZero: bool
      Removes zero values.
    qSuppressMissing: bool
      Removes missing values.
    qOpenFullyExpanded: bool
      If this property is set to true, the cells are opened expanded. The default value is false.
    qPopulateMissing: bool
      If this property is set to true, the missing symbols (if any) are replaced by 0 if the value is a numeric and by an empty string if the value is a string.
      The default value is false.
    qCalcCondition: NxCalcCond
      Specifies a calculation condition object.
      If CalcCondition.Cond is not fulfilled, the TreeData is excluded from the calculation and CalcCondition.Msg is evaluated.
      By default, there is no calculation condition.
      This property is optional.
    qTitle: StringExpr
      Title of the TreeData object, for example the title of a chart.
    qInitialDataFetch: list[NxTreeDataOption]
      Initial data set.
      This property is optional.
    qExpansionState: list[ExpansionData]
      Expansion state per dimension.
    qValueExprs: list[NxMeasure]
      List of measures to calculate on the whole tree.
    qContextSetExpression: str
      Set Expression valid for the whole cube. Used to limit computations to the set specified. *
    """

    qStateName: str = None
    qDimensions: list[NxTreeDimensionDef] = None
    qInterColumnSortOrder: list[int] = None
    qSuppressZero: bool = None
    qSuppressMissing: bool = None
    qOpenFullyExpanded: bool = None
    qPopulateMissing: bool = None
    qCalcCondition: NxCalcCond = None
    qTitle: StringExpr = None
    qInitialDataFetch: list[NxTreeDataOption] = None
    qExpansionState: list[ExpansionData] = None
    qValueExprs: list[NxMeasure] = None
    qContextSetExpression: str = None

    def __init__(self_, **kvargs):
        if "qStateName" in kvargs:
            if (
                type(kvargs["qStateName"]).__name__
                is self_.__annotations__["qStateName"]
            ):
                self_.qStateName = kvargs["qStateName"]
            else:
                self_.qStateName = kvargs["qStateName"]
        if "qDimensions" in kvargs:
            if (
                type(kvargs["qDimensions"]).__name__
                is self_.__annotations__["qDimensions"]
            ):
                self_.qDimensions = kvargs["qDimensions"]
            else:
                self_.qDimensions = [
                    NxTreeDimensionDef(**e) for e in kvargs["qDimensions"]
                ]
        if "qInterColumnSortOrder" in kvargs:
            if (
                type(kvargs["qInterColumnSortOrder"]).__name__
                is self_.__annotations__["qInterColumnSortOrder"]
            ):
                self_.qInterColumnSortOrder = kvargs["qInterColumnSortOrder"]
            else:
                self_.qInterColumnSortOrder = kvargs["qInterColumnSortOrder"]
        if "qSuppressZero" in kvargs:
            if (
                type(kvargs["qSuppressZero"]).__name__
                is self_.__annotations__["qSuppressZero"]
            ):
                self_.qSuppressZero = kvargs["qSuppressZero"]
            else:
                self_.qSuppressZero = kvargs["qSuppressZero"]
        if "qSuppressMissing" in kvargs:
            if (
                type(kvargs["qSuppressMissing"]).__name__
                is self_.__annotations__["qSuppressMissing"]
            ):
                self_.qSuppressMissing = kvargs["qSuppressMissing"]
            else:
                self_.qSuppressMissing = kvargs["qSuppressMissing"]
        if "qOpenFullyExpanded" in kvargs:
            if (
                type(kvargs["qOpenFullyExpanded"]).__name__
                is self_.__annotations__["qOpenFullyExpanded"]
            ):
                self_.qOpenFullyExpanded = kvargs["qOpenFullyExpanded"]
            else:
                self_.qOpenFullyExpanded = kvargs["qOpenFullyExpanded"]
        if "qPopulateMissing" in kvargs:
            if (
                type(kvargs["qPopulateMissing"]).__name__
                is self_.__annotations__["qPopulateMissing"]
            ):
                self_.qPopulateMissing = kvargs["qPopulateMissing"]
            else:
                self_.qPopulateMissing = kvargs["qPopulateMissing"]
        if "qCalcCondition" in kvargs:
            if (
                type(kvargs["qCalcCondition"]).__name__
                is self_.__annotations__["qCalcCondition"]
            ):
                self_.qCalcCondition = kvargs["qCalcCondition"]
            else:
                self_.qCalcCondition = NxCalcCond(**kvargs["qCalcCondition"])
        if "qTitle" in kvargs:
            if type(kvargs["qTitle"]).__name__ is self_.__annotations__["qTitle"]:
                self_.qTitle = kvargs["qTitle"]
            else:
                self_.qTitle = StringExpr(**kvargs["qTitle"])
        if "qInitialDataFetch" in kvargs:
            if (
                type(kvargs["qInitialDataFetch"]).__name__
                is self_.__annotations__["qInitialDataFetch"]
            ):
                self_.qInitialDataFetch = kvargs["qInitialDataFetch"]
            else:
                self_.qInitialDataFetch = [
                    NxTreeDataOption(**e) for e in kvargs["qInitialDataFetch"]
                ]
        if "qExpansionState" in kvargs:
            if (
                type(kvargs["qExpansionState"]).__name__
                is self_.__annotations__["qExpansionState"]
            ):
                self_.qExpansionState = kvargs["qExpansionState"]
            else:
                self_.qExpansionState = [
                    ExpansionData(**e) for e in kvargs["qExpansionState"]
                ]
        if "qValueExprs" in kvargs:
            if (
                type(kvargs["qValueExprs"]).__name__
                is self_.__annotations__["qValueExprs"]
            ):
                self_.qValueExprs = kvargs["qValueExprs"]
            else:
                self_.qValueExprs = [NxMeasure(**e) for e in kvargs["qValueExprs"]]
        if "qContextSetExpression" in kvargs:
            if (
                type(kvargs["qContextSetExpression"]).__name__
                is self_.__annotations__["qContextSetExpression"]
            ):
                self_.qContextSetExpression = kvargs["qContextSetExpression"]
            else:
                self_.qContextSetExpression = kvargs["qContextSetExpression"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldList:
    """
    Lists the fields present in the data model viewer. Is the layout for FieldListDef.

    Attributes
    ----------
    qItems: list[NxFieldDescription]
      Array of items.
    """

    qItems: list[NxFieldDescription] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs:
            if type(kvargs["qItems"]).__name__ is self_.__annotations__["qItems"]:
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [NxFieldDescription(**e) for e in kvargs["qItems"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericBookmarkEntry:
    """

    Attributes
    ----------
    qProperties: GenericBookmarkProperties
      Information about the properties of the bookmark.
    qBookmark: NxBookmark
      Information about the bookmark.
    qClassicBookmark: Bookmark
      Information about the Classic bookmark.
    qClassicMetadata: MetaData
      Information about the Classic bookmark metadata.
    """

    qProperties: GenericBookmarkProperties = None
    qBookmark: NxBookmark = None
    qClassicBookmark: Bookmark = None
    qClassicMetadata: MetaData = None

    def __init__(self_, **kvargs):
        if "qProperties" in kvargs:
            if (
                type(kvargs["qProperties"]).__name__
                is self_.__annotations__["qProperties"]
            ):
                self_.qProperties = kvargs["qProperties"]
            else:
                self_.qProperties = GenericBookmarkProperties(**kvargs["qProperties"])
        if "qBookmark" in kvargs:
            if type(kvargs["qBookmark"]).__name__ is self_.__annotations__["qBookmark"]:
                self_.qBookmark = kvargs["qBookmark"]
            else:
                self_.qBookmark = NxBookmark(**kvargs["qBookmark"])
        if "qClassicBookmark" in kvargs:
            if (
                type(kvargs["qClassicBookmark"]).__name__
                is self_.__annotations__["qClassicBookmark"]
            ):
                self_.qClassicBookmark = kvargs["qClassicBookmark"]
            else:
                self_.qClassicBookmark = Bookmark(**kvargs["qClassicBookmark"])
        if "qClassicMetadata" in kvargs:
            if (
                type(kvargs["qClassicMetadata"]).__name__
                is self_.__annotations__["qClassicMetadata"]
            ):
                self_.qClassicMetadata = kvargs["qClassicMetadata"]
            else:
                self_.qClassicMetadata = MetaData(**kvargs["qClassicMetadata"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericBookmarkLayout:
    """
    Is the layout for GenericBookmarkProperties.

    Attributes
    ----------
    qInfo: NxInfo
      Information about the object.
    qMeta: NxMeta
      Information on publishing and permissions.
    qBookmark: NxBookmark
      Information about the bookmark.
    qFieldInfos: list[LayoutFieldInfo]
      Information about the field selections associated with the bookmark.
    """

    qInfo: NxInfo = None
    qMeta: NxMeta = None
    qBookmark: NxBookmark = None
    qFieldInfos: list[LayoutFieldInfo] = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs:
            if type(kvargs["qInfo"]).__name__ is self_.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(**kvargs["qInfo"])
        if "qMeta" in kvargs:
            if type(kvargs["qMeta"]).__name__ is self_.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(**kvargs["qMeta"])
        if "qBookmark" in kvargs:
            if type(kvargs["qBookmark"]).__name__ is self_.__annotations__["qBookmark"]:
                self_.qBookmark = kvargs["qBookmark"]
            else:
                self_.qBookmark = NxBookmark(**kvargs["qBookmark"])
        if "qFieldInfos" in kvargs:
            if (
                type(kvargs["qFieldInfos"]).__name__
                is self_.__annotations__["qFieldInfos"]
            ):
                self_.qFieldInfos = kvargs["qFieldInfos"]
            else:
                self_.qFieldInfos = [
                    LayoutFieldInfo(**e) for e in kvargs["qFieldInfos"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericObjectEntry:
    """

    Attributes
    ----------
    qProperty: GenericObjectProperties
      Information about the generic object properties.
    qChildren: list[GenericObjectEntry]
      Information about the children of the generic object.
    qEmbeddedSnapshotRef: GenericBookmarkEntry
      Reference to a bookmark/snapshot that is embedded in the generic object.
    """

    qProperty: GenericObjectProperties = None
    qChildren: list[GenericObjectEntry] = None
    qEmbeddedSnapshotRef: GenericBookmarkEntry = None

    def __init__(self_, **kvargs):
        if "qProperty" in kvargs:
            if type(kvargs["qProperty"]).__name__ is self_.__annotations__["qProperty"]:
                self_.qProperty = kvargs["qProperty"]
            else:
                self_.qProperty = GenericObjectProperties(**kvargs["qProperty"])
        if "qChildren" in kvargs:
            if type(kvargs["qChildren"]).__name__ is self_.__annotations__["qChildren"]:
                self_.qChildren = kvargs["qChildren"]
            else:
                self_.qChildren = [GenericObjectEntry(**e) for e in kvargs["qChildren"]]
        if "qEmbeddedSnapshotRef" in kvargs:
            if (
                type(kvargs["qEmbeddedSnapshotRef"]).__name__
                is self_.__annotations__["qEmbeddedSnapshotRef"]
            ):
                self_.qEmbeddedSnapshotRef = kvargs["qEmbeddedSnapshotRef"]
            else:
                self_.qEmbeddedSnapshotRef = GenericBookmarkEntry(
                    **kvargs["qEmbeddedSnapshotRef"]
                )
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class HyperCube:
    """
    Renders the properties of a hypercube. Is the layout for HyperCubeDef.
    For more information about the definition of a hypercube, see Generic object.
    What is returned in HyperCube depends on the type of the hypercube (straight, pivot or stacked table, or tree) and on the method called (GetLayout, GetHyperCubeData, GetHyperCubePivotData, GetHyperCubeStackData, GetHyperCubeTreeData).

    Attributes
    ----------
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    qSize: Size
      Defines the size of the hypercube.
    qError: NxValidationError
      This parameter is optional and is displayed in case of error.
    qDimensionInfo: list[NxDimensionInfo]
      Information on the dimension.
    qMeasureInfo: list[NxMeasureInfo]
      Information on the measure.
    qEffectiveInterColumnSortOrder: list[int]
      Sort order of the columns in the hypercube.
      Column numbers are separated by a comma.
      Example: [1,0,2] means that the first column to be sorted was the column 1, followed by the column 0 and the column 2.
    qGrandTotalRow: list[NxCell]
      Aggregate for measures of all values in the field.
      The result value depends on the qAggrFunc defined in HyperCubeDef.
    qDataPages: list[NxDataPage]
      Set of data.
      Is empty if nothing has been defined in qInitialDataFetch in HyperCubeDef.
    qPivotDataPages: list[NxPivotPage]
      Set of data for pivot tables.
      Is empty if nothing has been defined in qInitialDataFetch in HyperCubeDef.
    qStackedDataPages: list[NxStackPage]
      Set of data for stacked tables.
      Is empty if nothing has been defined in qInitialDataFetch in HyperCubeDef.
    qMode: str
      Information about the mode of the visualization.

      One of:

      • S or DATA_MODE_STRAIGHT

      • P or DATA_MODE_PIVOT

      • K or DATA_MODE_PIVOT_STACK

      • T or DATA_MODE_TREE

      • D or DATA_MODE_DYNAMIC
    qNoOfLeftDims: int
      Number of left dimensions.
      Default value is -1.
      The index related to each left dimension depends on the position of the pseudo dimension (if any).
      For example, a pivot table with:

      • Four dimensions in the following order: Country, City, Product and Category

      • One pseudo dimension in position 1

      • Three left dimensions.

      implies that:

      • The index 0 corresponds to the left dimension Country.

      • The index 1 corresponds to the pseudo dimension.

      • The index 2 corresponds to the left dimension City.

      • Product and Category are top dimensions.

      Another example:

      • Four dimensions in the following order: Country, City, Product and Category.

      • One pseudo dimension in position -1.

      • Three left dimensions.

      implies that:

      • The index -1 corresponds to the pseudo dimension; the pseudo dimension is the most to the right.

      • The index 0 corresponds to the left dimension Country.

      • The index 1 corresponds to the left dimension City.

      • The index 2 corresponds to the left dimension Product.

      • Category is a top dimension.
    qIndentMode: bool
      Is used for pivot tables only.
      If set to true, the formatting of the results is slightly different.
      This property is optional.
    qLastExpandedPos: NxCellPosition
      Is used for pivot tables only.
      Position of the last expended cell.
      This property is optional.
    qHasOtherValues: bool
      True if other row exists.
    qTitle: str
      Title of the hypercube, for example the title of a chart.
    qTreeNodesOnDim: list[int]
      The total number of nodes on each dimension (only applicable when qMode = T ).
    qCalcCondMsg: str
      The message displayed if calculation condition is not fulfilled.
    qColumnOrder: list[int]
      The order of the columns.
    """

    qStateName: str = None
    qSize: Size = None
    qError: NxValidationError = None
    qDimensionInfo: list[NxDimensionInfo] = None
    qMeasureInfo: list[NxMeasureInfo] = None
    qEffectiveInterColumnSortOrder: list[int] = None
    qGrandTotalRow: list[NxCell] = None
    qDataPages: list[NxDataPage] = None
    qPivotDataPages: list[NxPivotPage] = None
    qStackedDataPages: list[NxStackPage] = None
    qMode: str = None
    qNoOfLeftDims: int = None
    qIndentMode: bool = None
    qLastExpandedPos: NxCellPosition = None
    qHasOtherValues: bool = None
    qTitle: str = None
    qTreeNodesOnDim: list[int] = None
    qCalcCondMsg: str = None
    qColumnOrder: list[int] = None

    def __init__(self_, **kvargs):
        if "qStateName" in kvargs:
            if (
                type(kvargs["qStateName"]).__name__
                is self_.__annotations__["qStateName"]
            ):
                self_.qStateName = kvargs["qStateName"]
            else:
                self_.qStateName = kvargs["qStateName"]
        if "qSize" in kvargs:
            if type(kvargs["qSize"]).__name__ is self_.__annotations__["qSize"]:
                self_.qSize = kvargs["qSize"]
            else:
                self_.qSize = Size(**kvargs["qSize"])
        if "qError" in kvargs:
            if type(kvargs["qError"]).__name__ is self_.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(**kvargs["qError"])
        if "qDimensionInfo" in kvargs:
            if (
                type(kvargs["qDimensionInfo"]).__name__
                is self_.__annotations__["qDimensionInfo"]
            ):
                self_.qDimensionInfo = kvargs["qDimensionInfo"]
            else:
                self_.qDimensionInfo = [
                    NxDimensionInfo(**e) for e in kvargs["qDimensionInfo"]
                ]
        if "qMeasureInfo" in kvargs:
            if (
                type(kvargs["qMeasureInfo"]).__name__
                is self_.__annotations__["qMeasureInfo"]
            ):
                self_.qMeasureInfo = kvargs["qMeasureInfo"]
            else:
                self_.qMeasureInfo = [
                    NxMeasureInfo(**e) for e in kvargs["qMeasureInfo"]
                ]
        if "qEffectiveInterColumnSortOrder" in kvargs:
            if (
                type(kvargs["qEffectiveInterColumnSortOrder"]).__name__
                is self_.__annotations__["qEffectiveInterColumnSortOrder"]
            ):
                self_.qEffectiveInterColumnSortOrder = kvargs[
                    "qEffectiveInterColumnSortOrder"
                ]
            else:
                self_.qEffectiveInterColumnSortOrder = kvargs[
                    "qEffectiveInterColumnSortOrder"
                ]
        if "qGrandTotalRow" in kvargs:
            if (
                type(kvargs["qGrandTotalRow"]).__name__
                is self_.__annotations__["qGrandTotalRow"]
            ):
                self_.qGrandTotalRow = kvargs["qGrandTotalRow"]
            else:
                self_.qGrandTotalRow = [NxCell(**e) for e in kvargs["qGrandTotalRow"]]
        if "qDataPages" in kvargs:
            if (
                type(kvargs["qDataPages"]).__name__
                is self_.__annotations__["qDataPages"]
            ):
                self_.qDataPages = kvargs["qDataPages"]
            else:
                self_.qDataPages = [NxDataPage(**e) for e in kvargs["qDataPages"]]
        if "qPivotDataPages" in kvargs:
            if (
                type(kvargs["qPivotDataPages"]).__name__
                is self_.__annotations__["qPivotDataPages"]
            ):
                self_.qPivotDataPages = kvargs["qPivotDataPages"]
            else:
                self_.qPivotDataPages = [
                    NxPivotPage(**e) for e in kvargs["qPivotDataPages"]
                ]
        if "qStackedDataPages" in kvargs:
            if (
                type(kvargs["qStackedDataPages"]).__name__
                is self_.__annotations__["qStackedDataPages"]
            ):
                self_.qStackedDataPages = kvargs["qStackedDataPages"]
            else:
                self_.qStackedDataPages = [
                    NxStackPage(**e) for e in kvargs["qStackedDataPages"]
                ]
        if "qMode" in kvargs:
            if type(kvargs["qMode"]).__name__ is self_.__annotations__["qMode"]:
                self_.qMode = kvargs["qMode"]
            else:
                self_.qMode = kvargs["qMode"]
        if "qNoOfLeftDims" in kvargs:
            if (
                type(kvargs["qNoOfLeftDims"]).__name__
                is self_.__annotations__["qNoOfLeftDims"]
            ):
                self_.qNoOfLeftDims = kvargs["qNoOfLeftDims"]
            else:
                self_.qNoOfLeftDims = kvargs["qNoOfLeftDims"]
        if "qIndentMode" in kvargs:
            if (
                type(kvargs["qIndentMode"]).__name__
                is self_.__annotations__["qIndentMode"]
            ):
                self_.qIndentMode = kvargs["qIndentMode"]
            else:
                self_.qIndentMode = kvargs["qIndentMode"]
        if "qLastExpandedPos" in kvargs:
            if (
                type(kvargs["qLastExpandedPos"]).__name__
                is self_.__annotations__["qLastExpandedPos"]
            ):
                self_.qLastExpandedPos = kvargs["qLastExpandedPos"]
            else:
                self_.qLastExpandedPos = NxCellPosition(**kvargs["qLastExpandedPos"])
        if "qHasOtherValues" in kvargs:
            if (
                type(kvargs["qHasOtherValues"]).__name__
                is self_.__annotations__["qHasOtherValues"]
            ):
                self_.qHasOtherValues = kvargs["qHasOtherValues"]
            else:
                self_.qHasOtherValues = kvargs["qHasOtherValues"]
        if "qTitle" in kvargs:
            if type(kvargs["qTitle"]).__name__ is self_.__annotations__["qTitle"]:
                self_.qTitle = kvargs["qTitle"]
            else:
                self_.qTitle = kvargs["qTitle"]
        if "qTreeNodesOnDim" in kvargs:
            if (
                type(kvargs["qTreeNodesOnDim"]).__name__
                is self_.__annotations__["qTreeNodesOnDim"]
            ):
                self_.qTreeNodesOnDim = kvargs["qTreeNodesOnDim"]
            else:
                self_.qTreeNodesOnDim = kvargs["qTreeNodesOnDim"]
        if "qCalcCondMsg" in kvargs:
            if (
                type(kvargs["qCalcCondMsg"]).__name__
                is self_.__annotations__["qCalcCondMsg"]
            ):
                self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
            else:
                self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
        if "qColumnOrder" in kvargs:
            if (
                type(kvargs["qColumnOrder"]).__name__
                is self_.__annotations__["qColumnOrder"]
            ):
                self_.qColumnOrder = kvargs["qColumnOrder"]
            else:
                self_.qColumnOrder = kvargs["qColumnOrder"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class HyperCubeDef:
    """
    Defines the properties of a hypercube.
    For more information about the definition of a hypercube, see Generic object.

    Attributes
    ----------
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    qDimensions: list[NxDimension]
      Array of dimensions.
    qMeasures: list[NxMeasure]
      Array of measures.
    qInterColumnSortOrder: list[int]
      Defines the sort order of the columns in the hypercube.
      Column numbers are separated by a comma.
      Example: [1,0,2] means that the first column to be sorted should be the column 1, followed by the column 0 and the column 2.
      The default sort order is the order in which the dimensions and measures have been defined in the hypercube. By default, the pseudo-dimension (if any) is the most to the right in the array.
      The index of the pseudo-dimension (if any) is -1.
      Pseudo dimensions only apply for pivot tables with more than one measure.
      A pseudo dimension groups together the measures defined in a pivot table. You can neither collapse/expand a pseudo dimension nor make any selections in it.
      Stacked pivot tables can only contain one measure.
    qSuppressZero: bool
      Removes zero values.
    qSuppressMissing: bool
      Removes missing values.
    qInitialDataFetch: list[NxPage]
      Initial data set.
    qReductionMode: str
      One of:

      • N or DATA_REDUCTION_NONE

      • D1 or DATA_REDUCTION_ONEDIM

      • S or DATA_REDUCTION_SCATTERED

      • C or DATA_REDUCTION_CLUSTERED

      • ST or DATA_REDUCTION_STACKED
    qMode: str
      Defines the way the data are handled internally by the engine.
      Default value is DATAMODE_STRAIGHT_ .
      A pivot table can contain several dimensions and measures whereas a stacked pivot table can contain several dimensions but only one measure.

      One of:

      • S or DATA_MODE_STRAIGHT

      • P or DATA_MODE_PIVOT

      • K or DATA_MODE_PIVOT_STACK

      • T or DATA_MODE_TREE

      • D or DATA_MODE_DYNAMIC
    qPseudoDimPos: int
    qNoOfLeftDims: int
      Number of left dimensions.
      Default value is -1. In that case, all dimensions are left dimensions.
      Hidden dimensions (e.g. due to unfulfilled calc condition on dimension level) is still counted in this context.
      The index related to each left dimension depends on the position of the pseudo dimension (if any).
      For example, a pivot table with:

      • Four dimensions in the following order: Country, City, Product and Category.

      • One pseudo dimension in position 1 (the position is defined in qInterColumnSortOrder )
      _qInterColumnSortOrder_ is (0,-1,1,2,3).

      • Three left dimensions ( qNoOfLeftDims is set to 3).

      implies that:

      • The index 0 corresponds to the left dimension Country.

      • The index 1 corresponds to the pseudo dimension.

      • The index 2 corresponds to the left dimension City.

      • Product and Category are top dimensions.

      Another example:

      • Four dimensions in the following order: Country, City, Product and Category.

      • Three left dimensions ( qNoOfLeftDims is set to 3).

      • One pseudo dimension.

      • The property qInterColumnSortOrder is left empty.

      Implies that:

      • The index 0 corresponds to the left dimension Country.

      • The index 1 corresponds to the left dimension City.

      • The index 2 corresponds to the left dimension Product.

      • Category is a top dimension.

      • The pseudo dimension is a top dimension.
    qAlwaysFullyExpanded: bool
      If this property is set to true, the cells are always expanded. It implies that it is not possible to collapse any cells.
      The default value is false.
    qMaxStackedCells: int
      Maximum number of cells for an initial data fetch (set in qInitialDataFetch ) when in stacked mode ( qMode is K).
      The default value is 5000.
    qPopulateMissing: bool
      If this property is set to true, the missing symbols (if any) are replaced by 0 if the value is a numeric and by an empty string if the value is a string.
      The default value is false.
    qShowTotalsAbove: bool
      If set to true, the total (if any) is shown on the first row.
      The default value is false.
    qIndentMode: bool
      This property applies for pivot tables and allows to change the layout of the table. An indentation is added to the beginning of each row.
      The default value is false.
    qCalcCond: ValueExpr
      Specifies a calculation condition, which must be fulfilled for the hypercube to be (re)calculated.
      As long as the condition is not met, the engine does not perform a new calculation.
      This property is optional. By default, there is no calculation condition.
    qSortbyYValue: int
      To enable the sorting by ascending or descending order in the values of a measure.
      This property applies to pivot tables and stacked pivot tables.
      In the case of a pivot table, the measure or pseudo dimension should be defined as a top dimension. The sorting is restricted to the values of the first measure in a pivot table.
    qTitle: StringExpr
      Title of the hypercube, for example the title of a chart.
    qCalcCondition: NxCalcCond
      Specifies a calculation condition object.
      If CalcCondition.Cond is not fulfilled, the hypercube is not calculated and CalcCondition.Msg is evaluated.
      By default, there is no calculation condition.
      This property is optional.
    qColumnOrder: list[int]
      The order of the columns.
    qExpansionState: list[ExpansionData]
      Expansion state per dimension for pivot mode ( qMode is P).
    qDynamicScript: list[str]
      Hypercube Modifier Dynamic script string
    qContextSetExpression: str
      Set Expression valid for the whole cube. Used to limit computations to the set specified. *
    """

    qStateName: str = None
    qDimensions: list[NxDimension] = None
    qMeasures: list[NxMeasure] = None
    qInterColumnSortOrder: list[int] = None
    qSuppressZero: bool = None
    qSuppressMissing: bool = None
    qInitialDataFetch: list[NxPage] = None
    qReductionMode: str = None
    qMode: str = "DATA_MODE_STRAIGHT"
    qPseudoDimPos: int = -1
    qNoOfLeftDims: int = -1
    qAlwaysFullyExpanded: bool = None
    qMaxStackedCells: int = 5000
    qPopulateMissing: bool = None
    qShowTotalsAbove: bool = None
    qIndentMode: bool = None
    qCalcCond: ValueExpr = None
    qSortbyYValue: int = None
    qTitle: StringExpr = None
    qCalcCondition: NxCalcCond = None
    qColumnOrder: list[int] = None
    qExpansionState: list[ExpansionData] = None
    qDynamicScript: list[str] = None
    qContextSetExpression: str = None

    def __init__(self_, **kvargs):
        if "qStateName" in kvargs:
            if (
                type(kvargs["qStateName"]).__name__
                is self_.__annotations__["qStateName"]
            ):
                self_.qStateName = kvargs["qStateName"]
            else:
                self_.qStateName = kvargs["qStateName"]
        if "qDimensions" in kvargs:
            if (
                type(kvargs["qDimensions"]).__name__
                is self_.__annotations__["qDimensions"]
            ):
                self_.qDimensions = kvargs["qDimensions"]
            else:
                self_.qDimensions = [NxDimension(**e) for e in kvargs["qDimensions"]]
        if "qMeasures" in kvargs:
            if type(kvargs["qMeasures"]).__name__ is self_.__annotations__["qMeasures"]:
                self_.qMeasures = kvargs["qMeasures"]
            else:
                self_.qMeasures = [NxMeasure(**e) for e in kvargs["qMeasures"]]
        if "qInterColumnSortOrder" in kvargs:
            if (
                type(kvargs["qInterColumnSortOrder"]).__name__
                is self_.__annotations__["qInterColumnSortOrder"]
            ):
                self_.qInterColumnSortOrder = kvargs["qInterColumnSortOrder"]
            else:
                self_.qInterColumnSortOrder = kvargs["qInterColumnSortOrder"]
        if "qSuppressZero" in kvargs:
            if (
                type(kvargs["qSuppressZero"]).__name__
                is self_.__annotations__["qSuppressZero"]
            ):
                self_.qSuppressZero = kvargs["qSuppressZero"]
            else:
                self_.qSuppressZero = kvargs["qSuppressZero"]
        if "qSuppressMissing" in kvargs:
            if (
                type(kvargs["qSuppressMissing"]).__name__
                is self_.__annotations__["qSuppressMissing"]
            ):
                self_.qSuppressMissing = kvargs["qSuppressMissing"]
            else:
                self_.qSuppressMissing = kvargs["qSuppressMissing"]
        if "qInitialDataFetch" in kvargs:
            if (
                type(kvargs["qInitialDataFetch"]).__name__
                is self_.__annotations__["qInitialDataFetch"]
            ):
                self_.qInitialDataFetch = kvargs["qInitialDataFetch"]
            else:
                self_.qInitialDataFetch = [
                    NxPage(**e) for e in kvargs["qInitialDataFetch"]
                ]
        if "qReductionMode" in kvargs:
            if (
                type(kvargs["qReductionMode"]).__name__
                is self_.__annotations__["qReductionMode"]
            ):
                self_.qReductionMode = kvargs["qReductionMode"]
            else:
                self_.qReductionMode = kvargs["qReductionMode"]
        if "qMode" in kvargs:
            if type(kvargs["qMode"]).__name__ is self_.__annotations__["qMode"]:
                self_.qMode = kvargs["qMode"]
            else:
                self_.qMode = kvargs["qMode"]
        if "qPseudoDimPos" in kvargs:
            if (
                type(kvargs["qPseudoDimPos"]).__name__
                is self_.__annotations__["qPseudoDimPos"]
            ):
                self_.qPseudoDimPos = kvargs["qPseudoDimPos"]
            else:
                self_.qPseudoDimPos = kvargs["qPseudoDimPos"]
        if "qNoOfLeftDims" in kvargs:
            if (
                type(kvargs["qNoOfLeftDims"]).__name__
                is self_.__annotations__["qNoOfLeftDims"]
            ):
                self_.qNoOfLeftDims = kvargs["qNoOfLeftDims"]
            else:
                self_.qNoOfLeftDims = kvargs["qNoOfLeftDims"]
        if "qAlwaysFullyExpanded" in kvargs:
            if (
                type(kvargs["qAlwaysFullyExpanded"]).__name__
                is self_.__annotations__["qAlwaysFullyExpanded"]
            ):
                self_.qAlwaysFullyExpanded = kvargs["qAlwaysFullyExpanded"]
            else:
                self_.qAlwaysFullyExpanded = kvargs["qAlwaysFullyExpanded"]
        if "qMaxStackedCells" in kvargs:
            if (
                type(kvargs["qMaxStackedCells"]).__name__
                is self_.__annotations__["qMaxStackedCells"]
            ):
                self_.qMaxStackedCells = kvargs["qMaxStackedCells"]
            else:
                self_.qMaxStackedCells = kvargs["qMaxStackedCells"]
        if "qPopulateMissing" in kvargs:
            if (
                type(kvargs["qPopulateMissing"]).__name__
                is self_.__annotations__["qPopulateMissing"]
            ):
                self_.qPopulateMissing = kvargs["qPopulateMissing"]
            else:
                self_.qPopulateMissing = kvargs["qPopulateMissing"]
        if "qShowTotalsAbove" in kvargs:
            if (
                type(kvargs["qShowTotalsAbove"]).__name__
                is self_.__annotations__["qShowTotalsAbove"]
            ):
                self_.qShowTotalsAbove = kvargs["qShowTotalsAbove"]
            else:
                self_.qShowTotalsAbove = kvargs["qShowTotalsAbove"]
        if "qIndentMode" in kvargs:
            if (
                type(kvargs["qIndentMode"]).__name__
                is self_.__annotations__["qIndentMode"]
            ):
                self_.qIndentMode = kvargs["qIndentMode"]
            else:
                self_.qIndentMode = kvargs["qIndentMode"]
        if "qCalcCond" in kvargs:
            if type(kvargs["qCalcCond"]).__name__ is self_.__annotations__["qCalcCond"]:
                self_.qCalcCond = kvargs["qCalcCond"]
            else:
                self_.qCalcCond = ValueExpr(**kvargs["qCalcCond"])
        if "qSortbyYValue" in kvargs:
            if (
                type(kvargs["qSortbyYValue"]).__name__
                is self_.__annotations__["qSortbyYValue"]
            ):
                self_.qSortbyYValue = kvargs["qSortbyYValue"]
            else:
                self_.qSortbyYValue = kvargs["qSortbyYValue"]
        if "qTitle" in kvargs:
            if type(kvargs["qTitle"]).__name__ is self_.__annotations__["qTitle"]:
                self_.qTitle = kvargs["qTitle"]
            else:
                self_.qTitle = StringExpr(**kvargs["qTitle"])
        if "qCalcCondition" in kvargs:
            if (
                type(kvargs["qCalcCondition"]).__name__
                is self_.__annotations__["qCalcCondition"]
            ):
                self_.qCalcCondition = kvargs["qCalcCondition"]
            else:
                self_.qCalcCondition = NxCalcCond(**kvargs["qCalcCondition"])
        if "qColumnOrder" in kvargs:
            if (
                type(kvargs["qColumnOrder"]).__name__
                is self_.__annotations__["qColumnOrder"]
            ):
                self_.qColumnOrder = kvargs["qColumnOrder"]
            else:
                self_.qColumnOrder = kvargs["qColumnOrder"]
        if "qExpansionState" in kvargs:
            if (
                type(kvargs["qExpansionState"]).__name__
                is self_.__annotations__["qExpansionState"]
            ):
                self_.qExpansionState = kvargs["qExpansionState"]
            else:
                self_.qExpansionState = [
                    ExpansionData(**e) for e in kvargs["qExpansionState"]
                ]
        if "qDynamicScript" in kvargs:
            if (
                type(kvargs["qDynamicScript"]).__name__
                is self_.__annotations__["qDynamicScript"]
            ):
                self_.qDynamicScript = kvargs["qDynamicScript"]
            else:
                self_.qDynamicScript = kvargs["qDynamicScript"]
        if "qContextSetExpression" in kvargs:
            if (
                type(kvargs["qContextSetExpression"]).__name__
                is self_.__annotations__["qContextSetExpression"]
            ):
                self_.qContextSetExpression = kvargs["qContextSetExpression"]
            else:
                self_.qContextSetExpression = kvargs["qContextSetExpression"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ListObject:
    """
    Renders the properties of a list object. Is the layout for ListObjectDef.
    For more information about the definition of a list object, see Generic object.
    ListObject is used by the GetLayout Method to display the properties of a list object.

    Attributes
    ----------
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    qSize: Size
      Defines the size of a list object.
    qError: NxValidationError
      This parameter is optional and is displayed in case of error.
    qDimensionInfo: NxDimensionInfo
      Information about the dimension.
    qExpressions: list[NxListObjectExpression]
      Lists the expressions in the list object.
    qDataPages: list[NxDataPage]
      Set of data.
      Is empty if nothing has been defined in qInitialDataFetch in ListObjectDef.
    """

    qStateName: str = None
    qSize: Size = None
    qError: NxValidationError = None
    qDimensionInfo: NxDimensionInfo = None
    qExpressions: list[NxListObjectExpression] = None
    qDataPages: list[NxDataPage] = None

    def __init__(self_, **kvargs):
        if "qStateName" in kvargs:
            if (
                type(kvargs["qStateName"]).__name__
                is self_.__annotations__["qStateName"]
            ):
                self_.qStateName = kvargs["qStateName"]
            else:
                self_.qStateName = kvargs["qStateName"]
        if "qSize" in kvargs:
            if type(kvargs["qSize"]).__name__ is self_.__annotations__["qSize"]:
                self_.qSize = kvargs["qSize"]
            else:
                self_.qSize = Size(**kvargs["qSize"])
        if "qError" in kvargs:
            if type(kvargs["qError"]).__name__ is self_.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(**kvargs["qError"])
        if "qDimensionInfo" in kvargs:
            if (
                type(kvargs["qDimensionInfo"]).__name__
                is self_.__annotations__["qDimensionInfo"]
            ):
                self_.qDimensionInfo = kvargs["qDimensionInfo"]
            else:
                self_.qDimensionInfo = NxDimensionInfo(**kvargs["qDimensionInfo"])
        if "qExpressions" in kvargs:
            if (
                type(kvargs["qExpressions"]).__name__
                is self_.__annotations__["qExpressions"]
            ):
                self_.qExpressions = kvargs["qExpressions"]
            else:
                self_.qExpressions = [
                    NxListObjectExpression(**e) for e in kvargs["qExpressions"]
                ]
        if "qDataPages" in kvargs:
            if (
                type(kvargs["qDataPages"]).__name__
                is self_.__annotations__["qDataPages"]
            ):
                self_.qDataPages = kvargs["qDataPages"]
            else:
                self_.qDataPages = [NxDataPage(**e) for e in kvargs["qDataPages"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Qix:
    def abort_request(self, qRequestId: int) -> object:
        """
        Sets an abort flag on a specific request in the current engine session.

        • If an abort flag is set on a pending request, the request is aborted.

        • If an abort flag is set on an ongoing request, the engine checks to see if it is possible to abort the request.


        qRequestId: int
          Identifier of request to abort.

        """
        params = {}
        params["qRequestId"] = qRequestId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AbortRequest", handle, **params)
        return response

    def abort_all(self) -> object:
        """
        Sets an abort flag on all pending and ongoing requests in the current engine session.

        • If an abort flag is set on a pending request, the request is aborted.

        • If an abort flag is set on an ongoing request, the engine checks to see if it is possible to abort the request.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AbortAll", handle)
        return response

    def get_progress(self, qRequestId: int) -> ProgressData:
        """
        Gives information about the progress of the DoReload and DoSave calls.
        For more information on DoReload and DoSave, see the DoReload Method and DoSave Method.


        qRequestId: int
          Identifier of the DoReload or DoSave request or 0.
          Complete information is returned if the identifier of the request is given.
          If the identifier is 0, less information is given. Progress messages and error messages are returned but information like when the request started and finished is not returned.

        """
        params = {}
        params["qRequestId"] = qRequestId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetProgress", handle, **params)["qProgressData"]
        obj = ProgressData(**response)
        obj._session = self._session
        return obj

    def get_interact(self, qRequestId: int) -> object:
        """
        Retrieves information on the user interaction that is requested by the engine.
        Engine can request user interactions only during script reload and when the reload is performed in debug mode ( qDebug is set to true when using the DoReload method ).
        When running reload in debug mode, the engine pauses the script execution to receive data about user interaction. The engine can pause:

        • Before executing a new script statement.

        • When an error occurs while executing the script.

        • When the script execution is finished.

        To know if the engine is paused and waits for a response to an interaction request, the GetProgress method should be used. The engine waits for a response if the property qUserInteractionWanted is set to true in the response of the GetProgress request.


        qRequestId: int
          Identifier of the request.
          Corresponds to the identifier of the DoReload request.

        """
        params = {}
        params["qRequestId"] = qRequestId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetInteract", handle, **params)
        return response

    def interact_done(self, qRequestId: int, qDef: InteractDef) -> object:
        """
        Informs the engine that a user interaction (which was earlier requested by the engine) was performed and indicates to the engine what to do next.


        qRequestId: int
          Identifier of the request.
          Corresponds to the identifier of the DoReload request.

        qDef: InteractDef
          User response to the current interaction.

        """
        params = {}
        params["qRequestId"] = qRequestId
        params["qDef"] = qDef
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("InteractDone", handle, **params)
        return response

    def get_authenticated_user(self) -> str:
        """
        Retrieves information about the authenticated user.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAuthenticatedUser", handle)["qReturn"]
        return response

    def get_active_doc(self) -> Doc:
        """
        Returns the handle of the current app.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetActiveDoc", handle)["qReturn"]
        obj = Doc(**response)
        obj._session = self._session
        return obj

    def allow_create_app(self) -> bool:
        """
        Indicates whether or not a user is able to create an app.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AllowCreateApp", handle)["qReturn"]
        return response

    def is_desktop_mode(self) -> bool:
        """
        Indicates whether the user is working in Qlik Sense Desktop.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("IsDesktopMode", handle)["qReturn"]
        return response

    def cancel_request(self, qRequestId: int) -> object:
        """
        Cancels an ongoing request. The request is stopped.


        qRequestId: int
          Identifier of the request to stop.

        """
        params = {}
        params["qRequestId"] = qRequestId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CancelRequest", handle, **params)
        return response

    def shutdown_process(self) -> object:
        """
        Shuts down the Qlik engine.
        This operation is possible only in Qlik Sense Desktop.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ShutdownProcess", handle)
        return response

    def replace_app_from_id(
        self, qTargetAppId: str, qSrcAppID: str, qIds: list[str]
    ) -> bool:
        """
        Replaces objects of a target app with the objects from a source app.
        The list of objects in the app to be replaced must be defined in qIds.
        The data model of the app cannot be updated.
        This operation is possible only in Qlik Sense Enterprise.

        The operation is successful if qSuccess is set to true.


        qTargetAppId: str
          Identifier (GUID) of the target app.
          The target app is the app to be replaced.

        qSrcAppID: str
          Identifier (GUID) of the source app.
          The objects in the source app will replace the objects in the target app.

        qIds: list[str]
          QRS identifiers (GUID) of the objects in the target app to be replaced. Only QRS-approved GUIDs are applicable.
          An object that is QRS-approved, is for example an object that has been published (for example, not private anymore).
          If an object is private, it should not be included in this list.
          If the array of identifiers contains objects that are not present in the source app, the objects related to these identifiers are removed from the target app.
          If qIds is empty, no objects are deleted in the target app.

        """
        params = {}
        params["qTargetAppId"] = qTargetAppId
        params["qSrcAppID"] = qSrcAppID
        params["qIds"] = qIds
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ReplaceAppFromID", handle, **params)["qSuccess"]
        return response

    def publish_app(self, qAppId: str, qName: str, qStreamId: str) -> object:
        """
        Publishes an app to the supplied stream.


        qAppId: str
          The Id of the app to publish.

        qName: str
          The name of the app to publish.

        qStreamId: str
          The stream Id of the app to publish.

        """
        params = {}
        params["qAppId"] = qAppId
        params["qName"] = qName
        params["qStreamId"] = qStreamId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("PublishApp", handle, **params)
        return response

    def is_personal_mode(self) -> bool:
        """
        Deprecated
        Indicates whether or not the user is working in personal mode (Qlik Sense Desktop).


        """
        warnings.warn("IsPersonalMode is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("IsPersonalMode", handle)["qReturn"]
        return response

    def get_unique_id(self) -> str:
        """
        Returns the unique identifier of the endpoint for the current user in the current app.
        This unique identifier can be used for logging purposes.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetUniqueID", handle)["qUniqueID"]
        return response

    def open_doc(
        self,
        qDocName: str,
        qUserName: str = None,
        qPassword: str = None,
        qSerial: str = None,
        qNoData: bool = None,
    ) -> Doc:
        """
        Opens an app and checks if the app needs to be migrated (if the app is deprecated).
        The OpenDoc method compares the version of the app with the version of Qlik Sense and migrates the app to the current version of Qlik Sense if necessary. Once the migration is done, the app is opened.
        If no migration is needed, the app is opened immediately.
        The following applies:

        • The app version is lower than 0.95: no migration is done. Apps older than the version 0.95 are not supported.

        • The app version is at least 0.95 and less than the Qlik Sense version: the app is migrated and then opened.

        • Qlik Sense and the app have the same version: the app is opened, no migration is needed.

        If the app is read-only, the app migration cannot occur. An error message is sent.

        Backups:

        In Qlik Sense Desktop, apps are automatically backed up before a migration.
        The backup files are located in %userprofile%\Documents\Qlik\Sense\AppsBackup\<Qlik Sense Desktop version>.
        In Qlik Sense Enterprise, no automatic back up is run. The back up should be done manually.


        qDocName: str
          The GUID (in Qlik Sense Enterprise) or Name (in Qlik Sense Desktop) of the app to retrieve.

        qUserName: str
          Name of the user that opens the app.

        qPassword: str
          Password of the user.

        qSerial: str
          Current Qlik Sense serial number.

        qNoData: bool
          Set this parameter to true to be able to open an app without loading its data.
          When this parameter is set to true, the objects in the app are present but contain no data. The script can be edited and reloaded.
          The default value is false.

        """
        params = {}
        params["qDocName"] = qDocName
        if qUserName is not None:
            params["qUserName"] = qUserName
        if qPassword is not None:
            params["qPassword"] = qPassword
        if qSerial is not None:
            params["qSerial"] = qSerial
        if qNoData is not None:
            params["qNoData"] = qNoData
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("OpenDoc", handle, **params)["qReturn"]
        obj = Doc(**response)
        obj._session = self._session
        return obj

    def product_version(self) -> str:
        """
        Deprecated
        Returns the Qlik Sense version number.


        """
        warnings.warn("ProductVersion is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ProductVersion", handle)["qReturn"]
        return response

    def get_app_entry(self, qAppID: str) -> AppEntry:
        """
        Retrieves the meta data of an app.


        qAppID: str
          Identifier of the app, as returned by the CreateApp method.
          One of:

          • Path and name of the app (Qlik Sense Desktop)

          • GUID (Qlik Sense Enterprise)

        """
        params = {}
        params["qAppID"] = qAppID
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAppEntry", handle, **params)["qEntry"]
        obj = AppEntry(**response)
        obj._session = self._session
        return obj

    def configure_reload(
        self, qCancelOnScriptError: bool, qUseErrorData: bool, qInteractOnError: bool
    ) -> object:
        """
        Configures the engine's behavior during a reload.
        The ConfigureReload method should be run before the DoReload method.


        qCancelOnScriptError: bool
          If set to true, the script execution is halted on error.
          Otherwise, the engine continues the script execution.
          This parameter is relevant only if the variable ErrorMode is set to 1.

        qUseErrorData: bool
          If set to true, any script execution error is returned in qErrorData by the GetProgress method.

        qInteractOnError: bool
          If set to true, the script execution is halted on error and the engine is waiting for an interaction to be performed. If the result from the interaction is 1 (_qDef.qResult_ is 1), the engine continues the script execution otherwise the execution is halted.
          This parameter is relevant only if the variable ErrorMode is set to 1 and the script is run in debug mode (_qDebug_ is set to true when calling the DoReload method).

        """
        params = {}
        params["qCancelOnScriptError"] = qCancelOnScriptError
        params["qUseErrorData"] = qUseErrorData
        params["qInteractOnError"] = qInteractOnError
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ConfigureReload", handle, **params)
        return response

    def cancel_reload(self) -> object:
        """
        Cancels an ongoing reload. The reload of the app is stopped. The indexation can be canceled and true is still the return value of the reload task.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CancelReload", handle)
        return response

    def get_bnf(self, qBnfType: str) -> list[BNFDef]:
        """
        Deprecated
        Gets the current Backus-Naur Form (BNF) grammar of the Qlik engine scripting language. The BNF rules define the syntax for the script statements and the script or chart functions.
        In the Qlik engine BNF grammar, a token is a string of one or more characters that is significant as a group. For example, a token could be a function name, a number, a letter, a parenthesis, and so on.


        qBnfType: str
          Returns a set of rules defining the syntax for:

          • The script statements and the script functions if qBnfType is set to S.

          • The chart functions if qBnfType is set to E.

          One of:

          • S or SCRIPT_TEXT_SCRIPT

          • E or SCRIPT_TEXT_EXPRESSION

        """
        warnings.warn("GetBNF is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qBnfType"] = qBnfType
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetBNF", handle, **params)["qBnfDefs"]
        return [BNFDef(e) for e in response]

    def get_functions(self, qGroup: str = None) -> list[Function]:
        """
        Gets the list of all the script functions.


        qGroup: str
          Name of the group.
          Default is all groups.

          One of:

          • ALL or FUNC_GROUP_ALL

          • U or FUNC_GROUP_UNKNOWN

          • NONE or FUNC_GROUP_NONE

          • AGGR or FUNC_GROUP_AGGR

          • NUM or FUNC_GROUP_NUMERIC

          • RNG or FUNC_GROUP_RANGE

          • EXP or FUNC_GROUP_EXPONENTIAL_AND_LOGARITHMIC

          • TRIG or FUNC_GROUP_TRIGONOMETRIC_AND_HYPERBOLIC

          • FIN or FUNC_GROUP_FINANCIAL

          • MATH or FUNC_GROUP_MATH_CONSTANT_AND_PARAM_FREE

          • COUNT or FUNC_GROUP_COUNTER

          • STR or FUNC_GROUP_STRING

          • MAPP or FUNC_GROUP_MAPPING

          • RCRD or FUNC_GROUP_INTER_RECORD

          • CND or FUNC_GROUP_CONDITIONAL

          • LOG or FUNC_GROUP_LOGICAL

          • NULL or FUNC_GROUP_NULL

          • SYS or FUNC_GROUP_SYSTEM

          • FILE or FUNC_GROUP_FILE

          • TBL or FUNC_GROUP_TABLE

          • DATE or FUNC_GROUP_DATE_AND_TIME

          • NUMI or FUNC_GROUP_NUMBER_INTERPRET

          • FRMT or FUNC_GROUP_FORMATTING

          • CLR or FUNC_GROUP_COLOR

          • RNK or FUNC_GROUP_RANKING

          • GEO or FUNC_GROUP_GEO

          • EXT or FUNC_GROUP_EXTERNAL

          • PROB or FUNC_GROUP_PROBABILITY

          • ARRAY or FUNC_GROUP_ARRAY

          • LEG or FUNC_GROUP_LEGACY

        """
        params = {}
        if qGroup is not None:
            params["qGroup"] = qGroup
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFunctions", handle, **params)["qFunctions"]
        return [Function(e) for e in response]

    def get_odbc_dsns(self) -> list[OdbcDsn]:
        """
        Returns the list of the ODBC connectors that are installed in the system.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetOdbcDsns", handle)["qOdbcDsns"]
        return [OdbcDsn(e) for e in response]

    def get_ole_db_providers(self) -> list[OleDbProvider]:
        """
        Returns the list of the OLEDB providers installed on the system.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetOleDbProviders", handle)["qOleDbProviders"]
        return [OleDbProvider(e) for e in response]

    def get_databases_from_connection_string(
        self, qConnection: Connection
    ) -> list[Database]:
        """
        Lists the databases in a ODBC, OLEDB or CUSTOM data source.


        qConnection: Connection
          Information about the connection.

        """
        params = {}
        params["qConnection"] = qConnection
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send(
            "GetDatabasesFromConnectionString", handle, **params
        )["qDatabases"]
        return [Database(e) for e in response]

    def is_valid_connection_string(self, qConnection: Connection) -> bool:
        """
        Checks if a connection string is valid.


        qConnection: Connection
          Information about the connection.

        """
        params = {}
        params["qConnection"] = qConnection
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("IsValidConnectionString", handle, **params)[
            "qReturn"
        ]
        return response

    def get_default_app_folder(self) -> str:
        """
        Returns the folder where the apps are stored.
        This method applies only if running Qlik Sense Desktop.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDefaultAppFolder", handle)["qPath"]
        return response

    def get_logical_drive_strings(self) -> list[DriveInfo]:
        """
        Lists the logical drives in the system.
        This method applies only if running Qlik Sense Desktop.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLogicalDriveStrings", handle)["qDrives"]
        return [DriveInfo(e) for e in response]

    def get_folder_items_for_path(self, qPath: str) -> list[FolderItem]:
        """
        Returns the files and folders located at a specified path.


        qPath: str
          Absolute or relative path.
          Relative paths are relative to the default Apps folder.

          In Qlik Sense Enterprise::

          The list is generated by the QRS. The GetDocList method only returns documents the current user is allowed to access.

          In Qlik Sense Desktop::

          The apps are located in C:\\Users\<user name>\Documents\Qlik\Sense\Apps.

        """
        params = {}
        params["qPath"] = qPath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFolderItemsForPath", handle, **params)[
            "qFolderItems"
        ]
        return [FolderItem(e) for e in response]

    def get_supported_code_pages(self) -> list[CodePage]:
        """
        Lists the supported code pages.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetSupportedCodePages", handle)["qCodePages"]
        return [CodePage(e) for e in response]

    def get_custom_connectors(self, qReloadList: bool = None) -> list[CustomConnector]:
        """
        List the custom connectors available in the system.


        qReloadList: bool
          Sets if the list of custom connectors should be reloaded or not.
          If set to false, only the connectors that were returned the previous time are returned. If new connectors have been added since the last call to the GetCustomConnectors method was made, the new connectors are not returned.
          If set to true, the GetCustomConnectors method looks for new connectors in the file system.
          The default value is false.

        """
        params = {}
        if qReloadList is not None:
            params["qReloadList"] = qReloadList
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetCustomConnectors", handle, **params)[
            "qConnectors"
        ]
        return [CustomConnector(e) for e in response]

    def get_stream_list(self) -> list[NxStreamListEntry]:
        """
        Deprecated
        Lists the streams.


        """
        warnings.warn("GetStreamList is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetStreamList", handle)["qStreamList"]
        return [NxStreamListEntry(e) for e in response]

    def engine_version(self) -> NxEngineVersion:
        """
        Returns the version number of the Qlik engine component.


        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("EngineVersion", handle)["qVersion"]
        obj = NxEngineVersion(**response)
        obj._session = self._session
        return obj

    def get_base_bnf(self, qBnfType: str) -> object:
        """
        Gets the current Backus-Naur Form (BNF) grammar of the Qlik engine scripting language, as well as a string hash calculated from that grammar. The BNF rules define the syntax for the script statements and the script or chart functions. If the hash changes between subsequent calls to this method, this indicates that the BNF has changed.
        In the Qlik engine grammars, a token is a string of one or more characters that is significant as a group. For example, a token could be a function name, a number, a letter, a parenthesis, and so on.


        qBnfType: str
          The type of grammar to return:

          • The script statements and the script functions if qBnfType is set to S.

          • The chart functions if qBnfType is set to E.

          One of:

          • S or SCRIPT_TEXT_SCRIPT

          • E or SCRIPT_TEXT_EXPRESSION

        """
        params = {}
        params["qBnfType"] = qBnfType
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetBaseBNF", handle, **params)
        return response

    def get_base_bnf_hash(self, qBnfType: str) -> str:
        """
        Gets a string hash calculated from the current Backus-Naur Form (BNF) grammar of the Qlik engine scripting language. If the hash changes between subsequent calls to this method, this indicates that the BNF grammar has changed.


        qBnfType: str
          The type of grammar to return:

          • The script statements and the script functions if qBnfType is set to S.

          • The chart functions if qBnfType is set to E.

          One of:

          • S or SCRIPT_TEXT_SCRIPT

          • E or SCRIPT_TEXT_EXPRESSION

        """
        params = {}
        params["qBnfType"] = qBnfType
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetBaseBNFHash", handle, **params)["qBnfHash"]
        return response

    def get_base_bnf_string(self, qBnfType: str) -> object:
        """
        Gets the current Backus-Naur Form (BNF) grammar of the Qlik engine scripting language, as well as a string hash calculated from that grammar. The BNF rules define the syntax for the script statements and the script or chart functions. If the hash changes between subsequent calls to this method, this indicates that the BNF has changed.
        In the Qlik engine grammars, a token is a string of one or more characters that is significant as a group. For example, a token could be a function name, a number, a letter, a parenthesis, and so on.


        qBnfType: str
          The type of grammar to return:

          • S: returns the script statements and the script functions.

          • E: returns the chart functions.

          One of:

          • S or SCRIPT_TEXT_SCRIPT

          • E or SCRIPT_TEXT_EXPRESSION

        """
        params = {}
        params["qBnfType"] = qBnfType
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetBaseBNFString", handle, **params)
        return response

    def save_as(self, qNewAppName: str) -> str:
        """
        Deprecated
        Save a copy of an app with a different name.
        Can be used to save a session app as an ordinary app.


        qNewAppName: str
          <Name of the saved app>

        """
        warnings.warn("SaveAs is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qNewAppName"] = qNewAppName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SaveAs", handle, **params)["qNewAppId"]
        return response
