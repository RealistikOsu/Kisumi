from typing import Union
import asyncio

ACCEPTED_TYPES = Union[bytes, bytearray]

class ByteBuffer:
    """A thread-safe implementation of a buffer of bytes."""

    __slots__ = (
        "_buf",
        "_lock",
    )

    def __init__(self, buf: bytearray) -> None:
        """Creates an instance of a `ByteBuffer` from an existing bytearray."""

        self._lock = asyncio.Lock()
        self._buf = bytearray()
    
    @staticmethod
    def new(self) -> "ByteBuffer":
        """Creates an empty instance of ByteBuffer."""

        return ByteBuffer(bytearray())

    @property
    def empty(self) -> bool:
        """Checks if the buffer is empty."""

        # should this be locked?
        return len(self._buf) == 0
    
    async def append(self, e: ACCEPTED_TYPES) -> None:
        """Appends `e` to the end of the buffer, acquiring the lock in the
        process."""

        async with self._lock:
            self._buf += e
    
    async def clear(self) -> bytearray:
        """Clears the contents of the `ByteBuffer`, returning its previous
        contents. Acquires the buffer lock."""

        async with self._lock:
            old = self._buf.copy()
            self._buf.clear()

        return old
