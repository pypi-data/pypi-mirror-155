"""
Details on the channel parameters used here can be found
in :mod:`~excentis.xra31.core`.
"""

import copy
import re
import time
import typing

from . import core, decorate, exceptions
from .trace import trace
from .version import Version

DEFAULT_JSON_CLIENT_VERSION = "v4.0.0"
MIN_JSON_CLIENT_VERSION = "v4.0.0"
JSON_CLIENT_VERSION = "v5.0.0"


class Detection(core.ChannelList):
    """Access the upstream channel list detected by the XRA-31."""
    def __init__(self, xra31):
        super().__init__()
        self.xra31 = xra31

        self._ofdma = []
        self._a_tdma = []

    def __update(self) -> None:
        response = self.xra31.session.get(self.xra31.url_api +
                                          "/channels/detecteduschannels",
                                          timeout=self.xra31.timeout)
        response.raise_for_status()
        response_json = response.json()

        channels = sorted(
            response_json["detectedOfdmaChannels"],
            key=lambda ofdma_channel: ofdma_channel["startFrequency"])
        self._ofdma.clear()
        for ofdma_channel in channels:
            self._ofdma.append(
                core.OfdmaChannel(-1, ofdma_channel["usChannelId"],
                                  ofdma_channel["startFrequency"],
                                  ofdma_channel["stopFrequency"]))

        channels = sorted(
            response_json["detectedAtdmaChannels"],
            key=lambda a_tdma_channel: a_tdma_channel["frequency"])
        self._a_tdma.clear()
        for a_tdma_channel in channels:
            self._a_tdma.append(
                core.ATdmaChannel(-1, a_tdma_channel["usChannelId"],
                                  a_tdma_channel["frequency"]))

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
    def upstream(self) -> typing.Iterable[core.UpstreamChannel]:
        self.__update()
        yield from copy.deepcopy(self._ofdma)
        yield from copy.deepcopy(self._a_tdma)

    @trace
    def wait_for_channel(
            self,
            channel_parameters: core.UpstreamChannel = None,
            *,
            channel_type: core.ChannelType = None,
            ucid: int = -1,
            frequency: float = 0.,
            timeout: float = None) -> typing.Optional[core.UpstreamChannel]:
        """Wait for an upstream channel to be detected by the XRA-31.

        :param channel_parameters: A channel containing the parameters.
        :type channel_parameters: core.UpstreamChannel, optional
        :param channel_type: The type of channel.
        :type channel_type: core.ChannelType, optional
        :param ucid: DOCSIS Upstream Channel ID.
        :type ucid: int, optional
        :param frequency: The frequency of the channel (MHz).
        :type frequency: float, optional
        :param timeout: Number of seconds to wait before giving up;
                        by default it will wait indefinitely.
        :type timeout: float, optional
        :return: The upstream channel if successful, ``None`` otherwise.
        :rtype: typing.Optional[core.UpstreamChannel]
        """
        stop = 0 if timeout is None else round(time.monotonic()) + timeout
        ucd_channel = self.find(channel_parameters,
                                channel_type=channel_type,
                                ucid=ucid,
                                frequency=frequency)
        while (not ucd_channel) and (stop == 0 or time.monotonic() < stop):
            time.sleep(.5)
            ucd_channel = self.find(channel_parameters,
                                    channel_type=channel_type,
                                    ucid=ucid,
                                    frequency=frequency)
        return ucd_channel


