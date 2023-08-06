"""
Core classes and enumerations needed for the representation of XRA-31 objects.
"""

import enum
import typing


class Annex(enum.IntEnum):
    """An enumeration of the two Annex types."""
    A = 0  #: EuroDOCSIS.
    B = 1  #: US DOCSIS.

    def __str__(self) -> str:
        # pylint: disable=invalid-sequence-index
        return ["EuroDOCSIS", "US DOCSIS"][self.value]


class ChannelState(enum.IntEnum):
    """An enumeration of the states a configured channel can be in."""
    UNLOCKED = 0  #: Unlocked.
    PLC_LOCKED = 1  #: PLC Locked (OFDM only).
    LOCKED = 2  #: Locked.

    def __str__(self) -> str:
        # pylint: disable=invalid-sequence-index
        return ["Unlocked", "PLC Locked", "Locked"][self.value]


class ChannelType(enum.IntEnum):
    """An enumeration of the different channel types."""
    OFDM = 0  #: Downstream OFDM.
    SC_QAM = 1  #: Downstream SC-QAM.
    OFDMA = 2  #: Upstream OFDMA.
    A_TDMA = 3  #: Upstream A-TDMA.

    def __str__(self) -> str:
        # pylint: disable=invalid-sequence-index
        return ["OFDM", "SC-QAM", "OFDMA", "A-TDMA"][self.value]


class ChannelModulation(enum.IntEnum):
    """An enumeration of the Downstream SC-QAM Modulations."""
    QAM64 = 0  #: 64-QAM.
    QAM256 = 1  #: 256-QAM.

    def __str__(self) -> str:
        # pylint: disable=invalid-sequence-index
        return ["64-QAM", "256-QAM"][self.value]


class Channel:
    """A generic XRA-31 channel including the parameters needed to identify it
    and its state at the XRA-31."""
    def __init__(self,
                 channel_type: ChannelType = None,
                 xra31_id: int = -1,
                 docsis_id: int = -1,
                 frequency: float = 0.,
                 *,
                 is_captured: bool = False):
        # Identifiers
        #: The channel's type (:class:`ChannelType`).
        self.channel_type = channel_type
        #: Unique identifier of the channel on the XRA-31.
        self.xra31_id = xra31_id
        #: The channel's DOCSIS ID (upstream UCID).
        self.docsis_id = docsis_id
        #: The channel's PLC (OFDM) or center frequency (MHz).
        self._frequency = int(frequency * 1e6 + .5)
        # State
        #: The channel's state (:class:`ChannelState`).
        self.state = ChannelState.UNLOCKED
        self.input_level = 0.
        """The input level at the XRA-31's connector (dBmV per 6 MHz for OFDM,
        dBmV per 1.6 MHz for OFDMA, dBmV for SC-QAM and A-TDMA)."""
        #: The MER at the XRA-31 (dB).
        self.mer = 0.
        #: Indicates if this channel is included in the capture.
        self.is_captured = is_captured

    @property
    def frequency(self) -> float:
        """The channel's PLC (OFDM) or center frequency (MHz)."""
        return float(self._frequency) / 1e6

    @frequency.setter
    def frequency(self, frequency: float) -> None:
        self._frequency = int(frequency * 1e6 + .5)

    @property
    def start_frequency(self) -> float:
        """Start frequency of the channel.
        Accurate for OFDM, SC-QAM and OFDMA."""
        return self.frequency

    @property
    def stop_frequency(self) -> float:
        """Stop frequency of the channel.
        Accurate for OFDM, SC-QAM and OFDMA."""
        return self.frequency

    def is_downstream(self) -> bool:
        """Indicates if it is an OFDM or a downstream SC-QAM channel."""
        return (self.channel_type == ChannelType.OFDM
                or self.channel_type == ChannelType.SC_QAM)

    def is_upstream(self) -> bool:
        """Indicates if it is an OFDMA or an A-TDMA channel."""
        return (self.channel_type == ChannelType.OFDMA
                or self.channel_type == ChannelType.A_TDMA)

    def __str__(self) -> str:
        return "{} channel at {}MHz".format(str(self.channel_type),
                                            self.frequency)


class DownstreamChannel(Channel):
    """Base for a downstream :class:`~excentis.xra31.core.Channel`."""
    def __init__(self,
                 channel_type: ChannelType = None,
                 xra31_id: int = -1,
                 frequency: float = 0.,
                 *,
                 docsis_id: int = -1,
                 is_reference: bool = False,
                 is_captured: bool = False):
        super().__init__(channel_type,
                         xra31_id,
                         docsis_id,
                         frequency,
                         is_captured=is_captured)
        self.is_reference = is_reference

    def is_downstream(self) -> bool:
        return True


