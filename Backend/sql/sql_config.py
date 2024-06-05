from sqlalchemy import *
from sqlalchemy.exc import OperationalError
import time
from sys import path
path.append(".")

from backend_logging.apalucha_logging import log as logger

def make_engine(database, log=True):
    username = database["username"]
    password = database["password"]
    port = database["port"]
    address = database["address"]
    name = database["name"]
    poolSize = database["poolSize"]
    maxOverflow = database["poolOverflow"]
    poolRecycle = database["poolRecycle"]
    poolTimeout = database["poolTimeout"]

    url = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(username, password, address, port, name)
    max_retries = 60
    delay_between_retries = 5

    for attempt in range(max_retries):
        try:
            # Use pre_ping to check connections before use
            engine = create_engine(url, pool_size=int(poolSize), max_overflow=int(maxOverflow), pool_pre_ping=True, pool_recycle=int(poolRecycle), pool_timeout=int(poolTimeout))
            # Try to connect to the database to see if it's up
            with engine.connect() as conn:
                if log:
                    logger("INFO", f"Successfully connected to the database on attempt {attempt + 1}")
                return engine
        except OperationalError as e:
            if log:
                logger("ERROR", f"Attempt {attempt + 1}: Database connection failed. Retrying in {delay_between_retries} seconds...")
            time.sleep(delay_between_retries)
    raise Exception("Failed to connect to the database after several attempts.")