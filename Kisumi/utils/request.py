# Request based utils.
from fastapi.requests import Request
from state import repos
from resources.db.geo.iploc import IPLocation

def get_ip(req: Request) -> str:
    """Fetches the IP of the request."""

    return req.headers.get("X-Real-IP")

async def geolocate_request(req: Request) -> IPLocation:
    """Geolocates the request IP, returning the `IPLocation` object
    for the request."""

    return await repos.geoloc.from_ip(
        get_ip(req),
    )
