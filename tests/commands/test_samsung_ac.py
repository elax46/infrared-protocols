"""Tests for the Samsung AC IR command encoder."""

from infrared_protocols.codes.samsung.ac import SamsungACStateBuilder


def test_samsung_ac_command_get_raw_timings() -> None:
    """Test Samsung AC command raw timings compilation for 21-byte protocol."""
    # Setup condition: Cool mode, 24°C, Fan Auto (based on the captured physical remote data)
    # Expected bytes layout (3 blocks of 7 bytes):
    # Block 1: [0x2A, 0x20, 0xF9, 0x00, 0x00, 0x00, 0x00]
    # Block 2: [0xDF, 0x00, 0xE9, 0x07, 0x00, 0x00, 0x00]
    # Block 3: [0x80, 0x06, 0x88, 0xFB, 0xC7, 0x01, 0x46]
    
    expected_raw_timings = [
        # === PACKET 0 (Block 1) ===
        # Leader pulse
        3000, -3000,
        # Byte 0: 0x2A (LSB first: 0,1,0,1,0,1,0,0)
        600, -400, 600, -1400, 600, -400, 600, -1400, 600, -400, 600, -1400, 600, -400, 600, -400,
        # Byte 1: 0x20 (LSB first: 0,0,0,0,0,1,0,0)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -1400, 600, -400, 600, -400,
        # Byte 2: 0xF9 (LSB first: 1,0,0,1,1,1,1,1)
        600, -1400, 600, -400, 600, -400, 600, -1400, 600, -1400, 600, -1400, 600, -1400, 600, -1400,
        # Byte 3: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 4: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 5: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 6: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Inter-packet sync gap after Block 1
        600, -4000,

        # === PACKET 1 (Block 2) ===
        # Leader pulse
        3000, -3000,
        # Byte 7: 0xDF (LSB first: 1,1,1,1,1,0,1,1)
        600, -1400, 600, -1400, 600, -1400, 600, -1400, 600, -1400, 600, -400, 600, -1400, 600, -1400,
        # Byte 8: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 9: 0xE9 (LSB first: 1,0,0,1,0,1,1,1)
        600, -1400, 600, -400, 600, -400, 600, -1400, 600, -400, 600, -1400, 600, -1400, 600, -1400,
        # Byte 10: 0x07 (LSB first: 1,1,1,0,0,0,0,0)
        600, -1400, 600, -1400, 600, -1400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 11: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 12: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 13: 0x00 (all zeros)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Inter-packet sync gap after Block 2
        600, -4000,

        # === PACKET 2 (Block 3) ===
        # Leader pulse
        3000, -3000,
        # Byte 14: 0x80 (LSB first: 0,0,0,0,0,0,0,1)
        600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -1400,
        # Byte 15: 0x06 (LSB first: 0,1,1,0,0,0,0,0)
        600, -400, 600, -1400, 600, -1400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 16: 0x88 (LSB first: 0,0,0,1,0,0,0,1) -> Target Temp (24°C)
        600, -400, 600, -400, 600, -400, 600, -1400, 600, -400, 600, -400, 600, -400, 600, -1400,
        # Byte 17: 0xFB (LSB first: 1,1,0,1,1,1,1,1)
        600, -1400, 600, -1400, 600, -400, 600, -1400, 600, -1400, 600, -1400, 600, -1400, 600, -1400,
        # Byte 18: 0xC7 (LSB first: 1,1,1,0,0,0,1,1)
        600, -1400, 600, -1400, 600, -1400, 600, -400, 600, -400, 600, -400, 600, -1400, 600, -1400,
        # Byte 19: 0x01 (LSB first: 1,0,0,0,0,0,0,0) -> Checksum Part 1
        600, -1400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400, 600, -400,
        # Byte 20: 0x46 (LSB first: 0,1,1,0,0,0,1,0) -> Checksum Part 2
        600, -400, 600, -1400, 600, -1400, 600, -400, 600, -400, 600, -400, 600, -1400, 600, -400,
        # Final end pulse
        600,
    ]

    builder = SamsungACStateBuilder(
        hvac_mode="cool",
        target_temperature=24,
        fan_mode="auto",
    )
    command = builder.to_command()
    timings = command.get_raw_timings()

    assert timings == expected_raw_timings
    assert command.modulation == 38000