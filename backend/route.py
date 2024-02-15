from flask import *
from flask_cors import CORS
from user_agents import parse
import datetime
import sys
from apscheduler.schedulers.background import BackgroundScheduler
import json
from sqlalchemy import *
from sqlalchemy.orm import *
sys.path.append('.')

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

def end_voting():
    global config

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
        scheduler.add_job(end_voting, 'date', run_date=vote_end)


# Engine
engine = make_engine(database)

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    session = sessionmaker(bind=engine)()
    token = login_admin(username, password, session, jwt_settings)
    session.close()
    if token == False:
        return jsonify({"error": "Invalid username or password"}), 401
    return jsonify({"token": token}), 200

@app.route('/voting', methods=['POST', 'GET'])
def vote():
    token = request.cookies.get("token")
    if token == None:
        pass
        return jsonify({"error": "Token not found"}), 401
    session = sessionmaker(bind=engine)()
    user, isAdmin = decode_jwt(jwt_settings["secret"], token, session, jwt_settings["algorithm"], jwt_settings["issuer"])
    if user == None:
        return jsonify({"error": "Failed to authenticate"}), 401
    
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
        if isAdmin:
            return jsonify({"error": "Admins can't vote"}), 403
        if config["voting"]['voteInProgress'] == False:
            return jsonify({"error": "Voting has not started"}), 425
        # User sends a vote -> {"vote": 1}
        data = request.get_json()
        vote = data["vote"]
        session = sessionmaker(bind=engine)()
        response = vote_film(vote, user, session)
        session.close()
        if response == False:
            return jsonify({"error": "Failed to vote"}), 500
        return jsonify({"message": "OK"}), 200

@app.route('/scoreboard', methods=['POST'])
def scoreboard(): 
    token = request.cookies.get("token")
    if token == None:
        return jsonify({"error": "Token not found"}), 401
    session = sessionmaker(bind=engine)()
    user, isAdmin = decode_jwt(jwt_settings["secret"], token, session, jwt_settings["algorithm"], jwt_settings["issuer"])
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
        config["voting"]['voteInProgress'] = True
        end = datetime.datetime.now() + datetime.timedelta(seconds=config["voting"]["voteDuration"])
        config["voting"]['voteEnd'] = str(end)
        films = unsorted_films(session)
        session.close()
        # save config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        # schedule end of voting
        scheduler.add_job(end_voting, 'date', run_date=end)
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
        films, votes = sorted_films(session)
        session.close()
        if films == False:
            return jsonify({"error": "Failed to retrieve films"}), 500
        return jsonify({"voteEnd": False, "films": films, "votes": votes}), 200

@app.route('/pdf', methods=['GET'])
def pdf():
    requestedPdf = request.args.get('user', default=None, type=str)
    if requestedPdf == None:
        return jsonify({"error": "Missing pdf parameter"}), 400
    token = request.cookies.get("token")
    if token == None:
        return jsonify({"error": "Token not found"}), 401
    session = sessionmaker(bind=engine)()
    user, isAdmin = decode_jwt(jwt_settings["secret"], token, session, jwt_settings["algorithm"], jwt_settings["issuer"])
    if user == None:
        return jsonify({"error": "Failed to authenticate"}), 401
    if isAdmin == False:
        return jsonify({"error": "Access denied"}), 403
    # Returns pdf
    pdfPath = pdfs_settings["path"] + requestedPdf + ".pdf"
    try:
        with open(pdfPath, 'rb') as f:
            return send_file(pdfPath), 200
    except FileNotFoundError or IsADirectoryError:
        return jsonify({"error": "PDF not found"}), 404
    except Exception as e:
        print(f"An error ocurred while trying to open the file {pdfPath}: {e}")
        return jsonify({"error": "An error ocurred while trying to open the file"}), 500

@app.route('/managment', methods=['POST'])
def managment():
    token = request.cookies.get("token")
    if token == None:
        return jsonify({"error": "Token not found"}), 401
    user, isAdmin = decode_jwt(jwt_settings["secret"], token, session, jwt_settings["algorithm"], jwt_settings["issuer"])
    if user == None:
        return jsonify({"error": "Failed to authenticate"}), 401
    if isAdmin == False:
        return jsonify({"error": "Access denied"}), 403
    session = sessionmaker(bind=engine)()
    request_data = request.get_json()
    if request_data == None:
        return jsonify({"error": "The request does not contain a JSON body"}), 400

    action = request_data["action"]
    action_data = request_data["data"]
    if action == "reset":
        print(action_data)
        if action_data["reset_secret"] == True:
            config["jwt"]["secret"] = generate_secret()
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            status = user_reset(session, deletion=True)
            if status == False:
                return jsonify({"error": "Failed to reset users"}), 500
        else:
            user_status = user_reset(session)
            if user_status == False:
                return jsonify({"error": "Failed to reset users"}), 500
        if action_data["full_reset"] == True:
            status = film_reset(session, deletion=True)
            if status == False:
                return jsonify({"error": "Failed to reset films"}), 500
        else:
            film_status = film_reset(session)
            if film_status == False:
                return jsonify({"error": "Failed to reset films"}), 500
        session.close()
        return jsonify({"message": "OK"}), 200
    if action == "remove_film":
        film_id = action_data["film_id"]
        session = sessionmaker(bind=engine)()
        film = remove_film(session, film_id)
        session.close()
        if film == False:
            return jsonify({"error": "Failed to remove film"}), 500
        return jsonify({"message": "OK"}), 200
    if action == "add_film":
        tilte = action_data["title"]
        team = action_data["team"]
        session = sessionmaker(bind=engine)()
        film = add_film(session, tilte, team)
        session.close()
        if film == False:
            return jsonify({"error": "Failed to add film"}), 500
        return jsonify({"message": "OK"}), 200
    if action == "remove_user":
        user_id = action_data["user_id"]
        isAdmin = action_data["isAdmin"]
        session = sessionmaker(bind=engine)()
        user = remove_user(session, user_id, isAdmin)
        session.close()
        if user == False:
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
            user = add_user(session, isAdmin, username, password, pdfs_settings, jwt_settings)
            pdfUrl = pdfs_settings['pdfUrl'] + f"?user={user}"
            message = {"message": "OK", "pdfUrl": pdfUrl}
        else:
            if username == None or password == None:
                return jsonify({"error": "Missing username or password"}), 400
            user = add_user(session, isAdmin, username, password)
            message = {"message": "OK"}
        session.close()
        if user == False:
            return jsonify({"error": "Failed to add user"}), 500
        return jsonify(message), 200
    
if __name__ == '__main__':
    app.run(host=config["flask"]["address"], port=config["flask"]["port"], debug=config["flask"]["debug"])