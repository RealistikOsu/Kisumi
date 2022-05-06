from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING
from functools import cache
from utils.hash import BCryptPassword
import uuid
import asyncio

if TYPE_CHECKING:
    from user.user import User

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
        "token",
        "_cached_md5",
        "_user",
    )

    def __init__(self, pw: BCryptPassword, token: Optional["TokenString"], user: "User") -> None:
        super().__init__()

        self._lock = asyncio.Lock()
        self._pw_bcrypt = pw
        self._cached_md5 = None
        self.token = token
        self._user = user
    
    async def generate_token(self) -> "TokenString":
        """Generates a random one-time use token that may be utilised within
        authentication. Acquires the authentication lock."""

        async with self._lock:
            return self.__generate_token()
    
    def __generate_token(self) -> "TokenString":
        """Generates a random one-time use token that may be utilised within
        authentication."""

        self.token = TokenString(self._user.id, _get_unique_token())
        return self.token
    
    def __compare_token(self, token: "TokenString") -> bool:
        """Compares a token to the stored token."""

        if self.token:
            return self.token == token
        
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
            elif isinstance(token, TokenString):
                return self.__compare_token(token)

        return False
    
    async def reload(self) -> None:
        """Reloads the authentication information for the user. Clears the cached
        password MD5. Acquires the authentication lock."""

        async with self._lock:
            self.__clear_cached_pw()
            raise NotImplementedError

class TokenString:
    """A string denoting a user ID and token combo, used for bancho authentication.
    Kisumi uses a format of `user_id|token` (string form) for client authentication."""

    __slots__ = (
        "user_id",
        "token",
    )

    def __init__(self, user_id: int, token: str) -> None:
        """Creates an instance of `TokenString` from """
        
        self.user_id = user_id
        self.token = token
    
    def __repr__(self) -> str:
        return f"<TokenString({self.user_id}, {self.token})"
    
    def __str__(self) -> str:
        return self.into_auth_str()
    
    def __eq__(self, o: object) -> bool:
        return isinstance(o, TokenString) \
            and o.token == self.token \
            and o.user_id == self.user_id
        
    
    def __hash__(self) -> int:
        return hash(self.token)
    
    @staticmethod
    def from_auth_str(auth_str: Optional[str]) -> Optional["TokenString"]:
        """Parses a `user_id|token` formatted string and creates an instance
        of `TokenString` from it. Returns `None` on fail."""

        # Validation.
        if not auth_str or auth_str.count("|") != 1:
            return
        
        user_id_str, token = auth_str.split("|")

        if not user_id_str.isnumeric():
            return
        
        return TokenString(
            int(user_id_str),
            token,
        )
    
    @cache
    def into_auth_str(self) -> str:
        """Formats the object into a bancho authentication string of
        `user_id|token`."""

        return f"{self.user_id}|{self.token}"

