"""
This site was created by Kaktus1549 from KaktusGame.eu

    ,*-.       /$$   /$$           /$$         /$$                          /$$$$$$                                         ,*-.  
    |* |      | $$  /$$/          | $$        | $$                         /$$__  $$                                        | *|
,.  | *|      | $$ /$$/   /$$$$$$ | $$   /$$ /$$$$$$   /$$   /$$  /$$$$$$$| $$  \__/  /$$$$$$  /$$$$$$/$$$$   /$$$$$$   ,.  |* |
|*|_|* | ,.   | $$$$$/   |____  $$| $$  /$$/|_  $$_/  | $$  | $$ /$$_____/| $$ /$$$$ |____  $$| $$_  $$_  $$ /$$__  $$  |*|_| *| ,.
`---.* |_|*|  | $$  $$    /$$$$$$$| $$$$$$/   | $$    | $$  | $$|  $$$$$$ | $$|_  $$  /$$$$$$$| $$ \ $$ \ $$| $$$$$$$$  `---. *|_|*|
    | *.--`   | $$\  $$  /$$__  $$| $$_  $$   | $$ /$$| $$  | $$ \____  $$| $$  \ $$ /$$__  $$| $$ | $$ | $$| $$_____/      |* .--`
    | *|      | $$ \  $$|  $$$$$$$| $$ \  $$  |  $$$$/|  $$$$$$/ /$$$$$$$/|  $$$$$$/|  $$$$$$$| $$ | $$ | $$|  $$$$$$$      | *|
    | *|      |__/  \__/ \_______/|__/  \__/   \___/   \______/ |_______/  \______/  \_______/|__/ |__/ |__/ \_______/      |* |

                                                                                                               Powered by Kaktus1549

Some cool ascii art :D
"""
import json
from sys import path

from os import getenv
apalucha = getenv("apalucha")
if apalucha is None:
    apalucha = "."
path.append(apalucha)


# Default values
apalucha_ascii_art = """
    ___                __           __             ___   ____ ___  __ __
   /   |  ____  ____ _/ /_  _______/ /_  ____ _   |__ \ / __ \__ \/ // /
  / /| | / __ \/ __ `/ / / / / ___/ __ \/ __ `/   __/ // / / /_/ / // /_
 / ___ |/ /_/ / /_/ / / /_/ / /__/ / / / /_/ /   / __// /_/ / __/__  __/
/_/  |_/ .___/\__,_/_/\__,_/\___/_/ /_/\__,_/   /____/\____/____/ /_/   
      /_/               
"""

try:
    with open("./config.json", 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    with open("./config.json", "w") as f:
        json.dump({"setuped": False}, f, indent=4)
        config = {"setuped": False}

from auth.tokens import generate_secret

# Checks if config is set up
if config['setuped'] == False:
    print("It seems like the config is not set up yet.")
    print("Setting up the config from environment variables...")

    # Database
    db_address = getenv("DB_ADDRESS", "127.0.0.1")
    db_port = int(getenv("DB_PORT", 3306))
    username = getenv("DB_USERNAME", "root")
    password = getenv("DB_PASSWORD", "root")
    name = getenv("DB_NAME", "apalucha")
    poolSize = int(getenv("DB_POOLSIZE", 20))
    adminTable = getenv("DB_TABLE_ADMIN", "Admins")
    userTable = getenv("DB_TABLE_USER", "Users")
    filmsTable = getenv("DB_TABLE_FILMS", "Films")

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
    debug = bool(getenv("DEBUG", False))

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
            "debug": debug
        }
    }
    with open("./config.json", "w") as f:
        json.dump(config, f, indent=4)

    print("Config saved! You can now run the website.")
    print("If you want to change the configuration, please edit the config.json file.")
    print("Gettings things ready...")
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
    app.run(host=config["flask"]["address"], port=config["flask"]["port"], debug=config["flask"]["debug"])