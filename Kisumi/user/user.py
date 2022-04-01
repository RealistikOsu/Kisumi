from dataclasses import dataclass
from .stats import Stats
from .client.constants.client import ClientType
from .client.client import (
    AbstractClient,
    StableClient,
)
from typing import (
    Optional,
)

@dataclass
class User:
    """An object representing a server user, alongside associated functionality."""

    id: int
    stats: Stats
    clients: list[AbstractClient]
    ...

    @property
    def stable_client(self) -> Optional[StableClient]:
        """Returns the primary stable client attached to the user if present,
        else returns `None`."""

        # User has no clients attrached.
        if not self.clients:
            return
        
        # If the first one is a valid stable client, return it. In the clients
        # list, the stable client shall always be prioritised.
        if (first_client := self.clients[0]).type is ClientType.STABLE:
            return first_client
        
        return
    
    async def insert_client(self, client: AbstractClient) -> None:
        """Attaches a client to a user, managing client prioritisation."""

        # Stable client assumes priority as long as no other ones are attached
        # (tourney).
        if client.type is ClientType.STABLE and not self.stable_client:
            self.clients.insert(0, client)
        else:
            self.clients.append(client)
        
        await client.on_attach(self)
