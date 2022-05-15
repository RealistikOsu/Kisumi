from packets.constants import LoginReply
from user.client.components.hwid import StableHWID
from user.client.client import StableClient
from packets import builders as packet
from state import repos
from fastapi.requests import Request
from typing import Optional
from utils.request import geolocate_request
from utils.hash import hash_md5
from models.request.login import LoginRequestModel

async def login_handle(
    request: Request,
) -> tuple[bytearray, Optional[str]]:
    """Handles the authentication process."""

    # Parse data.
    login_data = LoginRequestModel.from_req_body(
        (await request.body()).decode(),
    )
    hwid = StableHWID( # TODO: from_login()
        client_md5= login_data.osu_path_md5,
        adapter= login_data.adapters,
        adapter_md5= login_data.adapters_md5,
        uninstaller_md5= login_data.uninstall_md5,
        serial_md5= login_data.serial_md5,
    )
    user_id = 1000

    # Fetch user object.
    user = await repos.user_manager.get_user(user_id)

    if await user.clients.stable_client():
        return (
              packet.notification("You already seem to have been logged in...")
            + packet.login_reply(LoginReply.FAILED)
        ), None

    if user is None:
        return packet.login_reply(LoginReply.FAILED), None

    # Create client from data
    location = await geolocate_request(request)
    location.set_time_zone(login_data.utc_timezone)
    client = await StableClient.from_login(
        user= user,
        hwid= hwid,
        location= location,
        request= login_data,
    )

    # Auth
    if not await client.auth.authenticate(hash_md5("bruhh")):
        return packet.login_reply(LoginReply.FAILED), None

    await user.clients.attach(client)

    # Send the user info about the server.
    await client.queue.append(
          packet.heartbeat()
        + packet.login_reply(user.id)
        + packet.notification("Hello, world!")
        + packet.channel_info_end()
        + packet.stats_client(client)
        + packet.protocol_ver(19)
    )

    # Grant authentication token
    token = client.auth.generate_jwt()

    return await client.queue.clear(), token
