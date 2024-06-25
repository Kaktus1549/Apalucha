from flask import *
from flask_cors import CORS
from user_agents import parse
import datetime
import sys
from signal import SIGTERM
from time import sleep
from subprocess import Popen
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import json
from sqlalchemy import *
from sqlalchemy.orm import *
from dotenv import load_dotenv
from os import getenv, environ
sys.path.append('.')
load_dotenv()

# SQL
from sql.sql_init import *

# Auth
from auth.login import *
from auth.tokens import *

# Voting
from voting.voting import *
from voting.film_ranking import *

# Managment
from managment.film_mng import *
from managment.user_mng import *

# Logging
from backend_logging.apalucha_logging import log

# Functions 
def make_engine(database):
    username = database["username"]
    password = database["password"]
    port = database["port"]
    address = database["address"]
    name = database["name"]
    poolSize = database["poolSize"]

    url = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(username, password, address, port, name)

    engine = create_engine(url, pool_size=int(poolSize), max_overflow=0)
    return engine
def restart_program():
    sleep(1)
    # Start a new instance of the Flask application
    Popen([sys.executable, __file__])

    # Exit the current process
    sys.exit(0)


# Configs
config_file = "./config.json"
with open(config_file) as f:
    config = json.load(f)

# Scheduler
scheduler = BackgroundScheduler()
scheduler.start()

database = config["database"]
jwt_settings = config["jwt"]
pdfs_settings = config["pdfs"]
ballotbox_time = "10"
next_ballotbox_vote = None

def end_voting():
    global config

    session = sessionmaker(bind=engine)()
    status = count_votes(session)
    session.close()
    if status == False:
        return

    config["voting"]['voteInProgress'] = False
    config["voting"]['voteEnd'] = False

    # save config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

if config["voting"]['voteEnd'] != None and config["voting"]['voteEnd'] != False:
    # If voteEnd is in the past, end voting
    # Else, schedule the end of voting
    vote_end = datetime.datetime.strptime(config["voting"]['voteEnd'].split('.')[0], "%Y-%m-%d %H:%M:%S")
    if vote_end < datetime.datetime.now():
        end_voting()
    else:
        log("INFO", f"Scheduling end of voting for {vote_end}")
        scheduler.add_job(end_voting, 'date', run_date=vote_end)


# Engine
engine = make_engine(database)

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        token = None
        try:
            username = data['username']
            password = data['password']
        except KeyError:
            try:
                token = data['token']
            except KeyError:
                return jsonify({"error": "Missing username or password"}), 400
        if token != None:
            # Returns token as Set-Cookie
            return jsonify({"message": "OK"}), 200, {'Set-Cookie': f"token={token}; SameSite=Strict; Secure; HttpOnly; Path=/"}
        session = sessionmaker(bind=engine)()
        ip = request.headers.get('X-REAL-IP', request.remote_addr)
        token = login_admin(username, password, session, jwt_settings, ip)
        session.close()
        if token == "500":
            return jsonify({"error": "Internal server error"}), 500
        if token == False:
            return jsonify({"error": "Invalid username or password"}), 401
        return jsonify({"message": "OK"}), 200, {'Set-Cookie': f"token={token}; SameSite=Strict; Secure; HttpOnly; Path=/"}
    elif request.method == 'GET':
        token = request.cookies.get("token")
        if token == None:
            return jsonify({"error": "Token not found"}), 401
        session = sessionmaker(bind=engine)()
        user, isAdmin = decode_jwt(jwt_settings["secret"], token, session, jwt_settings["algorithm"], jwt_settings["issuer"], ip=request.headers.get('X-REAL-IP', request.remote_addr))
        session.close()
        if user == None:
            return jsonify({"error": "Failed to authenticate"}), 401
        return jsonify({"message": "OK"}), 200

