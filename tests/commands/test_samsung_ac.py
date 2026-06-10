"""Tests for the Samsung AC IR command encoder."""

from infrared_protocols.codes.samsung.ac import SamsungACStateBuilder


def test_samsung_ac_command_get_raw_timings() -> None:
    """Test Samsung AC command raw timings compilation for 21-byte protocol across states."""
    
    # Core test cases: (hvac_mode, temp, fan_mode, b16, b17, b19, b20)
    test_cases = [
        # Cool configurations
        ("cool", 16, "auto", 0x88, 0xFB, 0x01, 0x54),
        ("cool", 24, "auto", 0x88, 0xFB, 0x01, 0x46),
        ("cool", 24, "low", 0x48, 0xFB, 0x01, 0x56),
        ("cool", 24, "medium", 0x48, 0xFB, 0x01, 0x66),
        ("cool", 24, "high", 0x08, 0xFB, 0x01, 0x6E),
        ("cool", 25, "auto", 0x48, 0xFB, 0xC7, 0x46),
        ("cool", 26, "auto", 0x08, 0xFB, 0x81, 0x56),
        ("cool", 27, "auto", 0xC8, 0xFA, 0xC1, 0x56),
        ("cool", 30, "auto", 0xC8, 0xFA, 0x81, 0x57),
        
        # New mode configurations
        ("heat", 24, "auto", 0x88, 0xFB, 0x01, 0x06),
        ("dry", 24, "auto", 0x88, 0xFB, 0x01, 0x86),
        ("fan_only", 24, "auto", 0x08, 0xFB, 0x01, 0xD6),
    ]

    leader_high = 3000
    leader_low = 3000
    bit_high = 600
    zero_low = 400
    one_low = 1400
    gap_low = 4000

    # 1. Test ON states, modes, temperatures, and fans
    for mode, temp, fan, b16, b17, b19, b20 in test_cases:
        expected_payload = [0x00] * 21
        expected_payload[0:7] = [0x2A, 0x20, 0xF9, 0x00, 0x00, 0x00, 0x00]
        expected_payload[7:14] = [0xDF, 0x00, 0xE9, 0x07, 0x00, 0x00, 0x00]
        expected_payload[14:21] = [0x80, 0x06, b16, b17, 0xC7, b19, b20]

        expected_raw_timings = _compile_timings(expected_payload, leader_high, leader_low, bit_high, one_low, zero_low, gap_low)

        builder = SamsungACStateBuilder(hvac_mode=mode, target_temperature=temp, fan_mode=fan)
        command = builder.to_command()
        assert command.get_raw_timings() == expected_raw_timings, f"Failed ON timings check for {mode}, {temp}°C, fan {fan}"

    # 2. Test OFF state
    expected_off_payload = [0x00] * 21
    expected_off_payload[0:7] = [0x2A, 0x20, 0xFB, 0x00, 0x00, 0x00, 0x00]
    expected_off_payload[7:14] = [0xDC, 0x00, 0xE9, 0x07, 0x00, 0x00, 0x00]
    expected_off_payload[14:21] = [0x80, 0x06, 0x88, 0xFB, 0xC7, 0x01, 0x6E]
    
    expected_off_timings = _compile_timings(expected_off_payload, leader_high, leader_low, bit_high, one_low, zero_low, gap_low)
    
    builder_off = SamsungACStateBuilder(hvac_mode="off", target_temperature=24, fan_mode="auto")
    assert builder_off.to_command().get_raw_timings() == expected_off_timings


def _compile_timings(
    payload: list[int],
    leader_high: int,
    leader_low: int,
    bit_high: int,
    one_low: int,
    zero_low: int,
    gap_low: int,
) -> list[int]:
    """Helper to compile raw timings from a payload list."""
    timings = []
    for packet_idx in range(3):
        timings.append(leader_high)
        timings.append(-leader_low)
        start_byte = packet_idx * 7
        packet_bytes = payload[start_byte : start_byte + 7]
        for byte in packet_bytes:
            for _ in range(8):
                bit = byte & 1
                timings.append(bit_high)
                timings.append(-one_low if bit else -zero_low)
                byte >>= 1
        if packet_idx < 2:
            timings.append(bit_high)
            timings.append(-gap_low)
    timings.append(bit_high)
    return timings