# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class TwitchChannel:
    name:str

    def __post_init__(self):
        # remove any "#" if they exist, so that all the __str__ casting happens the same way
        self.name = self.name.replace("#", "")

    def __str__(self) -> str:
        return f"#{self.name}"
