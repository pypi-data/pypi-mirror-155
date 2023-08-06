"""Capture-related classes and enumerations."""

import copy
import enum
import pathlib
import re
import time
import typing

from . import core, decorate, exceptions
from .trace import trace
from .version import Version

DEFAULT_JSON_CLIENT_VERSION = "v4.0.0"
MIN_JSON_CLIENT_VERSION = "v5.2.0"
JSON_CLIENT_VERSION = "v5.2.0"


class PacketType(enum.IntEnum):
    """An enumeration of the packet types used for filtering."""
    # Actual packet types
    DATA = 0  #: Data.
    # Mapped from upstream content
    BURST = 1  #: Burst.
    # Mapped MMM types
    OTHER = 2  #: Other.
    RANGING = 3  #: Ranging.
    BW_REQ = 4  #: Bandwidth Request.
    SYNC = 5  #: SYNC.
    MAP_REFERENCE = 6  #: MAP on reference channel.
    MAP_NON_REFERENCE = 7  #: MAP on non-reference channel.

    _UPSTREAM_OFFSET = 1

    _MMM_OFFSET = 3
    _MMM_FIRST = 2
    _MMM_LAST = 7

    def __str__(self) -> str:
        # pylint: disable=invalid-sequence-index
        return ["Data", "Burst", "Other", "Ranging",
                "Bandwidth Request", "SYNC",
                "MAP on reference channel",
                "MAP on non-reference channel"][self.value]


class OfdmStream(enum.IntEnum):
    """An enumeration of the OFDM streams that can be added or removed."""
    PLC = 0  #: Physical Layer Link Channel.
    NCP = 1  #: Next Codeword Pointer.

    def __str__(self) -> str:
        # pylint: disable=invalid-str-returned
        return self.name


class OfdmProfile(enum.IntEnum):
    """An enumeration of the OFDM Profiles."""
    A = 0  #: Profile A.
    B = 1  #: Profile B.
    C = 2  #: Profile C.
    D = 3  #: Profile D.
    E = 4  #: Profile E.
    F = 5  #: Profile F.
    G = 6  #: Profile G.
    H = 7  #: Profile H.
    I = 8  #: Profile I.
    J = 9  #: Profile J.
    K = 10  #: Profile K.
    L = 11  #: Profile L.
    M = 12  #: Profile M.
    N = 13  #: Profile N.
    O = 14  #: Profile O.
    P = 15  #: Profile P.

    def __str__(self) -> str:
        # pylint: disable=invalid-str-returned
        return self.name


