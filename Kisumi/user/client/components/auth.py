from abc import ABC, abstractmethod
from time import time
from typing import (
    TYPE_CHECKING,
)
from .constants.tokens import AuthType
from utils.hash import BCryptPassword
from user.token import (
    AuthJWT,
    confirm_token_expiry,
    decode_jwt_str,
    encode_jwt_dict,
)
from state import config
import asyncio

if TYPE_CHECKING:
    from user.user import User

def _is_valid_md5(md5: str) -> bool:
    """Checks if the given `md5` meets the md5 specification."""

    # Simple, not in-depth check made to be quick.
    return isinstance(md5, str) and len(md5) == 32

class AbstractAuthComponent(ABC):
    """An abstract class representing the client authentication component."""

    @abstractmethod
    async def reload(self) -> None:
        ...
    
    @abstractmethod
    async def authenticate(self, token: str) -> bool:
        ...

class StableAuthComponent(AbstractAuthComponent):
    """A component utilised for processing a user's authentication."""

    __slots__ = (
        "_lock",
        "_pw_bcrypt",
        "_cached_md5",
        "_user",
    )

    def __init__(self, pw: BCryptPassword, user: "User") -> None:
        super().__init__()

        self._lock = asyncio.Lock()
        self._pw_bcrypt = pw
        self._cached_md5 = None
        self._user = user
    
    def generate_jwt_dict(self) -> AuthJWT:
        """Generates a new JWT auth token dict for the user with the default
        expiry."""

        t = int(time.time())

        return {
            "user_id": self._user.id,
            "start": t,
            "expiry": t + config.CRYPT_JWT_EXPIRY,
            "type": AuthType.STABLE,
        }
    
    def generate_jwt(self) -> str:
        """Generates a new auth JWT for the user, managing expiry."""
    
    def __confirm_jwt(self, jwt: str) -> bool:
        """Checks if the given JWT is valid, considering signing and expiry."""

        if self.token:
            return self.token == token
        
        return False
    
    def __confirm_jwt_dict(self, jwt: AuthJWT) -> bool:
        """Confirms an already decoded jwt"""
    
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
        if await self._pw_bcrypt.compare_async(md5):
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
            else:
                return await self.__confirm_jwt(token)
    
    async def reload(self) -> None:
        """Reloads the authentication information for the user. Clears the cached
        password MD5. Acquires the authentication lock."""

        async with self._lock:
            self.__clear_cached_pw()
            raise NotImplementedError
