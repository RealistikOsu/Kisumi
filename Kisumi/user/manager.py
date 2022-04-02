from .user import User
from utils.singleton import Singleton
from db.mysql import MySQLConnection
from typing import Optional
import asyncio

class UserManager(Singleton):
    """A class for managing and creating instances of users."""

    __slots__ = (
        "_users",
        "_lock",
    )

    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._lock = asyncio.Lock()
    
    # Private methods.
    def __insert_user(self, user: User) -> None:
        """Inserts the provided user object into storage."""

        self._users[user.id] = user
    
    def __retrieve_stored_user(self, user_id: int) -> Optional[User]:
        """Attempts to fetch an instance of `User` from the dict, returning
        `None` if it doesnt exist."""

        return self._users.get(user_id)
    
    async def __get_user(self, user_id: int, conn: MySQLConnection) -> Optional[User]:
        """Attempts to retrieve an insance of `User` with the given ID from
        the cache or database (the sources are checked in the order listed).
        
        Note:
            The only difference between this and the public variant is that
            this one does not acquire the lock.
        """
    
        if (user := self.__retrieve_stored_user(user_id)):
            return user
            
        # Db logic.
        ...

    # Public methods.
    async def get_user(self, user_id: int, conn: MySQLConnection) -> Optional[User]:
        """Attempts to retrieve an insance of `User` with the given ID from
        the cache or database (the sources are checked in the order listed).
        
        Note:
            Acquires the UserManager lock.
        """

        async with self._lock:
            return await self.__get_user(user_id, conn)
