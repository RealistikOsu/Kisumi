# XXX: Perhaps look into moving this into __innit__.py
from dataclasses import dataclass
from utils.hash import BCryptPassword
from .stats import Stats
from .client.constants.client import ClientType
from .client.client import (
    AbstractClient,
    StableClient,
)
from .client.components.auth import TokenString
from typing import (
    Any,
    Optional,
    Generator,
)

@dataclass
class User:
    """An object representing a server user, alongside associated functionality."""

    id: int
    name: str
    email: str
    stats: Stats
    clients: list[AbstractClient] # Ordered by priority
    scores: Any # Iterable object holding a list of top 100 scores and able to fetch more.
    password: BCryptPassword
    notifications: Any

    ...

    # Special Methods
    def __eq__(self, o: "User") -> bool:
        """Compares two instances of `User`."""

        return self.id == o.id
    
    def __hash__(self) -> int:
        """Makes the object hashable, letting it be able to be used in dictionaries
        as a key."""
        return self.id

    # Properies.
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
    
    @property
    def stable_clients(self) -> list[StableClient]:
        """Returns a list of all attached clients with the type `ClientType.STABLE`."""

        return [cl for cl in self.stable_clients_generator]
    
    @property
    def stable_clients_generator(self) -> Generator[StableClient, None, None]:
        """Same as `User.stable_clients` except returns a generator."""
        return (cl for cl in self.clients if cl.type is ClientType.STABLE)
    
    @property
    def client(self) -> Optional[AbstractClient]:
        """Returns the user's primary client if attached."""

        return self.clients[0] if self.clients else None

    @property
    def online(self) -> bool:
        """Checks if the user has any clients attached to it."""

        return bool(self.clients)
    
    # Public functions
    async def insert_client(self, client: AbstractClient) -> None:
        """Attaches a client to a user, managing client prioritisation."""

        # Stable client assumes priority as long as no other ones are attached
        # (tourney).
        if client.type is ClientType.STABLE and not self.stable_client:
            self.clients.insert(0, client)
        else:
            self.clients.append(client)
        
        await client.on_attach(self)
    
    async def stable_client_from_tokenstring(self, token: TokenString) -> Optional[StableClient]:
        """Iterates over all attached stable clients and returns one with a 
        matching `TokenString`."""

        for client in self.stable_clients_generator:
            if await client.auth.authenticate(token):
                return client
