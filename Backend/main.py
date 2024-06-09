#
# This site was created by Kaktus1549 from KaktusGame.eu
#
#     ,*-.       /$$   /$$           /$$         /$$                          /$$$$$$                                         ,*-.  
#     |* |      | $$  /$$/          | $$        | $$                         /$$__  $$                                        | *|
# ,.  | *|      | $$ /$$/   /$$$$$$ | $$   /$$ /$$$$$$   /$$   /$$  /$$$$$$$| $$  \__/  /$$$$$$  /$$$$$$/$$$$   /$$$$$$   ,.  |* |
# |*|_|* | ,.   | $$$$$/   |____  $$| $$  /$$/|_  $$_/  | $$  | $$ /$$_____/| $$ /$$$$ |____  $$| $$_  $$_  $$ /$$__  $$  |*|_| *| ,.
# `---.* |_|*|  | $$  $$    /$$$$$$$| $$$$$$/   | $$    | $$  | $$|  $$$$$$ | $$|_  $$  /$$$$$$$| $$ \ $$ \ $$| $$$$$$$$  `---. *|_|*|
#     | *.--`   | $$\  $$  /$$__  $$| $$_  $$   | $$ /$$| $$  | $$ \____  $$| $$  \ $$ /$$__  $$| $$ | $$ | $$| $$_____/      |* .--`
#     | *|      | $$ \  $$|  $$$$$$$| $$ \  $$  |  $$$$/|  $$$$$$/ /$$$$$$$/|  $$$$$$/|  $$$$$$$| $$ | $$ | $$|  $$$$$$$      | *|
#     | *|      |__/  \__/ \_______/|__/  \__/   \___/   \______/ |_______/  \______/  \_______/|__/ |__/ |__/ \_______/      |* |
#
#                                                                                                                Powered by Kaktus1549
# Some cool ascii art :D

import json
import secrets
from sqlalchemy.orm import Session
from werkzeug.serving import run_simple
import logging
import traceback
from sys import path, stdout

from os import getenv
apalucha = getenv("apalucha")
if apalucha is None:
    apalucha = "."
path.append(apalucha)

# Configure the logger for the application
from backend_logging.apalucha_logging import CustomRequestHandler, DailyFileHandler, log

console_logger = logging.getLogger('werkzeug')
console_logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(stdout)
stream_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
stream_handler.setFormatter(formatter)
console_logger.addHandler(stream_handler)

file_logger = logging.getLogger('logger')
file_logger.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(message)s')
daily_file_handler = DailyFileHandler(directory='./logs', encoding='utf-8')
daily_file_handler.setLevel(logging.DEBUG)
daily_file_handler.setFormatter(file_formatter)
file_logger.addHandler(daily_file_handler)

# Default values
apalucha_ascii_art = """
    ___                __           __             ___   ____ ___  __ __
   /   |  ____  ____ _/ /_  _______/ /_  ____ _   |__ \ / __ \__ \/ // /
  / /| | / __ \/ __ `/ / / / / ___/ __ \/ __ `/   __/ // / / /_/ / // /_
 / ___ |/ /_/ / /_/ / / /_/ / /__/ / / / /_/ /   / __// /_/ / __/__  __/
/_/  |_/ .___/\__,_/_/\__,_/\___/_/ /_/\__,_/   /____/\____/____/ /_/   
      /_/               
"""

def generate_secret(length=64):
    return secrets.token_urlsafe(length)

