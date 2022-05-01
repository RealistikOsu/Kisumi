from abc import ABC, abstractmethod
from .components.chat import AbstractChatComponent
from .components.auth import (
    AbstractAuthComponent,
    StableAuthComponent,
    TokenString,
)
from .components.queue import ByteBuffer
from .constants.client import ClientType
from .components.hwid import StableHWID
from typing import (
    TYPE_CHECKING,
    Optional,
)
from dataclasses import dataclass

if TYPE_CHECKING:
    from user.user import User

@dataclass
class AbstractClient(ABC):
    """An abstract client class."""

    type: ClientType
    auth: AbstractAuthComponent
    chat: AbstractChatComponent
    user: Optional["User"]
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

    auth: Optional[StableAuthComponent]
    queue: ByteBuffer
    hwid: StableHWID

    # Public methods
    async def on_attach(self, user: "User") -> None:
        """Handles the client being attached to a user object.
        
        Note:
            Creates the instance of auth.
        """
        self.user = user
        self.auth = StableAuthComponent(
            user.password,
            None,
            user,
        )
    
    # Staticmethods/Classmethods
    @staticmethod
    async def from_login(hwid: StableHWID) -> "StableClient":
        """Creates a default instance of `StableClient` using data from login."""

        client = StableClient(
            ClientType.STABLE,
            auth= None
        )
