"""Tests for the Samsung AC IR command encoders."""

import pytest

from infrared_protocols.codes.samsung.ac import (
    SamsungAC0292HvacMode,
    SamsungAC0292StateBuilder,
    SamsungAC2A20HvacMode,
    SamsungACFanMode,
    SamsungACSwingMode,
    SamsungACVariant1StateBuilder,
)
from infrared_protocols.commands.samsung import (
    SamsungAC0292Command,
    SamsungAC2A20Command,
)


def _payload(hex_values: str) -> list[int]:
    return [int(byte, 16) for byte in hex_values.split()]


@pytest.mark.parametrize(
    ("hvac_mode", "target_temperature", "fan_mode", "expected_payload"),
    [
        pytest.param(
            "cool",
            16,
            "auto",
            _payload("2A 20 F9 00 00 00 00 DF 00 E9 07 00 00 00 80 06 88 FB C7 01 54"),
            id="cool-16-auto",
        ),
        pytest.param(
            "cool",
            24,
            "auto",
            _payload("2A 20 F9 00 00 00 00 DF 00 E9 07 00 00 00 80 06 88 FB C7 01 46"),
            id="cool-24-auto",
        ),
        pytest.param(
            "cool",
            24,
            "low",
            _payload("2A 20 F9 00 00 00 00 DF 00 E9 07 00 00 00 80 06 48 FB C7 01 56"),
            id="cool-24-low",
        ),
        pytest.param(
            "cool",
            24,
            "medium",
            _payload("2A 20 F9 00 00 00 00 DF 00 E9 07 00 00 00 80 06 48 FB C7 01 66"),
            id="cool-24-medium",
        ),
        pytest.param(
            "cool",
            24,
            "high",
            _payload("2A 20 F9 00 00 00 00 DF 00 E9 07 00 00 00 80 06 08 FB C7 01 6E"),
            id="cool-24-high",
        ),
        pytest.param(
            "cool",
            25,
            "auto",
            _payload("2A 20 F9 00 00 00 00 DF 00 E9 07 00 00 00 80 06 48 FB C7 C7 46"),
            id="cool-25-auto",
        ),
        pytest.param(
            "cool",
            26,
            "auto",
            _payload("2A 20 F9 00 00 00 00 DF 00 E9 07 00 00 00 80 06 08 FB C7 81 56"),
            id="cool-26-auto",
        ),
        pytest.param(
            "cool",
            27,
            "auto",
            _payload("2A 20 F9 00 00 00 00 DF 00 E9 07 00 00 00 80 06 C8 FA C7 C1 56"),
            id="cool-27-auto",
        ),
        pytest.param(
            "cool",
            30,
            "auto",
            _payload("2A 20 F9 00 00 00 00 DF 00 E9 07 00 00 00 80 06 C8 FA C7 81 57"),
            id="cool-30-auto",
        ),
        pytest.param(
            "heat",
            24,
            "auto",
            _payload("2A 20 F9 00 00 00 00 DF 00 E9 07 00 00 00 80 06 88 FB C7 01 06"),
            id="heat-24-auto",
        ),
        pytest.param(
            "dry",
            24,
            "auto",
            _payload("2A 20 F9 00 00 00 00 DF 00 E9 07 00 00 00 80 06 88 FB C7 01 86"),
            id="dry-24-auto",
        ),
        pytest.param(
            "fan_only",
            24,
            "auto",
            _payload("2A 20 F9 00 00 00 00 DF 00 E9 07 00 00 00 80 06 08 FB C7 01 D6"),
            id="fan-only-24-auto",
        ),
    ],
)
def test_samsung_ac_2a20_state_builder(
    hvac_mode: SamsungAC2A20HvacMode,
    target_temperature: int,
    fan_mode: SamsungACFanMode,
    expected_payload: list[int],
) -> None:
    """Test Samsung AC 2A20 state builder payloads and timings."""
    builder = SamsungACVariant1StateBuilder(
        hvac_mode=hvac_mode,
        target_temperature=target_temperature,
        fan_mode=fan_mode,
    )

    command = builder.to_command()

    assert isinstance(command, SamsungAC2A20Command)
    assert command.payload == expected_payload
    assert command.modulation == 40000
    assert command.get_raw_timings() == _compile_2a20_timings(expected_payload)


