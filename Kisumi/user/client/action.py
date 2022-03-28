from dataclasses import dataclass
from .constants.actions import Actions
from scores.constants.mode import (
    Mode,
    CustomMode,
)
from typing import (
    Optional,
    Any,
)

@dataclass
class Action:
    """An object symbolising the user's current action."""

    id: Actions
    _text: str
    bmap: Optional[Any] # TODO: Wait for impl beatmap obj
    mode: Mode
    c_mode: CustomMode
    mods: ...

    @property
    def stable_text(self) -> str:
        """Returns the text to be used as a description of the user's status
        inside the stable client."""

        prefix = ""

        if self.id.is_game_client:
            prefix = self.c_mode.into_prefix
        elif self.id.is_bot_client:
            prefix = "BOT"
        elif self.id.is_web_client:
            prefix = "Web"
        
        return f"[{prefix}] {self._text}"
