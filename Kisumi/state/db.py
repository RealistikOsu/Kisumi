import aioredis
import traceback
from logger import error
from state import config
from db.mysql import MySQLPool

sql: MySQLPool
redis: aioredis.Redis

async def initialise_database_connections() -> int:
    global sql, redis

    try:
        sql = await MySQLPool.connect(
            host=config.MYSQL_HOST,
            username=str(config.MYSQL_USER),
            password=str(config.MYSQL_PASSWORD),
            database=config.MYSQL_DATABASE,
            port=config.MYSQL_PORT
        )
        await sql.test_connection()

        redis = await aioredis.create_redis_pool(str(config.REDIS_DSN))

        # Redis connection test.
        # TODO: Move to function.
        await redis.delete("conn_test") # Just in case.
        await redis.set("conn_test", 2)
        val = await redis.get("conn_test")

        assert val == 2, "Redis connection test failed!"
        await redis.delete("conn_test")

        return 0
    except Exception:
        error(f"Initialising connections failed!\nTraceback: {traceback.format_exc()}")
        return 1

