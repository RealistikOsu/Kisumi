# User related repositories.
from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Iterable,
    Optional,
    AsyncGenerator,
)
from user.client.constants.client import ClientType
from user.client.components.queue import ByteLike
from utils.event import Event

from packets.builders import presence

if TYPE_CHECKING:
    from user.client.client import AbstractClient, StableClient
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
    
    def __contains__(self, user: "User") -> bool:
        """Checks if the main user repo contains a specific user."""

        return user.id in self._repo
    
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

"""
@dataclass
class _AsyncUserIterator:
    "\""An iterator over an `AsyncUserRepo`.""\"

    lock: asyncio.Lock
    repo: dict[int, "User"]
    repo_iter = None
    initialised: bool = False

    async def initialise(self) -> None:
        \"""Acquires the lock."\""

        await self.lock.acquire()
        self.repo_iter = iter(self.repo.values())
        self.initialised = True

    async def finish(self) -> None:
        \"""Cleans up after iteration.\"""

        await self.lock.release()

    async def __anext__(self) -> "User":
        if not self.initialised:
            await self.initialise()
        try:
            return next(self.repo_iter)
        except StopIteration:
            await self.finish()
            raise StopAsyncIteration
"""

class AsyncUserRepo(UserRepo):
    """A thread-safe variant of the `UserRepo`. Thin wrapper around all functions,
    acquiring the repo lock."""

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name)
        self._lock = asyncio.Lock()
    
    async def insert(self, user: "User") -> bool:
        async with self._lock:
            return await super().insert(user)
    
    async def remove_id(self, user_id: int) -> bool:
        async with self._lock:
            return await super().remove_id(user_id)
    
    async def remove(self, user: "User") -> bool:
        async with self._lock:
            return await super().remove(user)
    
    async def get(self, user_id: int) -> Optional["User"]:
        async with self._lock:
            return await super().get(user_id)
    """
    def __aiter__(self) -> _AsyncUserIterator:
        \"""Returns an asynchronous iterator over the entire repo.\"""

        return _AsyncUserIterator(
            self._lock,
            self._repo,
        )
    """

    async def temp_user_list(self) -> list["User"]:
        """I AM MAD CAUSE NOTHING IS WORKING. RETURNS A LIST OF ALL
        USERS ADDED. NO FANCY ITERATORS AS THEY DONT LIKE ME."""

        # The most permanent solution is a temporary solution:tm:
        async with self._lock:
            return [user for user in self._repo.values()]

class OnlineUsersRepo:
    """A repository of all online users."""

    __slots__ = (
        "_repo",
        "on_online",
    )

    def __init__(self) -> None:
        self._repo = AsyncUserRepo("OnlineUsersRepo")
        self.on_online = Event()

        self.on_online.subscribe(self.on_online_event)
    """
    Bug induced rage go brr.
    async def clients(self) -> AsyncGenerator["AbstractClient", None]:
        \"""A generator over all of the users' main clients.\"""

        #return (user async for client in self._repo)
        async for user in self._repo:
            yield user.client
    
    async def stable_clients(self) -> AsyncGenerator["StableClient", None]:
        \"""Async generator over all users with a stable client.\"""

        async for client in self.clients():
            if client.type == ClientType.STABLE:
                yield client
    """

    # FIXME: Make these generators once sanity is restored.
    async def clients(self) -> list["AbstractClient"]:
        """List of all users' main clients."""

        return [user.client for user in await self._repo.temp_user_list()]
    
    async def stable_clients(self) -> list["StableClient"]:
        """Lists all users' stable clients."""

        return [
            client for client in await self.clients()
            if client.type == ClientType.STABLE
        ]
    
    async def on_online_event(self, user: "User") -> None:
        """Event hook function listening to new users. Responsible for notifying
        all users of a new user."""

        # Notify all stable clients of the new user.
        await self.broadcast(
            presence(user),
        )
    
    async def add_user(self, user: "User") -> None:
        """Adds the user to the online user list."""

        await self._repo.insert(user)
        await self.on_online.call(user)
    
    async def get(self, user_id: int) -> Optional["User"]:
        """Attempts to fetch an online user by user id. Returns `None` if
        the user is not online."""

        return await self._repo.get(user_id)
    
    async def broadcast(self, b: ByteLike) -> None:
        """Broadcasts a sequence of bytes to all users."""

        for client in await self.stable_clients():
            await client.queue.append(b)
    
