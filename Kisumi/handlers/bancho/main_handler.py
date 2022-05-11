from .router import router
from fastapi.requests import Request
from fastapi.responses import (
    PlainTextResponse,
    Response,
)
from user.token import decode_jwt_str
from state import config

from .login import login_handle

# The page people get if they access this from their web browser.
@router.route("/", methods= ["GET"])
async def main_get(req: Request) -> PlainTextResponse:
    return PlainTextResponse(
        f"{config.SERVER_NAME} - Powered by Kisumi!"
    )

@router.route("/", methods= ["POST"])
async def main_post(req: Request) -> Response:
    """The main handler for post requests to the bancho server."""

    # Only allow osu! clients past this point.
    if req.headers.get("User-Agent") != "osu!":
        return await main_get(req)

    # Select whether this is a login request or a packet request.
    jwt_str = req.headers.get("osu-token")
    jwt_dec = decode_jwt_str(jwt_str) if jwt_str else None

    # Packet request.
    if jwt_str:
        data = b""
        token = jwt_str
        ...
    # Login attempt
    else:
        data, token = await login_handle(req)

    print(data)
    print(f"{token!r}")
        
    return Response(
        content= bytes(data),
        headers= {
            "cho-token": token if token else "no",
        },
    )