class Channels(core.ChannelList):
    """Access and manipulate the capture channel selection."""
    def __init__(self, xra31):
        super().__init__()
        self.xra31 = xra31

        self._ofdm = []
        self._sc_qam = []
        self._ofdma = []
        self._a_tdma = []

    def __update(self) -> None:
        annex = self.xra31.configuration.annex

        response = self.xra31.session.get(self.xra31.url_api + "/capture",
                                          timeout=self.xra31.timeout)
        response.raise_for_status()

        selection = response.json()["selection"]

        channels = sorted(
            selection["ofdmChannels"],
            key=lambda channel_parameters: channel_parameters["plcFrequency"])
        self._ofdm.clear()
        for channel_parameters in channels:
            self._ofdm.append(
                core.OfdmChannel(channel_parameters["id"],
                                 channel_parameters["plcFrequency"],
                                 channel_parameters["fft"],
                                 channel_parameters["prefix"],
                                 channel_parameters["rolloffPeriod"],
                                 channel_parameters["startFrequency"],
                                 channel_parameters["stopFrequency"],
                                 is_reference=channel_parameters["isReference"]
                                 or False))
            self._ofdm[-1].is_captured = bool(
                "isCaptured" in channel_parameters
                and channel_parameters["isCaptured"])
            self._ofdm[
                -1].state = core.ChannelState.LOCKED if channel_parameters[
                    "fullLock"] else (core.ChannelState.PLC_LOCKED
                                      if channel_parameters["plcLock"] else
                                      core.ChannelState.UNLOCKED)
            self._ofdm[-1].input_level = channel_parameters["inputlevel"]
            self._ofdm[-1].mer = channel_parameters["mer"]

        channels = sorted(
            selection["dsScQamChannels"],
            key=lambda channel_parameters: channel_parameters["frequency"])
        self._sc_qam.clear()
        for channel_parameters in channels:
            self._sc_qam.append(
                core.ScQamChannel(
                    channel_parameters["id"],
                    channel_parameters["frequency"],
                    core.ChannelModulation(channel_parameters["modulation"]),
                    annex,
                    is_reference=channel_parameters["isReference"] or False))
            self._sc_qam[-1].is_captured = bool(
                "isCaptured" in channel_parameters
                and channel_parameters["isCaptured"])
            self._sc_qam[
                -1].state = core.ChannelState.LOCKED if channel_parameters[
                    "lock"] else core.ChannelState.UNLOCKED
            self._sc_qam[-1].input_level = channel_parameters["inputlevel"]
            self._sc_qam[-1].mer = channel_parameters["mer"]

        channels = sorted(selection["ofdmaChannels"],
                          key=lambda channel_parameters: channel_parameters[
                              "ucdInfo"]["startFrequency"])
        self._ofdma.clear()
        for channel_parameters in channels:
            self._ofdma.append(
                core.OfdmaChannel(
                    channel_parameters["id"],
                    channel_parameters["ucdInfo"]["usChannelId"],
                    channel_parameters["ucdInfo"]["startFrequency"],
                    channel_parameters["ucdInfo"]["stopFrequency"]))
            self._ofdma[-1].is_captured = bool(
                "isCaptured" in channel_parameters
                and channel_parameters["isCaptured"])
            self._ofdma[-1].state = (core.ChannelState.LOCKED
                                     if channel_parameters["locked"] else
                                     core.ChannelState.UNLOCKED)
            self._ofdma[-1].input_level = channel_parameters["inputlevel"]
            self._ofdma[-1].mer = channel_parameters["mer"]

        channels = sorted(selection["atdmaChannels"],
                          key=lambda channel_parameters: channel_parameters[
                              "ucdInfo"]["frequency"])
        self._a_tdma.clear()
        for channel_parameters in channels:
            self._a_tdma.append(
                core.ATdmaChannel(channel_parameters["id"],
                                  channel_parameters["ucdInfo"]["usChannelId"],
                                  channel_parameters["ucdInfo"]["frequency"]))
            self._a_tdma[-1].is_captured = bool(
                "isCaptured" in channel_parameters
                and channel_parameters["isCaptured"])
            self._a_tdma[-1].state = (core.ChannelState.LOCKED
                                      if channel_parameters["locked"] else
                                      core.ChannelState.UNLOCKED)
            self._a_tdma[-1].input_level = channel_parameters["inputlevel"]
            self._a_tdma[-1].mer = channel_parameters["mer"]

    def __post_channel(self, xra31_id: int) -> None:
        response = self.xra31.session.post(
            self.xra31.url_api + "/capture/channels/" + str(xra31_id),
            timeout=self.xra31.timeout)
        response.raise_for_status()

    def __delete_channel(self, xra31_id: int) -> None:
        response = self.xra31.session.delete(
            self.xra31.url_api + "/capture/channels/" + str(xra31_id),
            timeout=self.xra31.timeout)
        response.raise_for_status()

    @property
    @decorate.translate_requests
    @trace
    def ofdm(self) -> typing.Iterable[core.OfdmChannel]:
        self.__update()
        return copy.deepcopy(self._ofdm)

    @property
    @decorate.translate_requests
    @trace
    def sc_qam(self) -> typing.Iterable[core.ScQamChannel]:
        self.__update()
        return copy.deepcopy(self._sc_qam)

    @property
    @decorate.translate_requests
    @trace
    def downstream(self) -> typing.Iterable[core.Channel]:
        self.__update()
        yield from copy.deepcopy(self._ofdm)
        yield from copy.deepcopy(self._sc_qam)

    @property
    @decorate.translate_requests
    @trace
    def ofdma(self) -> typing.Iterable[core.OfdmaChannel]:
        self.__update()
        return copy.deepcopy(self._ofdma)

    @property
    @decorate.translate_requests
    @trace
    def a_tdma(self) -> typing.Iterable[core.ATdmaChannel]:
        self.__update()
        return copy.deepcopy(self._a_tdma)

    @property
    @decorate.translate_requests
    @trace
    def upstream(self) -> typing.Iterable[core.Channel]:
        self.__update()
        yield from copy.deepcopy(self._ofdma)
        yield from copy.deepcopy(self._a_tdma)

    @property
    @decorate.translate_requests
    @trace
    def channels(self) -> typing.Iterable[core.Channel]:
        self.__update()
        yield from copy.deepcopy(self._ofdm)
        yield from copy.deepcopy(self._sc_qam)
        yield from copy.deepcopy(self._ofdma)
        yield from copy.deepcopy(self._a_tdma)

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def add(self,
            channel_parameters: core.Channel = None,
            *,
            channel_type: core.ChannelType = None,
            xra31_id: int = -1,
            ucid: int = -1,
            frequency: float = 0.) -> bool:
        """Include a channel in the capture.

        :param channel_parameters: A channel containing
                                   the relevant parameters.
        :type channel_parameters: core.Channel, optional

        :param channel_type: The channel's type.
        :type channel_type: core.ChannelType, optional
        :param xra31_id: ID on the XRA-31.
        :type xra31_id: int, optional
        :param ucid: DOCSIS Upstream Channel ID.
        :type ucid: int, optional
        :param frequency: PLC (OFDM) or center frequency (MHz).
        :type frequency: float, optional
        :return: ``True`` if successful, ``False`` otherwise.
        :rtype: bool
        """
        capture_channel = self.find(channel_parameters,
                                    channel_type=channel_type,
                                    xra31_id=xra31_id,
                                    ucid=ucid,
                                    frequency=frequency)
        if not capture_channel:
            return False
        if not capture_channel.is_captured:
            self.__post_channel(capture_channel.xra31_id)
        return True

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def remove(self,
               channel_parameters: core.Channel = None,
               *,
               channel_type: core.ChannelType = None,
               xra31_id: int = -1,
               ucid: int = -1,
               frequency: float = 0.) -> bool:
        """Don't include a channel in the capture.

        :param channel_parameters: A channel containing
                                   the relevant parameters.
        :type channel_parameters: core.Channel, optional

        :param channel_type: The channel's type.
        :type channel_type: core.ChannelType, optional
        :param xra31_id: ID on the XRA-31.
        :type xra31_id: int, optional
        :param ucid: DOCSIS Upstream Channel ID.
        :type ucid: int, optional
        :param frequency: PLC (OFDM) or center frequency (MHz).
        :type frequency: float, optional
        :return: ``True`` if successful, ``False`` otherwise.
        :rtype: bool
        """
        capture_channel = self.find(channel_parameters,
                                    channel_type=channel_type,
                                    xra31_id=xra31_id,
                                    ucid=ucid,
                                    frequency=frequency)
        if not capture_channel:
            return False
        if capture_channel.is_captured:
            self.__delete_channel(capture_channel.xra31_id)
        return True

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def clear(self) -> None:
        """Ignore all channels."""
        for capture_channel in self.channels:
            if capture_channel.is_captured:
                self.__delete_channel(capture_channel.xra31_id)

    @decorate.translate_requests
    @trace
    def describe(self) -> typing.Dict[str, typing.Any]:
        """Get a minimal representation of the capture channel selection.

        :return: Description listing frequencies for downstream,
                 and UCIDs for upstream.
        :rtype: dict
        """
        self.__update()

        description = {}
        description[str(core.ChannelType.OFDM)] = [
            ofdm_channel.frequency for ofdm_channel in self._ofdm
            if ofdm_channel.is_captured
        ]
        description[str(core.ChannelType.SC_QAM)] = [
            sc_qam_channel.frequency for sc_qam_channel in self._sc_qam
            if sc_qam_channel.is_captured
        ]
        description[str(core.ChannelType.OFDMA)] = [
            ofdma_channel.ucid for ofdma_channel in self._ofdma
            if ofdma_channel.is_captured
        ]
        description[str(core.ChannelType.A_TDMA)] = [
            a_tdma_channel.ucid for a_tdma_channel in self._a_tdma
            if a_tdma_channel.is_captured
        ]
        return description

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def apply(self, description: dict) -> None:
        """Apply a capture channel selection.

        :param description: The selection description (:func:`describe`).
        :type description: dict
        """
        self.__update()

        ofdm = description[str(core.ChannelType.OFDM)] if str(
            core.ChannelType.OFDM) in description else []
        # OFDM PLC on 1MHz grid
        ofdm = [float(int(frequency + .5)) for frequency in ofdm]
        for ofdm_channel in self._ofdm:
            if ofdm_channel.frequency in ofdm:
                if not ofdm_channel.is_captured:
                    self.__post_channel(ofdm_channel.xra31_id)
            elif ofdm_channel.is_captured:
                self.__delete_channel(ofdm_channel.xra31_id)

        sc_qam = description[str(core.ChannelType.SC_QAM)] if str(
            core.ChannelType.SC_QAM) in description else []
        # SC-QAM frequency on 62.5kHz grid
        sc_qam = [
            float(int(frequency * 1e3 / 62.5 + .5) * 62500) / 1e6
            for frequency in sc_qam
        ]
        for sc_qam_channel in self._sc_qam:
            if sc_qam_channel.frequency in sc_qam:
                if not sc_qam_channel.is_captured:
                    self.__post_channel(sc_qam_channel.xra31_id)
            elif sc_qam_channel.is_captured:
                self.__delete_channel(sc_qam_channel.xra31_id)

        ofdma = description[str(core.ChannelType.OFDMA)] if str(
            core.ChannelType.OFDMA) in description else []
        for ofdma_channel in self._ofdma:
            if ofdma_channel.ucid in ofdma:
                if not ofdma_channel.is_captured:
                    self.__post_channel(ofdma_channel.xra31_id)
            elif ofdma_channel.is_captured:
                self.__delete_channel(ofdma_channel.xra31_id)

        a_tdma = description[str(core.ChannelType.A_TDMA)] if str(
            core.ChannelType.A_TDMA) in description else []
        for a_tdma_channel in self._a_tdma:
            if a_tdma_channel.ucid in a_tdma:
                if not a_tdma_channel.is_captured:
                    self.__post_channel(a_tdma_channel.xra31_id)
            elif a_tdma_channel.is_captured:
                self.__delete_channel(a_tdma_channel.xra31_id)


