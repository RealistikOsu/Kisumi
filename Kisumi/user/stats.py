from dataclasses import dataclass
from typing import TYPE_CHECKING, Any
from scores.constants.mode import (
    CustomMode,
    Mode,
)

if TYPE_CHECKING:
    from .user import User

@dataclass
class ModeStats:
    """An object representing the stats for a particular mode + c_mode
    combo."""

    _user: "User"

    mode: Mode
    c_mode: CustomMode

    # Actual Stats.
    total_score: int
    ranked_score: int
    pp: float
    play_count: int
    play_time: int
    accuracy: float
    max_combo: int
    rank: int

@dataclass
class Stats:
    """Object responsible for storing a user's stats for all modes, alongside
    non-mode specific ones."""

    _stats: dict[tuple[CustomMode, Mode], ModeStats]
    _user: "User"

    # Non-mode specific stats
    replay_views: int
    login_streak: int

    @property
    def preferred(self) -> ModeStats:
        """Return's the user's stats for their preferred modes."""

        return self.from_modes(
            self._user.settings.preferred_c_mode,
            self._user.settings.preferred_mode,
        )
    
    @property
    def current(self) -> "ModeStats":
        """Returns the user's current ModeStats based on their presence.
        If not online, returns preferred stats."""

        if self._user.client:
            return self.from_modes(
                self._user.client.action.c_mode,
                self._user.client.action.mode,
            )
        return self.preferred

    def from_modes(self, c_mode: CustomMode, mode: Mode) -> ModeStats:
        """Returns a user's stats for the corresponding c_mode + mode combo.
        
        Note:
            Invalid values will result in a `KeyError` being raised.
        """

        return self._stats[(c_mode, mode)]
    
    def insert_stats(self, stats: ModeStats) -> None:
        """Inserts an instance of `ModeStats` into the `Stats` object."""

        self._stats[(stats.c_mode, stats.mode)] = stats
