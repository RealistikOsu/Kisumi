from typing import (
    Union,
    Type,
    Any,
    get_origin,
    get_args,
)

def unpack_list_type(l: Type[list]) -> Type[Any]:
    """Unpacks the type of a single type list."""

    return get_args(l)[0]

# https://stackoverflow.com/a/58841311/15567752
def is_optional(anno: Type[Any]) -> bool:
    """Checks if the passed type annotation `anno` is an optional field."""

    # Optional is an alias for Union[T, None]
    return get_origin(anno) is Union \
        and type(None) in get_args(anno)
