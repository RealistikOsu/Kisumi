from typing import Generator
from .user import User
from abc import ABC, abstractmethod

class AbstractUserGroup(ABC):
    """An abstract class specifying the layout for an object stroing a group
    of users."""

    @abstractmethod
    async def contains_user(self, user_id: int) -> bool:
        ...
    
    @abstractmethod
    async def remove_user(self, user_id: int) -> bool:
        ...
    
    @abstractmethod
    async def add_user(self, user: User) -> bool:
        ...
    
    @abstractmethod
    async def __aiter__(self) -> Generator[User, None, None]:
        ...

class UserGroup(AbstractUserGroup):
    """Represents a direct, non thread-safe user group."""

    def __init__(self) -> None:
        self.users: list[User] = []
        self.user_ids: list[int] = []
    
    async def contains_user(self, user_id: int) -> bool:
        """Checks if the UserGroup contrains a user with the provided
        `user_id`."""

        return user_id in self.user_ids
    
    async def remove_user(self, user_id: int) -> bool:
        """Attempts to remove a user from the UserGroup, returning a bool
        corresponding to whether the action was a success.
        
        Removal can fail if:
            - No user with the given ID can be 
        """
        if self.contains_user(user_id):
            # We make the assumption the indexes are in the same place.
            idx = self.user_ids.index(user_id)
            del self.users[idx]
            return True

        return False
    
    async def add_user(self, user: User) -> bool:
        """Attempts to insert the user into the UserGroup. Returns `bool`
        corresponding to the result."""
        if not self.contains_user(user.id):
            self.users.append(user)
            self.user_ids.append(user.id)
            return True
        
        return False
    
    async def __aiter__(self) -> Generator[User, None, None]:
        """An asynchronous iterator yielding all of the users."""

        # No async lambdas :(
        async def _iter():
            return (u for u in self.users)
        
        return _iter()
