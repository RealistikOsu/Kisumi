# Builders for all currently implemented response packets.
from .writer import BinaryWriter
from .constants import (
    PacketIDs,
    LoginReply,
)
from typing import Union
from functools import cache

@cache
def heartbeat() -> bytearray:
    """Writes a simple heartbeat acknowledge backet."""

    return (
        BinaryWriter()
            .finish(PacketIDs.SRV_HEARTBEAT)
    )

def notification(content: str) -> bytearray:
    """Writes a notification packet buffer and returns it."""

    return (
        BinaryWriter()
            .write_str(content)
            .finish(PacketIDs.SRV_NOTIFICATION)
    )

def login_reply(resp_val: Union[int, LoginReply]) -> bytearray:
    """Builds a login response packet buffer and returns it."""

    return (
        BinaryWriter()
            .write_i32(
                resp_val.value if isinstance(resp_val, LoginReply) else resp_val
            )
            .finish(PacketIDs.SRV_LOGIN_REPONSE)
    )


