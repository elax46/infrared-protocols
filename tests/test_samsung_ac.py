"""Tests for the Samsung AC IR command encoder."""

from infrared_protocols.codes.samsung.ac import SamsungACCommand


def test_samsung_ac_command_get_raw_timings() -> None:
    """Test Samsung AC command raw timings compilation."""
    # Setup condition: Cool mode, 24°C, Fan High
    # Expected bytes layout based on the protocol:
    # byte 0: 0x02, byte 1: 0x92
    # byte 5: (24 - 16) << 4 = 8 << 4 = 0x80
    # byte 6: 0x01 (cool)
    # byte 7: 0xA0 (high)
    # bytes 2..4, 8..12: 0x00
    # Checksum: 0x00 ^ 0x00 ^ 0x00 ^ 0x80 ^ 0x01 ^ 0xA0 ^ ... = 0x21
    # Full payload to bit-blast: [0x02, 0x92, 0x00, 0x00, 0x00, 0x80, 0x01, 0xA0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x21]
    
    expected_raw_timings = [
        # Leader pulse
        3000,
        -3000,
        # Byte 0: 0x02 (LSB first: 0,1,0,0,0,0,0,0)
        600, -400, 600, -1400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 1: 0x92 (LSB first: 0,1,0,0,1,0,0,1)
        600, -400, 600, -1400, 600, -400, 600, -400, 600, -1400, 600, -400, 600, -400, 600, -1400,
        # Byte 2: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 3: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 4: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 5: 0x80 (LSB first: 0,0,0,0,0,0,0,1)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -1400,
        # Byte 6: 0x01 (LSB first: 1,0,0,0,0,0,0,0)
        600, -1400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 7: 0xA0 (LSB first: 0,0,0,0,0,1,0,1)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -1400, 600, -400, 600, -1400,
        # Byte 8: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 9: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 10: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 11: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 12: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 13: 0x21 (LSB first: 1,0,0,0,0,1,0,0) -> Checksum
        600, -1400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -1400, 600, -400, 600, -400,
        # End pulse
        600,
    ]

    builder = SamsungACCommand(
        hvac_mode="cool",
        target_temperature=24,
        fan_mode="high",
    )
    command = builder.to_command()
    timings = command.get_raw_timings()

    assert timings == expected_raw_timings
    assert command.modulation == 38000