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
sleep(1.5)
log("WARNING", "In order to successfully test the system, this docker container must be run with the SAME network as the API and the database!!")
log("WARNING", "If you FAIL to do so, the tests will fail!")
sleep(4.5)
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
original_voting_time = os.getenv("VOTING_TIME", None)
if original_voting_time is None:
    log("ERROR", "VOTING_TIME environment variable not found")
    exit()

db_address = "db"
db_port = "3306"

log("INFO", "Environment variables loaded")
sleep(1.5)

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
sleep(1.5)

admin_error_list = []

# Login
log("INFO", f"Logging in as {master_user}... ")
token = api_login(url, master_user, master_password)
if token is None:
    log("ERROR", "Login failed")
    exit()
sleep(1.5)

log("INFO", "---- Testing /managment endpoint and admin related operations ----")

# Film testing 

log("INFO", "Testing film related operations... ")
test_film = "IWannaBeYours"
test_film_team = "Arctic Monkeys"

log("INFO", f"Creating film {test_film}... ")
if api_create_film(url, token, test_film, test_film_team):
    log("INFO", "Endpoint said film was created")
    log("INFO", "Checking if film is in database... ")
    sleep(1.5)
    session = Session(engine)
    if check_film_exists(session, test_film):
        session.close()
        session = Session(engine)
        log("INFO", "Film is in database, proceeding to delete")
        sleep(1.5)
        if api_delete_film(url, token, test_film):
            log("INFO", "Endpoint said film was deleted")
            sleep(1.5)
            session.close()
            session = Session(engine)
            if not check_film_exists(session, test_film):
                log("INFO", "Film is not in database")
            else:
                log("ERROR", "Film is still in database")
                delete_film(session, test_film)
                admin_error_list.append("Failed to delete film via endpoint")
        else:
            log("ERROR", "Endpoint said film was not deleted")
            admin_error_list.append("Endpoint says film was not deleted")
    else:
        log("ERROR", "Film is not in database")
        admin_error_list.append("Failed to create film")
    session.close()
else:
    log("ERROR", "Endpoint said film was not created")
    admin_error_list.append("Endpoint says film was not created")
sleep(1.5)

# User testing
test_admin = "KneeSocks"
test_admin_password = "Arct1cM0nk3ysF0rTheW1n?!."

log("INFO", f"Creating admin {test_admin}... ")
sleep(1.5)
if api_create_user(url, token, True, test_admin, test_admin_password):
    log("INFO", "Endpoint said admin was created")
    log("INFO", "Checking if admin is in database... ")
    session = Session(engine)
    if check_user_exists(session, test_admin, True):
        log("INFO", "Admin is in database, proceeding to delete")
        session.close()
        session = Session(engine)
        sleep(1.5)
        if api_delete_user(url, token, True, test_admin):
            log("INFO", "Endpoint said admin was deleted")
            session.close()
            session = Session(engine)
            sleep(1.5)
            if not check_user_exists(session, test_admin, True):
                log("INFO", "Admin is no longer in database")
            else:
                log("ERROR", "Admin is still in database")
                delete_testing_user(session, test_admin, True)
                admin_error_list.append("Failed to delete admin via endpoint")
        else:
            log("ERROR", "Endpoint said admin was not deleted")
            admin_error_list.append("Endpoint says admin was not deleted")
    else:
        log("ERROR", "Admin is not in database")
        admin_error_list.append("Failed to create admin via endpoint")
    session.close()
else:
    log("ERROR", "Endpoint said admin was not created")
    admin_error_list.append("Endpoint says admin was not created")
sleep(1.5)

# Non-admin user testing

try:
    pdf_url = api_create_user(url, token, False)
    user_id = pdf_url.split("?user=")[1]
    log("INFO", f"Created user {user_id}")
    session = Session(engine)
    log("INFO", "Checking if user is in database... ")
    sleep(1.5)
    if check_user_exists(session, user_id, False):
        log("INFO", "User is in database, proceeding to delete")
        session.close()
        session = Session(engine)
        sleep(1.5)
        if api_delete_user(url, token, False, user_id):
            log("INFO", "Endpoint said user was deleted")
            session.close()
            session = Session(engine)
            sleep(1.5)
            if not check_user_exists(session, user_id, False):
                log("INFO", "User is no longer in database")
            else:
                log("ERROR", "User is still in database")
                delete_testing_user(session, user_id, False)
                admin_error_list.append("Failed to delete non-admin user via endpoint")
        else:
            log("ERROR", "Endpoint said user was not deleted")
            admin_error_list.append("Endpoint says user was not deleted")
    else:
        log("ERROR", "User is not in database")
        admin_error_list.append("Failed to create non-admin user via endpoint")
    session.close()
