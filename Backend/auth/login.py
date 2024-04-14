import bcrypt
from sqlalchemy import *
from sqlalchemy.orm import *
from sys import path
from os import getenv
apalucha = getenv("apalucha")
if apalucha is None:
    apalucha = "."
path.append(apalucha)

from sql.sql_init import Admin
from auth.tokens import generate_jwt
from sql.sql_config import make_engine
from backend_logging.apalucha_logging import log

def create_admin(username, password, session):
    try:
        log("INFO", f"Creating admin \"{username}\"")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_admin = Admin(Username=username, PasswordHash=hashed_password)
        session.add(new_admin)
        session.commit()
        log("INFO", f"Admin \"{username}\" created")
        return True
    except Exception as e:
        log("ERROR", f"Failed to create admin \"{username}\": {e}")
        return False
def login_admin(username, password, session, jwt_settings, ip="-----"):
    try:
        if jwt_settings == None:
            log("ERROR", "jwt_settings must be provided")
            return False
        admin = session.query(Admin).filter_by(Username=username).first()
        if admin == None:
            log("ERROR", f"Failed attempt to login as admin \"{username}\" from IP address {ip}")
            return False
        if bcrypt.checkpw(password.encode('utf-8'), admin.PasswordHash.encode('utf-8')):
            token = generate_jwt(jwt_settings["secret"], jwt_settings["expiration"], jwt_settings["issuer"], jwt_settings["algorithm"], username, isAdmin=True)
            if token == None:
                log("ERROR", f"Failed to generate token for admin \"{username}\" from IP address {ip}")
                return False
            log("INFO", f"Admin \"{username}\" logged in from IP address {ip}")
            return token
        log("ERROR", f"Failed attempt to login as admin \"{username}\" from IP address {ip}")
        return False
    except Exception as e:
        log("ERROR", f"Got exception while logging in as admin \"{username}\" from IP address {ip}: {e}")
        return "500"