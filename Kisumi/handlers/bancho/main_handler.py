from .router import router
from fastapi.requests import Request
from fastapi.responses import (
    PlainTextResponse,
    Response,
)
from user.client.components.auth import TokenString
from state import config

from .login import login_handle

# The page people get if they access this from their web browser.
@router.route("/", methods= ["GET"])
async def main_get() -> PlainTextResponse:
    return PlainTextResponse(
        f"{config.SERVER_NAME} - Powered by Kisumi!"
    )

@router.route("/", methods= ["POST"])
async def main_post(req: Request) -> Response:
    """The main handler for post requests to the bancho server."""

    # Only allow osu! clients past this point.
    if req.headers.get("User-Agent") != "osu!":
        return await main_get()

    # Select whether this is a login request or a packet request.
    auth_token = TokenString.from_auth_str(
        req.headers.get("osu-token"),
    )

    # Packet request.
    if auth_token:
        ...
    # Login attempt
    else:
        data, token = await login_handle(req)
        
        return Response(
            content= data,
            headers= {
                "cho_token": token.into_auth_str() if token else "no",
            },
        )
