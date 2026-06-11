"""State builders for Samsung Air Conditioners."""

from dataclasses import dataclass
from typing import Literal

from ...commands import Command
from ...commands.samsung import SamsungAC0292Command, SamsungAC2A20Command

type SamsungAC2A20HvacMode = Literal["off", "cool", "heat", "dry", "fan_only"]
type SamsungAC0292HvacMode = Literal["off", "auto", "cool", "dry", "fan_only", "heat"]
type SamsungACFanMode = Literal["auto", "low", "medium", "high"]
type SamsungACSwingMode = Literal["off", "vertical"]

_MODE_AUTO = 0
_MODE_COOL = 1
_MODE_DRY = 2
_MODE_FAN = 3
_MODE_HEAT = 4

_0292_FAN_VALUE: dict[SamsungACFanMode, int] = {
    "auto": 0,
    "low": 2,
    "medium": 4,
    "high": 5,
}

_0292_HVAC_VALUE: dict[SamsungAC0292HvacMode, int] = {
    "auto": _MODE_AUTO,
    "cool": _MODE_COOL,
    "dry": _MODE_DRY,
    "fan_only": _MODE_FAN,
    "heat": _MODE_HEAT,
}

_0292_OFF_PAYLOAD = [
    0x02,
    0xB2,
    0x0F,
    0x00,
    0x00,
    0x00,
    0xC0,
    0x01,
    0xD2,
    0x0F,
    0x00,
    0x00,
    0x00,
    0x00,
    0x01,
    0x02,
    0xFF,
    0x71,
    0x80,
    0x11,
    0xC0,
]


@dataclass(frozen=True, slots=True)
class SamsungACVariant1StateBuilder:
    """Builder for Samsung AC variant 1 2A20 21-byte IR commands."""

    hvac_mode: SamsungAC2A20HvacMode
    target_temperature: int
    fan_mode: SamsungACFanMode
    swing: bool = False
    turbo: bool = False
    quiet: bool = False
    smart_saver: bool = False
    auto_clean: bool = False

    def to_command(self) -> Command:
        """Compile the logical state into a 21-byte payload."""
        if self.turbo:
            return SamsungAC2A20Command(
                payload=[
                    0x2A,
                    0x20,
                    0xF9,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0xDF,
                    0x00,
                    0x61,
                    0xFF,
                    0x3B,
                    0xC0,
                    0x08,
                    0x78,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                ]
            )

        if self.quiet:
            return SamsungAC2A20Command(
                payload=[
                    0x2A,
                    0x20,
                    0xF8,
                    0x00,
                    0x00,
                    0x00,
                    0x02,
                    0xDF,
                    0x00,
                    0x71,
                    0xFF,
                    0x38,
                    0xC0,
                    0x08,
                    0x78,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                ]
            )

        if self.swing:
            return SamsungAC2A20Command(
                payload=[
                    0x14,
                    0x90,
                    0x7C,
                    0x00,
                    0x00,
                    0x00,
                    0x80,
                    0x6F,
                    0x80,
                    0xC0,
                    0x6B,
                    0x1C,
                    0x60,
                    0x04,
                    0x3C,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                ]
            )

        if self.smart_saver:
            return SamsungAC2A20Command(
                payload=[
                    0x28,
                    0x20,
                    0xF9,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0xDF,
                    0x00,
                    0x69,
                    0xD7,
                    0x3F,
                    0xC0,
                    0x08,
                    0x78,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                ]
            )

        if self.auto_clean:
            return SamsungAC2A20Command(
                payload=[
                    0x2A,
                    0x20,
                    0xF9,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0xDF,
                    0x00,
                    0x61,
                    0xFF,
                    0x78,
                    0xC1,
                    0x08,
                    0x78,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                ]
            )

        payload = [0x00] * 21

        if self.hvac_mode == "off":
            payload[0:7] = [0x2A, 0x20, 0xFB, 0x00, 0x00, 0x00, 0x00]
            payload[7:14] = [0xDC, 0x00, 0xE9, 0x07, 0x00, 0x00, 0x00]
            payload[14:21] = [0x80, 0x06, 0x88, 0xFB, 0xC7, 0x01, 0x6E]
            return SamsungAC2A20Command(payload=payload)

        payload[0:7] = [0x2A, 0x20, 0xF9, 0x00, 0x00, 0x00, 0x00]
        payload[7:14] = [0xDF, 0x00, 0xE9, 0x07, 0x00, 0x00, 0x00]
        payload[14:21] = [0x80, 0x06, 0x00, 0x00, 0xC7, 0x00, 0x00]

        temp = max(16, min(30, self.target_temperature))
        lookup_key = (self.hvac_mode, temp, self.fan_mode)

        state_mapping: dict[
            tuple[SamsungAC2A20HvacMode, int, SamsungACFanMode],
            tuple[int, int, int, int],
        ] = {
            ("cool", 16, "auto"): (0x88, 0xFB, 0x01, 0x54),
            ("cool", 23, "auto"): (0xC8, 0xFA, 0xC1, 0x55),
            ("cool", 24, "auto"): (0x88, 0xFB, 0x01, 0x46),
            ("cool", 24, "low"): (0x48, 0xFB, 0x01, 0x56),
            ("cool", 24, "medium"): (0x48, 0xFB, 0x01, 0x66),
            ("cool", 24, "high"): (0x08, 0xFB, 0x01, 0x6E),
            ("cool", 25, "auto"): (0x48, 0xFB, 0xC7, 0x46),
            ("cool", 26, "auto"): (0x08, 0xFB, 0x81, 0x56),
            ("cool", 27, "auto"): (0xC8, 0xFA, 0xC1, 0x56),
            ("cool", 30, "auto"): (0xC8, 0xFA, 0x81, 0x57),
            ("heat", 24, "auto"): (0x88, 0xFB, 0x01, 0x06),
            ("dry", 24, "auto"): (0x88, 0xFB, 0x01, 0x86),
            ("fan_only", 24, "auto"): (0x08, 0xFB, 0x01, 0xD6),
        }

        if lookup_key not in state_mapping:
            lookup_key = (self.hvac_mode, temp, "auto")
        if lookup_key not in state_mapping:
            lookup_key = ("cool", temp, "auto")

        b16, b17, b19, b20 = state_mapping[lookup_key]
        payload[16] = b16
        payload[17] = b17
        payload[19] = b19
        payload[20] = b20

        return SamsungAC2A20Command(payload=payload)


