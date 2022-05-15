from .client.client import (
    AbstractClient,
    StableClient,
)
from .client.constants.client import ClientType
from typing import (
    Optional,
    TYPE_CHECKING,
)
from state import repos
import asyncio

if TYPE_CHECKING:
    from .user import User

class ClientList:
    """A class storing all clients attached to a user."""

    __slots__ = (
        "_user",
        "_clients",
    )

    # Special Methods.
    def __init__(self, user: "User") -> None:
        """Creates a default instance of `ClientList` for the provided `user`."""

        self._user = user
        self._clients: dict[str, AbstractClient] = {}
        self._lock = asyncio.Lock()
    
    def __len__(self) -> int:
        """Returns the amount of attached clients."""

        return len(self._clients)
    
    # Yes __len__ is enough but implementing __bool__ is slightly faster.
    def __bool__(self) -> bool:
        """Checks if the client has any clients attached."""

        return bool(self._clients)
    
    # Private methods.
    def __insert_client(self, client: AbstractClient) -> None:
        """Inserts a client in the next available position in the
        dictionary."""

        self._clients[client.id] = client
    
    def __insert_client_front(self, client: AbstractClient) -> None:
        """Inserts a client to the front of the client dictionary."""

        self._clients = {
            client.id: client
        } | self._clients
    
    async def __on_client_attach(self, client: AbstractClient) -> None:
        """Actions performed when a client is attached to a user."""

        await client.on_attach(self._user)
        # If this is our first client added.
        if len(self) == 1:
            await repos.online.add_user(self._user)
    
    def __client_from_id(self, client_id: str) -> Optional[AbstractClient]:
        """Attempts to fetch a client from the corresponding `client_id`.
        
        Returns:
            Instance of child class inheriting from `AbstractClient` if exists.
            Else `None`.
        """

        return self._clients.get(client_id)
    
    def __client_type_from_id(self, client_id: str) -> Optional[ClientType]:
        """Returns the type of a client with the ID of `client_id`."""

        if client := self.__client_from_id(client_id):
            return client.type
    
    async def __attach_client(self, client: AbstractClient) -> None:
        """Handles attaching a client to a user."""

        # Stable clients have different ordering logic.
        if client.type == ClientType.STABLE and not self.__stable_client():
            self.__insert_client_front(client)
        else:
            self.__insert_client(client)
        
        await self.__on_client_attach(client)
    
    def __has_any(self, client_type: ClientType) -> bool:
        """Checks if the client list features any clients of the provided
        `client_type`."""

        return any(
            client.type == client_type for client in self._clients.values()
        )
    
    def __stable_client(self) -> Optional[StableClient]:
        """Takes advantage of the ordering, fetches the primary stable client."""

        if not self:
            return
        
        first_client = next(iter(self._clients.values()))
        return first_client if first_client.type == ClientType.STABLE \
            else None
    
    def __get_of_type(self, client_type: ClientType) -> Optional[AbstractClient]:
        """Gets the first client of the given type."""

        for client in self._clients.values():
            if client.type == client_type:
                return client
    
    def __get_all_of_type(self, client_type: ClientType) -> list[AbstractClient]:
        """Gets all attached clients of given type."""

        return [
            cl for cl in self._clients.values()
            if cl.type == client_type
        ]

    # Public methods
    async def attach(self, client: AbstractClient) -> None:
        """Attaches a client to the user, registering it.
        
        Note:
            Acquires the user client list lock.
            Stable clients are given priority in the ordering.
        """

        async with self._lock:
            self.__attach_client(client)
    
    async def from_id(self, client_id: str) -> Optional[AbstractClient]:
        """Attempts to fetch an instance inheriting form `AbstractClient`
        with the matching id.

        Note:
            Acquires the user client list lock.
        
        Returns:
            Child class of `AbstractClient` if attached to this specific user.
            Else `None`.
        """
        
        async with self._lock:
            return self.__client_from_id(client_id)
    
    async def type_from_id(self, client_id: str) -> Optional[ClientType]:
        """Returns the client type enum of a client with the given `client_id`.
        
        Note:
            Acquires the user client list lock.
        
        Returns:
            Enum of `ClientType` of the found client if found.
            Else `None`.
        """

        async with self._lock:
            return self.__client_type_from_id(client_id)
    
    async def has_any(self, client_type: ClientType) -> bool:
        """Checks if the user has any clients of type `client_type` attached.
        
        Note:
            Acquires the user client list lock.
        """

        async with self._lock:
            return self.__has_any(client_type)
    
    async def get_with_type(self, client_type: ClientType) -> Optional[ClientType]:
        """Returns the first client of the given `client_type`.
        
        Note:
            Acquires the user client list lock.
        
        Returns:
            Child class of `AbstractClient` if exists.
            Else `None`.
        """

        async with self._lock:
            return self.__get_of_type(client_type)
    
    async def get_all_with_type(self, client_type: ClientType) -> Optional[ClientType]:
        """Returns all clients of the given `client_type`.
        
        Note:
            Acquires the user client list lock.
        
        Returns:
            List of child class of `AbstractClient` that may be empty.
        """

        async with self._lock:
            return self.__get_all_of_type(client_type)
    
    async def stable_client(self) -> Optional[StableClient]:
        """Returns the primary stable client if exists.
        
        Note:
            Acquires the user client list lock.
        """

        async with self._lock:
            return self.__stable_client()
