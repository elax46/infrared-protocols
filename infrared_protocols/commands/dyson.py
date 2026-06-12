from typing import override
from . import Command

class DysonCoolCommand(Command):
    """Dyson Cool infrared command."""
    payload: int

    def __init__(
        self,
        *,
        payload: int,
        modulation: int = 38000,
        repeat_count: int = 1,
    ) -> None:
        """Initialize a Dyson Cool infrared command.
        
        Args:
            payload: The 24-bit payload data.
            modulation: The modulation frequency in Hz (default: 38000).
            repeat_count: The number of times to repeat the command (default: 1).
            
        Raises:
            ValueError: If payload is not a valid 24-bit integer.
        """
        super().__init__(modulation=modulation, repeat_count=repeat_count)
        if payload < 0 or payload > 0xFFFFFF:
            raise ValueError("Dyson payload must be a valid 24-bit integer")
        self.payload = payload

    @override
    def get_raw_timings(self) -> list[int]:
        leader_high = 8940
        leader_low = 4440
        bit_high = 590
        zero_low = 520
        one_low = 1630
        gap_low = 4000

        timings: list[int] = []
        
        for packet_idx in range(self.repeat_count + 1):
            timings.append(leader_high)
            timings.append(leader_low)
            
            data = self.payload
            for i in range(24):
                bit = (data >> i) & 1
                timings.append(bit_high)
                timings.append(one_low if bit else zero_low)
                    
            timings.append(bit_high)
            
            if packet_idx < self.repeat_count:
                timings.append(gap_low)
            
        return timings