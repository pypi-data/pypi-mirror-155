"""Various XRA-31-specific decorators to ease implementation."""

import functools
import logging
import warnings

import requests.exceptions

from . import exceptions


def deprecated(function):
    """Declare a function is deprecated."""
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            message = "{}: {}({}) is deprecated".format(
                function.__module__, function.__name__,
                args[0].__class__.__name__)
        except (IndexError, AttributeError):
            message = "{}: {}() is deprecated".format(function.__module__,
                                                      function.__name__)
        warnings.warn(message, DeprecationWarning, stacklevel=2)
        return function(*args, **kwargs)

    return wrapper


def require_full_access(function):
    """Declare a function requires full access mode or not."""
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(args[0].__class__.__name__)
        try:
            args[0].xra31.require_full_access(True)
        except exceptions.Xra31FullAccessException:
            logger.error("Full access mode should be available for %s.%s",
                         args[0].__class__.__name__, function.__name__)
            raise
        return function(*args, **kwargs)

    return wrapper


def require_capture_state(active: bool = True):
    """Declare a function requires a capture to be active or not."""
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(args[0].__class__.__name__)
            try:
                args[0].xra31.require_capture_active(active)
            except exceptions.Xra31StateException:
                logger.error("Capture should be %s for %s",
                             "active" if active else "inactive",
                             function.__name__)
                raise
            return function(*args, **kwargs)

        return wrapper

    return decorator


def require_capture_inactive(function):
    """Declare a function requires a capture to be inactive."""
    return (require_capture_state(False))(function)


def require_capture_active(function):
    """Declare a function requires a capture to be active."""
    return (require_capture_state(True))(function)


def translate_requests(function):
    """Translate :mod:`requests.exceptions`
    to :mod:`excentis.xra31.exceptions`."""
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except requests.exceptions.HTTPError as error:
            # raise_for_status scenario
            if error.response:
                if 400 <= error.response.status_code < 500:
                    raise exceptions.Xra31ClientException(error) from None
                if 500 <= error.response.status_code < 600:
                    raise exceptions.Xra31ServerException(error) from None
            raise exceptions.Xra31HttpException(error) from None
        except requests.exceptions.ConnectionError as error:
            raise exceptions.Xra31ConnectionException(error) from None
        except requests.exceptions.Timeout as error:
            raise exceptions.Xra31TimeoutException(error) from None
        # other requests Exceptions
        except requests.exceptions.RequestException as error:
            raise exceptions.Xra31RestException(error) from None
        # other requests Warnings
        except requests.exceptions.RequestsWarning as error:
            raise exceptions.Xra31RestWarning(error) from None

    return wrapper
