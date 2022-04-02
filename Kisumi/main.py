from starlette.applications import Starlette
from logger import error, DEBUG, info
from state import config
import asyncio
import uvicorn
import sys

# Pre-config imports.
from state.db import (
    initialise_database_connections,
)

# Use uvloop if possible.
try:
    __import__("uvloop").install()
except ImportError:
    error("Uvloop could not be installed! Expect degraded performance.")

_STARTUP_TASKS = (
    initialise_database_connections(),
)

async def on_startup() -> None:
    info("Kisumi is starting...")

    # Run all startup tasks.
    for task in _STARTUP_TASKS:
        await task
    
    info(f"Completed {len(_STARTUP_TASKS)} startup tasks!")

async def on_shutdown() -> None:
    info("Kisumi is shutting down...")

    ...

def main(argv: list[str]) -> int:
    """Kisumi main entry point."""

    uvicorn.run(
        Starlette(
            debug= DEBUG,
            on_startup= (
                on_startup,
            ),
            on_shutdown= (
                on_shutdown,
            ),
        ),
        port= config.SERVER_PORT,
        access_log= False,
        log_level= "error",
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(
        main(sys.argv[1:])
    )
