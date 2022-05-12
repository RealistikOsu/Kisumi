from dataclasses import dataclass
from utils.vector2 import Vector2
from .constants import COUNTRY_CODES
from logger import warning
from geoip2.models import City

@dataclass
class IPLocation:
    """Class representing the geolocation of a specific IP address."""

    ip: str
    city: str
    country: str
    location: Vector2
    utc_offset: int

    def country_into_enum(self) -> int:
        """Converts the country iso code into an enum used by osu."""
        try:
            return COUNTRY_CODES.index(self.country)
        except ValueError:
            warning("Attempted to get the enum for the out of range country"
                   f"{self.country}. This should never happen.")
            return 0
    
    @staticmethod
    def from_city(ip: str, city: City, time_zone: int = 0) -> "IPLocation":
        """Creates an instance of `IPLocation` from MMDB IP city data."""

        return IPLocation(
            ip= ip,
            city= city.city.name,
            country= city.country.iso_code,
            location= Vector2(
                x= city.location.latitude,
                y= city.location.longitude,
            ),
            utc_offset= time_zone,
        )
    
    @staticmethod
    def default() -> "IPLocation":
        """Creates a new, default instance of `IPLocation`."""

        return IPLocation(
            ip= "0.0.0.0",
            city= "NA",
            country= "XX",
            location= Vector2(0.0, 0.0),
            utc_offset= 0,
        )
    
    # Yeahh this is compensation for how to share this data with multiple client tyles...
    def set_time_zone(self, offset: int) -> None:
        """Sets the time zone for a specific IP to `offset`."""

        self.utc_offset = offset
