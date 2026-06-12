"""Standalone verification: compare generated timings against real Broadlink-captured raw durations for all 8 Dyson commands.

Run: python3 test_dyson_fix.py
"""

import base64

UNIT = 32.84

CAPTURED = {
    "cool_on": "JgAkAEoaGjMaGhoZGzIaGRoZGhkaGxoZGxkaGhoZGhkaGRoyGgANBQAAAAA=",
    "off": "JgAkAEobGTMaGhoaGjIaGRoZGhkaGxoaGhoZGhoZGhoaMRsZGQANBQAAAAA=",
    "on": "JgAkAEsaGjIbGRsZGjIbGBsYGxgbGhoaGhoaGRsZGhkaGRoZGgANBQAAAAA=",
    "speed_up": "JgBIAEobGTMaGhkbGTMZGxkaGRoYHBk0GRsZMxkbGTMZGhkaGQAM0UobGTMaGhoaGTMaGRoZGhkaGxoyGxoZMxoaGTIbGRoZGQANBQ==",
    "speed_down": "JgBIAEobGTMaGhoaGjIaGRoZGhkaMxsyGzIbMhoyGzEbGRoxGwAM9ksaGjIbGhkaGjIaGhoZGhkZNBozGjIbMhsxGzIaGRoyGgANBQ==",
    "time_up": "JgBIAEsaGjIbGhkaGjIaGhoZGhkZGxozGjIbMhoyGxkaMhoZGgAMpEsaGjIbGhkaGjIaGhoZGhkZGxozGjIbMhsxGxkaMhoZGgANBQ==",
    "time_down": "JgBIAEobGTMaGhoaGTIbGRoZGhkaMxsyGxoZGhoyGjIbGRoZGQAMuUoaGjMaGRsZGjIbGBsYGxgbMxozGhoaGRozGjIaGRoZGgANBQ==",
    "swing": "JgBIAEoaGjMaGhoZGjMaGRoZGhkaMxsZGzIaGhoyGhkbGBsxGwAMvUoaGjMaGRoaGjIaGhoZGhgaNBoaGjMaGRozGhkaGRoyGgANBQ==",
}

ACTION_MAPPING = {
    "on": 0x4800,
    "cool_on": 0x4801,
    "off": 0x4802,
    "swing": 0x48A9,
    "speed_up": 0x4854,
    "speed_down": 0x48FD,
    "time_up": 0x487A,
    "time_down": 0x48CC,
}

REPEAT_MAPPING = {
    "on": 1, "cool_on": 1, "off": 1, "swing": 2,
    "speed_up": 2, "speed_down": 2, "time_up": 2, "time_down": 2,
}


def get_captured_durations(b64: str) -> list[int]:
    """Decode base64-encoded Broadlink IR data and extract duration timings.
    
    Args:
        b64: Base64-encoded IR data string.
        
    Returns:
        List of duration values in microseconds.
    """
    raw = base64.b64decode(b64)
    length = raw[2] | (raw[3] << 8)
    data = raw[4:4 + length]
    durations = []
    i = 0
    while i < len(data):
        v = data[i]
        if v == 0:
            ext = (data[i + 1] << 8) | data[i + 2]
            durations.append(round(ext * UNIT))
            i += 3
        else:
            durations.append(round(v * UNIT))
            i += 1
    # drop trailing zeros/footer gap marker (last >5000us = gap, not part of bit data)
    return durations


def generate_timings(payload: int, repeat_count: int) -> list[int]:
    """Generate Dyson IR packet timings for a given payload and repeat count.

    Args:
        payload: 15-bit command payload.
        repeat_count: Number of packets to generate, including repeats.

    Returns:
        A list of durations in microseconds representing the IR signal.
    """
    header_mark = 2440
    header_space = 870
    bit_mark = 850
    zero_space = 850
    one_space = 1660
    footer_mark = 850
    repeat_gap = 108000

    timings: list[int] = []
    for packet_idx in range(repeat_count):
        timings.append(header_mark)
        timings.append(header_space)
        for i in range(14, -1, -1):
            bit = (payload >> i) & 1
            timings.append(bit_mark)
            timings.append(one_space if bit else zero_space)
        timings.append(footer_mark)
        if packet_idx < repeat_count - 1:
            timings.append(repeat_gap)
    return timings


def bits_from_durations(durations: list[int]) -> str:
    """Extract the 15-bit payload from a captured duration list (first frame only)."""
    bits = ""
    j = 2
    while j + 1 < len(durations) and len(bits) < 15:
        s = durations[j + 1]
        if s > 5000:
            break
        bits += "1" if s > 1200 else "0"
        j += 2
    return bits


print(f"{'action':12s} {'captured 15-bit':17s} {'generated 15-bit':17s} match")
print("-" * 60)
all_ok = True
for action, b64 in CAPTURED.items():
    captured = get_captured_durations(b64)
    captured_bits = bits_from_durations(captured)

    payload = ACTION_MAPPING[action]
    generated_bits = format(payload, "015b")

    ok = captured_bits == generated_bits
    all_ok &= ok
    status = "OK" if ok else "MISMATCH"
    print(f"{action:12s} {captured_bits:17s} {generated_bits:17s} {status}")

print("-" * 60)
print("ALL PAYLOADS MATCH" if all_ok else "SOME PAYLOADS MISMATCH")