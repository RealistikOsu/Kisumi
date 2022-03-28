from abc import ABC, abstractmethod
from chat.message import Message
from chat.channel import Channel

class AbstractChatComponent(ABC):
    """An abstract base class for the client chat component."""

    @abstractmethod
    async def receive_private_message(self, msg: Message) -> None:
        ...
    
    @abstractmethod
    async def receive_public_message(self, channel: Channel, msg: Message) -> None:
        ...
    
    @abstractmethod
    async def send_private_message(self, msg: Message) -> bool:
        ...
    
    @abstractmethod
    async def send_public_message(self, channel: Channel, msg: Message) -> bool:
        ...
