from enums import IntEnum
from functools import cached_property

class Actions(IntEnum):
    """Enum representing the in-game client actions."""

    IDLE = 0
    AFK = 1
    PLAYING = 2
    EDITING = 3
    MODDING = 4
    MULTIPLAYER = 5
    WATCHING = 6
    UNKNOWN = 7
    TESTING = 8
    SUBMITTING = 9
    PAUSED = 10
    LOBBY = 11
    MULTIPLAYING = 12
    DIRECT = 13

    # Bot based ones.
    BOT_IDLE = 14
    BOT_WATCHING = 15
    BOT_TESTING = 16

    # Web based ones.
    WEB_IDLE = 17
    WEB_MAPS = 18
    WEB_PROFILE = 19
    
    @cached_property
    def is_game_client(self) -> bool:
        """Property corresponding to whether the action originates from an
        osu!stable game client."""

        return self.value <= 13
    
    @cached_property
    def is_bot_client(self) -> bool:
        """Property corresponding to whether the action originates from a custom
        bot client."""

        return 13 < self.value < 17
    
    @cached_property
    def is_web_client(self) -> bool:
        """Property corresponding to whether the action originates from a web browser based
        client."""

        return 16 < self.value < 20
    
    @cached_property
    def into_stable_enum(self) -> "Actions":
        """Converts the current action enum into one compatible with osu!stable's
        action system."""

        if self.is_game_client:
            return self
        
        return _ACTION_MAP[self]

_ACTION_MAP = {
    # Bot
    Actions.BOT_IDLE: Actions.IDLE,
    Actions.BOT_WATCHING: Actions.WATCHING,
    Actions.BOT_TESTING: Actions.TESTING,
    # Web
    Actions.WEB_IDLE: Actions.IDLE,
    Actions.WEB_MAPS: Actions.DIRECT,
    Actions.WEB_PROFILE: Actions.IDLE,
}
