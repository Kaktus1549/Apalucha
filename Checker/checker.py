from dotenv import load_dotenv
import os
from sys import path
from time import sleep
path.append(".")
load_dotenv()

from Database.engine import make_engine
from Database.query import *
from Logging.checker_loger import log
from API.endpoints import *

log("INFO", "Starting Apalucha checker... ")
log("INFO", "Loading environment variables... ")

# Load environment variables

url = os.getenv("URL", None)
if url is None:
    log("ERROR", "URL environment variable not found")
    exit()
db_password = os.getenv("DB_PASSWORD", None)
if db_password is None:
    log("ERROR", "DB_PASSWORD environment variable not found")
    exit()
db_username = os.getenv("DB_USERNAME", None)
if db_username is None:
    log("ERROR", "DB_USERNAME environment variable not found")
    exit()
master_user = os.getenv("MASTER_USERNAME", None)
if master_user is None:
    log("ERROR", "MASTER_USERNAME environment variable not found")
    exit()
master_password = os.getenv("MASTER_PASSWORD", None)
if master_password is None:
    log("ERROR", "MASTER_PASSWORD environment variable not found")
    exit()

db_address = "db"
db_port = "3306"

log("INFO", "Environment variables loaded")

# Create engine
log("INFO", "Creating engine... ")
database = {
    "username": db_username,
    "password": db_password,
    "port": db_port,
    "address": db_address,
    "name": "apalucha",
    "poolSize": 5
}
engine = make_engine(database)
log("INFO", "Engine created")

error_count = 0

# Login
log("INFO", f"Logging in as {master_user}... ")
token = api_login(url, master_user, master_password)
if token is None:
    log("ERROR", "Login failed")
    exit()

# Film testing 

log("INFO", "Testing film related operations... ")
test_film = "IWannaBeYours"
test_film_team = "Arctic Monkeys"

log("INFO", f"Creating film {test_film}... ")
if api_create_film(url, token, test_film, test_film_team):
    log("INFO", "Endpoint said film was created")
    log("INFO", "Checking if film is in database... ")
    session = Session(engine)
    if check_film_exists(session, test_film):
        log("INFO", "Film is in database, proceeding to delete")
        if api_delete_film(url, token, test_film):
            log("INFO", "Endpoint said film was deleted")
            if not check_film_exists(session, test_film):
                log("INFO", "Film is not in database")
            else:
                log("ERROR", "Film is still in database")
                delete_film(session, test_film)
                error_count += 1
        else:
            log("ERROR", "Endpoint said film was not deleted")
            error_count += 1
    else:
        log("ERROR", "Film is not in database")
        error_count += 1
    session.close()
else:
    log("ERROR", "Endpoint said film was not created")
    error_count += 1

# User testing
test_admin = "KneeSocks"
test_admin_password = "Arct1cM0nk3ysF0rTheW1n?!."

log("INFO", f"Creating admin {test_admin}... ")
if api_create_user(url, token, True, test_admin, test_admin_password):
    log("INFO", "Endpoint said admin was created")
    log("INFO", "Checking if admin is in database... ")
    session = Session(engine)
    if check_user_exists(session, test_admin, True):
        log("INFO", "Admin is in database, proceeding to delete")
        if api_delete_user(url, token, True, test_admin):
            log("INFO", "Endpoint said admin was deleted")
            if not check_user_exists(session, test_admin, True):
                log("INFO", "Admin is no longer in database")
            else:
                log("ERROR", "Admin is still in database")
                delete_testing_user(session, test_admin, True)
                error_count += 1
        else:
            log("ERROR", "Endpoint said admin was not deleted")
            error_count += 1
    else:
        log("ERROR", "Admin is not in database")
        error_count += 1
    session.close()
else:
    log("ERROR", "Endpoint said admin was not created")
    error_count += 1

# Non-admin user testing

try:
    pdf_url = api_create_user(url, token, False)
    user_id = pdf_url.split("?user=")[1]
    log("INFO", f"Created user {user_id}")
    session = Session(engine)
    log("INFO", "Checking if user is in database... ")
    if check_user_exists(session, user_id, False):
        log("INFO", "User is in database, proceeding to delete")
        if api_delete_user(url, token, False, user_id):
            log("INFO", "Endpoint said user was deleted")
            if not check_user_exists(session, user_id, False):
                log("INFO", "User is no longer in database")
            else:
                log("ERROR", "User is still in database")
                delete_testing_user(session, user_id, False)
                error_count += 1
        else:
            log("ERROR", "Endpoint said user was not deleted")
            error_count += 1
    else:
        log("ERROR", "User is not in database")
        error_count += 1
    session.close()
except Exception as e:
    log("ERROR", f"Failed to create non-admin user: {e}")
    error_count += 1

log("INFO", "Testing finished")
if error_count == 0:
    log("INFO", "No errors found, system is operational!")
elif error_count < 3:
    log("ERROR", "Some errors found, system may be operational")
else:
    log("CRITICAL", "Too many errors found, system is not operational")

log("INFO", "Exiting Apalucha checker... ")
exit()