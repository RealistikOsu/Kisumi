from typing import (
    Any,
    TypeVar,
    Optional,
    Generic,
    Union,
)
import asyncio

T = TypeVar("T")
ALLOWED_IDX = Union[int, str, tuple[Any, ...]]

class LRUCache(Generic[T]):
    """A thread-safe implementation of an LRU (least recently used) cache,
    managing a max capacity and dropping the least recently used items."""

    def __init__(self, capacity: int) -> None:
        # Check we arent stupid and end up in a loop.
        assert capacity > 2, "A cache may have a minimum value of 3."

        self._capacity = capacity
        self._cache: dict[ALLOWED_IDX, T] = {}
        self._lock = asyncio.Lock()
    
    # Python "special" functions.
    def __len__(self) -> int:
        """Returns how many items are currently stored within the cache."""

        # I don't think this requires a lock as it doesn't deal with the data.
        return len(self._cache)
    
    def __repr__(self) -> str:
        return f"<LRUCache({len(self)}/{self._capacity})>"
    
    # Cache related private function (mainly ones that dont acquire the lock)
    def __clear_till_capacity_met(self) -> None:
        """Removes items from the front of the cache until the capacity is left."""

        c_iter = self._cache.keys()
        while len(self) > self._capacity:
            # Iterator hack to allow us to remove the first index efficiently.
            self.__drop(next(c_iter))
        
    def __insert(self, key: ALLOWED_IDX, val: T, ignore_cap_check: bool = False) -> None:
        """Inserts an object `T` with the index `key`. Handling removing excess items."""

        self._cache[key] = val
        if not ignore_cap_check: self.__clear_till_capacity_met()
    
    def __fetch(self, key: ALLOWED_IDX) -> Optional[T]:
        """Retrieves a cache entry with the given result. If found, moves
        the entry to the front of the cache, else returns `None`."""

        val = self._cache.pop(key, None)

        if val is None: return

        # Move to front by reinserting to make this a LRU cache.
        self.__insert(key, val, True)

        return val
    
    def __drop(self, key: ALLOWED_IDX) -> None:
        """Drops an item with index from the cache. Assumes the key 100%
        exists in the cache."""

        del self._cache[key]
    
    # Public functions (acquire lock)
    async def insert(self, key: ALLOWED_IDX, val: T) -> None:
        """Inserts the object `val` at the index `key` of the cache, performing
        cache maintenence in the process.
        
        Note:
            Acquires the cache lock.
        """

        async with self._lock:
            self.__insert(key, val)
    
    async def fetch(self, key: ALLOWED_IDX) -> Optional[T]:
        """Retrieves a cache entry located at the index `key`. If not found,
        returns `None`.
        
        Note:
            Acquires the cache lock.
        """

        async with self._lock:
            return self.__fetch(key)
    
    async def drop(self, key: ALLOWED_IDX) -> None:
        """Drops an entry with the index `key` if present.
        
        Note:
            Acquires the cache lock.
            Raises `KeyError` if the entry does not exist.
        """

        async with self._lock:
            return self.__drop(key)
