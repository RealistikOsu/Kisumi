from enums import IntEnum

class AuthType(IntEnum):
    """Type of authenticated JWT used."""

    STABLE = 0
    LAZER = 1
    WEB = 2
    IRC = 3