def test_samsung_ac_2a20_state_builder_off() -> None:
    """Test Samsung AC 2A20 off state payload and timings."""
    expected_payload = _payload(
        "2A 20 FB 00 00 00 00 DC 00 E9 07 00 00 00 80 06 88 FB C7 01 6E"
    )

    builder = SamsungACVariant1StateBuilder(
        hvac_mode="off",
        target_temperature=24,
        fan_mode="auto",
    )
    command = builder.to_command()

    assert isinstance(command, SamsungAC2A20Command)
    assert command.payload == expected_payload
    assert command.get_raw_timings() == _compile_2a20_timings(expected_payload)


@pytest.mark.parametrize(
    ("builder", "expected_payload"),
    [
        pytest.param(
            SamsungACVariant1StateBuilder(
                hvac_mode="cool",
                target_temperature=24,
                fan_mode="auto",
                turbo=True,
            ),
            _payload("2A 20 F9 00 00 00 00 DF 00 61 FF 3B C0 08 78 00 00 00 00 00 00"),
            id="turbo",
        ),
        pytest.param(
            SamsungACVariant1StateBuilder(
                hvac_mode="cool",
                target_temperature=24,
                fan_mode="auto",
                quiet=True,
            ),
            _payload("2A 20 F8 00 00 00 02 DF 00 71 FF 38 C0 08 78 00 00 00 00 00 00"),
            id="quiet",
        ),
        pytest.param(
            SamsungACVariant1StateBuilder(
                hvac_mode="cool",
                target_temperature=24,
                fan_mode="auto",
                swing=True,
            ),
            _payload("14 90 7C 00 00 00 80 6F 80 C0 6B 1C 60 04 3C 00 00 00 00 00 00"),
            id="swing",
        ),
        pytest.param(
            SamsungACVariant1StateBuilder(
                hvac_mode="cool",
                target_temperature=24,
                fan_mode="auto",
                smart_saver=True,
            ),
            _payload("28 20 F9 00 00 00 00 DF 00 69 D7 3F C0 08 78 00 00 00 00 00 00"),
            id="smart-saver",
        ),
        pytest.param(
            SamsungACVariant1StateBuilder(
                hvac_mode="cool",
                target_temperature=24,
                fan_mode="auto",
                auto_clean=True,
            ),
            _payload("2A 20 F9 00 00 00 00 DF 00 61 FF 78 C1 08 78 00 00 00 00 00 00"),
            id="auto-clean",
        ),
    ],
)
def test_samsung_ac_2a20_special_functions(
    builder: SamsungACVariant1StateBuilder,
    expected_payload: list[int],
) -> None:
    """Test Samsung AC 2A20 special function payloads and timings."""
    command = builder.to_command()

    assert isinstance(command, SamsungAC2A20Command)
    assert command.payload == expected_payload
    assert command.get_raw_timings() == _compile_2a20_timings(expected_payload)


