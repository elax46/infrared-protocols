"""Dyson cool mode command mapping.

Provides a small builder to convert high-level actions into
DysonCoolCommand instances containing the appropriate payload.
"""

from dataclasses import dataclass
from typing import Literal

from ...commands import Command
from ...commands.dyson import DysonCoolCommand

@dataclass(frozen=True)
class DysonCoolStateBuilder:
    action: Literal[
        "on", "cool_on", "off", 
        "swing", 
        "speed_up", "speed_down", 
        "time_up", "time_down"
    ]

    def to_command(self) -> Command:
        """Convert the builder state into a DysonCoolCommand.

        Returns:
            Command: A DysonCoolCommand instance containing the payload
            corresponding to the builder's action.
        """

        action_mapping = {
            "on": 0x481A1B,        
            "cool_on": 0x481A13,   
            "off": 0x481A32,       
            "swing": 0x481A69,     
            "speed_up": 0x481A54,   
            "speed_down": 0x481AFD, 
            "time_up": 0x481A5E,   
            "time_down": 0x481A3D, 
        }

        payload = action_mapping[self.action]
        return DysonCoolCommand(payload=payload)