# Due to Python's generalisation of all integers as `int`, we have to separate
# them to work with the binary format. This additionally allows for complete
# type hinting.
from typing import Union, Type

__all__ = (
    "u8",
    "i8",
    "u16",
    "i16",
    "u32",
    "i32",
    "i64",
    "u64",
    "SERIALISABLE_TYPES",
    "SERIALISABLE_TYPES_ANNOTATION",
)

class u8: pass
class i8: pass
class u16: pass
class i16: pass
class u32: pass
class i32: pass
class u64: pass
class i64: pass

SERIALISABLE_TYPES = (
    u8,
    i8,
    u16,
    i16,
    u32,
    i32,
    u64,
    i64,
    float,
    str,
)

SERIALISABLE_TYPES_ANNOTATION = Union[
    Type[u8],
    Type[i8],
    Type[u16],
    Type[i16],
    Type[u32],
    Type[i32],
    Type[u64],
    Type[i64],
    Type[float],
    Type[str],
]
