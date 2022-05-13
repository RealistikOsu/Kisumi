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
from resources.db.geo.iploc import IPLocation
from typing import (
    TYPE_CHECKING,
    Optional,
)
from dataclasses import dataclass
from models.request.login import LoginRequestModel
import uuid

if TYPE_CHECKING:
    from user.user import User
    from user.stats import ModeStats

@dataclass
class AbstractClient(ABC):
    """An abstract client class."""

    type: ClientType
    id: str
    auth: AbstractAuthComponent
    chat: AbstractChatComponent
    user: Optional["User"]
    action: Action
    location: IPLocation
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
    timezone: int

    # Public methods
    async def on_attach(self, user: "User") -> None:
        """Handles the client being attached to a user object.
        
        Note:
            Creates the instance of auth.
        """
        
        ...
    
    # Staticmethods/Classmethods
    @staticmethod
    async def from_login(user: "User", hwid: StableHWID, location: IPLocation,
                         request: LoginRequestModel) -> "StableClient":
        """Creates a default instance of `StableClient` using data from login."""

        return StableClient(
            type= ClientType.STABLE,
            auth= StableAuthComponent(
                user.password,
                user,
            ),
            chat= None,
            queue= ByteBuffer.new(),
            hwid= hwid,
            action= Action.new(),
            location= location,
            user= user,
            timezone= request.utc_timezone,
            id= str(uuid.uuid4()),
        )

    async def logout(self) -> None:
        return #await super().logout()
    
    @property
    def current_stats(self) -> "ModeStats":
        return self.user.stats.from_modes(
            self.action.c_mode,
            self.action.mode,
        )
