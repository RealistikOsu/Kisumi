from abc import ABC, abstractmethod
from typing import Optional
from utils import hash
import uuid
import asyncio

# While the probability is ridiculously low, in theory these could clash.
def _get_unique_token() -> str:
    """Generates a unique one-time token utilised for authentication."""

    return str(uuid.uuid4())

def _is_valid_uuid4(token: str) -> bool:
    """Checks if the `token` given is valid uuid 4."""

    return token.count("-") == 4 \
        and len(token) == 36

def _is_valid_md5(md5: str) -> bool:
    """Checks if the given `md5` meets the md5 specification."""

    # Simple, not in-depth check made to be quick.
    return len(md5) == 32

class AbstractAuthComponent(ABC):
    """An abstract class representing the client authentication component."""

    @abstractmethod
    async def reload(self) -> None:
        ...
    
    @abstractmethod
    async def authenticate(self, token: str) -> bool:
        ...

class UserAuthComponent(AbstractAuthComponent):
    """A component utilised for processing a user's authentication."""

    __slots__ = (
        "_lock",
        "_pw_bcrypt",
        "_token",
        "_cached_md5",
    )

    def __init__(self, pw: str, token: Optional[str]) -> None:
        super().__init__()

        self._lock = asyncio.Lock()
        self._pw_bcrypt = pw
        self._cached_md5 = None
        self._token = token
    
    async def generate_token(self) -> str:
        """Generates a random one-time use token that may be utilised within
        authentication. Acquires the authentication lock."""

        async with self._lock:
            return self.__generate_token()
    
    def __generate_token(self) -> str:
        """Generates a random one-time use token that may be utilised within
        authentication."""

        self._token = _get_unique_token()
        return self._token
    
    def __compare_token(self, token: str) -> bool:
        """Compares a token to the stored token."""

        if self._token:
            return self._token == token
        
        return False
    
    async def clear_cached_password(self) -> None:
        """Clears the cached password MD5 for the user, forcing the MD5 to
        be checked again the next time. Acquires the authentication lock."""

        async with self._lock:
            self.__clear_cached_pw()
    
    # Making these a functions just in case i want to make a timed cache in the future.
    def __clear_cached_pw(self) -> None:
        """Clears the cached pw md5."""

        self._cached_md5 = None
    
    def __set_cached_pw(self, pw: str) -> None:
        """Sets the cached password md5."""

        self._cached_md5 = pw
    
    async def __compare_bcrypt(self, md5: str) -> bool:
        """Compares the stored bcrypt password to the given password md5,
        managing caching."""

        if self._cached_md5 is not None:
            return md5 == self._cached_md5
        
        # Compare pw.
        if await hash.compare_pw_async(md5, self._pw_bcrypt):
            self.__set_cached_pw(md5)
            return True
        
        return False
    
    async def authenticate(self, token: str) -> bool:
        """Handles user authentication, accepting password md5 or token
        as input. Acquires the authentication lock."""

        async with self._lock:
            # It is a password MD5.
            if _is_valid_md5(token):
                return await self.__compare_bcrypt(token)
            elif _is_valid_uuid4(token):
                return self.__compare_token(token)

        return False
    
    async def reload(self) -> None:
        """Reloads the authentication information for the user. Clears the cached
        password MD5. Acquires the authentication lock."""

        async with self._lock:
            self.__clear_cached_pw()
            raise NotImplementedError