@app.route('/voting', methods=['POST', 'GET'])
def vote():
    token = request.cookies.get("token")
    if token == None:
        return jsonify({"error": "Token not found"}), 401
    session = sessionmaker(bind=engine)()
    user, isAdmin = decode_jwt(jwt_settings["secret"], token, session, jwt_settings["algorithm"], jwt_settings["issuer"], ip=request.headers.get('X-REAL-IP', request.remote_addr))
    session.close()
    if user == "500":
        return jsonify({"error": "Internal server error"}), 500
    if user == None:
        return jsonify({"error": "Failed to authenticate"}), 401
    if isAdmin:
        return jsonify({"error": "Admins can't vote"}), 403
    
    if request.method == 'GET':
        if config["voting"]['voteInProgress'] == False:
            return jsonify({"error": "Voting has not started"}), 425
        # Returns json with all films
        session = sessionmaker(bind=engine)()
        films = unsorted_films(session)
        session.close()
        if films == False:
            return jsonify({"error": "Could not retrieve films"}), 500
        return jsonify(films), 200
    elif request.method == 'POST':
        if config["voting"]['voteInProgress'] == False:
            return jsonify({"error": "Voting has not started"}), 425
        # User sends a vote -> {"vote": 1}
        data = request.get_json()
        if data == None:
            return jsonify({"error": "Missing data"}), 400
        vote = data["vote"]
        session = sessionmaker(bind=engine)()
        # Tryes to get address from header X-REAL-IP, if not, gets it from request.remote_addr
        ip = request.headers.get('X-REAL-IP', request.remote_addr)
        response = vote_film(vote, user, session, ip)
        session.close()
        if response == False:
            return jsonify({"error": "Failed to vote"}), 500
        return jsonify({"message": "OK"}), 200

