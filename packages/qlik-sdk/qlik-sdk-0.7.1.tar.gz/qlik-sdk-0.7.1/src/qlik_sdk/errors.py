from enum import Enum


class CustomException(Exception):
    """
    CustomException represents a custom exception
    """


class CustomExceptionMsg(Enum):
    """
    CustomExceptionMsg - messages for custom exceptions
    """

    EMPTY_HOST = "Empty host in config"
    MISSING_CONFIG_PROPERTY = "Missing config property"
    UNSUPPORTED_AUTH_TYPE = "Unsupported authType"
    UNSUPPORTED_PROPERTY = "Unsupported property"
    NOT_IMPLEMENTED = "Not implemented"
