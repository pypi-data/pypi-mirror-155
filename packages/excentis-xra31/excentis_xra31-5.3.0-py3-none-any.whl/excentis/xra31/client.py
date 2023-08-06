"""A Python client for the XRA-31."""

import json
import logging
import time
import typing

import requests

from . import analysis, capture, configuration, decorate, exceptions
from .trace import trace
from .version import Version

try:
    from importlib.metadata import version as metadata_version
except ImportError:
    from importlib_metadata import version as metadata_version  # type: ignore

MIN_SERVER_VERSION = "r5.2.0"


class Client:
    """A Python client for the XRA-31."""
    @decorate.translate_requests
    def __init__(self, address: str = "localhost"):
        """Create a connection with an XRA-31.

        :param address: Address of the XRA-31.
        :type address: str, optional
        """
        #: The XRA-31's address.
        self.address = address
        self.token = -1
        self._session = requests.Session()
        self._session_time = time.monotonic()

        self._version = ""
        self._min_version = ""
        self._server_version = ""
        #: The minimal XRA-31 server version.
        self.min_server_version = MIN_SERVER_VERSION

        #: The XRA-31's request timeout in seconds (read/connect).
        self.timeout = 10.

        #: The :class:`~excentis.xra31.configuration.Configuration` object.
        self.configuration = configuration.Configuration(self)
        #: The :class:`~excentis.xra31.capture.Capture` object.
        self.capture = capture.Capture(self)
        #: The :class:`~excentis.xra31.analysis.Analysis` object.
        self.analysis = analysis.Analysis(self)

        response = self._session.get(self.url_api + "/system/customer",
                                     timeout=self.timeout)
        response.raise_for_status()
        response_json = response.json()

        #: The XRA-31's system serial.
        self.system_serial = response_json["system_serial"]
        #: The XRA-31's licensed company.
        self.company = response_json["company"]

        self.logger = logging.getLogger(__package__)

        if (self.server_version == "unknown" or Version(self.server_version) <
                Version(self.min_server_version)):
            raise exceptions.Xra31VersionException(
                "This API client (" + self.version +
                ") requires an XRA-31 version >=" + self.min_server_version +
                (", but found " + self.server_version
                 if self.server_version != "unknown" else ""))

        if (self.min_version == "unknown"
                or Version(self.version) < Version(self.min_version)):
            raise exceptions.Xra31VersionException(
                "The XRA-31's version (" + self.server_version +
                ") requires an API client version >=" + self.min_version +
                ", but found " + self.version)

    def __enter__(self) -> "Client":
        self.get_full_access()
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.release()

    def __bool__(self) -> bool:
        return self.token != -1

    @property
    def version(self) -> str:
        """The XRA-31 API client version."""
        if not self._version:
            self._version = metadata_version("excentis_xra31")
        return self._version

    @property
    def min_version(self) -> str:
        """The minimal XRA-31 API client version required by the server."""
        if not self._min_version:
            try:
                response = self._session.get(self.url_api +
                                             "/system/versions/client",
                                             timeout=self.timeout)
                response.raise_for_status()
                self._min_version = response.json()["identifier"]
            except json.decoder.JSONDecodeError:
                self._min_version = "unknown"
        return self._min_version

    @property
    def server_version(self) -> str:
        """The XRA-31's server version."""
        if not self._server_version:
            try:
                response = self._session.get(self.url_api +
                                             "/system/versions/active",
                                             timeout=self.timeout)
                response.raise_for_status()
                self._server_version = "{}.{}.{}".format(
                    response.json()["major"],
                    response.json()["minor"],
                    response.json()["patch"])
            except json.decoder.JSONDecodeError:
                self._server_version = "unknown"
        return self._server_version

    @property
    def session(self) -> requests.Session:
        # pylint: disable=missing-function-docstring
        now = time.monotonic()
        if now - self._session_time < .05:
            time.sleep(.05 - now + self._session_time)
        self._session_time = time.monotonic()
        return self._session

    @property
    def url(self) -> str:
        """The XRA-31's URL."""
        return "http://{address}".format(address=self.address)

    @property
    def url_api(self) -> str:
        """The XRA-31's API URL."""
        return "http://{address}/api/v1".format(address=self.address)

    @decorate.translate_requests
    @trace
    def get_full_access(self) -> None:
        """Enter full access mode."""
        if self:
            return
        response = self.session.get(self.url_api + "/system/privilegeToken",
                                    params={'forced': 'true'},
                                    timeout=self.timeout)
        response.raise_for_status()
        self.token = response.json()["privilegeToken"]
        self._session.headers["x-privilegetoken"] = str(self.token)

    @decorate.translate_requests
    @trace
    def try_full_access(self) -> bool:
        """Try to enter full access mode.

        :return: ``True`` if successful, ``False`` otherwise.
        :rtype: bool
        """
        if self:
            return True
        response = self.session.get(self.url_api + "/system/privilegeToken",
                                    timeout=self.timeout)
        if not response.ok:
            return False
        self.token = response.json()["privilegeToken"]
        self._session.headers["x-privilegetoken"] = str(self.token)
        return True

    @trace
    def require_capture_active(self, active: bool = True) -> None:
        # pylint: disable=missing-function-docstring
        if self.capture.active != active:
            raise exceptions.Xra31StateException

    @trace
    def require_full_access(self, full_access: bool = True) -> None:
        # pylint: disable=missing-function-docstring
        if self.try_full_access() != full_access:
            raise exceptions.Xra31FullAccessException

    @decorate.translate_requests
    @trace
    def release(self) -> None:
        """Release full access mode."""
        if not self:
            return
        request = requests.Request('DELETE',
                                   self.url_api + "/system/privilegeToken")
        prepped = self._session.prepare_request(request)
        self.token = -1
        self._session.headers.pop("x-privilegetoken")
        response = self.session.send(prepped, timeout=self.timeout)
        response.raise_for_status()

    def __str__(self) -> str:
        return "{} ({}) at {}".format(self.system_serial, self.company,
                                      self.url)

    @trace
    def describe(self) -> typing.Dict[str, typing.Any]:
        """Representation of an XRA-31 configuration."""
        description = {}
        description["configuration"] = self.configuration.describe()
        description["capture"] = self.capture.describe()
        return description

    @trace
    def apply(self, description: dict) -> None:
        """Apply an XRA-31 configuration.

        :param description: The configuration description (:func:`describe`).
        :type description: dict
        """
        self.require_full_access()
        self.require_capture_active(False)
        if "configuration" in description:
            self.configuration.apply(description["configuration"])
        if "capture" in description:
            self.capture.apply(description["capture"])
