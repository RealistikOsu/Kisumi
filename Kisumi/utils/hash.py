import bcrypt
import asyncio

PW_PREFIX = "$2b$10$"

def hash_bcrypt(password: str) -> str:
    """Hashes a password using the bcrypt hash, removing the first 7 bytes
    for database optimisation."""

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(10),
    ).decode().removeprefix(PW_PREFIX)

def compare_pw(password: str, bcrypt_trunc: str) -> bool:
    """Compares a plaintext password to a bcrypt with the header (first 7 bytes)
    truncated."""

    return bcrypt.checkpw(
        password.encode(),
        (PW_PREFIX + bcrypt_trunc).encode(),
    )

async def compare_pw_async(password: str, bcrypt_trunc: str) -> bool:
    """Compares a plaintext password to a bcrypt with the header (first 7 bytes)
    truncated. Runs the process within a loop executor."""

    loop = asyncio.get_running_loop()

    return loop.run_in_executor(
        None,
        compare_pw,
        password, bcrypt_trunc,
    )
