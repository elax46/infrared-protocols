"""Command codes and state builders for Samsung Air Conditioners."""

from dataclasses import dataclass
from typing import Literal

from ...commands import Command


@dataclass(frozen=True)
class SamsungACProtocolCommand(Command):
    """Concrete implementation of the Samsung AC IR Command."""

    modulation: int
    timings: list[int]

    def get_raw_timings(self) -> list[int]:
        """Return the calculated raw IR timings with negative space markers."""
        return self.timings


@dataclass(frozen=True)
class SamsungACCommand:
    """Builder for Samsung AC IR commands (14-byte extended protocol)."""

    hvac_mode: Literal["off", "cool", "heat", "dry", "fan_only"]
    target_temperature: int
    fan_mode: Literal["auto", "low", "medium", "high"]

    def to_command(self) -> Command:
        """Compile the logical state into a 14-byte payload and generate the IR Command."""
        payload = [0x00] * 14

        # Fixed header bytes for Samsung AC protocol
        payload[0] = 0x02
        payload[1] = 0x92

        # Temperature encoding (standard range 16-30°C mapped as temp - 16)
        target_temp = max(16, min(30, self.target_temperature))
        payload[5] = (target_temp - 16) << 4

        # HVAC Mode encoding
        if self.hvac_mode == "off":
            payload[6] = 0x00
        elif self.hvac_mode == "cool":
            payload[6] = 0x01
        elif self.hvac_mode == "heat":
            payload[6] = 0x02
        else:
            payload[6] = 0x03  # Default to Dry / Fan Only

        # Fan Speed encoding
        if self.fan_mode == "high":
            payload[7] = 0xA0
        elif self.fan_mode == "medium":
            payload[7] = 0x80
        else:
            payload[7] = 0x40  # Auto / Low

        # Checksum calculation (XOR of significant data bytes)
        checksum = 0
        for byte in payload[2:13]:
            checksum ^= byte
        payload[13] = checksum

        # Generate physical raw timings (standard 38kHz carrier frequency)
        raw_timings: list[int] = []

        # Leader Pulse: 3000µs Mark, -3000µs Space (aligned to library style)
        raw_timings.extend([3000, -3000])

        # Bit blast (LSB first for each byte)
        for byte in payload:
            for i in range(8):
                bit = (byte >> i) & 1
                if bit == 1:
                    # Bit 1: 600µs Mark, -1400µs Space
                    raw_timings.extend([600, -1400])
                else:
                    # Bit 0: 600µs Mark, -400µs Space
                    raw_timings.extend([600, -400])

        # Final Stop Bit (only a pulse, no ending gap required for single frames)
        raw_timings.extend([600])

        return SamsungACProtocolCommand(modulation=38000, timings=raw_timings)