class Filtering:
    # pylint: disable=protected-access
    """Access the capture filtering parameters,
    including the packet types, OFDM profiles and OFDM streams."""
    def __init__(self, xra31):
        self.xra31 = xra31

        self._parameters = {}
        self._token = -1

    def __update(self) -> None:
        # update only when there may be changes
        if self.xra31 and self._token == self.xra31.token:
            return
        response = self.xra31.session.get(self.xra31.url_api + "/capture",
                                          timeout=self.xra31.timeout)
        response.raise_for_status()
        self._parameters = response.json()["filter"]
        self._token = self.xra31.token

    def __set_parameter(self, name: str, value) -> None:
        self.__update()
        self._parameters[name] = value
        self.__post_parameters()

    def __set_parameters(self, parameters: dict) -> None:
        self.__update()
        for name, value in parameters.items():
            self._parameters[name] = value
        self.__post_parameters()

    def __post_parameters(self) -> None:
        self._token = -1
        response = self.xra31.session.post(self.xra31.url_api +
                                           "/capture/filter",
                                           json=self._parameters,
                                           timeout=self.xra31.timeout)
        response.raise_for_status()

    @property
    @decorate.translate_requests
    @trace
    def packet_types(self) -> typing.List[PacketType]:
        """The packet types, as listed in :class:`PacketType`."""
        self.__update()
        packet_types = []
        if "includeData" in self._parameters and self._parameters[
                "includeData"]:
            packet_types.append(PacketType.DATA)
        if "usDataBurst" in self._parameters and self._parameters[
                "usDataBurst"]:
            packet_types.append(PacketType.BURST)
        if "mmmTypes" in self._parameters:
            for mmm_type in self._parameters["mmmTypes"]:
                packet_types.append(
                    PacketType(mmm_type + PacketType._MMM_OFFSET))
        return packet_types

    @packet_types.setter
    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def packet_types(self, packet_types: typing.Iterable[PacketType]) -> None:
        self.__update()
        self._parameters["includeData"] = PacketType.DATA in packet_types
        self._parameters["usDataBurst"] = PacketType.BURST in packet_types
        self._parameters["mmmTypes"].clear()
        for packet_type in packet_types:
            if (PacketType._MMM_FIRST <= packet_type.value <=
                    PacketType._MMM_LAST):
                mmm_id = packet_type.value - PacketType._MMM_OFFSET
                self._parameters["mmmTypes"].append(mmm_id)
        self._parameters["mmmTypes"].sort()
        self.__post_parameters()

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def add_packet_type(self, packet_type: PacketType) -> None:
        """Add a packet type."""
        if packet_type == PacketType.DATA:
            self.__set_parameter("includeData", True)
        elif packet_type == PacketType.BURST:
            self.__set_parameter("usDataBurst", True)
        else:
            self.__update()
            mmm_id = packet_type.value - PacketType._MMM_OFFSET
            if mmm_id not in self._parameters["mmmTypes"]:
                self._parameters["mmmTypes"].append(mmm_id)
                self._parameters["mmmTypes"].sort()
                self.__post_parameters()

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def remove_packet_type(self, packet_type: PacketType) -> None:
        """Remove a packet type."""
        if packet_type == PacketType.DATA:
            self.__set_parameter("includeData", False)
        elif packet_type == PacketType.BURST:
            self.__set_parameter("usDataBurst", False)
        else:
            self.__update()
            mmm_id = packet_type.value - PacketType._MMM_OFFSET
            if mmm_id in self._parameters["mmmTypes"]:
                self._parameters["mmmTypes"].remove(mmm_id)
                self.__post_parameters()

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def clear_packet_types(self) -> None:
        """Remove all packet types."""
        self.__update()
        self._parameters["includeData"] = False
        self._parameters["usDataBurst"] = False
        self._parameters["mmmTypes"] = []
        self.__post_parameters()

    @property
    @decorate.translate_requests
    @trace
    def ofdm_streams(self) -> typing.List[OfdmStream]:
        """The OFDM streams, as listed in :class:`OfdmStream`."""
        self.__update()
        ofdm_stream = []
        if "dsPlc" in self._parameters and self._parameters["dsPlc"]:
            ofdm_stream.append(OfdmStream.PLC)
        if "dsNcp" in self._parameters and self._parameters["dsNcp"]:
            ofdm_stream.append(OfdmStream.NCP)
        return ofdm_stream

    @ofdm_streams.setter
    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def ofdm_streams(self, ofdm_streams: typing.Iterable[OfdmStream]) -> None:
        self.__update()
        self._parameters["dsPlc"] = OfdmStream.PLC in ofdm_streams
        self._parameters["dsNcp"] = OfdmStream.NCP in ofdm_streams
        self.__post_parameters()

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def add_ofdm_stream(self, stream: OfdmStream) -> None:
        """Add an OFDM stream."""
        if stream == OfdmStream.PLC:
            self.__set_parameter("dsPlc", True)
        elif stream == OfdmStream.NCP:
            self.__set_parameter("dsNcp", True)

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def remove_ofdm_stream(self, stream: OfdmStream) -> None:
        """Remove an OFDM stream."""
        if stream == OfdmStream.PLC:
            self.__set_parameter("dsPlc", False)
        elif stream == OfdmStream.NCP:
            self.__set_parameter("dsNcp", False)

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def clear_ofdm_streams(self) -> None:
        """Remove all OFDM streams."""
        self.__update()
        self._parameters["dsPlc"] = False
        self._parameters["dsNcp"] = False
        self.__post_parameters()

    @property
    @decorate.translate_requests
    @trace
    def ofdm_profiles(self) -> typing.List[OfdmProfile]:
        """The OFDM profiles, as listed in :class:`OfdmProfile`."""
        self.__update()
        return [
            OfdmProfile(profile) for profile in self._parameters["dsProfiles"]
        ]

    @ofdm_profiles.setter
    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def ofdm_profiles(self,
                      ofdm_profiles: typing.Iterable[OfdmProfile]) -> None:
        self.__update()
        self._parameters["dsProfiles"] = sorted(ofdm_profiles)
        self.__post_parameters()

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def add_ofdm_profile(self, profile: OfdmProfile) -> None:
        """Add an OFDM profile."""
        self.xra31.require_full_access()
        self.__update()
        if profile.value not in self._parameters["dsProfiles"]:
            self._parameters["dsProfiles"].append(profile.value)
            self._parameters["dsProfiles"].sort()
            self.__post_parameters()

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def remove_ofdm_profile(self, profile: OfdmProfile) -> None:
        """Remove an OFDM profile."""
        self.__update()
        if profile.value in self._parameters["dsProfiles"]:
            self._parameters["dsProfiles"].remove(profile.value)
            self._parameters["dsProfiles"].sort()
            self.__post_parameters()

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def clear_ofdm_profiles(self) -> None:
        """Remove all OFDM profiles."""
        self.__set_parameter("dsProfiles", [])

    @trace
    def describe(self) -> typing.Dict[str, typing.Any]:
        """Get a minimal representation of the capture filtering.

        :return: Description listing packet types,
                 OFDM profiles and OFDM streams.
        :rtype: dict
        """
        description = {}
        description["packet_types"] = [
            str(packet_type) for packet_type in self.packet_types
        ]
        description["ofdm_profiles"] = [
            str(ofdm_profile) for ofdm_profile in self.ofdm_profiles
        ]
        description["ofdm_streams"] = [
            str(ofdm_stream) for ofdm_stream in self.ofdm_streams
        ]
        return description

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @trace
    def apply(self, description: dict) -> None:
        """Apply a filtering configuration.

        :param description: The filtering description (:func:`describe`).
        :type description: dict
        """
        if "packet_types" in description:
            packet_type_names = [
                str(packet_type) for packet_type in PacketType
            ]
            packet_types = [
                PacketType(packet_type_names.index(packet_type))
                for packet_type in description["packet_types"]
                if packet_type in packet_type_names
            ]
            self.packet_types = packet_types

        if "ofdm_profiles" in description:
            ofdm_profile_names = [
                str(ofdm_profile) for ofdm_profile in OfdmProfile
            ]
            ofdm_profiles = [
                OfdmProfile(ofdm_profile_names.index(ofdm_profile))
                for ofdm_profile in description["ofdm_profiles"]
                if ofdm_profile in ofdm_profile_names
            ]
            self.ofdm_profiles = ofdm_profiles

        if "ofdm_streams" in description:
            ofdm_stream_names = [
                str(ofdm_stream) for ofdm_stream in OfdmStream
            ]
            ofdm_streams = [
                OfdmStream(ofdm_stream_names.index(ofdm_stream))
                for ofdm_stream in description["ofdm_streams"]
                if ofdm_stream in ofdm_stream_names
            ]
            self.ofdm_streams = ofdm_streams


