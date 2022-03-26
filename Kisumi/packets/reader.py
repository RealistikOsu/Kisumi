# An implementation of a binary deserialiser for usage with 
from .constants import HEADER_LEN
from .types import *
from typing import Union
import struct

class BinaryReader:
    """A binary-deserialisation class managing a buffer of bytes. Tailored for
    usage within osu's binary formats, such as Bancho packets and replays."""

    __slots__ = (
        "_buffer",
        "_offset",
    )

    def __init__(self, buffer: Union[bytearray, bytes]) -> None:
        """Creates an instance of `BinaryReader` from an existing array of bytes."""

        self._buffer = buffer
        self._offset = 0
    
    def read_bytes(self, amount: int) -> Union[bytearray, bytes]:
        """Reads `amount` bytes from the current offset and increments the
        offset of the reader by `amount`. Returns the buffer slice."""

        buf_slice = self._buffer[self._offset:self.__incr_offset(amount)]
        self._offset += amount
        return buf_slice
    
    def __incr_offset(self, amount: int) -> int:
        """Increments the reader offset by `amount`, returning its new value."""

        self._offset += amount
        return self._offset
    
    # Primitive type readers.
    def read_u8(self) -> u8:
        """Reads an unsigned 8-bit integer from the buffer."""

        # Since the bytearray itself stores 8-bit integers, there is no
        # further processing necessary. This can however fail if there
        # is no more data to be read, however that means something already
        # is very messed up.
        return self.read_bytes(1)[0]
    
    def read_i8(self) -> i8:
        """Reads a signed 8-bit integer from the buffer."""

        return struct.unpack("<b", self.read_bytes(1))[0]
    
    def read_u16(self) -> u16:
        """Reads an unsigned 16-bit integer from the buffer."""

        return struct.unpack("<H", self.read_bytes(2))[0]
    
    def read_i16(self) -> i16:
        """Reads a signed 16-bit integer from the buffer."""

        return struct.unpack("<h", self.read_bytes(2))[0]
    
    def read_u32(self) -> u32:
        """Reads an unsigned 32-bit integer from the buffer."""

        return struct.unpack("<I", self.read_bytes(4))[0]
    
    def read_i32(self) -> i32:
        """Reads a signed 32-bit integer from the buffer."""

        return struct.unpack("<i", self.read_bytes(4))[0]
    
    def read_u64(self) -> u64:
        """Reads an unsigned 64-bit integer from the buffer."""

        return struct.unpack("<Q", self.read_bytes(8))[0]
    
    def read_i64(self) -> i64:
        """Reads a signed 64-bit integer from the buffer."""

        return struct.unpack("<q", self.read_bytes(8))[0]
    
    def read_f32(self) -> float:
        """Reads a 32-bit floating point integer from the buffer."""

        return struct.unpack("<f", self.read_bytes(4))[0]

    # osu! specific types
    def read_osu_header(self) -> tuple[u16, u32]:
        """Reads an osu packet header, returning its packet id and length.
        
        Note:
            Raises `AssertionError` if the `offset + 3` byte (pad byte) does
            not equal to 0. This is because that means the reader has encountered
            a misread.
        """

        packet_id = self.read_u16()
        assert self.read_bytes(1)[0] == 0, "Missing padding byte! Misread occured."
        packet_length = self.read_u32()
        return packet_id, packet_length
    
    def read_uleb128(self) -> int:
        """Reads an unsigned 128-bit LEB variable length integer from the buffer."""

        if self.read_bytes(1)[0] != 0x0B:
            return ""

        val = shift = 0
        while True:
            b = self.read_bytes(1)[0]
            val |= (b & 0b01111111) << shift
            if (b & 0b10000000) == 0:
                break
            shift += 7
        return val
    
    def read_str(self) -> str:
        """Reads an osu-styled binary string from the buffer."""

        # The exists byte.
        if self.read_bytes(1)[0] == 0:
            return ""
        
        length = self.read_uleb128()
        return self.read_bytes(length).decode()