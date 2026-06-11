"""Dyson infrared protocol structural command."""

from typing import override

from . import Command


class DysonCoolCommand(Command):
    """Dyson Cool IR command encoder supporting the 15-bit protocol.

    Timings layout (in microseconds):
    - Leader pulse: 1480µs high, 520µs low
    - Logical '0': 520µs high, 500µs low
    - Logical '1': 520µs high, 1020µs low
    - End pulse: 520µs high
    - Inter-packet gap: 4000µs low
    """

    payload: int

    def __init__(
        self,
        *,
        payload: int,
        modulation: int = 38000,
        repeat_count: int = 1,
    ) -> None:
        """Initialize the Dyson Cool structural command."""
        super().__init__(modulation=modulation, repeat_count=repeat_count)
        if payload < 0 or payload > 0x7FFF:
            raise ValueError("Dyson payload must be a valid 15-bit integer")
        self.payload = payload

    @override
    def get_raw_timings(self) -> list[int]:
        """Compile the 15-bit payload into raw IR microsecond timings."""
        leader_high = 1480
        leader_low = 520
        bit_high = 520
        zero_low = 500
        one_low = 1020
        gap_low = 4000

        timings: list[int] = []
        
        # Transmit back-to-back bursts based on the requested repeat count
        for packet_idx in range(self.repeat_count + 1):
            # Leader pulse
            timings.append(leader_high)
            timings.append(-leader_low)
            
            # Serialize 15 bits (MSB first for standard Dyson structural frames)
            data = self.payload
            for i in range(14, -1, -1):
                bit = (data >> i) & 1
                timings.append(bit_high)
                timings.append(-one_low if bit else -zero_low)
                    
            # Stop bit marker / inter-packet gap
            timings.append(bit_high)
            if packet_idx < self.repeat_count:
                timings.append(-gap_low)
            
        return timings