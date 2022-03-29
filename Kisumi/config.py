import sys
from pathlib import Path
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DEBUG = "debug" in map(str.lower, sys.argv)

MYSQL_HOST = config("MYSQL_HOST", cast=str, default="localhost")
MYSQL_USER = config("MYSQL_USER", cast=str)
MYSQL_PASSWORD = config("MYSQL_PASSWORD", cast=Secret)
MYSQL_DATABASE = config("MYSQL_DATABASE", cast=str)
MYSQL_PORT = config("MYSQL_PORT", cast=int, default=3306)

DATA_DIR = config("DATA_DIR", cast=Path)

REDIS_DB_NUMBER = config("REDIS_DB_NUMBER", cast=int, default=0)
REDIS_HOST = config("REDIS_HOST", cast=str, default="localhost")
REDIS_PASSWORD = config("REDIS_PASSWORD", cast=Secret)


