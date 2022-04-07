# FastAPI-style parsing of req args into classes.
# TODO: Rewite https://i.imgur.com/VrsELCI.png
from dataclasses import dataclass
from abc import ABC, abstractmethod
from email.policy import default
from starlette.requests import Request
from typing import (
    Optional,
    SupportsIndex,
    TypeVar,
    Type,
    get_args,
)
from utils.typing import is_optional

T = TypeVar("T")

class AbstractRequestParser(ABC):
    """An abstract class guidelining the layout of a request parser function."""

    @abstractmethod
    async def parse(self, req: Request) -> Optional[T]:
        """Attempts to parse the current element from a request object.
        Returns `None` if failed."""

        ...

# Actual parsers.
@dataclass
class Header(AbstractRequestParser):
    """Parses a header value from the request."""

    name: str
    cast: Type[T] = str
    default: Optional[T] = None

    async def _retrieve_arg_dict(self, req: Request) -> SupportsIndex:
        """Retrieves an indexable dict from which the arg can be retrieved."""

        return req.headers

    async def parse(self, req: Request) -> Optional[T]:
        """Attempts to parse the current header from a request object.
        Returns `None` if failed."""

        value = self._retrieve_arg_dict(req).get(self.name, self.default)
        if value:
            return self.cast(value)
        return None

class PostArg(Header):
    """Parses a post argument from the request."""

    async def _retrieve_arg_dict(self, req: Request) -> SupportsIndex:
        assert req.method == "POST", "Attempted to parse post args on a non-post req."

        return await req.form() # The result of this is cached internally so its fine.

class GetArg(Header):
    """Parses a GET (url) argument from the request."""

    async def _retrieve_arg_dict(self, req: Request) -> SupportsIndex:
        return req.query_params

class Body(AbstractRequestParser):
    """Returns the request body."""

    def __init__(self, into_str: bool = False) -> None:
        super().__init__()
        self._into_str = into_str

    async def parse(self, req: Request) -> Optional[bytearray]:
        return bytearray(req.body()) if not self._into_str \
            else (await req.body()).decode()

_ALL_PARSERS = (
    Header,
    PostArg,
    GetArg,
    Body,
)

# Parsing model.
Ty = TypeVar("Ty", bound= "RequestStruct")
class RequestStruct:
    """Base Model inherited by all request parsing model."""

    async def _parse(self: T, req: Request) -> bool:
        """Parses data from the request according to the class annotations."""

        for name, parser in self.__annotations__.items():
            assert type(parser) in _ALL_PARSERS, f"Type {parser!r} is not a valid parser."

            # Optional[Header(...)] support
            if optional := is_optional(parser):
                parser = get_args(parser)[0]
            
            val = await parser.parse(req)

            if val is None and not optional:
                return False

            setattr(self, name, val)
        
        return True
    
    @classmethod
    async def from_request(cls: Type[T], req: Request) -> Optional[T]:
        """Attempts to parse a request struct from a request"""

        inst = cls()
        if await inst.parse(req):
            return inst
