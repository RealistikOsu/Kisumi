from dataclasses import dataclass
from inspect import get_annotations
from typing import (
    Any,
    Awaitable,
    Optional,
    Union,
    Callable,
    Type,
    GenericAlias,
    get_type_hints,
)
from .types import *
from .reader import BinaryReader
from user.user import User
from user.client.components.queue import ByteLike
from .constants import PacketID

# TODO: Make a coroutine function alias.
PACKET_CORO_FUNC = Callable[[User, Type[Union[int, str, float]], Awaitable[Optional[ByteLike]]]]
@dataclass
class PacketHandler:
    """A class representing a handler function for a specific packet id."""

    id: PacketID
    handler: PACKET_CORO_FUNC
    req_priv: ... # Privilege enum type.

    def read_from_annotations(
        self, reader: BinaryReader
    ) -> tuple[SERIALISABLE_TYPES_ANNOTATION, ...]:
        """Prepares the function arguments (without the user object) for the
        handler"""

        args = []

        arg_iter = iter(get_annotations(self.handler))
        # Skip first item as it will always be the user.
        next(arg_iter)

        for arg_type in arg_iter:
            # Some handlers directly take the reader in.
            if arg_type is BinaryReader:
                args.append(reader)
            # Array alias
            # TODO: Probably move this into the reader itself.
            elif type(arg_type) is GenericAlias:
                # List len
                arr_len = reader.read_u16()
                args.append(
                    [reader.read_i32() for _ in range(arr_len)] # TODO: Replace with type.
                )
            else:
                assert arg_type in SERIALISABLE_TYPES, \
                    f"Attempted to serialise unserialisable type {arg_type}"

                args.append(reader.read_type(arg_type))

        return args
    
    def meets_privileges(self, user: User) -> bool:
        """Checks if the user provided meeths the packet execution privileges."""

        return True

    async def call(self, user: User, reader: BinaryReader) -> Optional[ByteLike]:
        """Calls the main handler for the packet, reading the packet based
        on the annotations.
        
        Note:
            Does no validation itself. All on you buddy.
        """

        args = self.read_from_annotations(reader)

        return await self.handler(user, *args)

class PacketRouter:
    """A router for identifying packet ids to their respective handlers."""

    __slots__ = (
        "_repo",
    )

    def __init__(self) -> None:
        self._repo: dict[PacketID, PacketHandler] = {}

    def register_packet(self, p_id: PacketID, p_handle: PACKET_CORO_FUNC,
                        privilege: Optional[Any] = None) -> None:
        """Registers a packet handler for a packet of id `p_id`."""

        self._repo[p_id] = PacketHandler(
            id= p_id,
            handler= p_handle,
            privilege= privilege,
        )
    
    def register(self, p_id: PacketID, p_handle: PACKET_CORO_FUNC,
                        privilege: Optional[Any] = None) -> PACKET_CORO_FUNC:
        """Decorator equivalent of `register_packet`."""

        def wrapper(coro: PACKET_CORO_FUNC) -> PACKET_CORO_FUNC:
            self.register_packet(p_id, p_handle, privilege)
            return coro
        
        return wrapper
    
    def fetch_handler(self, p_id: PacketID) -> Optional[PacketHandler]:
        """Fetches a registered handler for a packet with id `p_id`. If
        not registered, returns `None`."""

        return self._repo.get(p_id)