class Output:
    """Access the capture output parameters."""
    def __init__(self, xra31):
        self.xra31 = xra31

        self._parameters = {}
        self._token = -1

    def __update(self) -> None:
        # update only when there may be changes
        if self.xra31 and self._token == self.xra31.token:
            return
        response = self.xra31.session.get(self.xra31.url_api + "/capture",
                                          timeout=self.xra31.timeout)
        response.raise_for_status()
        self._parameters = response.json()["fileOutput"]
        self._token = self.xra31.token

    def __set_parameter(self, name: str, value) -> None:
        self.__update()
        self._parameters[name] = value
        self._token = -1
        response = self.xra31.session.post(self.xra31.url_api +
                                           "/capture/fileoutput",
                                           json=self._parameters,
                                           timeout=self.xra31.timeout)
        response.raise_for_status()

    def __set_parameters(self, parameters: dict) -> None:
        self.__update()
        for name, value in parameters.items():
            self._parameters[name] = value
        self._token = -1
        response = self.xra31.session.post(self.xra31.url_api +
                                           "/capture/fileoutput",
                                           json=self._parameters,
                                           timeout=self.xra31.timeout)
        response.raise_for_status()

    @property
    @decorate.translate_requests
    @trace
    @decorate.deprecated
    def directory(self) -> str:
        """The directory in which the capture is stored.

        .. deprecated:: v5.0.0
            Use :attr:`path` instead,
            accessing property :py:data:`pathlib.PurePath.parent`."""
        self.__update()
        return self._parameters["directory"]

    @directory.setter
    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    @decorate.deprecated
    def directory(self, directory: str) -> None:
        self.__set_parameter("directory", directory)

    @property
    @decorate.translate_requests
    @trace
    @decorate.deprecated
    def filename(self) -> str:
        """The filename of the capture.

        .. deprecated:: v5.0.0
            Use :attr:`path` instead,
            accessing property :py:data:`pathlib.PurePath.name`."""
        self.__update()
        return self._parameters["fileName"]

    @filename.setter
    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    @decorate.deprecated
    def filename(self, filename: str) -> None:
        filename = re.sub(r"\.pcap$", "", filename)
        self.__set_parameter("fileName", filename + ".pcap")

    @property
    @decorate.translate_requests
    @trace
    def path(self) -> pathlib.PurePosixPath:
        """The path (:class:`pathlib.PurePosixPath`) of the capture.

        .. versionadded:: v5.0.0"""
        self.__update()
        return pathlib.PurePosixPath(
            self._parameters["directory"]) / self._parameters["fileName"]

    @path.setter
    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def path(self, path: typing.Union[str, pathlib.PurePosixPath]) -> None:
        path = pathlib.PurePosixPath(path)
        directory = path.parent
        filename = re.sub(r"\.pcap$", "", path.name)
        self.__set_parameters({
            "directory": "" if str(directory) == "." else str(directory),
            "fileName": filename + ".pcap"
        })

    @property
    @decorate.translate_requests
    @trace
    def duration(self) -> typing.Optional[float]:
        """The maximum duration of the capture (s), ``None`` for unlimited.
        Setting the maximum capture duration
        resets the maximum capture size."""
        self.__update()
        result = self._parameters["maxDurationCapture"]
        return result if result > 0. else None

    @duration.setter
    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def duration(self, duration: float) -> None:
        if not duration or duration < 0.:
            duration = 0.
        self.__set_parameters({
            "maxDurationCapture": duration,
            "maxBytesCapture": 0
        })

    @property
    @decorate.translate_requests
    @trace
    def size(self) -> typing.Optional[float]:
        """The maximum size of the capture (MB), ``None`` for unlimited.
        Setting the maximum capture size
        resets the maximum capture duration."""
        self.__update()
        result = self._parameters["maxBytesCapture"]
        return result if result > 0 else None

    @size.setter
    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def size(self, size: float) -> None:
        if not size or size < 0:
            size = 0
        self.__set_parameters({
            "maxBytesCapture": size,
            "maxDurationCapture": 0
        })

    @property
    @decorate.translate_requests
    @trace
    def number_of_files(self) -> int:
        """The number of files in a rolling file capture."""
        self.__update()
        result = self._parameters["numberOfFiles"]
        return result if result > 1 else None

    @number_of_files.setter
    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def number_of_files(self, number_of_files: int) -> None:
        if not number_of_files or number_of_files < 1:
            number_of_files = 1
        self.__set_parameter("numberOfFiles", number_of_files)

    @property
    @decorate.translate_requests
    @trace
    def file_duration(self) -> typing.Optional[float]:
        """The maximum file duration before rolling over to the next file
        in a rolling file capture (s), ``None`` for unlimited.
        Setting the maximum file duration
        resets the maximum file size in a rolling file capture."""
        self.__update()
        result = self._parameters["maxDurationPerFile"]
        return result if result > 0. else None

    @file_duration.setter
    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def file_duration(self, file_duration: float) -> None:
        if not file_duration or file_duration < 0.:
            file_duration = 0.
        self.__set_parameters({
            "maxDurationPerFile": file_duration,
            "maxBytesPerFile": 0
        })

    @property
    @decorate.translate_requests
    @trace
    def file_size(self) -> typing.Optional[float]:
        """The file size before rolling over to the next file
        in a rolling file capture (MB), ``None`` for unlimited.
        Setting the maximum file size
        resets the maximum file duration in a rolling file capture."""
        self.__update()
        result = self._parameters["maxBytesPerFile"]
        return result if result > 0 else None

    @file_size.setter
    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def file_size(self, file_size: float) -> None:
        if not file_size or file_size < 0:
            file_size = 0
        self.__set_parameters({
            "maxBytesPerFile": file_size,
            "maxDurationPerFile": 0
        })

    @decorate.translate_requests
    @trace
    def describe(self) -> typing.Dict[str, typing.Any]:
        """Get a minimal representation of the capture output configuration.

        :return: A full description of the output configuration.
        :rtype: dict
        """
        description = {}
        self.__update()
        description["path"] = str(
            pathlib.PurePosixPath(self._parameters["directory"]) /
            self._parameters["fileName"])

        duration = self._parameters["maxDurationCapture"]
        description["duration"] = (duration if duration > 0 else None)
        size = self._parameters["maxBytesCapture"]
        description["size"] = (size if size > 0 else None)

        number_of_files = self._parameters["numberOfFiles"]
        description["number_of_files"] = (number_of_files
                                          if number_of_files > 1 else None)
        file_duration = self._parameters["maxDurationPerFile"]
        description["file_duration"] = (file_duration
                                        if file_duration > 0 else None)
        file_size = self._parameters["maxBytesPerFile"]
        description["file_size"] = (file_size if file_size > 0 else None)
        return description

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def apply(self, description: dict) -> None:
        """Apply a capture output configuration.

        :param description: The output configuration description
                            (:func:`describe`).
        :type description: dict
        """

        parameters = {}
        if "directory" in description:
            parameters["directory"] = description["directory"]
        if "filename" in description:
            parameters["fileName"] = re.sub(r"\.pcap$", "",
                                            description["filename"]) + ".pcap"
        if "path" in description:
            path = pathlib.PurePosixPath(description["path"])
            parameters["directory"] = str(path.parent)
            if parameters["directory"] == ".":
                parameters["directory"] = ""
            parameters["fileName"] = re.sub(r"\.pcap$", "",
                                            path.name) + ".pcap"
        if "duration" in description:
            duration = description["duration"]
            parameters["maxDurationCapture"] = (duration if duration
                                                and duration > 0 else 0)
            parameters["maxBytesCapture"] = 0
        if "size" in description:
            size = description["size"]
            parameters["maxBytesCapture"] = (size if size and size > 0 else 0)
            if "maxDurationCapture" not in parameters:
                parameters["maxDurationCapture"] = 0
        if "number_of_files" in description:
            number_of_files = description["number_of_files"]
            parameters["numberOfFiles"] = (number_of_files if number_of_files
                                           and number_of_files > 1 else 1)
        if "file_duration" in description:
            file_duration = description["file_duration"]
            parameters["maxDurationPerFile"] = (file_duration if file_duration
                                                and file_duration > 0 else 0)
            parameters["maxBytesPerFile"] = 0
        if "file_size" in description:
            file_size = description["file_size"]
            parameters["maxBytesPerFile"] = (file_size if file_size
                                             and file_size > 0 else 0)
            if "maxDurationPerFile" not in parameters:
                parameters["maxDurationPerFile"] = 0
        if ("maxBytesCapture" in parameters and parameters["maxBytesCapture"]
                and "maxDurationCapture" in parameters
                and parameters["maxDurationCapture"]):
            raise exceptions.Xra31ConfigurationException(
                "Maximum capture size and capture duration"
                " can not be set simultaneously.")
        if ("maxBytesPerFile" in parameters and parameters["maxBytesPerFile"]
                and "maxDurationPerFile" in parameters
                and parameters["maxDurationPerFile"]):
            raise exceptions.Xra31ConfigurationException(
                "Maximum file size and file duration in a rolling file capture"
                " can not be set simultaneously.")
        self.__set_parameters(parameters)


