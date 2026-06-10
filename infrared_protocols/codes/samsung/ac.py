"""Command codes and state builders for Samsung Air Conditioners."""

from dataclasses import dataclass
from typing import Literal

from ...commands import Command
from ...commands.samsung import SamsungACCommand as StructuralACCommand


@dataclass(frozen=True)
class SamsungACStateBuilder:
    """Builder for Samsung AC IR commands (21-byte extended protocol)."""

    hvac_mode: Literal["off", "cool", "heat", "dry", "fan_only"]
    target_temperature: int
    fan_mode: Literal["auto", "low", "medium", "high"]

    def to_command(self) -> Command:
        """Compile the logical state into a 21-byte payload and generate the IR Command."""
        # Initialize a 21-byte array
        payload = [0x00] * 21

        # Block 1: Header and address (Fixed for this specific AC unit)
        payload[0:7] = [0x2A, 0x20, 0xF9, 0x00, 0x00, 0x00, 0x00]

        # Block 2: Base configuration (Fixed for this specific AC unit)
        payload[7:14] = [0xDF, 0x00, 0xE9, 0x07, 0x00, 0x00, 0x00]

        # Block 3: Dynamic state (Base initialization for Cool mode, Auto fan)
        payload[14:21] = [0x80, 0x06, 0x00, 0xFB, 0xC7, 0x00, 0x00]

        # Temporary hardcoded mapping (Proof of Concept) for temperature.
        # Uses raw hexadecimal values and checksums extracted from the physical remote.
        if self.target_temperature == 24:
            payload[16] = 0x88
            payload[19] = 0x01
            payload[20] = 0x46
        elif self.target_temperature == 25:
            payload[16] = 0x48
            payload[19] = 0x01
            payload[20] = 0x46
        elif self.target_temperature == 26:
            payload[16] = 0x08
            payload[19] = 0x81
            payload[20] = 0x56
        else:
            # Safety fallback to 25°C if an unmapped temperature is requested
            payload[16] = 0x48
            payload[19] = 0x01
            payload[20] = 0x46

        return StructuralACCommand(payload=payload)