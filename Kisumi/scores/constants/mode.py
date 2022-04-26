from enum import IntEnum
from enums import IntEnum
from functools import cached_property

class CustomMode(IntEnum):
    """Enums representing the server-side implemented modes."""

    VANILLA = 0
    RELAX = 1
    AUTOPILOT = 2

    @cached_property
    def into_prefix(self) -> str:
        """Converts the custom mode into its 2 letter prefix."""

        return _C_MODE_CODE[self.value]
    
    @cached_property
    def name(self) -> str:
        """Returns CustomMode name as a string."""

        return _C_MODE_CODE[self.value].lower()

_C_MODE_CODE = (
    "VN",
    "RX",
    "AP",
)

class Mode(IntEnum):
    """Enums representing the in-game modes."""

    STANDARD = 0
    TAIKO = 1
    CATCH = 2
    MANIA = 3

    @cached_property
    def name(self) -> str:
        """Returns the common name of the mode as a string."""

        return _MODE_NAMES[self.value]

_MODE_NAMES = (
    "standard",
    "taiko",
    "catch",
    "mania",
)
