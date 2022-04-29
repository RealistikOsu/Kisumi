from enums import IntEnum, StrEnum, auto

class Language(IntEnum):
    """Enumeration of the available langauges messages can be written in."""

    ENGLISH_UK = 0
    ENGLISH_US = 1

class LocalisedMessage(StrEnum):
    """String enumerations for the localised string identifier."""

    WELCOME_TEXT_1 = auto()
    ...
