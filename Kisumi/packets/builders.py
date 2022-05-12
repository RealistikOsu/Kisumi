# Builders for all currently implemented response packets.
from .writer import BinaryWriter
from .constants import (
    PacketID,
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
            .finish(PacketID.SRV_HEARTBEAT)
    )

def notification(content: str) -> bytearray:
    """Writes a notification packet buffer and returns it."""

    return (
        BinaryWriter()
            .write_str(content)
            .finish(PacketID.SRV_NOTIFICATION)
    )

def login_reply(resp_val: Union[int, LoginReply]) -> bytearray:
    """Builds a login response packet buffer and returns it."""

    return (
        BinaryWriter()
            .write_i32(
                resp_val.value if isinstance(resp_val, LoginReply)
                else resp_val
            )
            .finish(PacketID.SRV_LOGIN_REPONSE)
    )

@cache
def channel_info_end() -> bytearray:
    """Builds a packet notifying the user that all channel info has been sent."""

    return (
        BinaryWriter()
            .finish(PacketID.SRV_CHANNEL_INFO_END)
    )

# TODO: Remove placeholder data
def presence(user: "User") -> bytearray:
    """Builds a presence for a user's main client."""

    return presence_client(user.client)

def presence_client(client: "AbstractClient") -> bytearray:
    """Builds a presence for a specific client."""

    return (
        BinaryWriter()
            .write_i32(client.user.id) # user ID
            .write_str(client.user.name) # username
            .write_u8(client.location.utc_offset + 24) # Timezone offset + 24
            .write_u8(client.location.country_into_enum()) # Country Enum
            .write_u8(0b11111111) # TODO: Banchopriv
            .write_u8(int(client.location.location.x)) # Lat
            .write_u8(int(client.location.location.y)) # Long
            .write_i32(client.current_stats.rank) # Get current rank based on client
            .finish(PacketID.SRV_USER_PRESENCE)
    )

def stats(user: "User") -> bytearray:
    """Builds a stats packet for the user's main client."""

    return stats_client(user.client)

def stats_client(client: "AbstractClient") -> bytearray:
    """Builds a stats packet for a specific client."""

    return (
        BinaryWriter()
            .write_i32(client.user.id)
            .write_u8(client.action.id.into_stable_enum)
            .write_str(client.action.stable_text)
            .write_str("") # TODO: client.action.bmap.md5
            .write_i32(0) # TODO: client.action.mods
            .write_u8(client.action.mode.value)
            .write_i32(0) # TODO: client.action.bmap.id
            .write_i64(client.current_stats.ranked_score)
            .write_f32(client.current_stats.accuracy / 100)
            .write_i32(client.current_stats.play_count)
            .write_i64(client.current_stats.total_score)
            .write_i32(client.current_stats.rank)
            .write_i16(int(client.current_stats.pp))
            .finish(PacketID.SRV_USER_STATS)
    )

@cache
def protocol_ver(ver: int = 19) -> bytearray:
    """Builds a packet telling the client of the protocol version.
    
    Note:
        All modern builds (as of 12/5/22) use 19 as the version.
    """

    return (
        BinaryWriter()
            .write_i32(ver)
            .finish(PacketID.SRV_PROTOCOL_VERSION)
    )