class UpstreamChannel(Channel):
    """Base for an upstream :class:`~excentis.xra31.core.Channel`."""
    def __init__(self,
                 channel_type: ChannelType = None,
                 xra31_id: int = -1,
                 ucid: int = -1,
                 *,
                 frequency: float = 0.,
                 is_captured: bool = False):
        super().__init__(channel_type,
                         xra31_id,
                         ucid,
                         frequency,
                         is_captured=is_captured)

    @property
    def ucid(self) -> int:
        """DOCSIS Upstream Channel ID."""
        return self.docsis_id

    @ucid.setter
    def ucid(self, ucid: int) -> None:
        self.docsis_id = ucid

    def is_upstream(self) -> bool:
        return True

    def __str__(self) -> str:
        return "{} channel with UCID {}".format(str(self.channel_type),
                                                self.ucid)


class OfdmChannel(DownstreamChannel):
    """OFDM :class:`~excentis.xra31.core.Channel`."""
    def __init__(self,
                 xra31_id: int = -1,
                 plc_frequency: int = 0,
                 fft_size: int = 0,
                 cyclic_prefix: int = 0,
                 rolloff_period: int = 0,
                 start_frequency: float = None,
                 stop_frequency: float = None,
                 *,
                 docsis_id: int = -1,
                 is_reference: bool = False,
                 is_captured: bool = False):
        super().__init__(ChannelType.OFDM,
                         xra31_id,
                         float(plc_frequency),
                         docsis_id=docsis_id,
                         is_reference=is_reference,
                         is_captured=is_captured)
        self._start_frequency = int(start_frequency * 1e6 +
                                    .5) if start_frequency else self._frequency
        self._stop_frequency = int(stop_frequency * 1e6 +
                                   .5) if stop_frequency else self._frequency
        #: FFT size.
        self.fft_size = fft_size
        #: Cyclic prefix, in OFDM samples at the rate of 204.8 MHz.
        self.cyclic_prefix = cyclic_prefix
        #: Roll-off period, in OFDM samples at the rate of 204.8 MHz.
        self.rolloff_period = rolloff_period

    @property
    def start_frequency(self) -> float:
        return float(self._start_frequency) / 1e6

    @start_frequency.setter
    def start_frequency(self, start_frequency: float) -> None:
        self._start_frequency = int(start_frequency * 1e6 + .5)

    @property
    def stop_frequency(self) -> float:
        return float(self._stop_frequency) / 1e6

    @stop_frequency.setter
    def stop_frequency(self, stop_frequency: float) -> None:
        self._stop_frequency = int(stop_frequency * 1e6 + .5)

    @property
    def plc_frequency(self) -> int:
        """PLC Frequency, the start of the contiguous 6 MHz spectral region
        within which the PLC modulation takes place (MHz)."""
        return int(self.frequency + .5)

    @plc_frequency.setter
    def plc_frequency(self, plc_frequency: int) -> None:
        self.frequency = float(plc_frequency)


class ScQamChannel(DownstreamChannel):
    """Downstream SC-QAM :class:`~excentis.xra31.core.Channel`."""
    def __init__(self,
                 xra31_id: int = -1,
                 frequency: float = 0.,
                 modulation: ChannelModulation = ChannelModulation.QAM256,
                 annex: Annex = Annex.A,
                 *,
                 docsis_id: int = -1,
                 is_reference: bool = False,
                 is_captured: bool = False):
        super().__init__(ChannelType.SC_QAM,
                         xra31_id,
                         frequency,
                         docsis_id=docsis_id,
                         is_reference=is_reference,
                         is_captured=is_captured)
        self._frequency = int(frequency * 1e3 / 62.5 + .5) * 62500
        self.annex = annex
        self.modulation = modulation

    @property
    def frequency(self) -> float:
        """The SC-QAM channel frequency on a 62.5kHz grid (MHz)."""
        return float(self._frequency) / 1e6

    @frequency.setter
    def frequency(self, frequency: float) -> None:
        self._frequency = int(frequency * 1e3 / 62.5 + .5) * 62500

    @property
    def _channel_width(self) -> float:
        return 8. if self.annex == Annex.A else 6.

    @property
    def start_frequency(self) -> float:
        return self.frequency - self._channel_width * .5

    @property
    def stop_frequency(self) -> float:
        return self.frequency + self._channel_width * .5


class OfdmaChannel(UpstreamChannel):
    """OFDMA :class:`~excentis.xra31.core.Channel`."""
    def __init__(self,
                 xra31_id: int = -1,
                 ucid: int = -1,
                 start_frequency: float = 0.,
                 stop_frequency: float = 0.,
                 *,
                 is_captured: bool = False):
        super().__init__(ChannelType.OFDMA,
                         xra31_id,
                         ucid,
                         frequency=start_frequency,
                         is_captured=is_captured)
        self._stop_frequency = int(stop_frequency * 1e6 +
                                   .5) if stop_frequency else self._frequency

    @property
    def frequency(self) -> float:
        return .5 * (self.start_frequency + self.stop_frequency)

    @property
    def start_frequency(self) -> float:
        return float(self._frequency) / 1e6

    @start_frequency.setter
    def start_frequency(self, start_frequency: float) -> None:
        self._frequency = int(start_frequency * 1e6 + .5)

    @property
    def stop_frequency(self) -> float:
        return float(self._stop_frequency) / 1e6

    @stop_frequency.setter
    def stop_frequency(self, stop_frequency: float) -> None:
        self._stop_frequency = int(stop_frequency * 1e6 + .5)


