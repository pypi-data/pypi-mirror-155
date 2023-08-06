"""Explicit tracing of function calls for debugging purposes."""

import functools
import logging

# pylint: disable=invalid-name
tracer = logging.getLogger(__package__ + ".trace")


def trace(function):
    """Decorator to make function access traceable through debug logging."""
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        name = ""
        if tracer.getEffectiveLevel() <= logging.DEBUG:
            try:
                name = "{}: {}({})".format(function.__module__,
                                           function.__name__,
                                           args[0].__class__.__name__)
            except (IndexError, AttributeError):
                name = "{}: {}()".format(function.__module__,
                                         function.__name__)
        tracer.debug("%s start", name)
        result = function(*args, **kwargs)
        tracer.debug("%s ready", name)
        return result

    return wrapper
