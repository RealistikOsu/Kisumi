# An implementation of a binary deserialiser for usage with 
from .constants import HEADER_LEN
from .types import *
import struct

class BinaryReader:
    """A binary-deserialisation class managing a buffer of bytes. Tailored for
    usage within osu's binary formats, such as Bancho packets and replays."""
