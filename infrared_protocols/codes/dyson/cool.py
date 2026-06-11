"""Command codes and state builders for Dyson Cool fans."""

from dataclasses import dataclass
from typing import Literal

from ...commands import Command
from ...commands.dyson import DysonCoolCommand


@dataclass(frozen=True)
class DysonCoolStateBuilder:
    """Logical state builder for Dyson Cool fan remotes mapping events to 15-bit payloads."""

    action: Literal[
        "on", "off", "swing", "time_up", "time_down",
        "speed_1", "speed_2", "speed_3", "speed_4", "speed_5",
        "speed_6", "speed_7", "speed_8", "speed_9", "speed_10"
    ]

    def to_command(self) -> Command:
        """Map the logical action to its corresponding verified 15-bit hex sequence."""
        action_mapping = {
            "on": 0x4801,        # 100100000000001
            "off": 0x4001,       # 100000000000001
            "swing": 0x4118,     # 100000100011000
            "time_up": 0x4072,   # 100000001110010
            "time_down": 0x4312, # 100001100010010
            "speed_1": 0x40ED,   # 100000001101101
            "speed_2": 0x4086,   # 100000001000110
            "speed_3": 0x40EC,   # 100000001101100
            "speed_4": 0x40A4,   # 100000001010100
            "speed_5": 0x40A0,   # 100000001010000
            "speed_6": 0x4087,   # 100000001000111
            "speed_7": 0x40A5,   # 100000001010101
            "speed_8": 0x40A0,   # 100000001010000
            "speed_9": 0x40A1,   # 100000001010001
            "speed_10": 0x40A0,  # 100000001010000
        }

        payload = action_mapping[self.action]
        return DysonCoolCommand(payload=payload)