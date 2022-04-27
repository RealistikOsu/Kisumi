from dataclasses import dataclass
from inspect import get_annotations
from typing import (
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

@dataclass
class PacketHandler:
    """A class representing a handler function for a specific packet id."""

    id: ... # Packet ID enum
    # TODO: Make a coroutine function alias.
    handler: Callable[[User, Type[Union[int, str, float]], Awaitable[Optional[Union[bytearray, bytes]]]]]
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

                    ...
