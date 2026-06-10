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

        # Check if the requested mode is OFF
        if self.hvac_mode == "off":
            payload[0:7] = [0x2A, 0x20, 0xFB, 0x00, 0x00, 0x00, 0x00]
            payload[7:14] = [0xDC, 0x00, 0xE9, 0x07, 0x00, 0x00, 0x00]
            payload[14:21] = [0x80, 0x06, 0x88, 0xFB, 0xC7, 0x01, 0x6E]
            return StructuralACCommand(payload=payload)

        # === ON STATE ===
        payload[0:7] = [0x2A, 0x20, 0xF9, 0x00, 0x00, 0x00, 0x00]
        payload[7:14] = [0xDF, 0x00, 0xE9, 0x07, 0x00, 0x00, 0x00]
        payload[14:21] = [0x80, 0x06, 0x00, 0x00, 0xC7, 0x00, 0x00]

        mode = self.hvac_mode
        temp = max(16, min(30, self.target_temperature))
        fan = self.fan_mode

        # Core state matrix: (hvac_mode, temp, fan_mode) -> (Byte 16, Byte 17, Byte 19, Byte 20)
        state_mapping: dict[tuple[str, int, str], tuple[int, int, int, int]] = {
            # === COOL MODE ===
            ("cool", 16, "auto"): (0x88, 0xFB, 0x01, 0x54),
            ("cool", 23, "auto"): (0xC8, 0xFA, 0xC1, 0x55),
            ("cool", 24, "auto"): (0x88, 0xFB, 0x01, 0x46),
            ("cool", 24, "low"): (0x48, 0xFB, 0x01, 0x56),
            ("cool", 24, "medium"): (0x48, 0xFB, 0x01, 0x66),
            ("cool", 24, "high"): (0x08, 0xFB, 0x01, 0x6E),
            ("cool", 25, "auto"): (0x48, 0xFB, 0xC7, 0x46),
            ("cool", 26, "auto"): (0x08, 0xFB, 0x81, 0x56),
            ("cool", 27, "auto"): (0xC8, 0xFA, 0xC1, 0x56),
            ("cool", 30, "auto"): (0xC8, 0xFA, 0x81, 0x57),

            # === HEAT MODE ===
            ("heat", 24, "auto"): (0x88, 0xFB, 0x01, 0x06),

            # === DRY MODE ===
            ("dry", 24, "auto"): (0x88, 0xFB, 0x01, 0x86),

            # === FAN ONLY MODE ===
            ("fan_only", 24, "auto"): (0x08, 0xFB, 0x01, 0xD6),
        }

        # Lookup with safe fallback cascading down to ("cool", temp, "auto") if exact combo isn't mapped
        lookup_key = (mode, temp, fan)
        if lookup_key not in state_mapping:
            lookup_key = (mode, temp, "auto")
        if lookup_key not in state_mapping:
            lookup_key = ("cool", temp, "auto")

        b16, b17, b19, b20 = state_mapping[lookup_key]

        payload[16] = b16
        payload[17] = b17
        payload[19] = b19
        payload[20] = b20

        return StructuralACCommand(payload=payload)