except Exception as e:
    log("ERROR", f"Failed to create non-admin user: {e}")
    admin_error_list.append("Failed to create non-admin user")
sleep(1.5)
log("INFO", "Testing finished")
if len(admin_error_list) == 0:
    log("INFO", "0/7 tests failed, /managment endpoint and admin related operations are fully operational")
elif len(admin_error_list) <= 3:
    log("ERROR", f"{len(admin_error_list)}/7 tests failed, admin related operations are partially operational")
else:
    log("CRITICAL", f"{len(admin_error_list)}/7 tests failed, admin related operations are not operational")
log("INFO", "Admin related operations shouldn't interfere with the rest of the system")
sleep(5)

log("INFO", "---- Testing voting related operations ----")

log("WARNING", "Make sure that voting is NOT running on the system before proceeding with the tests")
log("WARNING", "No other users should be voting while these tests are running")

voting_error_list = []
voting_time = 10
film_name = "IWannaBeYours"
log("INFO", f"Setting voting time to {voting_time} seconds")
time = api_change_settings(url, token, voting_time)
if time == False:
    log("ERROR", "Failed to change voting time, cannot proceed with voting tests")
    exit()
sleep(1.5)
log("INFO", f"Creating film {film_name}... ")
if api_create_film(url, token, film_name, "Arctic Monkeys"):
    log("INFO", "Film created")
    sleep(1.5)
    log("INFO", "Creating voting user and getting voting token... ")
    user_url = api_create_user(url, token, False)
    log("INFO", "User created")
    user = user_url.split("?user=")[1]
    log("INFO", f"Getting voting token for user {user}... ")
    pdf_url = url + "/pdf?user=" + user
    user_token = api_get_voting_token(token, pdf_url)
    if user_token is None:
        log("ERROR", "Failed to get voting token")
        exit()
    sleep(1.5)
    log("INFO", "Voting token received")
    sleep(1.5)
    log("INFO", "Starting voting and sending vote... ")
    vote_duration = api_start_voting(url, token)
    if vote_duration is None:
        log("ERROR", "Failed to start voting")
        exit()
    vote = api_vote(url, user_token, film_name)
    if vote is False:
        log("ERROR", "Failed to vote")
        exit()
    log("INFO", "Vote sent waiting for voting to end... ")
    sleep(vote_duration)
    log("INFO", "Voting ended, getting results... ")
    results = api_check_vote_results(url, token, film_name)
    if results is None:
        log("ERROR", "Something went wrong while getting results")
        log("INFO", "Checking if vote was registered... ")
        user_check = check_user_vote(Session(engine), user, film_name)
        if user_check:
            log("INFO", "Vote was registered")
            log("INFO", "Checking if final vote was registered... ")
            film_check = check_film_vote(Session(engine), film_name)
            if film_check:
                log("INFO", "Final vote was registered, there might be a problem with checkers results")
                voting_error_list.append("Final vote was registered, there might be a problem with checkers results")
            else:
                log("ERROR", "Final vote was not registered")
                voting_error_list.append("Final vote was not registered")
        else:
            log("ERROR", "Vote was not registered")
            voting_error_list.append("Failed to register vote")
    log("INFO", "Reseting voting... ")
    reset = api_reset_voting(url, token)
    if reset is False:
        log("ERROR", "Failed to reset voting")
        exit()

log("INFO", "Resetting voting time... ")  
time = api_change_settings(url, token, original_voting_time)
if time == False:
    log("ERROR", "Failed to reset voting time")
    exit()      

log("INFO", "Removing film and user... ")
session = Session(engine)
delete_film(session, film_name)
delete_testing_user(session, user, False)
session.close()
log("INFO", "Finished voting tests")
sleep(5)

# Clears the screen
print("\033c")
log("INFO", "---- Checker results ----")
if len(admin_error_list) == 0 and len(voting_error_list) == 0:
    log("INFO", "All tests were successfully passed, system is fully operational!")
else:
    if len(admin_error_list) > 0:
        log("ERROR", f"Admin related operations failed {len(admin_error_list)}/7 tests, system might not be fully operational")
        log("ERROR", "These tests failed: ")
        for error in admin_error_list:
            log("ERROR", f"    - {error}")
    else:
        log("INFO", "Admin related operations passed all tests")
    if len(voting_error_list) > 0:
        log("ERROR", f"Voting related operations failed {len(voting_error_list)}/6 tests -> SYSTEM IS DEFINITELY NOT OPERATIONAL")
        log("ERROR", "These tests failed: ")
        for error in voting_error_list:
            log("ERROR", f"    - {error}")
    else:
        log("INFO", "Voting related operations passed all tests")
log("INFO", "Exiting Apalucha checker... ")
exit()