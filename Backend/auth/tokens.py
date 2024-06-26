import jwt
import datetime
import secrets
from sys import path
from os import getenv
import json
from sqlalchemy import *
from sqlalchemy.orm import *
apalucha = getenv("apalucha")
if apalucha is None:
    apalucha = "."
path.append(apalucha)
from sql.sql_init import Admin, User
from backend_logging.apalucha_logging import log
with open("config.json", "r") as f:
    config = json.load(f)
    debug = config["flask"]["debug"]

def generate_secret(length=64):
    log("INFO", "Generating secret")
    return secrets.token_urlsafe(length)
def generate_jwt(secret, expiration, issuer, algorithm, userId, isAdmin=False):
    try:
        payload = {
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=expiration),
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "iss": issuer,
            "sub": userId,
            "admin": isAdmin
        }
        token =  jwt.encode(payload, secret, algorithm=algorithm)
    except Exception as e:
        token = None
        log("ERROR", f"Got exception while generating token for user {userId}: {e}")
    return token
def check_user(user, isAdmin, session):
    if isAdmin:
        result = session.query(Admin).filter_by(Username=user).first()
        if result == None:
            return False
        return True
    else:
        result = session.query(User).filter_by(ID=user).first()
        if result == None:
            return False
        return True
def decode_jwt(secret, token, session, algorithm="HS256", issuer=None, ip="-----"):
    try:
        if debug:
            log("DEBUG", f"Decoding token from {ip}")
        payload = jwt.decode(token, secret, algorithms=algorithm, issuer=issuer)
        if payload["iss"] != issuer:
            if debug:
                log("ERROR", f"Token from {ip} has invalid issuer")
            return None, None
        user_check = check_user(payload["sub"], payload["admin"], session)
        if user_check == False:
            if debug:
                log("ERROR", f"Token from {ip} has invalid user")
            return None, None
        if debug:
            log("DEBUG", f"Token from {ip} decoded successfully")
        return payload["sub"], payload["admin"]
    except jwt.ExpiredSignatureError:
        if debug:
            log("ERROR", f"Token from {ip} has expired")
        return None, None
    except jwt.InvalidTokenError:
        if debug:
            log("ERROR", f"Token from {ip} is invalid")
        return None, None
    except Exception as e:
        log("ERROR", f"Got exception while decoding token from {ip}: {e}")
        return "500", "500"
def generate_ballotbox_jwt(secret, expiration, issuer, algorithm):
    try:
        payload = {
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=expiration),
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "iss": issuer,
            "sub": "ballotbox"
        }
        token =  jwt.encode(payload, secret, algorithm=algorithm)
    except Exception as e:
        token = None
        log("ERROR", f"Got exception while generating token for ballot-box: {e}")
    return token
def decode_ballotbox_jwt(secret, token, algorithm="HS256", issuer=None, ip="-----"):
    try:
        if debug:
            log("DEBUG", f"Decoding token from {ip}")
        payload = jwt.decode(token, secret, algorithms=algorithm, issuer=issuer)
        if payload["iss"] != issuer:
            if debug:
                log("ERROR", f"Token from {ip} has invalid issuer")
            return None
        if debug:
            log("DEBUG", f"Token from {ip} decoded successfully")
        return True
    except jwt.ExpiredSignatureError:
        if debug:
            log("ERROR", f"Token from {ip} has expired")
        return None
    except jwt.InvalidTokenError:
        if debug:
            log("ERROR", f"Token from {ip} is invalid")
        return None
    except Exception as e:
        log("ERROR", f"Got exception while decoding token from {ip}: {e}")
        return None