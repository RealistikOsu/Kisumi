import aioredis
import traceback
from logger import error
from state import config
from motor import motor_asyncio

mongo_client: motor_asyncio.AsyncIOMotorClient
mongo: motor_asyncio.AsyncIOMotorDatabase
redis: aioredis.Redis

async def initialise_database_connections() -> None:
    global mongo_client, mongo, redis

    # Exception handling is done by starlette.
    mongo_client = motor_asyncio.AsyncIOMotorClient(
        config.MONGO_HOST,
        config.MONGO_PORT,
    )

    mongo = mongo_client[config.MONGO_DB]

    redis = await aioredis.create_redis_pool(str(config.REDIS_DSN))

    # Redis connection test.
    # TODO: Move to function.
    await redis.delete("conn_test") # Just in case.
    await redis.set("conn_test", 2)
    val = await redis.get("conn_test")

    assert val == 2, "Redis connection test failed!"
    await redis.delete("conn_test")

    return 0

