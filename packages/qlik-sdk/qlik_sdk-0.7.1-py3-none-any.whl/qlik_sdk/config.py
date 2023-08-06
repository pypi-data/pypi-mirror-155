from dataclasses import dataclass

from .auth_type import AuthType
from .errors import CustomException, CustomExceptionMsg


@dataclass
class Config:
    host: str
    auth_type: AuthType
    api_key: str = None

    def validate(self):
        """
        Validate that the config is correct,
        raises error for incorrect config
        """
        if not self.host:
            raise CustomException(CustomExceptionMsg.EMPTY_HOST.value)
        if not self.auth_type:
            raise CustomException(
                CustomExceptionMsg.MISSING_CONFIG_PROPERTY.value + ": auth_type"
            )
        if self.auth_type == AuthType.APIKey:
            if not self.api_key:
                raise CustomException(
                    CustomExceptionMsg.MISSING_CONFIG_PROPERTY.value + ": api_key"
                )
            allowed_keys = {"host", "auth_type", "api_key"}
            for k in self.__dict__.keys():
                if k not in allowed_keys:
                    raise CustomException(
                        CustomExceptionMsg.UNSUPPORTED_PROPERTY.value + ": " + k
                    )
        else:
            raise CustomException(
                CustomExceptionMsg.UNSUPPORTED_AUTH_TYPE.value
                + ": "
                + str(self.auth_type)
            )
