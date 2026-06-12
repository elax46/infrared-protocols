import pytest

from infrared_protocols.codes.dyson.cool import DysonCoolStateBuilder
from infrared_protocols.commands.dyson import DysonCoolCommand


def test_dyson_cool_payload_validation() -> None:
    """Verify Dyson cool command payload validation rejects invalid values."""
    with pytest.raises(ValueError, match="Dyson payload must be a valid 16-bit integer"):
        DysonCoolCommand(payload=0x10000)


def test_dyson_cool_command_get_raw_timings() -> None:
    """Verify raw timing generation for the Dyson cool off action."""
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
    """Verify extended Dyson cool actions generate valid raw timings."""
    builder = DysonCoolStateBuilder(action=action)
    command = builder.to_command()
    timings = command.get_raw_timings()

    assert len(timings) > 0
    assert timings[0] == 8940
    assert timings[1] == 4440