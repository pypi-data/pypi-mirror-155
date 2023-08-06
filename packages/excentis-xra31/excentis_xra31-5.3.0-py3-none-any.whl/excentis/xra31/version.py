"""Version comparison, for internal use."""

import re

from . import exceptions


class Version:
    """Version comparison, for internal use"""

    VERSION_PATTERN = re.compile(
        r"^(?:v|r)?(?P<major>[0-9]+)\.(?P<minor>[0-9]+)"
        r"(?:\.(?P<micro>[0-9]+))?"
        r"(?:(?P<pre_label>a|b|rc)(?P<pre_number>[0-9]+)?)?")

    def __init__(self, identifier: str):
        match = Version.VERSION_PATTERN.search(identifier)
        if not match:
            raise exceptions.Xra31VersionException(
                "Invalid version identifier: {0}".format(identifier))
        self.major = int(match.group("major"))
        self.minor = int(match.group("minor"))
        self.micro = int(match.group("micro") or 0)
        self.pre_label = (match.group("pre_label") or "f")[-1]
        self.pre_number = int(match.group("pre_number") or 0)

        self._hash = "{:0>8d}{:0>8d}{:0>8d}{:0>1}{:0>7d}".format(
            self.major, self.minor, self.micro, self.pre_label,
            self.pre_number)

    def __lt__(self, other) -> bool:
        return self._hash < other._hash

    def __le__(self, other) -> bool:
        return self._hash <= other._hash
