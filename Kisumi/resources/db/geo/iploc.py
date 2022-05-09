from dataclasses import dataclass
from utils.vector2 import Vector2
from .constants import COUNTRY_CODES
from logger import warning

@dataclass
class IPGeoLoc:
    """Class representing the geolocation of a specific IP address."""

    ip: str
    city: str
    country: str
    location: Vector2

    def country_into_enum(self) -> int:
        """Converts the country iso code into an enum used by osu."""
        try:
            return COUNTRY_CODES.index(self.country)
        except ValueError:
            warning("Attempted to get the enum for the out of range country"
                   f"{self.country}. This should never happen.")
            return 0
