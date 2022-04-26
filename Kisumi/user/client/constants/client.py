from enums import IntEnum

class ClientType(IntEnum):
    """An enumeration for the available types of clients."""

    STABLE = 0 # Current releases of osu!
    LAZER = 1 # Reserved
    WEB = 2 # Websocket web client.
    IRC = 3
    API_BOT = 4
