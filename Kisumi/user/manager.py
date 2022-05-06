from utils.singleton import Singleton
from repositories.user import UserRepo
from typing import Optional, TYPE_CHECKING
import asyncio

if TYPE_CHECKING:
    from .user import User

class UserManager(Singleton):
    """A class for managing and creating instances of users."""

    __slots__ = (
        "_users",
        "_lock",
    )

    def __init__(self) -> None:
        self._repo = UserRepo("Manager")
        self._lock = asyncio.Lock()
    
    # Private methods.
    async def __get_user(self, user_id: int) -> Optional["User"]:
        """Attempts to retrieve an insance of `User` with the given ID from
        the cache or database (the sources are checked in the order listed).
        
        Note:
            The only difference between this and the public variant is that
            this one does not acquire the lock.
        """
    
        if (user := await self._repo.get(user_id)):
            return user
            
        # Db logic.
        ...

    # Public methods.
    async def get_user(self, user_id: int) -> Optional["User"]:
        """Attempts to retrieve an insance of `User` with the given ID from
        the cache or database (the sources are checked in the order listed).
        
        Note:
            Acquires the UserManager lock.
        """

        async with self._lock:
            return await self.__get_user(user_id)
