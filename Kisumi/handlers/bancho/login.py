from user.client.components.auth import TokenString
from fastapi.requests import Request
from pydantic import BaseModel
from typing import Optional

class LoginRequestModel(BaseModel):
    """A validated model for login data."""

async def login_handle(
    request: Request,
) -> tuple[bytearray, Optional[TokenString]]:
    """Handles the authentication process."""

    return b"", None
