# An implementation of a binary serialiser specifically tailored to be utilised
# with osu's binary formats.
from typing import (
    Union,
    TypeVar,
    Callable,
    Type,
)
from functools import cache
from .constants import HEADER_LEN
from .types import *
import struct

T = TypeVar("T", *SERIALISABLE_TYPES)
__all__ = (
    "BinaryWriter",
)

class BinaryWriter:
    """A binary serialiser managing the contents of a bytearray. It by itself
    is not thread-safe."""

    __slots__ = ("_buffer",)

    def __init__(self, pralloc_header: bool = True) -> None:
        # Pre-allocate the header.
        self._buffer = bytearray(b"\x00" * HEADER_LEN) \
            if pralloc_header else bytearray()
    
    # Using the struct module to write primitive types into the buffer.
    # https://docs.python.org/3/library/struct.html#format-characters
    # osu! uses little endian values.
    def write_i8(self, num: i8) -> "BinaryWriter":
        """Writes a signed 8-bit integer to the buffer."""

        self._buffer += struct.pack("<b", num)
        return self

    def write_u8(self, num: u8) -> "BinaryWriter":
        """Writes an 8-bit unsigned integer into the buffer."""

        self._buffer.append(num)
        return self
    
    def write_i16(self, num: i16) -> "BinaryWriter":
        """Writes a signed 16-bit integer to the buffer."""

        self._buffer += struct.pack("<h", num)
        return self

    def write_u16(self, num: u16) -> "BinaryWriter":
        """Writes an 16-bit unsigned integer into the buffer."""

        self._buffer += struct.pack("<H", num)
        return self

    def write_i32(self, num: i32) -> "BinaryWriter":
        """Writes a signed 32-bit integer to the buffer."""

        self._buffer += struct.pack("<i", num)
        return self

    def write_u32(self, num: u32) -> "BinaryWriter":
        """Writes an 8-bit unsigned integer into the buffer."""

        self._buffer += struct.pack("<I", num)
        return self

    def write_i64(self, num: i64) -> "BinaryWriter":
        """Writes a signed 64-bit integer to the buffer."""

        self._buffer += struct.pack("<l", num)
        return self

    def write_u64(self, num: u64) -> "BinaryWriter":
        """Writes an 8-bit unsigned integer into the buffer."""

        self._buffer += struct.pack("<L", num)
        return self
    
    def write_f32(self, num: float) -> "BinaryWriter":
        """Writes a 32-bit floating point integer into the buffer."""

        self._buffer += struct.pack("<f", num)
        return self
    
    # Relatively more osu!-standardised types.
    def write_uleb128(self, num: u32) -> "BinaryWriter":
        """Writes an unsigned LEB128 variable length integer into the buffer."""

        if num == 0:
            return self.write_u8(0)
        
        while num != 0:
            self.write_u8(num & 127)
            num >>= 7
            if num != 0:
                self._buffer[-1] |= 128
        
        return self
    
    def write_str(self, string: str) -> "BinaryWriter":
        """Writes an osu-styled binary string into the buffer.
        The osu-styled string consists of an 'existis byte', followed by an
        uleb128 of its length and the UTF-8 string bytes.
        """

        if string:
            (
                self.write_u8(11)
                    .write_uleb128(len(string))
                    .write_raw(string.encode())
            )
        
        else:
            self.write_u8(0)
        
        return self
    
    def write_list(self, l: list[T], typ: Type[T]) -> "BinaryWriter":
        """Writes a list of the given type `typ` into the buffer prefixed by
        its length as u16."""

        self.write_u16(len(l))
        writer = _writer_from_type(typ)

        for elem in l:
            writer(self, elem)
        
        return self

    def write_osu_list(self, l: list[i32]) -> "BinaryWriter":
        """Writes a u16 prefixed list of i32s into the buffer."""

        return self.write_list(l, i32)
    
    def write_raw(self, contents: Union[bytes, bytearray]) -> "BinaryWriter":
        """Appends raw binary bytes onto the buffer."""

        self._buffer += contents
        return self
    
    def finish(self, packet_id: u16) -> bytearray:
        """Completes packet serialisation by writing the packet header to the front."""

        # FIXME: Bruh.
        self._buffer[0:1] = struct.pack("<H", packet_id)
        self._buffer[3:6] = struct.pack("<I", len(self._buffer) - HEADER_LEN)
        return self._buffer


_READERS = {
    u8: BinaryWriter.write_u8,
    i8: BinaryWriter.write_i8,
    u16: BinaryWriter.write_u16,
    i16: BinaryWriter.write_i16,
    u32: BinaryWriter.write_u32,
    i32: BinaryWriter.write_i32,
    u64: BinaryWriter.write_u64,
    i64: BinaryWriter.write_i64,
    str: BinaryWriter.write_str,
    float: BinaryWriter.write_f32,
}

@cache
def _writer_from_type(typ: Type[T]) -> Callable[[BinaryWriter, T], BinaryWriter]:
    """Fetches the binary writer function corresponding to the type trying
    to be read.
    
    Note:
        Raises an assertion error if the type is not serialisable.
    """

    assert typ in _READERS

    return _READERS[typ]