class ATdmaChannel(UpstreamChannel):
    """A-TDMA :class:`~excentis.xra31.core.Channel`."""
    def __init__(self,
                 xra31_id: int = -1,
                 ucid: int = -1,
                 frequency: float = 0.,
                 modulation_rate: float = 1.280,
                 *,
                 is_captured: bool = False):
        super().__init__(ChannelType.A_TDMA,
                         xra31_id,
                         ucid,
                         frequency=frequency,
                         is_captured=is_captured)
        self.modulation_rate = modulation_rate  #: Modulation rate (MHz).

    @property
    def _channel_width(self) -> float:
        return int(self.modulation_rate * 1.25 + .5)

    @property
    def start_frequency(self) -> float:
        return self.frequency - self._channel_width * .5

    @property
    def stop_frequency(self) -> float:
        return self.frequency + self._channel_width * .5


class ChannelList:
    """Base for an XRA-31 :class:`~excentis.xra31.core.Channel` list."""
    def __init__(self):
        pass

    def __iter__(self) -> typing.Iterator[Channel]:
        yield from self.channels

    def __contains__(self, candidate: Channel) -> bool:
        return self.find(candidate) is not None

    @property
    def ofdm(self) -> typing.Iterable[OfdmChannel]:
        """Get the OFDM channels."""
        return []

    @property
    def sc_qam(self) -> typing.Iterable[ScQamChannel]:
        """Get the downstream SC-QAM channels."""
        return []

    @property
    def downstream(self) -> typing.Iterable[DownstreamChannel]:
        """Get the downstream channels."""
        yield from self.ofdm
        yield from self.sc_qam

    @property
    def ofdma(self) -> typing.Iterable[OfdmaChannel]:
        """Get the OFDMA channels."""
        return []

    @property
    def a_tdma(self) -> typing.Iterable[ATdmaChannel]:
        """Get the A-TDMA channels."""
        return []

    @property
    def upstream(self) -> typing.Iterable[UpstreamChannel]:
        """Get the upstream channels."""
        yield from self.ofdma
        yield from self.a_tdma

    @property
    def channels(self) -> typing.Iterable[Channel]:
        """Get all channels."""
        yield from self.downstream
        yield from self.upstream

    def filter(self,
               channel_type: ChannelType = None) -> typing.Iterable[Channel]:
        """Get all channels with a given :class:`ChannelType`."""
        if channel_type == ChannelType.OFDM:
            yield from self.ofdm
        elif channel_type == ChannelType.SC_QAM:
            yield from self.sc_qam
        elif channel_type == ChannelType.OFDMA:
            yield from self.ofdma
        elif channel_type == ChannelType.A_TDMA:
            yield from self.a_tdma
        else:
            yield from self.channels

    def find(self,
             channel_parameters: Channel = None,
             *,
             channel_type: ChannelType = None,
             xra31_id: int = -1,
             ucid: int = -1,
             frequency: float = 0.) -> typing.Optional[Channel]:
        """Find a channel.
        Parameters can be set selectively within channel_parameters, or
        individually.
        If a perfect frequency match can't be found,
        a channel containing the frequency is returned if available.

        :param channel_parameters: A channel containing the parameters.
        :type channel_parameters: Channel, optional
        :param channel_type: The type of channel.
        :type channel_type: ChannelType, optional
        :param xra31_id: Channel identifier at the XRA-31.
        :type xra31_id: int, optional
        :param ucid: DOCSIS Upstream Channel ID.
        :type ucid: int, optional
        :param frequency: The frequency of the channel (MHz).
        :type frequency: float, optional
        :return: The channel if found, ``None`` otherwise.
        :rtype: core.Channel
        """
        if channel_parameters:
            channel_type = channel_parameters.channel_type
            xra31_id = channel_parameters.xra31_id
            frequency = channel_parameters.frequency
            if not channel_parameters.is_downstream():
                ucid = channel_parameters.docsis_id
            else:
                ucid = -1
        if frequency <= 1. and xra31_id == -1 and ucid == -1:
            return None
        if xra31_id != -1:
            for candidate in self.filter(channel_type):
                if candidate.xra31_id == xra31_id:
                    return candidate
        elif ucid != -1:
            for candidate in self.filter(channel_type):
                if candidate.is_upstream() and candidate.docsis_id == ucid:
                    return candidate
        else:
            frequency = float(int(frequency * 1e6 + .5)) / 1e6
            if channel_type == ChannelType.SC_QAM:
                frequency = float(
                    int(frequency * 1e3 / 62.5 + .5) * 62500) / 1e6
            for candidate in self.filter(channel_type):
                if frequency == candidate.frequency:
                    return candidate
            for candidate in self.filter(channel_type):
                if (candidate.start_frequency - .001 <= frequency <=
                        candidate.stop_frequency + .001):
                    return candidate
        return None