@dataclass(frozen=True, slots=True)
class SamsungAC0292StateBuilder:
    """Builder for Samsung AC 0292 21-byte IR commands."""

    hvac_mode: SamsungAC0292HvacMode
    target_temperature: int
    fan_mode: SamsungACFanMode
    swing_mode: SamsungACSwingMode = "off"

    def to_command(self) -> Command:
        """Compile the logical state into a 21-byte payload."""
        if self.hvac_mode == "off":
            return SamsungAC0292Command(payload=_0292_OFF_PAYLOAD.copy())

        section1 = _apply_0292_checksum([0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0xF0])
        section2 = _apply_0292_checksum([0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00])
        section3 = [0x01, 0x02, 0x00, 0x71, 0x00, 0x11, 0xF0]

        swing = 0x2 if self.swing_mode == "vertical" else 0x7
        section3[2] = 0x80 | (swing << 4)
        section3[4] = (max(16, min(30, self.target_temperature)) - 16) << 4

        mode = _0292_HVAC_VALUE[self.hvac_mode]
        fan = 6 if mode == _MODE_AUTO else _0292_FAN_VALUE[self.fan_mode]
        section3[5] = 0x01 | (fan << 1) | (mode << 4)

        return SamsungAC0292Command(
            payload=section1 + section2 + _apply_0292_checksum(section3)
        )


def _apply_0292_checksum(section: list[int]) -> list[int]:
    section = list(section)
    checksum = _0292_section_checksum(section)
    section[1] = (section[1] & 0x0F) | ((checksum & 0x0F) << 4)
    section[2] = (section[2] & 0xF0) | ((checksum >> 4) & 0x0F)
    return section


def _0292_section_checksum(section: list[int]) -> int:
    total = (
        section[0].bit_count()
        + (section[1] & 0x0F).bit_count()
        + (section[2] >> 4).bit_count()
        + sum(byte.bit_count() for byte in section[3:7])
    )
    return total ^ 0xFF


SamsungAC2A20StateBuilder = SamsungACVariant1StateBuilder
SamsungACStateBuilder = SamsungACVariant1StateBuilder
