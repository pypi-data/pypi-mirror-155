"""Exceptions specific to the XRA-31."""
import os

import requests.exceptions


class Xra31Warning(Warning):
    """Warning for XRA-31."""


class Xra31Exception(Exception):
    """Raised in case of an XRA-31 related exception."""


class Xra31VersionException(Xra31Exception):
    """Raised in case of a client-server version mismatch."""


class Xra31RestException(Xra31Exception):
    """Raised in case of a REST Exception."""


class Xra31RestWarning(Xra31Warning):
    """Raised in case of a REST Warning."""


class Xra31ConnectionException(Xra31RestException):
    """Raised in case of a REST Connection Exception."""


class Xra31HttpException(Xra31RestException):
    """Raised in case of a REST HTTP Exception."""
    def __init__(self, error, *args, **kwargs):
        super().__init__(error, *args, **kwargs)
        self.details = []
        if isinstance(error, requests.exceptions.HTTPError):
            response = error.response.json()
            if "errorMsg" in response:
                self.details.append(response["errorMsg"])
            else:
                try:
                    for error_msg in iter(response):
                        if "msg" in error_msg:
                            self.details.append(error_msg["msg"])
                except TypeError:
                    pass

    def __str__(self) -> str:
        result = super().__str__()
        for msg in self.details:
            result += os.linesep + msg
        return result


class Xra31ClientException(Xra31HttpException):
    """Raised in case of a REST HTTP Client Exception."""


class Xra31ServerException(Xra31HttpException):
    """Raised in case of a REST HTTP Server Exception."""


class Xra31StateException(Xra31Exception):
    """Raised in case an action is incompatible with the current state."""


class Xra31FullAccessException(Xra31Exception):
    """Raised in case full-access mode is required."""


class Xra31TimeoutException(Xra31Exception):
    """Raised in case a timeout occurred."""


class Xra31ConfigurationException(Xra31Exception):
    """Raised in case of an inconsistent configuration for the XRA-31."""


class Xra31FileNotFoundException(Xra31Exception):
    """Raised in case a file can not be found on the XRA-31."""
