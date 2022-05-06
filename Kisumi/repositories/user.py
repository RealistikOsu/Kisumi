# User related repositories.
from abc import ABC, abstractmethod
import asyncio
from re import L
from typing import (
    TYPE_CHECKING,
    Iterable,
    Optional,
)

if TYPE_CHECKING:
    from user.client.components.auth import TokenString
    from user.client.client import StableClient
    from user.user import User

class AbstractUserRepo(ABC):
    """An abstract base class for any user-based repository."""

    @abstractmethod
    async def insert(self, user: "User") -> bool:
        ...
    
    @abstractmethod
    async def remove(self, user: "User") -> bool:
        ...

    @abstractmethod
    async def remove_id(self, user_id: int) -> bool:
        ...
    
    @abstractmethod
    async def get(self, user_id: int) -> Optional["User"]:
        ...

class UserRepo(AbstractUserRepo):
    """Handles the storage of direct user references. Not thread-safe."""

    __slots__ = (
        "name",
        "_repo",
    )

    # Special Methods
    def __init__(self, name: Optional[str] = None) -> None:
        """Creates an empty instance of `UserRepo` with an optional name
        `name`.
        
        Note:
            The `name` attribute is completely optional and does not alter any
            functionality.
        """

        self.name = name
        self._repo: dict[int, "User"] = {}
    
    def __len__(self) -> int:
        """Returns the length of the repository."""

        return len(self._repo)
    
    def __iter__(self) -> Iterable["User"]:
        """Returns an iterator over the entire repo."""

        return iter(self._repo.values())
    
    def __str__(self) -> str:
        """Returns a string representation of the repo."""

        return self.name or "UserRepo"
    
    def __repr__(self) -> str:
        """Returns a debugging string representation of the repo."""

        if self.name is not None:
            return f"<{self.name} UserRepo({len(self)})>"
        
        return f"<UserRepo({len(self)})>"
    
    # Public methods.
    async def insert(self, user: "User") -> bool:
        """Inserts an instance of `User` into the repository, returning a
        bool corresponding to the success.
        
        Note:
            Adding a user that is already in the repo does nothing but
            returns `True`.
        
        Returns:
            Always `True`.
        """

        self._repo[user.id] = user
        return True
    
    async def remove_id(self, user_id: int) -> bool:
        """Removes a user with the id `user_id` from the repo.
        
        Returns:
            `False` if the user does not exist in the repo.
            `True` on success.
        """

        try:
            del self._repo[user_id]
            return True
        except KeyError:
            return False
    
    async def remove(self, user: "User") -> bool:
        """Removes a `User` instance from the repository.

        Note:
            Internally, a thin wrapper around `UserRepo.remove_id`.
        
        Returns:
            `False` if the user does not exist in the repo.
            `True` on success.
        """

        return await self.remove_id(user.id)
    
    async def get(self, user_id: int) -> Optional["User"]:
        """Attempts to retrieve a user with the given `user_id` from the,
        repository.
        
        Args:
            user_id (int): The ID of the user to attempt to fetch.
        
        Returns:
            Instance of `User` with the given ID if found.
            Else `None`.
        """

        return self._repo.get(user_id)

#class StableClientsRepo(AbstractUserRepo):
class _StableClientsIter:
    """An iterator over all stable clients."""

    __slots__ = (
        "_repo",
        "_idx",
        "_repo_len",
    )

    def __init__(self, repo: "StableClientsRepo") -> None:
        # TODO: Pass the data directly rather than use private variables.
        self._repo = repo
        self._repo_len = len(repo) # Cache this
        self._repo_val_iter = None

    async def init_iter(self) -> None:
        await self._repo._lock.acquire()
        self._repo_val_iter = iter(self._repo._stable_repo.values())
    
    async def __anext__(self) -> "StableClient":
        """Returns the next indexed client."""
        
        try:
            return next(self._repo_val_iter)
        except StopIteration:
            await self._repo._lock.release()
            raise StopAsyncIteration
    

class StableClientsRepo:
    """A thread-safe repository for storing online users."""

    def __init__(self) -> None:
        # Different indexes
        self._stable_repo: dict["TokenString", "StableClient"] = {}
        self._lock = asyncio.Lock()
    
    def __len__(self) -> int:
        return len(self._stable_repo)
    
    async def __aiter__(self) -> "_StableClientsIter":
        """Stats a locked async iteration over all clients."""

        iterator = _StableClientsIter(self)
        await iterator.init_iter()
        return iterator
    
    # Private methods
    def __insert_client(self, client: "StableClient") -> None:
        """Inserts a client identified by a tokenstring."""

        self._stable_repo[client.auth.token] = client
    
    def __get_client(self, ts: "TokenString") -> Optional["StableClient"]:
        """Attemtps to fetch a client by the TokenString `ts`."""

        return self._stable_repo.get(ts)
    
    async def __remove_client(self, ts: "TokenString") -> bool:
        """Removes a client from the online users list."""
    
    # Public methods.
    async def insert_client(self, client: "StableClient") -> bool:
        """Marks a stable client as online."""

        async with self._lock:
            self.__insert_client(client)
            return True
    
    async def get(self, ts: "TokenString") -> Optional["StableClient"]:
        """Gets a client from a tokenstring instance"""

        async with self._lock:
            return self.__get_client(ts)
    
    async def broadcast(self, data: bytearray) -> None:
        """Broadcasts a set of packets to all members of the repo."""

        # Create a copy so we dont acquire the lock for extended periods of time.
        # TODO: Investigate whether this should actually be done.
        repo_copy = self._stable_repo.copy()
        for client in repo_copy.values():
            await client.queue.append(data)
