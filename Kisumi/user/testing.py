# TEMPORARY FILE
# Holds constants just for testing!!! I haven't hooked up a db yet.
from utils.hash import BCryptPassword
from user.user import User
from user.stats import Stats, ModeStats
from scores.constants.mode import CustomMode, Mode

REALISTIK_USER = User(
    1000,
    None,
    [],
    BCryptPassword.from_str("bruhh"),
)

REALISTIK_STATS = Stats(
    {(c_mode, mode): ModeStats(
        REALISTIK_USER,
        mode,
        c_mode,
        0, 0, 0.0, 0, 0, 0.0, 0, 0
    ) for c_mode in CustomMode for mode in Mode}
)
