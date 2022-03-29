from abc import ABC, abstractmethod
from .components.chat import AbstractChatComponent
from .components.auth import (
    AbstractAuthComponent,
    UserAuthComponent,
)
from .components.queue import ByteBuffer
from .constants.client import ClientType
from dataclasses import dataclass

class AbstractClient(ABC):
    """An abstract client class."""

    type: ClientType
    auth: AbstractAuthComponent
    chat: AbstractChatComponent
    ...

    @abstractmethod
    async def logout(self) -> None:
        ...

@dataclass
class StableClient(AbstractClient):
    """A class representing the stable game client (2013-2022)"""

    auth: UserAuthComponent
    queue: ByteBuffer
