# Builders for all currently implemented response packets.
from .writer import BinaryWriter
from .constants import PacketIDs

def heartbeat() -> bytearray:
    """Writes a simple heartbeat acknowledge backet."""

    return (
        BinaryWriter()
            .finish(PacketIDs.SRV_HEARTBEAT)
    )
