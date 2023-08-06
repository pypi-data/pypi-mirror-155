"""
XRA-31 Python and Command-line Interface
Excentis XRA-31 Development Team <support.xra31@excentis.com>
"""

from . import analysis, capture, configuration, exceptions
from .client import Client
from .core import (Annex, ATdmaChannel, Channel, ChannelList,
                   ChannelModulation, ChannelState, ChannelType,
                   DownstreamChannel, OfdmaChannel, OfdmChannel, ScQamChannel,
                   UpstreamChannel)
from .trace import tracer

try:
    from importlib.metadata import version as metadata_version
except ImportError:
    from importlib_metadata import version as metadata_version  # type: ignore


def connect(address: str = "localhost",
            full_access: bool = False,
            force: bool = False) -> Client:
    """Opens a connection with the XRA-31 and
    returns a :class:`~excentis.xra31.Client` object.

    :param address: Address of the XRA-31.
    :type address: str, optional
    :param full_access: Connect in full access mode.
    :type full_access: bool, optional
    :param force: Force full access mode if it's in use.
    :type force: bool, optional
    :return: XRA-31 :class:`~excentis.xra31.Client` object.
    """
    client = Client(address)
    if full_access:
        if force:
            client.get_full_access()
        else:
            client.try_full_access()
    return client


def version() -> str:
    """The XRA-31 API client version."""
    return metadata_version("excentis_xra31")


__all__ = [
    "exceptions", "analysis", "capture", "configuration", "Client", "Annex",
    "ChannelState", "ChannelType", "ChannelModulation", "Channel",
    "DownstreamChannel", "UpstreamChannel", "OfdmChannel", "ScQamChannel",
    "OfdmaChannel", "ATdmaChannel", "ChannelList", "tracer", "connect",
    "version"
]
