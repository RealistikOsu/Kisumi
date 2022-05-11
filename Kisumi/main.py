from starlette.routing import Host
from fastapi.applications import FastAPI
from logger import error, DEBUG, info
import asyncio
import uvicorn
import sys

# Pre-config imports.
from state.db import (
    initialise_database_connections,
)
from state import config, repos
from user._testing import (
    configure_test_user,
)

# Router imports.
from handlers.bancho.router import router as bancho_router

# FIXME: Find another way to initalise these files.
from handlers.bancho.main_handler import main_post as _

# Use uvloop if possible.
try:
    __import__("uvloop").install()
except ImportError:
    error("Uvloop could not be installed! Expect degraded performance.")

_STARTUP_TASKS = (
    initialise_database_connections(),
    configure_test_user(),
    repos.json_loader.load(),
    repos.geoloc.kisumi_load(),
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


BANCHO_SUBDOMAINS = ("c", "c4", "c5", "c6", "ce")
def main(argv: list[str]) -> int:
    """Kisumi main entry point."""

    uvicorn.run(
        FastAPI(
            title= "Kisumi",
            openapi_url= None,
            docs_url= None,
            redoc_url= None,
            debug= DEBUG,
            on_startup= (
                on_startup,
            ),
            on_shutdown= (
                on_shutdown,
            ),
            routes= (
                # The bancho protocol operates on many donains, alongside supporting
                # switchers.
                *(Host(f"{subdomain}.ppy.sh", bancho_router, "Bancho Switcher")
                for subdomain in BANCHO_SUBDOMAINS),
                *(Host(f"{subdomain}.{config.SERVER_DOMAIN}", bancho_router, "Bancho Devserver")
                for subdomain in BANCHO_SUBDOMAINS),
            ),
        ),
        port= config.SERVER_PORT,
        #access_log= False,
        #log_level= "error",
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(
        main(sys.argv[1:])
    )
