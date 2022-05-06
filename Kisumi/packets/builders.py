# Builders for all currently implemented response packets.
from .writer import BinaryWriter
from .constants import (
    PacketIDs,
    LoginReply,
)
from typing import Union, TYPE_CHECKING
from functools import cache

if TYPE_CHECKING:
    from user.user import User
    from user.client.client import AbstractClient

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
                resp_val.value if isinstance(resp_val, LoginReply)
                else resp_val
            )
            .finish(PacketIDs.SRV_LOGIN_REPONSE)
    )

@cache
def channel_info_end() -> bytearray:
    """Builds a packet notifying the user that all channel info has been sent."""

    return (
        BinaryWriter()
            .finish(PacketIDs.SRV_CHANNEL_INFO_END)
    )

# TODO: Remove placeholder data
def presence(user: "User") -> bytearray:
    """Builds a presence for a user's main client."""

def presence_client(client: "AbstractClient") -> bytearray:
    """Builds a presence for a specific client."""

    return (
        BinaryWriter()
            .write_i32(client.user.id) # user ID
            .write_str(client.user.name) # username
            .write_u8(24) # Timezone offset + 24
            .write_u8(45) # Country Enum
            .write_u8(0b11111111) # Banchopriv
            .write_u8(0) # Lat
            .write_u8(0) # Long
            .write_i32(client.current_stats.rank) # Get current rank based on client
            .finish(PacketIDs.SRV_USER_PRESENCE)
    )