class Capture:
    """Access capture-related settings and actions."""
    def __init__(self, xra31):
        self.xra31 = xra31

        self._status = {}
        self._token = -1

        self._channels = Channels(self.xra31)
        self.filtering = Filtering(self.xra31)
        self.output = Output(self.xra31)

    def __update(self) -> None:
        response = self.xra31.session.get(self.xra31.url_api +
                                          "/capture/status",
                                          timeout=self.xra31.timeout)
        response.raise_for_status()
        self._status = response.json()
        self._token = self.xra31.token

    @property
    @trace
    def channels(self) -> Channels:
        """Get the list of channels."""
        return self._channels

    @channels.setter
    @decorate.require_full_access
    @decorate.require_capture_inactive
    @trace
    def channels(self, channels: typing.Iterable[core.Channel]) -> None:
        self._channels.clear()
        for channel in channels:
            self._channels.add(channel)

    @property
    @decorate.translate_requests
    @trace
    def active(self) -> bool:
        """Indicates if the capture is recording."""
        self.__update()
        return self._status["active"]

    @property
    @decorate.translate_requests
    @trace
    @decorate.deprecated
    def filename(self) -> typing.Optional[str]:
        """The active, or latest when inactive, capture filename.

        .. deprecated:: v5.0.0
            Use :attr:`active_path` and :attr:`captured_path` instead,
           accessing property :py:data:`pathlib.PurePath.name`."""
        self.__update()
        path = self.active_path if self.active else self.captured_path
        return path.name if path else None

    @property
    @decorate.translate_requests
    @trace
    def active_path(self) -> typing.Optional[pathlib.PurePosixPath]:
        """The path to the active capture, if available.

        .. versionadded:: v5.0.0"""
        self.__update()
        return (pathlib.PurePosixPath(
            re.sub(r"^/mnt/data/captures/", "", self._status["activePath"]))
                if "activePath" in self._status and self._status["activePath"]
                else None)

    @property
    @decorate.translate_requests
    @trace
    def captured_path(self) -> typing.Optional[pathlib.PurePosixPath]:
        """The path to the most recently completed capture, if available.

        .. versionadded:: v5.0.0"""
        self.__update()
        return (pathlib.PurePosixPath(
            re.sub(r"^/mnt/data/captures/", "", self._status["previousPath"]))
                if "previousPath" in self._status
                and self._status["previousPath"] else None)

    @property
    @decorate.translate_requests
    @trace
    def duration(self) -> float:
        """The duration of the current capture."""
        self.__update()
        return self._status["milliSecondsSinceStart"] / 1000.

    @property
    @decorate.translate_requests
    @trace
    def size(self) -> float:
        """The file size of the current capture."""
        self.__update()
        return self._status["bytesCaptured"] / 1024. / 1024.

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def start(self) -> None:
        """Start a capture."""
        response = self.xra31.session.post(self.xra31.url_api + "/capture",
                                           timeout=self.xra31.timeout)
        response.raise_for_status()

    @trace
    def wait_for_end(
            self,
            timeout: float = None) -> typing.Optional[pathlib.PurePosixPath]:
        """Wait for a capture to end.

        :param timeout: Number of seconds to wait before giving up;
                        by default it will wait indefinitely.
        :type timeout: float, optional

        :return: The path of the most recent capture if successful,
                 ``None`` otherwise.
        :rtype: pathlib.PurePosixPath

        .. versionchanged:: v5.0.0
            return type.
        """
        stop = 0 if timeout is None else round(time.monotonic()) + timeout
        capture_active = self.active
        while capture_active and (stop == 0 or time.monotonic() < stop):
            time.sleep(.5)
            capture_active = self.active
        return self.captured_path if not capture_active else None

    @trace
    def wait_for_file_end(
            self,
            timeout: float = None) -> typing.Optional[pathlib.PurePosixPath]:
        """Wait for a file rollover in a rolling file capture.

        :param timeout: Number of seconds to wait before giving up;
                        by default it will wait indefinitely.
        :type timeout: float, optional

        :return: The path of the most recent capture if successful,
                 ``None`` otherwise.
        :rtype: pathlib.PurePosixPath

        .. versionchanged:: v5.0.0
            return type.
        """
        active_path = self.active_path
        stop = 0 if timeout is None else round(time.monotonic()) + timeout
        capture_active = self.active
        while capture_active and self.active_path == active_path and (
                stop == 0 or time.monotonic() < stop):
            time.sleep(.5)
            capture_active = self.active
        return (self.captured_path if not capture_active
                or self.active_path != active_path else None)

    @decorate.require_full_access
    @decorate.translate_requests
    @trace
    def stop(self) -> None:
        """Stop a capture."""
        if not self.active:
            return
        response = self.xra31.session.delete(self.xra31.url_api + "/capture",
                                             timeout=self.xra31.timeout)
        response.raise_for_status()

    @trace
    def describe(self) -> typing.Dict[str, typing.Any]:
        """Get a minimal representation of the capture configuration.

        :return: Description listing channels, filtering and output.
        :rtype: dict
        """
        description = {}
        description["min_client_version"] = JSON_CLIENT_VERSION
        description["channels"] = self.channels.describe()
        description["filtering"] = self.filtering.describe()
        description["output"] = self.output.describe()
        return description

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @trace
    def apply(self, description: dict) -> None:
        """Apply a capture configuration.

        :param description: The capture description (:func:`describe`).
        :type description: dict
        """

        min_client_version = (description["min_client_version"]
                              if "min_client_version" in description else
                              DEFAULT_JSON_CLIENT_VERSION)
        client_version = self.xra31.version
        if not (Version(MIN_JSON_CLIENT_VERSION) <= Version(min_client_version)
                <= Version(client_version)):
            raise exceptions.Xra31VersionException(
                "This API client requires a capture description"
                " min_client_version between " + MIN_JSON_CLIENT_VERSION +
                " and " + client_version + ", but found " + min_client_version)

        if "channels" in description:
            self.xra31.logger.info("Select channels")
            self.channels.apply(description["channels"])
        if "filtering" in description:
            self.xra31.logger.info("Configure filtering")
            self.filtering.apply(description["filtering"])
        if "output" in description:
            self.xra31.logger.info("Configure output")
            self.output.apply(description["output"])
