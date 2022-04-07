from user.client.components.auth import TokenString
from models.misc_models import LoginRequestStruct
from typing import Optional

async def login_handle(
    data: LoginRequestStruct,
) -> tuple[bytearray, Optional[TokenString]]:
    """Handles the authentication process."""

    return b"", None
