from enum import Enum


class AuthType(Enum):
    """AuthType - represents a type of authentication"""

    APIKey = "APIKey"
    """ bearer authentication - using token representing a user in your tenant """
