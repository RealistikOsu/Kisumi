from enum import IntEnum
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