@app.route('/scoreboard', methods=['POST', 'GET'])
def scoreboard(): 
    if request.method == 'POST':
        token = request.cookies.get("token")
        if token == None:
            return jsonify({"error": "Token not found"}), 401
        session = sessionmaker(bind=engine)()
        user, isAdmin = decode_jwt(jwt_settings["secret"], token, session, jwt_settings["algorithm"], jwt_settings["issuer"], ip=request.headers.get('X-REAL-IP', request.remote_addr))
        session.close()
        if user == "500":
            return jsonify({"error": "Internal server error"}), 500
        if user == None:
            return jsonify({"error": "Failed to authenticate"}), 401
        if isAdmin == False:
            return jsonify({"error": "Access denied"}), 403 
        
        # if voteEnd is null, start voting and returns unsorted films
        # if voteEnd is not null, and voteEnd is in future, returns unsorted films + remaining time
        # if voteEnd is not null, and voteEnd is in past, returns sorted films

        session = sessionmaker(bind=engine)()
        voteEnd = config["voting"]['voteEnd']

        if voteEnd == None:
            log("INFO", f"Admin \"{user}\" from IP address {request.headers.get('X-REAL-IP', request.remote_addr)} started voting")
            config["voting"]['voteInProgress'] = True
            end = datetime.datetime.now() + datetime.timedelta(seconds=config["voting"]["voteDuration"])
            config["voting"]['voteEnd'] = str(end)
            log("INFO", f"Scheduling end of voting for {end}")
            films = unsorted_films(session)
            session.close()
            # save config
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            # schedule end of voting
            scheduler.add_job(end_voting, 'date', run_date=end)
            log("INFO", "Voting has started")
            if films == False:
                return jsonify({"error": "Failed to retrieve films"}), 500
            return jsonify({"voteEnd": end, "voteDuration": config["voting"]["voteDuration"], "films": films}), 200
        elif voteEnd != False and datetime.datetime.strptime(voteEnd.split('.')[0], "%Y-%m-%d %H:%M:%S") > datetime.datetime.now():
            films = unsorted_films(session)
            session.close()
            remaining = datetime.datetime.strptime(config["voting"]['voteEnd'].split('.')[0], "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()
            remaining = remaining.total_seconds()
            if films == False:
                return jsonify({"error": "Failed to retrieve films"}), 500
            return jsonify({"voteEnd": config["voting"]['voteEnd'], "voteDuration": remaining, "films": films}), 200
        else:
            log("INFO", "Voting has ended, sorting films")
            films, votes = sorted_films(session)
            session.close()
            if films == False:
                return jsonify({"error": "Failed to retrieve films"}), 500
            return jsonify({"voteEnd": False, "films": films, "votes": votes}), 200
    elif request.method == 'GET':
        # Check if user is allowed to see the scoreboard
        token = request.cookies.get("token")
        if token == None:
            return jsonify({"error": "Token not found"}), 401
        session = sessionmaker(bind=engine)()
        user, isAdmin = decode_jwt(jwt_settings["secret"], token, session, jwt_settings["algorithm"], jwt_settings["issuer"], ip=request.headers.get('X-REAL-IP', request.remote_addr))
        session.close()
        if user == "500":
            return jsonify({"error": "Internal server error"}), 500
        if user == None:
            return jsonify({"error": "Failed to authenticate"}), 401
        if isAdmin == False:
            return jsonify({"error": "Access denied"}), 403
        # Else, returns OK
        return jsonify({"message": "OK"}), 200

@app.route('/pdf', methods=['GET'])
def pdf():
    requestedPdf = request.args.get('user', default=None, type=str)
    if requestedPdf == None:
        return jsonify({"error": "Missing pdf parameter"}), 400
    token = request.cookies.get("token")
    if token == None:
        return redirect("/login?origin=/pdf?user=" + requestedPdf)
    session = sessionmaker(bind=engine)()
    user, isAdmin = decode_jwt(jwt_settings["secret"], token, session, jwt_settings["algorithm"], jwt_settings["issuer"], ip=request.headers.get('X-REAL-IP', request.remote_addr))
    session.close()
    if user == "500":
        return redirect("/error/500")
    if user == None:
        return redirect("/login?origin=/pdf?user=" + requestedPdf)
    if isAdmin == False:
        return redirect("/error/403")
    # Returns pdf
    pdfPath = pdfs_settings["path"] + requestedPdf + ".pdf"
    try:
        with open(pdfPath, 'rb') as f:
            return send_file(pdfPath), 200
    except FileNotFoundError or IsADirectoryError:
        return redirect("/error/404")
    except Exception as e:
        log("ERROR", f"An error ocurred while trying to open the file {pdfPath}: {e}")
        return redirect("/error/500")

@app.route('/managment', methods=['POST'])
def managment():
    token = request.cookies.get("token")
    if token == None:
        return jsonify({"error": "Token not found"}), 401
    session = sessionmaker(bind=engine)()
    user, isAdmin = decode_jwt(jwt_settings["secret"], token, session, jwt_settings["algorithm"], jwt_settings["issuer"], ip=request.headers.get('X-REAL-IP', request.remote_addr))
    session.close()
    if user == "500":
        return jsonify({"error": "Internal server error"}), 500
    if user == None:
        return jsonify({"error": "Failed to authenticate"}), 401
    if isAdmin == False:
        return jsonify({"error": "Access denied"}), 403
    request_data = request.get_json()
    if request_data == None:
        return jsonify({"error": "The request does not contain a JSON body"}), 400

    try:
        action = request_data["action"]
        action_data = request_data["data"]
    except KeyError:
        return jsonify({"error": "Missing action or data"}), 400
    ip = request.headers.get('X-REAL-IP', request.remote_addr)
    if action == "reset":
        config["voting"]['voteInProgress'] = False
        config["voting"]['voteEnd'] = None
        if action_data["reset_secret"] == True:
            config["jwt"]["secret"] = generate_secret()
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            session = sessionmaker(bind=engine)()
            status = user_reset(session, deletion=True, admin=user, ip=ip)
            session.close()
            if status == False:
                return jsonify({"error": "Failed to reset users"}), 500
        else:
            session = sessionmaker(bind=engine)()
            user_status = user_reset(session, deletion=False, admin=user, ip=ip)
            session.close()
            if user_status == False:
                return jsonify({"error": "Failed to reset users"}), 500
        if action_data["full_reset"] == True:
            session = sessionmaker(bind=engine)()
            status = film_reset(session, deletion=True, admin=user, ip=ip)
            session.close()
            if status == False:
                return jsonify({"error": "Failed to reset films"}), 500
        else:
            session = sessionmaker(bind=engine)()
            film_status = film_reset(session, deletion=False, admin=user, ip=ip)
            session.close()
            if film_status == False:
                return jsonify({"error": "Failed to reset films"}), 500
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        return jsonify({"message": "OK"}), 200
    if action == "remove_film":
        film_id = action_data["film_id"]
        session = sessionmaker(bind=engine)()
        film = remove_film(session, film_id, admin=user, ip=ip)
        session.close()
        if film == False:
            return jsonify({"error": "Failed to remove film"}), 500
        return jsonify({"message": "OK"}), 200
    if action == "add_film":
        tilte = action_data["title"]
        team = action_data["team"]
        session = sessionmaker(bind=engine)()
        film = add_film(session, tilte, team, admin=user, ip=ip)
        session.close()
        if film == False:
            return jsonify({"error": "Failed to add film"}), 500
        return jsonify({"message": "OK"}), 200
    if action == "remove_user":
        user_id = action_data["user_id"]
        isAdmin = action_data["isAdmin"]
        session = sessionmaker(bind=engine)()
        user_removal = remove_user(session, user_id, isAdmin, admin=user, ip=ip)
        session.close()
        if user_removal == False:
            return jsonify({"error": "Failed to remove user"}), 500
        return jsonify({"message": "OK"}), 200
    if action == "add_user":
        isAdmin = action_data["isAdmin"]
        try:
            username = action_data["username"]
            password = action_data["password"]
        except KeyError:
            username = None
            password = None
        session = sessionmaker(bind=engine)()
        if isAdmin == False:
            user = add_user(session, isAdmin, username, password, pdfs_settings, jwt_settings, admin=user, ip=ip)
            session.close()
            pdfUrl = pdfs_settings['pdfUrl'] + f"?user={user}"
            message = {"message": "OK", "pdfUrl": pdfUrl}
        else:
            if username == None or password == None:
                return jsonify({"error": "Missing username or password"}), 400
            user = add_user(session, isAdmin, username, password, admin=user, ip=ip)
            session.close()
            message = {"message": "OK"}
        if user == False:
            return jsonify({"error": "Failed to add user"}), 500
        return jsonify(message), 200
    if action == "change_settings":
        changed_anything = False
        for key, value in action_data.items():
            if key == "voteDuration":
                changed_anything = True
                log("INFO", f"Admin \"{user}\" from IP address {ip} changed vote duration from {config['voting']['voteDuration']} to {value}")
                config["voting"]["voteDuration"] = value
            if key == "poolSize":
                log("INFO", f"Admin \"{user}\" from IP address {ip} changed pool size from {config['database']['poolSize']} to {value}")
                config["database"]["poolSize"] = value
                changed_anything = True
            if key == "expiration":
                log("INFO", f"Admin \"{user}\" from IP address {ip} changed expiration from {config['jwt']['expiration']} to {value}")
                config["jwt"]["expiration"] = value
                changed_anything = True
            if key == "debug":
                log("INFO", f"Admin \"{user}\" from IP address {ip} changed debug from {config['flask']['debug']} to {value}")
                config["flask"]["debug"] = value
                changed_anything = True
        if changed_anything == False:
            return jsonify({"error": "No settings changed"}), 400
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        log("INFO", "Settings successfully changed")
        log("INFO", "Restarting program")
        thread = threading.Thread(target=restart_program)
        thread.start()
        return jsonify({"message": "OK"}), 200
    if action == "webhooks":
        webhooks_data = action_data
        changed_anything = False
        if webhooks_data == None:
            return jsonify({"error": "Missing data"}), 400
        if webhooks_data["webhook_logging"] != None:
            # DISCORD_WEBHOOK_URL => url
            # WEBHOOK_LOGGER => enabled/disabled
            # All stored in environment variables
            logger = getenv("WEBHOOK_LOGGER")
            if logger != str(webhooks_data["webhook_logging"]):
                log("INFO", f"Admin \"{user}\" from IP address {ip} changed webhook logging from \"{logger}\" to \"{webhooks_data['webhook_logging']}\"")
                environ["WEBHOOK_LOGGER"] = str(webhooks_data["webhook_logging"])
                changed_anything = True
        if webhooks_data["url"] != None:
            url = getenv("DISCORD_WEBHOOK_URL")
            if url != str(webhooks_data["url"]):
                log("INFO", f"Admin \"{user}\" from IP address {ip} changed webhook url from \"{url}\" to \"{webhooks_data['url']}\"")
                environ["DISCORD_WEBHOOK_URL"] = str(webhooks_data["url"])
                changed_anything = True

        if changed_anything == False:
            return jsonify({"error": "No settings changed"}), 400
        log("INFO", "Settings successfully changed")
        log("WARNING", "Restarting program")
        thread = threading.Thread(target=restart_program)
        thread.start()
        return jsonify({"message": "OK"}), 200
    if action == "ballotbox":
        # returns token for ballotbox
        token = generate_ballotbox_jwt(jwt_settings["secret"], jwt_settings["expiration"], jwt_settings["issuer"], jwt_settings["algorithm"])
        if token == None:
            return jsonify({"error": "Failed to generate token"}), 500
        return jsonify({"message": "OK"}), 200, {'Set-Cookie': f"ballottoken={token}; SameSite=Strict; Secure; HttpOnly; Path=/"}
    return jsonify({"error": "Invalid action"}), 400

@app.route('/ballotbox', methods=['GET','POST'])
def ballotbox():
    global next_ballotbox_vote
    
    token = request.cookies.get("ballottoken")
    if token == None:
        return jsonify({"error": "Token not found"}), 401
    session = sessionmaker(bind=engine)()
    ip_addr = request.headers.get('X-REAL-IP', request.remote_addr)
    is_valid = decode_ballotbox_jwt(jwt_settings["secret"], token, jwt_settings["algorithm"], jwt_settings["issuer"], ip_addr)
    session.close()
    if is_valid == None:
        return jsonify({"error": "Failed to authenticate"}), 401
    
    if config["voting"]['voteInProgress'] == False:
        return jsonify({"error": "Voting has not started"}), 425
    
    if next_ballotbox_vote != None:
        if next_ballotbox_vote > datetime.datetime.now():
            remaining = next_ballotbox_vote - datetime.datetime.now()
            remaining = remaining.total_seconds()
            return jsonify({"error": "You have to wait to vote again", "remaining": remaining}), 425
    
    if config["voting"]['voteInProgress'] == False:
        return jsonify({"error": "Voting has not started"}), 425
    
    if request.method == 'GET':
        session = sessionmaker(bind=engine)()
        films = unsorted_films(session)
        session.close()
        if films == False:
            return jsonify({"error": "Failed to retrieve films"}), 500
        return jsonify(films), 200
    elif request.method == 'POST':
        data = request.get_json()
        if data == None:
            return jsonify({"error": "Missing data"}), 400
        vote = data["vote"]
        session = sessionmaker(bind=engine)()
        ip = request.headers.get('X-REAL-IP', request.remote_addr)
        response = ballotbox_vote(vote, session, ip)
        session.close()
        if response == False:
            return jsonify({"error": "Failed to vote"}), 500
        next_ballotbox_vote = datetime.datetime.now() + datetime.timedelta(seconds=int(ballotbox_time))
        return jsonify({"message": "OK", "remaining": ballotbox_time}), 200