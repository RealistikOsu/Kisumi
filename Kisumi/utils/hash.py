import bcrypt
import asyncio

PW_PREFIX = "$2b$10$"

class BCryptPassword:
    """A class representing a BCrypt password, associating common functionality
    with it."""

    __slots__ = (
        "_bcrypt_pw",
    )

    # Special methods
    def __init__(self, bcrypt_pw: bytes) -> None:
        """Creates an instance of `BCryptPassword` from a normal BCrypt hashed password."""
        
        self._bcrypt_pw = bcrypt_pw
    
    def __str__(self) -> str:
        """Casts the `BCryptPassword` instance into a string."""

        return self.into_str()
    
    def __eq__(self, o: "BCryptPassword") -> bool:
        """Compares two instances of `BCryptPassword`."""

        return self.compare(o)
    
    # Staticmethods.
    @staticmethod
    def from_db_bcrypt(db_str: str) -> "BCryptPassword":
        """Creates an instance of `BCryptPassword` from a string that had its
        header removed for storage optimisation."""

        return BCryptPassword((PW_PREFIX + db_str).encode())
    
    @staticmethod
    def from_bcrypt(bc_str: str) -> "BCryptPassword":
        """Creates an instance of `BCryptPassword` from a bcrypt decoded string."""

        # We base quite a lot of assumptions on the header being constant.
        assert bc_str.startswith(PW_PREFIX), f"Password missing correct header ('{PW_PREFIX}')"
        return BCryptPassword(bc_str.encode())
    
    @staticmethod
    def from_str(plaintext: str) -> "BCryptPassword":
        """Creates an instance of `BCryptPassword` from a plaintext password, running all
        of the BCrypt computation."""

        return BCryptPassword(hash_bcrypt(
            plaintext,
        ))
    
    @staticmethod
    async def from_str_async(plaintext: str) -> "BCryptPassword":
        """Same as `BCryptPassword.from_str` but performs the BCrypt computation in an
        asynchronous loop executor."""

        return BCryptPassword(await hash_bcrypt_async(
            plaintext,
        ))
    
    # Into methods.
    def into_db_str(self) -> str:
        """Returns the hashed password with its header removed."""

        return self._bcrypt_pw.removeprefix(PW_PREFIX)
    
    def into_str(self) -> str:
        """Returns the regular hashed password string."""

        return self._bcrypt_pw.decode()
    
    # Comparison related.
    def compare(self, plaintext: str) -> bool:
        """Compares `BCryptPassword` to a plaintext password, returning a bool of the
        result."""

        return self.__compare(
            plaintext.encode(),
        )
    
    async def compare_async(self, plaintext: str) -> bool:
        """Compares `BCryptPassword` to a plaintext password, returning a bool of the
        result. Runs the BCrypt computation inside of a threadpool."""

        return await self.__compare_async(
            plaintext.encode(),
        )
    
    # Private methods.
    def __compare(self, bc: bytes) -> bool:
        """Compares the BCrypt bytes `bc` to the one stored in the object."""

        return bcrypt.checkpw(
            self._bcrypt_pw,
            bc,
        )

    async def __compare_async(self, bc: bytes) -> bool:
        """Same as `BCryptPassword.__compare` but ran in a loop executor."""

        # Make run in executor code snipped into a utils function.
        loop = asyncio.get_running_loop()

        return await loop.run_in_executor(
            None,
            self.__compare,
            bc,
        )

def hash_bcrypt(password: str) -> bytes:
    """Hashes a password using the bcrypt hash, removing the first 7 bytes
    for database optimisation."""

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(10),
    )

async def hash_bcrypt_async(password: str) -> bytes:
    """Same as `hash_bcrypt` except runs the computation in a loop executor."""

    loop = asyncio.get_running_loop()

    return await loop.run_in_executor(
        None,
        hash_bcrypt,
        password,
    )
