from __future__ import annotations
from typing import (
    Any,
    Union,
    Optional,
    Iterable,
)
import aiomysql

FORMAT_ARGS = Iterable[Union[int, str]]

class MySQLConnection:
    """A thin wrapper around an asynchronous MySQL connection, offering a
    slightly cleaner (in my opinion) API while maintaining performance.
    This class is NOT thread-safe.
    """

    __slots__ = (
        "_conn",
    )

    def __init__(self, conn: aiomysql.Connection) -> None:
        """Creates an insance of `MySQLConnection` from an already established
        `conn` aiomysql connection."""
        
        self._conn = conn
    
    async def execute(self, query: str, args: FORMAT_ARGS = ()) -> Optional[int]:
        """Executes a MySQL query formatted with `args`, resulting the cursor's
        last row id."""

        async with self._conn.cursor() as cur:
            await cur.execute(query, args)
            return cur.lastrowid
    
    async def fetchall(self, query: str, args: FORMAT_ARGS = ()) -> tuple[tuple[Any, ...], ...]:
        """Executes a MySQL query formatted with `args`, returning all results
        as a tuple of tuples."""

        async with self._conn.cursor() as cur:
            await cur.execute(query, args)
            return await cur.fetchall()
    
    async def fetchone(self, query: str, args: FORMAT_ARGS = ()) -> Optional[tuple[Any, ...]]:
        """Executes a MySQL query formatted with `args`, returning the first
        row as a tuple."""

        async with self._conn.cursor() as cur:
            await cur.execute(query, args)
            return await cur.fetchone()
    
    async def fetchcol(self, query: str, args: FORMAT_ARGS = ()) -> Optional[Any]:
        """Executes a MySQL query formatted with `args`, returning the first
        column of the first row. Thin function around `fetchone`."""

        row = await self.fetchone(query, args)

        return row[0] if row else None
    
    async def fetchiter(self, query: str, args: FORMAT_ARGS = ()) -> _MySQLCursorIter:
        """Executes a MySQL query formatted with `args`, returning an iterator
        allowing you to fetch rows on demand."""

        cur = self._conn.cursor()
        await cur.execute(query, args)

        return _MySQLCursorIter(cur)

class _MySQLCursorIter:
    """An iterable result allowing for using large result sets memory
    efficiently."""

    __slots__ = (
        "_cur",
    )

    def __init__(self, cur: aiomysql.Cursor) -> None:
        self._cur = cur
    
    async def __aiter__(self) -> _MySQLCursorIter:
        return self
    
    async def __anext__(self) -> tuple[Any, ...]:
        res = await self._cur.fetchone()
        if not res:
            raise StopAsyncIteration
        return res
    
    # Destructor
    #def __del__(self) -> None:
    #    self._cur.close()

class MySQLPool:
    """A thin wrapper around the aiomysql connection pool with the purpose of 
    yielding only `MySQLConnection` instances."""

    __slots__ = (
        "_pool",
    )

    def __init__(self, conn: aiomysql.Pool) -> None:
        """Creates an instance of `MySQLPool` from an existing pool."""

        self._pool = conn
    
    async def acquire_connection(self) -> MySQLConnection:
        """Acquires the MySQL connection from the pool, waiting until there
        is a free one."""

        return MySQLConnection(
            await self._pool._acquire(),
        )
    
    async def release_connection(self, conn: MySQLConnection) -> None:
        """Releases a connection from the pool."""

        await self._pool.release(conn._conn)
    
    async def acquire(self) -> _MySQLAcquireContextManager:
        """Acquires a MySQL connection using a context manager."""

        return _MySQLAcquireContextManager(self)

# Heavily inspired by aiomysql's context managers.
class _MySQLAcquireContextManager:
    """A context manager for the acquisition of MySQL connections from a
    pool."""

    __slots__ = (
        "_pool",
    )

    def __init__(self, pool: MySQLPool) -> None:
        self._pool = pool
    
    async def __aenter__(self) -> MySQLConnection:
        return await self._pool.acquire_connection()
    
    async def __aexit__(self, *_) -> None:
        return await self._pool.release_connection()
