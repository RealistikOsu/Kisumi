import sys
from pathlib import Path
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DEBUG = "debug" in map(str.lower, sys.argv)

MONGO_HOST = config("MONGO_HOST", default= "localhost")
MONGO_PORT = config("MONGO_PORT", cast= int, default= 27017)
MONGO_DB = config("MONGO_DB", default= "rosu")

REDIS_DSN = config("REDIS_DSN", cast= Secret)

DATA_DIR = config("DATA_DIR", cast= Path)

SERVER_NAME = config("SERVER_NAME", cast= str, default= "RealistikOsu")
SERVER_DOMAIN = config("SERVER_DOMAIN", cast= str, default= "ussr.pl")
SERVER_PORT = config("SERVER_PORT", cast= int, default= 5344)