class Configuration(core.ChannelList):
    """Add and remove XRA-31 channels (OFDM, SC-QAM, OFDMA, A-TDMA),
    and monitor their status."""
    def __init__(self, xra31):
        super().__init__()
        self.xra31 = xra31

        #: Channels detected by the XRA-31.
        self.detection = Detection(self.xra31)

        self._annex = core.Annex.A
        self._ofdm = []
        self._sc_qam = []
        self._ofdma = []
        self._a_tdma = []

    def __update_annex(self) -> None:
        self.__update_sc_qam()

    def __update_ofdm(self) -> None:
        response = self.xra31.session.get(self.xra31.url_api +
                                          "/channels/ofdm",
                                          timeout=self.xra31.timeout)
        response.raise_for_status()

        channels = sorted(
            response.json()["channels_ofdm"],
            key=lambda channel_parameters: channel_parameters["plcFrequency"])
        self._ofdm.clear()
        for channel_parameters in channels:
            self._ofdm.append(
                core.OfdmChannel(
                    channel_parameters["id"],
                    channel_parameters["plcFrequency"],
                    channel_parameters["fft"],
                    channel_parameters["prefix"],
                    channel_parameters["rolloffPeriod"],
                    channel_parameters["startFrequency"],
                    channel_parameters["stopFrequency"],
                    is_reference=channel_parameters["isReference"]))
            self._ofdm[
                -1].state = core.ChannelState.LOCKED if channel_parameters[
                    "fullLock"] else (core.ChannelState.PLC_LOCKED
                                      if channel_parameters["plcLock"] else
                                      core.ChannelState.UNLOCKED)
            self._ofdm[-1].input_level = channel_parameters["inputlevel"]
            self._ofdm[-1].mer = channel_parameters["mer"]

    def __update_sc_qam(self) -> None:
        response = self.xra31.session.get(self.xra31.url_api +
                                          "/channels/dsscqam",
                                          timeout=self.xra31.timeout)
        response.raise_for_status()
        response_json = response.json()

        self._annex = core.Annex.B if response_json[
            "annex"] == 1 else core.Annex.A

        channels = sorted(
            response_json["channels_dsscqam"],
            key=lambda channel_parameters: channel_parameters["frequency"])
        self._sc_qam.clear()
        for channel_parameters in channels:
            self._sc_qam.append(
                core.ScQamChannel(
                    channel_parameters["id"],
                    channel_parameters["frequency"],
                    core.ChannelModulation(channel_parameters["modulation"]),
                    self._annex,
                    is_reference=channel_parameters["isReference"]))
            self._sc_qam[
                -1].state = core.ChannelState.LOCKED if channel_parameters[
                    "lock"] else core.ChannelState.UNLOCKED
            self._sc_qam[-1].input_level = channel_parameters["inputlevel"]
            self._sc_qam[-1].mer = channel_parameters["mer"]

    def __update_ofdma(self) -> None:
        response = self.xra31.session.get(self.xra31.url_api +
                                          "/channels/ofdma",
                                          timeout=self.xra31.timeout)
        response.raise_for_status()

        channels = sorted(response.json()["channels_ofdma"],
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
            self._ofdma[-1].state = (core.ChannelState.LOCKED
                                     if channel_parameters["locked"] else
                                     core.ChannelState.UNLOCKED)
            self._ofdma[-1].input_level = channel_parameters["inputlevel"]
            self._ofdma[-1].mer = channel_parameters["mer"]

    def __update_a_tdma(self) -> None:
        response = self.xra31.session.get(self.xra31.url_api +
                                          "/channels/atdma",
                                          timeout=self.xra31.timeout)
        response.raise_for_status()

        channels = sorted(response.json()["channels_atdma"],
                          key=lambda channel_parameters: channel_parameters[
                              "ucdInfo"]["frequency"])
        self._a_tdma.clear()
        for channel_parameters in channels:
            self._a_tdma.append(
                core.ATdmaChannel(channel_parameters["id"],
                                  channel_parameters["ucdInfo"]["usChannelId"],
                                  channel_parameters["ucdInfo"]["frequency"]))
            self._a_tdma[-1].state = (core.ChannelState.LOCKED
                                      if channel_parameters["locked"] else
                                      core.ChannelState.UNLOCKED)
            self._a_tdma[-1].input_level = channel_parameters["inputlevel"]
            self._a_tdma[-1].mer = channel_parameters["mer"]

    @property
    @decorate.translate_requests
    @trace
    def annex(self) -> core.Annex:
        """The active :class:`~excentis.xra31.core.Annex`."""
        self.__update_annex()
        return self._annex

    @annex.setter
    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def annex(self, annex: core.Annex) -> None:
        response = self.xra31.session.post(self.xra31.url_api +
                                           "/channels/dsscqam/setannex",
                                           json={"annex": annex.value},
                                           timeout=self.xra31.timeout)
        response.raise_for_status()

    @property
    @decorate.translate_requests
    @trace
    def ofdm(self) -> typing.Iterable[core.OfdmChannel]:
        self.__update_ofdm()
        return copy.deepcopy(self._ofdm)

    @property
    @decorate.translate_requests
    @trace
    def sc_qam(self) -> typing.Iterable[core.ScQamChannel]:
        self.__update_sc_qam()
        return copy.deepcopy(self._sc_qam)

    @property
    @decorate.translate_requests
    @trace
    def ofdma(self) -> typing.Iterable[core.OfdmaChannel]:
        self.__update_ofdma()
        return copy.deepcopy(self._ofdma)

    @property
    @decorate.translate_requests
    @trace
    def a_tdma(self) -> typing.Iterable[core.ATdmaChannel]:
        self.__update_a_tdma()
        return copy.deepcopy(self._a_tdma)

    def __post_downstream(self, channels) -> None:
        response = self.xra31.session.post(self.xra31.url_api +
                                           "/channels/downstream",
                                           json=channels,
                                           timeout=self.xra31.timeout)
        response.raise_for_status()

    def __add_downstream(  # pylint: disable=C0330
        self,
        plc_frequency: int = 0,
        fft_size: int = 4096,
        cyclic_prefix: int = 192,
        frequency: float = 0.,
        modulation: core.ChannelModulation = core.ChannelModulation.QAM256
    ) -> bool:
        frequency = float(int(frequency * 1e3 / 62.5 + .5) *
                          62500) / 1e6 if frequency > .001 else 0.
        channels = {"ofdmChannels": [], "dsScQamChannels": []}
        if plc_frequency != 0:
            channels["ofdmChannels"].append({
                "plcFrequency": plc_frequency,
                "fft": fft_size,
                "prefix": cyclic_prefix,
            })
        elif frequency != 0.:
            channels["dsScQamChannels"].append({
                "frequency":
                frequency,
                "modulation":
                1 if modulation == core.ChannelModulation.QAM256 else 0
            })
        else:
            return False

        for ofdm_channel in self.ofdm:
            channels["ofdmChannels"].append({
                "id":
                ofdm_channel.xra31_id,
                "plcFrequency":
                ofdm_channel.plc_frequency,
                "fft":
                ofdm_channel.fft_size,
                "prefix":
                ofdm_channel.cyclic_prefix,
            })
        for sc_qam_channel in self.sc_qam:
            channels["dsScQamChannels"].append({
                "id":
                sc_qam_channel.xra31_id,
                "frequency":
                sc_qam_channel.frequency,
                "modulation":
                1 if sc_qam_channel.modulation == core.ChannelModulation.QAM256
                else 0
            })
        self.__post_downstream(channels)
        return True

    def __remove_downstream(self,
                            channel_parameters: core.Channel = None,
                            *,
                            channel_type: core.ChannelType = None,
                            xra31_id: int = -1,
                            frequency: float = 0.) -> bool:
        client_channel = self.find(channel_parameters,
                                   channel_type=channel_type,
                                   xra31_id=xra31_id,
                                   frequency=frequency)
        if not client_channel or not client_channel.is_downstream():
            return False
        channels = {"ofdmChannels": [], "dsScQamChannels": []}
        for ofdm_channel in self.ofdm:
            if ofdm_channel.xra31_id == client_channel.xra31_id:
                continue
            channels["ofdmChannels"].append({
                "id":
                ofdm_channel.xra31_id,
                "plcFrequency":
                ofdm_channel.plc_frequency,
                "fft":
                ofdm_channel.fft_size,
                "prefix":
                ofdm_channel.cyclic_prefix
            })
        for sc_qam_channel in self.sc_qam:
            if sc_qam_channel.xra31_id == client_channel.xra31_id:
                continue
            channels["dsScQamChannels"].append({
                "id":
                sc_qam_channel.xra31_id,
                "frequency":
                sc_qam_channel.frequency,
                "modulation":
                1 if sc_qam_channel.modulation == core.ChannelModulation.QAM256
                else 0
            })
        self.__post_downstream(channels)
        return True

    def __post_upstream(self, channels) -> None:
        response = self.xra31.session.post(self.xra31.url_api +
                                           "/channels/upstream",
                                           json=channels,
                                           timeout=self.xra31.timeout)
        response.raise_for_status()

    def __add_upstream(self,
                       channel_parameters: core.Channel = None,
                       *,
                       xra31_id: int = -1,
                       ucid: int = -1,
                       frequency: float = 0.) -> bool:
        add_channel = self.detection.find(channel_parameters,
                                          xra31_id=xra31_id,
                                          ucid=ucid,
                                          frequency=frequency)
        if not add_channel:
            return False
        channels = {"ofdmaChannels": [], "atdmaChannels": []}
        if add_channel.channel_type == core.ChannelType.OFDMA:
            channels["ofdmaChannels"].append({"usChannelId": add_channel.ucid})
        else:
            channels["atdmaChannels"].append({"usChannelId": add_channel.ucid})

        for ofdma_channel in self.ofdma:
            channels["ofdmaChannels"].append({
                "id": ofdma_channel.xra31_id,
                "usChannelId": ofdma_channel.ucid
            })
        for a_tdma_channel in self.a_tdma:
            channels["atdmaChannels"].append({
                "id": a_tdma_channel.xra31_id,
                "usChannelId": a_tdma_channel.ucid
            })
        self.__post_upstream(channels)
        return True

    def __remove_upstream(self,
                          channel_parameters: core.Channel = None,
                          *,
                          channel_type: core.ChannelType = None,
                          xra31_id: int = -1,
                          ucid: int = -1,
                          frequency: float = 0.) -> bool:
        client_channel = self.find(channel_parameters,
                                   channel_type=channel_type,
                                   xra31_id=xra31_id,
                                   ucid=ucid,
                                   frequency=frequency)

        if not client_channel or not client_channel.is_upstream():
            return False
        channels = {"ofdmaChannels": [], "atdmaChannels": []}
        for ofdma_channel in self.ofdma:
            if ofdma_channel.xra31_id == client_channel.xra31_id:
                continue
            channels["ofdmaChannels"].append({
                "id": ofdma_channel.xra31_id,
                "usChannelId": ofdma_channel.ucid
            })
        for a_tdma_channel in self.a_tdma:
            if a_tdma_channel.xra31_id == client_channel.xra31_id:
                continue
            channels["atdmaChannels"].append({
                "id": a_tdma_channel.xra31_id,
                "usChannelId": a_tdma_channel.ucid
            })
        self.__post_upstream(channels)
        return True

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def add_ofdm(self,
                 plc_frequency: int,
                 fft_size: int = 4096,
                 cyclic_prefix: int = 192) -> bool:
        """Add an :class:`~excentis.xra31.core.OfdmChannel`.

        :param plc_frequency: PLC frequency (MHz).
        :type plc_frequency: int
        :param fft_size: FFT size, defaults to 4096.
        :type fft_size: int, optional
        :param cyclic_prefix: Cyclic prefix, defaults to 192.
        :type cyclic_prefix: int, optional
        :return: ``True`` if successful, ``False`` otherwise.
        :rtype: bool
        """
        return self.__add_downstream(plc_frequency=plc_frequency,
                                     fft_size=fft_size,
                                     cyclic_prefix=cyclic_prefix)

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def add_sc_qam(  # pylint: disable=C0330
        self,
        frequency: float,
        modulation: core.ChannelModulation = core.ChannelModulation.QAM256
    ) -> bool:
        """Add an :class:`~excentis.xra31.ScQamChannel`.

        :param frequency: Center frequency (MHz).
        :type frequency: float
        :param modulation: :class:`~excentis.xra31.core.ChannelModulation`,
                            defaults to 256-QAM.
        :type modulation: core.ChannelModulation, optional
        :return: ``True`` if successful, ``False`` otherwise.
        :rtype: bool
        """
        return self.__add_downstream(frequency=frequency,
                                     modulation=modulation)

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def add_ofdma(self,
                  channel_parameters: core.Channel = None,
                  *,
                  xra31_id: int = -1,
                  ucid: int = -1,
                  frequency: float = 0.) -> bool:
        """Add an :class:`~excentis.xra31.OfdmaChannel`.

        :param channel_parameters: A channel containing
                                   the relevant parameters.
        :type channel_parameters: core.Channel, optional

        :param xra31_id: Channel identifier at the XRA-31.
        :type xra31_id: int, optional
        :param ucid: DOCSIS Upstream Channel ID.
        :type ucid: int, optional
        :param frequency: Center frequency (MHz).
        :type frequency: float, optional
        :return: ``True`` if successful, ``False`` otherwise.
        :rtype: bool
        """
        return self.__add_upstream(channel_parameters,
                                   xra31_id=xra31_id,
                                   ucid=ucid,
                                   frequency=frequency)

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def add_a_tdma(self,
                   channel_parameters: core.Channel = None,
                   *,
                   xra31_id: int = -1,
                   ucid: int = -1,
                   frequency: float = 0.) -> bool:
        """Add an :class:`~excentis.xra31.ATdmaChannel`.

        :param channel_parameters: A channel containing
                                   the relevant parameters.
        :type channel_parameters: core.Channel, optional

        :param xra31_id: Channel identifier at the XRA-31.
        :type xra31_id: int, optional
        :param ucid: DOCSIS Upstream Channel ID.
        :type ucid: int, optional
        :param frequency: Center frequency (MHz).
        :type frequency: float, optional
        :return: ``True`` if successful, ``False`` otherwise.
        :rtype: bool
        """
        return self.__add_upstream(channel_parameters,
                                   xra31_id=xra31_id,
                                   ucid=ucid,
                                   frequency=frequency)

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
        """Remove a channel.

        :param channel_parameters: A channel containing
                                   the relevant parameters.
        :type channel_parameters: core.Channel, optional

        :param channel_type: The :class:`~excentis.xra31.core.ChannelType`.
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
        client_channel = self.find(channel_parameters,
                                   channel_type=channel_type,
                                   xra31_id=xra31_id,
                                   ucid=ucid,
                                   frequency=frequency)
        if not client_channel:
            return False
        if client_channel.is_downstream():
            return self.__remove_downstream(xra31_id=xra31_id,
                                            frequency=frequency)
        return self.__remove_upstream(xra31_id=xra31_id,
                                      ucid=ucid,
                                      frequency=frequency)

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def clear(self) -> None:
        """Remove all channels."""
        self.__post_downstream({"ofdmChannels": [], "dsScQamChannels": []})

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def clear_upstream(self) -> None:
        """Remove all upstream channels."""
        self.__post_upstream({"ofdmaChannels": [], "atdmaChannels": []})

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def remove_ofdm(self,
                    channel_parameters: core.Channel = None,
                    *,
                    xra31_id: int = -1,
                    frequency: float = 0.) -> bool:
        """Remove an :class:`~excentis.xra31.core.OfdmChannel`.

        :param channel_parameters: A channel containing
                                   the relevant parameters.
        :type channel_parameters: core.Channel, optional

        :param xra31_id: Channel identifier at the XRA-31.
        :type xra31_id: int, optional
        :param frequency: PLC frequency (MHz).
        :type frequency: float, optional
        :return: ``True`` if successful, ``False`` otherwise.
        :rtype: bool
        """
        return self.__remove_downstream(channel_parameters,
                                        xra31_id=xra31_id,
                                        frequency=frequency)

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def remove_sc_qam(self,
                      channel_parameters: core.Channel = None,
                      *,
                      xra31_id: int = -1,
                      frequency: float = 0.) -> bool:
        """Remove an :class:`~excentis.xra31.core.ScQamChannel`.

        :param channel_parameters: A channel containing
                                   the relevant parameters.
        :type channel_parameters: core.Channel, optional

        :param xra31_id: Channel identifier at the XRA-31.
        :type xra31_id: int, optional
        :param frequency: Center frequency (MHz).
        :type frequency: float, optional
        :return: ``True`` if successful, ``False`` otherwise.
        :rtype: bool
        """
        return self.__remove_downstream(channel_parameters,
                                        xra31_id=xra31_id,
                                        frequency=frequency)

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def remove_ofdma(self,
                     channel_parameters: core.Channel = None,
                     *,
                     xra31_id: int = -1,
                     ucid: int = -1,
                     frequency: float = 0.) -> bool:
        """Remove an :class:`~excentis.xra31.core.OfdmaChannel`.

        :param channel_parameters: A channel containing
                                   the relevant parameters.
        :type channel_parameters: core.Channel, optional

        :param xra31_id: Channel identifier at the XRA-31.
        :type xra31_id: int, optional
        :param ucid: DOCSIS Upstream Channel ID.
        :type ucid: int, optional
        :param frequency: Center frequency (MHz).
        :type frequency: float, optional
        :return: ``True`` if successful, ``False`` otherwise.
        :rtype: bool
        """
        return self.__remove_upstream(channel_parameters,
                                      xra31_id=xra31_id,
                                      ucid=ucid,
                                      frequency=frequency)

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def remove_a_tdma(self,
                      channel_parameters: core.Channel = None,
                      *,
                      xra31_id: int = -1,
                      ucid: int = -1,
                      frequency: float = 0.) -> bool:
        """Remove an :class:`~excentis.xra31.core.ATdmaChannel`.

        :param channel_parameters: A channel containing
                                   the relevant parameters.
        :type channel_parameters: core.Channel, optional

        :param xra31_id: Channel identifier at the XRA-31.
        :type xra31_id: int, optional
        :param ucid: DOCSIS Upstream Channel ID.
        :type ucid: int, optional
        :param frequency: Center frequency (MHz).
        :type frequency: float, optional
        :return: ``True`` if successful, ``False`` otherwise.
        :rtype: bool
        """
        return self.__remove_upstream(channel_parameters,
                                      xra31_id=xra31_id,
                                      ucid=ucid,
                                      frequency=frequency)

    @trace
    def wait_for_state(self,
                       channel_parameters: core.Channel = None,
                       state: core.ChannelState = core.ChannelState.LOCKED,
                       *,
                       channel_type: core.ChannelType = None,
                       xra31_id: int = -1,
                       ucid: int = -1,
                       frequency: float = 0.,
                       timeout: float = None) -> bool:
        """Wait for a channel to arrive in
        state :class:`~excentis.xra31.core.ChannelState`.

        :param channel_parameters: A channel containing
                                   the relevant parameters.
        :type channel_parameters: core.Channel, optional
        :param state: The target state, defaults to
                      :attr:`~excentis.xra31.core.ChannelState.LOCKED`.
        :type state: core.ChannelState, optional

        :param channel_type: The :class:`~excentis.xra31.core.ChannelType`.
        :type channel_type: core.ChannelType, optional
        :param xra31_id: Channel identifier at the XRA-31.
        :type xra31_id: int, optional
        :param ucid: DOCSIS Upstream Channel ID.
        :type ucid: int, optional
        :param frequency: PLC (OFDM) or center frequency (MHz).
        :type frequency: float, optional
        :param timeout: Number of seconds to wait before giving up;
                        by default it will wait indefinitely.
        :type timeout: float, optional
        :return: ``True`` if successful, ``False`` otherwise.
        :rtype: bool
        """
        stop = 0 if timeout is None else round(time.monotonic()) + timeout
        channel = self.find(channel_parameters,
                            channel_type=channel_type,
                            xra31_id=xra31_id,
                            ucid=ucid,
                            frequency=frequency)
        while not channel or channel.state != state and (
                stop == 0 or time.monotonic() < stop):
            time.sleep(.5)
            channel = self.find(channel_parameters,
                                channel_type=channel_type,
                                xra31_id=xra31_id,
                                ucid=ucid,
                                frequency=frequency)
        return channel is not None and channel.state == state

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @decorate.translate_requests
    @trace
    def set_reference(self,
                      channel_parameters: core.Channel = None,
                      *,
                      channel_type: core.ChannelType = None,
                      xra31_id: int = -1,
                      frequency: float = 0.) -> bool:
        """Select the reference downstream channel.  Note that this removes
        all upstream channels.

        :param channel_parameters: A channel containing
                                   the relevant parameters.
        :type channel_parameters: core.Channel, optional

        :param channel_type: The channel's type.
        :type channel_type: core.ChannelType, optional
        :param xra31_id: ID on the XRA-31.
        :type xra31_id: int, optional
        :param frequency: PLC (OFDM) or center frequency (MHz).
        :type frequency: float, optional
        :return: ``True`` if successful, ``False`` otherwise.
        :rtype: bool
        """
        channel = self.find(channel_parameters,
                            channel_type=channel_type,
                            xra31_id=xra31_id,
                            frequency=frequency)
        if not channel:
            return False
        response = self.xra31.session.put(self.xra31.url_api +
                                          "/channels/setreferencechannel/" +
                                          str(channel.xra31_id),
                                          timeout=self.xra31.timeout)
        response.raise_for_status()
        return True

    @trace
    def describe(self) -> typing.Dict[str, typing.Any]:
        """Representation of information used
        to configure the XRA-31 channels."""
        description = {}
        description["min_client_version"] = JSON_CLIENT_VERSION
        description["annex"] = str(self.annex)
        description[str(core.ChannelType.OFDM)] = [{
            "plc_frequency":
            ofdm_channel.plc_frequency,
            "fft_size":
            ofdm_channel.fft_size,
            "cyclic_prefix":
            ofdm_channel.cyclic_prefix,
            "is_reference":
            ofdm_channel.is_reference
        } for ofdm_channel in self.ofdm]
        description[str(core.ChannelType.SC_QAM)] = [{
            "frequency":
            sc_qam_channel.frequency,
            "modulation":
            str(sc_qam_channel.modulation),
            "is_reference":
            sc_qam_channel.is_reference
        } for sc_qam_channel in self.sc_qam]
        description[str(core.ChannelType.OFDMA)] = [
            ofdma_channel.ucid for ofdma_channel in self.ofdma
        ]
        description[str(core.ChannelType.A_TDMA)] = [
            a_tdma_channel.ucid for a_tdma_channel in self.a_tdma
        ]

        return description

    @decorate.require_full_access
    @decorate.require_capture_inactive
    @trace
    def apply(self,
              description: dict,
              downstream: bool = True,
              upstream: bool = True,
              timeout: float = None):
        """Apply a configuration.

        :param description: The configuration description (:func:`describe`).
        :type description: dict
        :param downstream: Whether or not to apply downstream
                           channel configuration.
        :type downstream: bool, optional
        :param upstream: Whether or not to apply upstream
                         channel configuration.
        :type upstream: bool, optional
        :param timeout: Timeout before which upstream channels must
                        have been detected (s),
                        defaults to ``None`` (unlimited).
        :type timeout: float, optional
        """

        min_client_version = (description["min_client_version"]
                              if "min_client_version" in description else
                              DEFAULT_JSON_CLIENT_VERSION)
        client_version = self.xra31.version
        if not (Version(MIN_JSON_CLIENT_VERSION) <= Version(min_client_version)
                <= Version(client_version)):
            raise exceptions.Xra31VersionException(
                "This API client requires a configuration description"
                " min_client_version between " + MIN_JSON_CLIENT_VERSION +
                " and " + client_version + ", but found " + min_client_version)

        if downstream:
            self.xra31.logger.info("Clear channels")
            self.clear()
        elif upstream:
            self.xra31.logger.info("Clear upstream channels")
            self.clear_upstream()

        if (upstream and (str(core.ChannelType.OFDMA) not in description
                          or not description[str(core.ChannelType.OFDMA)])
                and (str(core.ChannelType.A_TDMA) not in description
                     or not description[str(core.ChannelType.A_TDMA)])):
            upstream = False

        reference = core.DownstreamChannel()
        if downstream:
            if "annex" in description:
                annex = (core.Annex.A if re.match(
                    "^(a|euro|eurodocsis)$", description["annex"].strip(),
                    re.IGNORECASE) else core.Annex.B)
                self.xra31.logger.info("Set Annex to " + str(annex))
                self.annex = annex

            if str(core.ChannelType.OFDM) in description:
                self.xra31.logger.info("Configure OFDM channels")
                for channel_parameters in description[str(
                        core.ChannelType.OFDM)]:
                    if not all(parameter in channel_parameters
                               for parameter in ("plc_frequency", "fft_size",
                                                 "cyclic_prefix")):
                        raise exceptions.Xra31ConfigurationException(
                            "Received incomplete OFDM configuration: " +
                            str(channel_parameters))
                    self.add_ofdm(channel_parameters["plc_frequency"],
                                  channel_parameters["fft_size"],
                                  channel_parameters["cyclic_prefix"])
                    if (not reference.frequency
                            and "is_reference" in channel_parameters
                            and channel_parameters["is_reference"]):
                        reference.channel_type = core.ChannelType.OFDM
                        reference.frequency = channel_parameters[
                            "plc_frequency"]
                        self.xra31.logger.info("Set reference {}".format(
                            str(reference)))
                        self.set_reference(channel_type=reference.channel_type,
                                           frequency=reference.frequency)

            if str(core.ChannelType.SC_QAM) in description:
                self.xra31.logger.info("Configure SC-QAM channels")
                for channel_parameters in description[str(
                        core.ChannelType.SC_QAM)]:
                    if not all(parameter in channel_parameters
                               for parameter in ("frequency", "modulation")):
                        raise exceptions.Xra31ConfigurationException(
                            "Received incomplete SC-QAM configuration: " +
                            str(channel_parameters))
                    self.add_sc_qam(
                        channel_parameters["frequency"],
                        core.ChannelModulation.QAM256 if re.match(
                            "^(qam)?256(-qam)?$",
                            str(channel_parameters["modulation"]).strip(),
                            re.IGNORECASE) else core.ChannelModulation.QAM64)
                    if (not reference.frequency
                            and "is_reference" in channel_parameters
                            and channel_parameters["is_reference"]):
                        reference.channel_type = core.ChannelType.SC_QAM
                        reference.frequency = channel_parameters["frequency"]
                        self.xra31.logger.info("Set reference {}".format(
                            str(reference)))
                        self.set_reference(channel_type=reference.channel_type,
                                           frequency=reference.frequency)

        if upstream:
            # find reference channel
            if reference.frequency == 0:
                for ofdm_channel in self.ofdm:
                    if ofdm_channel.is_reference:
                        reference = ofdm_channel
            if reference.frequency == 0:
                for sc_qam_channel in self.sc_qam:
                    if sc_qam_channel.is_reference:
                        reference = sc_qam_channel
            if reference.frequency == 0:
                raise exceptions.Xra31ConfigurationException(
                    "Can not configure upstream in the absence of "
                    "a reference downstream channel")

            self.xra31.logger.info("Wait for reference {} to lock...".format(
                str(reference)))
            if not self.wait_for_state(channel_parameters=reference,
                                       state=core.ChannelState.LOCKED,
                                       timeout=timeout):
                raise exceptions.Xra31TimeoutException(
                    "Timeout while waiting for "
                    "reference {} to lock".format(str(reference)))

            if str(core.ChannelType.OFDMA) in description:
                self.xra31.logger.info("Configure OFDMA channels")
                for ucid in description[str(core.ChannelType.OFDMA)]:
                    self.xra31.logger.info(
                        "Wait for channel descriptor with UCID {}".format(
                            ucid))
                    if not self.detection.wait_for_channel(ucid=ucid,
                                                           timeout=timeout):
                        raise exceptions.Xra31TimeoutException(
                            "Timeout while waiting for "
                            "channel descriptor with UCID {}".format(ucid))
                    self.add_ofdma(ucid=ucid)
            if str(core.ChannelType.A_TDMA) in description:
                self.xra31.logger.info("Configure A-TDMA channels")
                for ucid in description[str(core.ChannelType.A_TDMA)]:
                    self.xra31.logger.info(
                        "Wait for channel descriptor with UCID {}".format(
                            ucid))
                    if not self.detection.wait_for_channel(ucid=ucid,
                                                           timeout=timeout):
                        raise exceptions.Xra31TimeoutException(
                            "Timeout while waiting for "
                            "channel descriptor with UCID {}".format(ucid))
                    self.add_a_tdma(ucid=ucid)
