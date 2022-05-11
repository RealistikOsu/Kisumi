# The Kisumi Geo API.
from utils.vector2 import Vector2
from utils.cache import LRUCache
from typing import Optional
from geoip2 import database
from logger import info, error
from .iploc import IPLocation
import os

class GeolocationDB:
    """A wrapper around the MaxMind GeoIP DB."""

    __slots__ = (
        "_reader",
        "_cache",
    )

    def __init__(self) -> None:
        """Creates a default instance of `GeolocationDB`.
        
        Note:
            To load a MMDB, please use the `load` function.
        """

        self._reader: Optional[database.Reader] = None
        self._cache: LRUCache[IPLocation] = LRUCache(200) # Do we really need this?
    
    def load(self, location: str = "resources/ip.mmdb") -> bool:
        """Attempts to load a MMDB geoip database from `location`, returning
        bool of success."""

        if not os.path.exists(location):
            return False
        
        try:
            self._reader = database.Reader(location)
        except Exception: # Do something more specific.
            return False
        
        return True
    
    async def kisumi_load(self, location: str = "resources/ip.mmdb") -> None:
        """A startup task version of `load` that raises an exception on fail."""

        info("Loading the geolocation database...")

        if not self.load():
            raise Exception("Failed to load database!")
        
        info("Geolocation database loaded!")
    
    async def from_ip(self, ip: str) -> IPLocation:
        """Attempts to create an instance of `IPLocation` from the database
        or cache."""

        assert self._reader is not None, "Database reader not established! Use " \
                                         "GeolocationDB.load() first!"

        if cached_ip := await self._cache.fetch(ip):
            # Cache hit
            return cached_ip
        
        # Miss, use db
        city_data = self._reader.city(ip)
        ip_loc = IPLocation.from_city(ip, city_data)

        # Cache for the future.
        await self._cache.insert(ip, ip_loc)
        return ip_loc
