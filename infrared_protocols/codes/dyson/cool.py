"""Command codes and state builders for Dyson Cool fans."""

from dataclasses import dataclass
from typing import Literal

from ...commands import Command
from ...commands.dyson import DysonCoolCommand


@dataclass(frozen=True)
class DysonCoolStateBuilder:
    """Logical state builder for Dyson Cool fan remotes mapping events to 16-bit payloads.
    
    Matches the physical remote layout: Power, Swing, Speed Up/Down, and Timer Up/Down.
    """

    action: Literal[
        "on", "cool_on", "off", 
        "swing", 
        "speed_up", "speed_down", 
        "time_up", "time_down"
    ]

    def to_command(self) -> Command:
        """Map the logical action to its corresponding verified 16-bit hex sequence."""
        action_mapping = {
            "on": 0x4800,        
            "cool_on": 0x4801,   
            "off": 0x4802,       
            "swing": 0x48A9,     
            "speed_up": 0x4854,   
            "speed_down": 0x48FD, 
            "time_up": 0x487A,   
            "time_down": 0x48CC, 
        }

        payload = action_mapping[self.action]
        return DysonCoolCommand(payload=payload)