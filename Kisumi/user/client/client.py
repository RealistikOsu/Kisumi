from abc import ABC, abstractmethod, abstractproperty
from scores.constants.mode import CustomMode, Mode
from .components.chat import AbstractChatComponent
from .components.auth import (
    AbstractAuthComponent,
    StableAuthComponent,
)
from .components.queue import ByteBuffer
from .constants.client import ClientType
from .components.hwid import StableHWID
from .components.action import Action
from typing import (
    TYPE_CHECKING,
    Optional,
)
from dataclasses import dataclass

if TYPE_CHECKING:
    from user.user import User
    from user.stats import ModeStats

@dataclass
class AbstractClient(ABC):
    """An abstract client class."""

    type: ClientType
    auth: AbstractAuthComponent
    chat: AbstractChatComponent
    user: Optional["User"]
    action: Action
    ...

    @abstractmethod
    async def logout(self) -> None:
        ...
    
    @abstractmethod
    async def on_attach(self, user: "User") -> None:
        ...
    
    @abstractproperty
    def current_stats(self) -> "ModeStats":
        ...

@dataclass
class StableClient(AbstractClient):
    """A class representing the stable game client (2013-2022)"""

    auth: Optional[StableAuthComponent]
    queue: ByteBuffer
    hwid: StableHWID
    c_mode: CustomMode = CustomMode.VANILLA
    mode: Mode = Mode.STANDARD

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
        await self.auth.generate_token()
        #await stable_clients.insert_client(self)
    
    # Staticmethods/Classmethods
    @staticmethod
    async def from_login(hwid: StableHWID) -> "StableClient":
        """Creates a default instance of `StableClient` using data from login."""

        return StableClient(
            type= ClientType.STABLE,
            auth= None,
            chat= None,
            user= None,
            queue= ByteBuffer.new(),
            hwid= hwid,
            action= Action.new(),
        )

    async def logout(self) -> None:
        return #await super().logout()
    
    @property
    def current_stats(self) -> "ModeStats":
        return self.user.stats.from_modes(self.c_mode, self.mode)
