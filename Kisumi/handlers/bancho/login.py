from packets.constants import LoginReply
from user.client.components.auth import TokenString
from user.client.components.hwid import StableHWID
from user.client.client import StableClient
from packets import builders as packet
from state.repos import user_manager, stable_clients
from fastapi.requests import Request
from pydantic import BaseModel
from typing import Optional

class LoginRequestModel(BaseModel):
    """A validated model for login data."""

async def login_handle(
    request: Request,
) -> tuple[bytearray, Optional[TokenString]]:
    """Handles the authentication process."""

    # Parse data.
    hwid = StableHWID(
        "b",
        "b",
        "b",
        "b",
        "b",
    )

    # Fetch user object.
    user = await user_manager.get_user(1000)

    if user is None:
        return packet.login_reply(LoginReply.FAILED), None

    # Create client from data
    client = await StableClient.from_login(
        hwid,
    )
    await user.insert_client(client)
    await stable_clients.insert_client(client)

    # Broadcast our presence. TODO: mopve to stable_clients.insert_client
    await stable_clients.broadcast(
        packet.presence_client(client)
    )

    # Send the user info about the server.
    await client.queue.append(
          packet.heartbeat()
        + packet.login_reply(user.id)
        + packet.notification("Hello, world!")
        + packet.channel_info_end()
    )


    return await client.queue.clear(), client.auth.token
