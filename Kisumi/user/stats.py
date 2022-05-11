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

    # XXX: COmmit note: Gonna be using models
    def into_mongo(self) -> dict[str, Any]:
        """Converts the ModeStats object into a MongoDB compatible dict."""

        # TODO: Automate this.
        return {
            "mode": self.mode.value,
            "c_mode": self.c_mode.value,
            "total_score": self.total_score,
            "ranked_score": self.ranked_score,
            "pp": self.pp,
            "play_count": self.play_count,
            "accuracy": self.accuracy,
            "max_combo": self.max_combo,
            # Rank is redis.
        }
    
    @staticmethod
    def from_mongo(self, user: "User", m_res: dict[str. Any]) -> "ModeStats":
        """Creates an instance of `ModeStats` from MongoDB data."""

        # Enum casts
        m_res["mode"] = Mode(m_res["mode"])
        m_res["c_mode"] = CustomMode(m_res["mode"])
        return ModeStats(
            **m_res,
            rank= 0,
        )

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

    def from_modes(self, c_mode: CustomMode, mode: Mode) -> ModeStats:
        """Returns a user's stats for the corresponding c_mode + mode combo.
        
        Note:
            Invalid values will result in a `KeyError` being raised.
        """

        return self._stats[(c_mode, mode)]
    
    def insert_stats(self, stats: ModeStats) -> None:
        """Inserts an instance of `ModeStats` into the `Stats` object."""

        self._stats[(stats.c_mode, stats.mode)] = stats
