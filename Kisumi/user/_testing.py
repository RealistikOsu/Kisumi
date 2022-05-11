# TEMPORARY FILE
# Holds constants just for testing!!! I haven't hooked up a db yet.
from utils.hash import BCryptPassword
from user.user import User
from user.stats import Stats, ModeStats
from user.settings import Settings
from scores.constants.mode import CustomMode, Mode
from state.repos import user_manager
from utils.hash import hash_md5

async def configure_test_user() -> None:
    """Configures a user instance made for testing."""

    REALISTIK_USER = User(
        1000,
        "RealistikDash",
        "realistik@da.sh",
        None,
        [],
        None,
        BCryptPassword.from_str(hash_md5("bruhh")),
        None,
        [],
        Settings.new(),
    )

    REALISTIK_STATS = Stats(
        {(c_mode, mode): ModeStats(
            REALISTIK_USER,
            mode,
            c_mode,
            0, 0, 0.0, 0, 0, 0.0, 0, 0
        ) for c_mode in CustomMode for mode in Mode},
        REALISTIK_USER, 0, 0
    )

    REALISTIK_USER.stats = REALISTIK_STATS
    await user_manager._repo.insert(REALISTIK_USER)
