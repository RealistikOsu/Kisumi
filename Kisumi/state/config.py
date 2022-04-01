import sys
from pathlib import Path
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DEBUG = "debug" in map(str.lower, sys.argv)

MYSQL_HOST = config("MYSQL_HOST", cast=str, default="localhost")
MYSQL_USER = config("MYSQL_USER", cast=Secret)
MYSQL_PASSWORD = config("MYSQL_PASSWORD", cast=Secret)
MYSQL_DATABASE = config("MYSQL_DATABASE")
MYSQL_PORT = config("MYSQL_PORT", cast=int, default=3306)

REDIS_DSN = config("REDIS_DSN", cast=Secret)

DATA_DIR = config("DATA_DIR", cast=Path)

SERVER_NAME = config("SERVER_NAME", cast=str, default="RealistikOsu")
SERVER_DOMAIN = config("SERVER_DOMAIN", cast=str, default="ussr.pl")
SERVER_PORT = config("SERVER_PORT", cast=int, default=5344)
