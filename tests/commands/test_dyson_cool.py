import pytest

from infrared_protocols.codes.dyson.cool import DysonCoolStateBuilder
from infrared_protocols.commands.dyson import DysonCoolCommand


def test_dyson_cool_payload_validation() -> None:
    """Test that DysonCoolCommand validates 24-bit payload constraint."""
    with pytest.raises(ValueError, match="Dyson payload must be a valid 24-bit integer"):
        DysonCoolCommand(payload=0x1000000)


def test_dyson_cool_command_get_raw_timings() -> None:
    """Verify raw timings for a simple 'off' Dyson Cool command.

    Ensures the command produced by DysonCoolStateBuilder(action="off")
    yields the expected leading and subsequent timing values.
    """
    builder = DysonCoolStateBuilder(action="off")
    command = builder.to_command()
    timings = command.get_raw_timings()

    assert timings[0] == 8940
    assert timings[1] == 4440
    assert timings[2] == 590
    assert timings[3] == 520
    assert timings[4] == 590
    assert timings[5] == 1630


@pytest.mark.parametrize(
    "action",
    [
        "cool_on",
        "speed_up",
        "speed_down",
        "time_up",
        "time_down",
        "swing",
    ],
)
def test_dyson_cool_extended_actions(action: str) -> None:
    """Ensure extended Dyson Cool actions produce a valid timing sequence.

    Verifies that for various extended actions the generated command has
    a non-empty timing list and that the leading timings match expected
    Dyson header values.
    """
    builder = DysonCoolStateBuilder(action=action)
    command = builder.to_command()
    timings = command.get_raw_timings()

    assert len(timings) > 0
    assert timings[0] == 8940
    assert timings[1] == 4440