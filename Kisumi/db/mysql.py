from typing import (
    Any,
    Union,
    Optional,
)
import aiomysql

FORMAT_ARGS = Union[list, tuple]

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
