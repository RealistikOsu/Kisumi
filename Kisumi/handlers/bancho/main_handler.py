from .router import router
from starlette.requests import Request
from starlette.responses import (
    PlainTextResponse,
    Response,
)
from state import config

# The page people get if they access this from their web browser.
@router.route("/", methods= ["GET"])
async def main_get(_: Request) -> PlainTextResponse:
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
    auth_token = req.headers.get("osu-token")

    # Packet request.
    if auth_token:
        ...
    # Login attempt
    else:
        ...
