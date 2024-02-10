from flask import *
from flask_cors import CORS
from user_agents import parse
import datetime
import sys
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

database = config["database"]
jwt_settings = config["jwt"]
pdfs_settings = config["pdfs"]
voting = config["voting"]

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
    return jsonify({"token": token})


# REMOVES THIS ROUTES IN PRODUCTION
@app.route('/testing', methods=['GET'])
def testing():
    token = generate_jwt(jwt_settings["secret"], jwt_settings["expiration"], jwt_settings["issuer"], jwt_settings["algorithm"], "3")
    return jsonify({"token": token})
@app.route('/atesting', methods=['GET'])
def atesting():
    token = generate_jwt(jwt_settings["secret"], jwt_settings["expiration"], jwt_settings["issuer"], jwt_settings["algorithm"], "admin", True)
    return jsonify({"token": token})

@app.route('/voting', methods=['POST', 'GET'])
def vote():
    token = request.cookies.get("token")
    if token == None:
        pass
        return jsonify({"error": "401"}), 401
    user, isAdmin = decode_jwt(jwt_settings["secret"], token, jwt_settings["algorithm"], jwt_settings["issuer"])
    if user == None:
        return jsonify({"error": "401"}), 401
    
    if request.method == 'GET':
        if voting['voteInProgress'] == False:
            return jsonify({"error": "425"}), 425
        # Returns json with all films
        session = sessionmaker(bind=engine)()
        films = unsorted_films(session)
        session.close()
        if films == False:
            return jsonify({"error": "500"}), 500
        return jsonify(films)
    elif request.method == 'POST':
        if isAdmin:
            return jsonify({"error": "403"}), 403
        if voting['voteInProgress'] == False:
            return jsonify({"error": "425"}), 425
        # User sends a vote -> {"vote": 1}
        data = request.get_json()
        vote = data["vote"]
        session = sessionmaker(bind=engine)()
        response = vote_film(vote, user, session)
        session.close()
        if response == False:
            return jsonify({"error": "500"}), 500
        return jsonify({"message": "200"}), 200

@app.route('/scoreboard', methods=['POST'])
def scoreboard():
    token = request.cookies.get("token")
    if token == None:
        return jsonify({"error": "401"}), 401
    user, isAdmin = decode_jwt(jwt_settings["secret"], token, jwt_settings["algorithm"], jwt_settings["issuer"])
    if user == None:
        return jsonify({"error": "401"}), 401
    if isAdmin == False:
        return jsonify({"error": "403"}), 403
    
    # if voteEnd is null, start voting and returns unsorted films
    # if voteEnd is not null, and voteEnd is in future, returns unsorted films + remaining time
    # if voteEnd is not null, and voteEnd is in past, returns sorted films

    session = sessionmaker(bind=engine)()

    if voting['voteEnd'] == None:
        voting['voteInProgress'] = True
        end = datetime.datetime.now() + datetime.timedelta(seconds=voting["voteDuration"])
        voting['voteEnd'] = end
        films = unsorted_films(session)
        session.close()
        if films == False:
            return jsonify({"error": "500"}), 500
        return jsonify({"voteEnd": end, "voteDuration": voting["voteDuration"], "films": films})
    elif voting['voteEnd'] > datetime.datetime.now():
        films = unsorted_films(session)
        session.close()
        remaining = voting['voteEnd'] - datetime.datetime.now()
        remaining = remaining.total_seconds()
        if films == False:
            return jsonify({"error": "500"}), 500
        return jsonify({"voteEnd": voting['voteEnd'], "voteDuration": remaining, "films": films})
    else:
        films = sorted_films(session)
        session.close()
        if films == False:
            return jsonify({"error": "500"}), 500
        return jsonify({"voteEnd": False, "films": films})

@app.route('/pdf', methods=['GET'])
def pdf():
    requestedPdf = request.args.get('user', default=None, type=str)
    if requestedPdf == None:
        return jsonify({"error": "400"}), 400
    token = request.cookies.get("token")
    if token == None:
        return jsonify({"error": "401"}), 401
    user, isAdmin = decode_jwt(jwt_settings["secret"], token, jwt_settings["algorithm"], jwt_settings["issuer"])
    if user == None:
        return jsonify({"error": "401"}), 401
    if isAdmin == False:
        return jsonify({"error": "403"}), 403
    # Returns pdf
    pdfPath = pdfs_settings["path"] + requestedPdf + ".pdf"
    try:
        with open(pdfPath, 'rb') as f:
            return send_file(pdfPath)
    except FileNotFoundError or IsADirectoryError:
        return jsonify({"error": "404"}), 404
    except Exception as e:
        print(f"An error ocurred while trying to open the file {pdfPath}: {e}")
        return jsonify({"error": "500"}), 500

@app.route('/managment', methods=['POST'])
def managment():
    token = request.cookies.get("token")
    if token == None:
        return jsonify({"error": "401"}), 401
    user, isAdmin = decode_jwt(jwt_settings["secret"], token, jwt_settings["algorithm"], jwt_settings["issuer"])
    if user == None:
        return jsonify({"error": "401"}), 401
    if isAdmin == False:
        return jsonify({"error": "403"}), 403
    request_data = request.get_json()
    if request_data == None:
        return jsonify({"error": "400"}), 400
    action = request_data["action"]
    action_data = request_data["data"]
    if action == "reset":
        session = sessionmaker(bind=engine)()
        film = film_reset(session)
        user = user_reset(session)
        session.close()
        if film == False or user == False:
            return jsonify({"error": "500"}), 500
        return jsonify({"message": "200"}), 200
    if action == "remove_film":
        film_id = action_data["film_id"]
        session = sessionmaker(bind=engine)()
        film = remove_film(session, film_id)
        session.close()
        if film == False:
            return jsonify({"error": "500"}), 500
        return jsonify({"message": "200"}), 200
    if action == "add_film":
        tilte = action_data["title"]
        team = action_data["team"]
        session = sessionmaker(bind=engine)()
        film = add_film(session, tilte, team)
        session.close()
        if film == False:
            return jsonify({"error": "500"}), 500
        return jsonify({"message": "200"}), 200
    if action == "remove_user":
        user_id = action_data["user_id"]
        isAdmin = action_data["isAdmin"]
        session = sessionmaker(bind=engine)()
        user = remove_user(session, user_id, isAdmin)
        session.close()
        if user == False:
            return jsonify({"error": "500"}), 500
        return jsonify({"message": "200"}), 200
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
            message = {"message": "200", "pdfUrl": pdfUrl}
        else:
            if username == None or password == None:
                return jsonify({"error": "400"}), 400
            user = add_user(session, isAdmin, username, password)
            message = {"message": "200"}
        session.close()
        if user == False:
            return jsonify({"error": "500"}), 500
        return jsonify(message), 200