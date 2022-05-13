# XXX: Perhaps look into moving this into __innit__.py
from dataclasses import dataclass
from utils.hash import BCryptPassword
from .stats import Stats
from .settings import Settings
from .client.constants.client import ClientType
from .client.client import (
    AbstractClient,
    StableClient,
)
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
    clients: dict[str, AbstractClient] # TODO: Client List object with lock.
    scores: Any # Iterable object holding a list of top 100 scores and able to fetch more.
    password: BCryptPassword
    notifications: Any
    name_history: list[str]
    settings: Settings

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

        return self.client if self.client.type is ClientType.STABLE else None
    
    @property
    def stable_clients(self) -> list[StableClient]:
        """Returns a list of all attached clients with the type `ClientType.STABLE`."""

        return [cl for cl in self.stable_clients_generator]
    
    @property
    def stable_clients_generator(self) -> Generator[StableClient, None, None]:
        """Same as `User.stable_clients` except returns a generator."""
        return (cl for cl in self.clients.values() 
                if cl.type is ClientType.STABLE)
    
    @property
    def client(self) -> Optional[AbstractClient]:
        """Returns the user's primary client if attached."""

        return next(iter(self.clients)) if self.clients else None

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
            # Dies ordered dicts that dont allow indexes.
            self.__insert_client_to_front(client)
        else:
            self.clients[client.id] = client
        
        await client.on_attach(self)
    
    def __insert_client_to_front(self, client: AbstractClient) -> None:
        """Inserts a client to the front of the client registry. Temporary
        function prior to the addition of a proper client manager."""

        self.client = {
                client.id: client
        } | self.client
