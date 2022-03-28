from abc import ABC, abstractmethod

class AbstractAuthComponent(ABC):
    """An abstract class representing the client authentication component."""

    @abstractmethod
    async def reload(self) -> None:
        ...
    
    @abstractmethod
    async def authenticate(self, token: str) -> bool:
        ...
