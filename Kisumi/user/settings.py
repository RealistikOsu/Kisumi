from dataclasses import dataclass
from scores.constants.mode import (
    CustomMode,
    Mode,
)

@dataclass
class Settings:
    """Class representing user settings."""

    # User settings.
    preferred_mode: Mode
    preferred_c_mode: CustomMode
    language: ...
    overwrite_rules: ...
