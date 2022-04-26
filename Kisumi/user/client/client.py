from abc import ABC, abstractmethod
from .components.chat import AbstractChatComponent
from .components.auth import (
    AbstractAuthComponent,
    StableAuthComponent,
)
from .components.queue import ByteBuffer
from .constants.client import ClientType
from .components.hwid import StableHWID
from typing import (
    TYPE_CHECKING,
)
from dataclasses import dataclass

if TYPE_CHECKING:
    from user.user import User

class AbstractClient(ABC):
    """An abstract client class."""

    type: ClientType
    auth: AbstractAuthComponent
    chat: AbstractChatComponent
    ...

    @abstractmethod
    async def logout(self) -> None:
        ...
    
    @abstractmethod
    async def on_attach(self, user: "User") -> None:
        ...

@dataclass
class StableClient(AbstractClient):
    """A class representing the stable game client (2013-2022)"""

    auth: StableAuthComponent
    queue: ByteBuffer
    hwid: StableHWID