@pytest.mark.parametrize(
    (
        "hvac_mode",
        "target_temperature",
        "fan_mode",
        "swing_mode",
        "expected_payload",
    ),
    [
        pytest.param(
            "cool",
            16,
            "auto",
            "off",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 F2 FE 71 00 11 F0"),
            id="cool-16-auto-off",
        ),
        pytest.param(
            "cool",
            23,
            "auto",
            "off",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 C2 FE 71 70 11 F0"),
            id="cool-23-auto-off",
        ),
        pytest.param(
            "cool",
            24,
            "auto",
            "off",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 E2 FE 71 80 11 F0"),
            id="cool-24-auto-off",
        ),
        pytest.param(
            "cool",
            25,
            "auto",
            "off",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 D2 FE 71 90 11 F0"),
            id="cool-25-auto-off",
        ),
        pytest.param(
            "cool",
            26,
            "auto",
            "off",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 D2 FE 71 A0 11 F0"),
            id="cool-26-auto-off",
        ),
        pytest.param(
            "cool",
            27,
            "auto",
            "off",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 C2 FE 71 B0 11 F0"),
            id="cool-27-auto-off",
        ),
        pytest.param(
            "cool",
            30,
            "auto",
            "off",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 C2 FE 71 E0 11 F0"),
            id="cool-30-auto-off",
        ),
        pytest.param(
            "cool",
            24,
            "low",
            "off",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 D2 FE 71 80 15 F0"),
            id="cool-24-low-off",
        ),
        pytest.param(
            "cool",
            24,
            "medium",
            "off",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 D2 FE 71 80 19 F0"),
            id="cool-24-medium-off",
        ),
        pytest.param(
            "cool",
            24,
            "high",
            "off",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 C2 FE 71 80 1B F0"),
            id="cool-24-high-off",
        ),
        pytest.param(
            "heat",
            24,
            "auto",
            "off",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 E2 FE 71 80 41 F0"),
            id="heat-24-auto-off",
        ),
        pytest.param(
            "dry",
            24,
            "auto",
            "off",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 E2 FE 71 80 21 F0"),
            id="dry-24-auto-off",
        ),
        pytest.param(
            "fan_only",
            24,
            "auto",
            "off",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 D2 FE 71 80 31 F0"),
            id="fan-only-24-auto-off",
        ),
        pytest.param(
            "cool",
            25,
            "medium",
            "vertical",
            _payload("02 92 0F 00 00 00 F0 01 D2 0F 00 00 00 00 01 E2 AE 71 90 19 F0"),
            id="cool-25-medium-vertical",
        ),
    ],
)
def test_samsung_ac_0292_state_builder(
    hvac_mode: SamsungAC0292HvacMode,
    target_temperature: int,
    fan_mode: SamsungACFanMode,
    swing_mode: SamsungACSwingMode,
    expected_payload: list[int],
) -> None:
    """Test Samsung AC 0292 state builder payloads and timings."""
    builder = SamsungAC0292StateBuilder(
        hvac_mode=hvac_mode,
        target_temperature=target_temperature,
        fan_mode=fan_mode,
        swing_mode=swing_mode,
    )

    command = builder.to_command()

    assert isinstance(command, SamsungAC0292Command)
    assert command.payload == expected_payload
    assert command.modulation == 38000
    assert command.get_raw_timings() == _compile_0292_timings(expected_payload)


def test_samsung_ac_0292_state_builder_off() -> None:
    """Test Samsung AC 0292 off state payload and timings."""
    expected_payload = _payload(
        "02 B2 0F 00 00 00 C0 01 D2 0F 00 00 00 00 01 02 FF 71 80 11 C0"
    )

    builder = SamsungAC0292StateBuilder(
        hvac_mode="off",
        target_temperature=24,
        fan_mode="auto",
    )
    command = builder.to_command()

    assert isinstance(command, SamsungAC0292Command)
    assert command.payload == expected_payload
    assert command.get_raw_timings() == _compile_0292_timings(expected_payload)


def test_samsung_ac_0292_command_rejects_invalid_payload_length() -> None:
    """Test Samsung AC 0292 payload length validation."""
    with pytest.raises(ValueError, match="exactly 21 bytes"):
        SamsungAC0292Command(payload=[0x00])


def _compile_2a20_timings(payload: list[int]) -> list[int]:
    timings: list[int] = [3100, -9850]
    for index, byte in enumerate(payload):
        for bit in range(8):
            timings.extend([570, -1460 if (byte >> bit) & 1 else -440])
        if index in (6, 13):
            timings.extend([570, -3950])
    timings.append(570)
    return timings


def _compile_0292_timings(payload: list[int]) -> list[int]:
    timings: list[int] = [690, -17844]
    for offset in range(0, len(payload), 7):
        timings.extend([3086, -8864])
        for byte in payload[offset : offset + 7]:
            for bit in range(8):
                timings.extend([586, -1432 if (byte >> bit) & 1 else -436])
        timings.extend([586, -30000 if offset + 7 >= len(payload) else -2886])
    return timings
