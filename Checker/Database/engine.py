from sqlalchemy import *
from sqlalchemy.exc import OperationalError
from time import sleep
from sys import path
path.append(".")

from Logging.checker_loger import log

def make_engine(database):
    username = database["username"]
    password = database["password"]
    port = database["port"]
    address = database["address"]
    name = database["name"]
    poolSize = database["poolSize"]

    url = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(username, password, address, port, name)
    max_retries = 60
    delay_between_retries = 5

    for attempt in range(max_retries):
        try:
            # Use pre_ping to check connections before use
            engine = create_engine(url, pool_size=int(poolSize), pool_pre_ping=True)
            # Try to connect to the database to see if it's up
            with engine.connect() as conn:
                log("INFO", f"Successfully connected to the database on attempt {attempt + 1}")
                return engine
        except OperationalError as e:
            log("ERROR", f"Attempt {attempt + 1}: Database connection failed. Retrying in {delay_between_retries} seconds...")
            sleep(delay_between_retries)
    raise Exception("Failed to connect to the database after several attempts.")