try:
    with open("./config.json", 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    with open("./config.json", "w") as f:
        json.dump({"setuped": False}, f, indent=4)
        config = {"setuped": False}

# Checks if config is set up
if config['setuped'] == False:
    log("INFO", "It seems like the config is not set up yet.")
    log("INFO", "Setting up the config from environment variables...")
    try:
        # Database
        db_address = getenv("DB_ADDRESS", "127.0.0.1")
        db_port = int(getenv("DB_PORT", 3306))
        username = getenv("DB_USERNAME", "root")
        password = getenv("DB_PASSWORD", "root")
        name =  "apalucha"
        poolSize = int(getenv("DB_POOLSIZE", 20))
        poolOverflow = int(getenv("DB_POOL_OVERFLOW", 20))
        poolRecycle = int(getenv("DB_POOL_RECYCLE", 3600))
        poolTimeout = int(getenv("DB_POOL_TIMEOUT", 30))
        adminTable = "Admins"
        userTable = "Users"
        filmsTable = "Films"

        # Master user
        masterUsername = getenv("MASTER_USERNAME", "admin")
        masterPassword = getenv("MASTER_PASSWORD", "klfdjlajflculakjfa099_")

        # JWT
        secret = getenv("JWT_SECRET", generate_secret())
        if secret is None or secret == "":
            secret = generate_secret()
        expiration = int(getenv("JWT_EXPIRATION", 3600))
        issuer = getenv("JWT_ISSUER", "https://apalucha.kaktusgame.eu")
        algorithm = getenv("JWT_ALGORITHM", "HS256")

        # PDFs
        loginUrl = getenv("PDF_LOGIN_URL", "https://apalucha.kaktusgame.eu/login")
        pdfUrl = getenv("PDF_URL", "https://apalucha.kaktusgame.eu/pdf")

        # Voting
        voteDuration = int(getenv("VOTE_DURATION", 180))
        
        # Flask
        web_address = getenv("WEB_ADDRESS", "0.0.0.0")
        web_port = int(getenv("WEB_PORT", 5000))
        debug = getenv("DEBUG", False)
        if debug in ["True", "true", "1"]:
            debug = True
        else:
            debug = False

        # Save to config
        config = {
            "setuped": True,
            "database": {
                "address": db_address,
                "port": db_port,
                "username": username,
                "password": password,
                "name": name,
                "poolSize": poolSize,
                "poolOverflow": poolOverflow,
                "poolRecycle": poolRecycle,
                "poolTimeout": poolTimeout,
                "tableNames": {
                    "admin": adminTable,
                    "user": userTable,
                    "films": filmsTable
                }
            },
            "jwt": {
                "secret": secret,
                "expiration": expiration,
                "issuer": issuer,
                "algorithm": algorithm
            },
            "pdfs":{
                "path": "./pdfs/",
                "template":"template.pdf",
                "loginUrl":loginUrl,
                "pdfUrl":pdfUrl
            },
            "voting":{
                "voteDuration": voteDuration,
                "voteInProgress": False,
                "voteEnd": None
            },
            "flask":{
                "address": web_address,
                "port": web_port,
                "debug": debug,
                "masterUsername": masterUsername,
                "masterPassword": masterPassword
            }
        }
        with open("./config.json", "w") as f:
            json.dump(config, f, indent=4)

        # Create master user
        from sql.sql_config import make_engine
        from auth.login import create_admin

        db_config = {
            "address": db_address,
            "port": db_port,
            "username": username,
            "password": password,
            "name": name,
            "poolSize": poolSize,
            "poolOverflow": poolOverflow,
            "poolRecycle": poolRecycle,
            "poolTimeout": poolTimeout
        }
        engine = make_engine(db_config)
        session = Session(engine)
        create_admin(masterUsername, masterPassword, session)
        session.close()
        print(f"Master user created! Username: {masterUsername}, Password: {masterPassword}")

        log("INFO", "Config saved! You can now run the website.")
        log("INFO", "If you want to change the configuration, please edit the config.json file.")
        log("INFO", "Gettings things ready...")
    except Exception as e:
        log("ERROR", f"An error occurred while setting up the config: {e}")
        log("ERROR", traceback.format_exc())
        log("ERROR", "Please check the environment variables.")
else:
    print(apalucha_ascii_art)
    print("Config already set up. If you want to change the configuration, please edit the config.json file.")
    print("Gettings things ready...")


# Run the website
from route import *

if __name__ == "__main__":
    # Clear the terminal
    print("\033c")
    print(apalucha_ascii_art)
    print(f"Master user: {config['flask']['masterUsername']}, Password: {config['flask']['masterPassword']}")
    run_simple(config["flask"]["address"], config["flask"]["port"], app, use_debugger=config["flask"]["debug"], request_handler=lambda *args: CustomRequestHandler(*args, console_logger=console_logger, file_logger=file_logger))