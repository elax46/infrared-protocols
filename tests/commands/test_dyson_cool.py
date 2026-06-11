"""Tests for the Dyson Cool IR command encoder and state builder."""

import pytest

from infrared_protocols.codes.dyson.cool import DysonCoolStateBuilder
from infrared_protocols.commands.dyson import DysonCoolCommand


def test_dyson_cool_payload_validation() -> None:
    """Test that DysonCoolCommand enforces strict 16-bit boundaries."""
    with pytest.raises(ValueError, match="Dyson payload must be a valid 16-bit integer"):
        DysonCoolCommand(payload=0x10000)  


def test_dyson_cool_command_get_raw_timings() -> None:
    """Test that Dyson logical actions compile to exact structural timings."""
    # L'azione "off" mappa il payload 0x4001 -> In binario su 16 bit: 0100 0000 0000 0001
    builder = DysonCoolStateBuilder(action="off")
    command = builder.to_command()
    timings = command.get_raw_timings()


    assert timings[0] == 8940
    assert timings[1] == 4440


    assert timings[2] == 590
    assert timings[3] == 520


    assert timings[4] == 590
    assert timings[5] == 1630


def test_dyson_cool_extended_actions() -> None:
    """Test that specialized speeds and timer increments compile safely."""
    test_cases = ["speed_5", "speed_10", "time_up", "time_down", "swing"]
    
    for action in test_cases:
        builder = DysonCoolStateBuilder(action=action)
        command = builder.to_command()
        timings = command.get_raw_timings()
        
        assert len(timings) > 0

        assert timings[0] == 8940
        assert timings[1] == 4440