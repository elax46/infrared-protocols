"""Command codes and state builders for Samsung Air Conditioners."""

from dataclasses import dataclass
from typing import Literal

from ...commands import Command
from ...commands.samsung import SamsungACCommand as StructuralACCommand


@dataclass(frozen=True)
class SamsungACStateBuilder:
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

        return StructuralACCommand(payload=payload)