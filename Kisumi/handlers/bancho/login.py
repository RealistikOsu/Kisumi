from packets.constants import LoginReply
from user.client.components.hwid import StableHWID
from user.client.client import StableClient
from packets import builders as packet
from state import repos
from fastapi.requests import Request
from pydantic import BaseModel
from typing import Optional
from utils.request import geolocate_request
from utils.hash import hash_md5

class LoginRequestModel(BaseModel):
    """A validated model for login data."""

    username: str
    password_md5: str
    osu_version: str
    utc_timezone: int
    display_city: bool
    allow_dms: bool
    osu_path_md5: str
    adapters: str
    adapters_md5: str
    uninstall_md5: str
    serial_md5: str

    @staticmethod
    def from_req_body(body: str) -> "LoginRequestModel":
        """"""

async def login_handle(
    request: Request,
) -> tuple[bytearray, Optional[str]]:
    """Handles the authentication process."""

    # Parse data.
    hwid = StableHWID(
        "b",
        "b",
        "b",
        "b",
        "b",
    )
    user_id = 1000

    # Fetch user object.
    user = await repos.user_manager.get_user(user_id)

    if user.stable_client:
        return (
              packet.notification("You already seem to have been logged in...")
            + packet.login_reply(LoginReply.FAILED)
        ), None

    if user is None:
        return packet.login_reply(LoginReply.FAILED), None

    # Create client from data
    location = await geolocate_request(request)
    client = await StableClient.from_login(
        user= user,
        hwid= hwid,
        location= location,
    )

    # Auth
    if not await client.auth.authenticate(hash_md5("bruhh")):
        return packet.login_reply(LoginReply.FAILED), None

    await user.insert_client(client)
    await repos.online.add_user(user)

    # Send the user info about the server.
    await client.queue.append(
          packet.heartbeat()
        + packet.login_reply(user.id)
        + packet.notification("Hello, world!")
        + packet.channel_info_end()
    )

    # Grant authentication token
    token = client.auth.generate_jwt()

    return await client.queue.clear(), token
