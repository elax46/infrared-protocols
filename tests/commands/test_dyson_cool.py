"""Tests for the Dyson Cool IR command encoder and state builder."""

import pytest

from infrared_protocols.codes.dyson.cool import DysonCoolStateBuilder
from infrared_protocols.commands.dyson import DysonCoolCommand


def test_dyson_cool_payload_validation() -> None:
    """Test that DysonCoolCommand enforces strict 15-bit boundaries."""
    with pytest.raises(ValueError, match="Dyson payload must be a valid 15-bit integer"):
        DysonCoolCommand(payload=0x8000)  # Out of boundary (16th bit set)


def test_dyson_cool_command_get_raw_timings() -> None:
    """Test that Dyson logical actions compile to exact structural timings."""
    builder = DysonCoolStateBuilder(action="off")
    command = builder.to_command()
    timings = command.get_raw_timings()

    # Verify leader pulse structure
    assert timings[0] == 1480
    assert timings[1] == -520

    # Bit 0 (MSB) is '1' -> 520, -1020
    assert timings[2] == 520
    assert timings[3] == -1020

    # Bit 1 is '0' -> 520, -500
    assert timings[4] == 520
    assert timings[5] == -500


def test_dyson_cool_extended_actions() -> None:
    """Test that specialized speeds and timer increments compile safely."""
    test_cases = ["speed_5", "speed_10", "time_up", "time_down", "swing"]
    
    for action in test_cases:
        builder = DysonCoolStateBuilder(action=action)
        command = builder.to_command()
        timings = command.get_raw_timings()
        
        assert len(timings) > 0
        assert timings[0] == 1480
        assert timings[1] == -520