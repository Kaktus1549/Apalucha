import jwt
import datetime
import secrets
from sys import path
from os import getenv
from sqlalchemy import *
from sqlalchemy.orm import *
apalucha = getenv("apalucha")
if apalucha is None:
    apalucha = "."
path.append(apalucha)
from sql.sql_init import Admin, User
from backend_logging.apalucha_logging import log

def generate_secret(length=64):
    log("INFO", "Generating secret")
    return secrets.token_urlsafe(length)
def generate_jwt(secret, expiration, issuer, algorithm, userId, isAdmin=False):
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=expiration),
            "iat": datetime.datetime.utcnow(),
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
        log("INFO", f"Decoding token from {ip}")
        payload = jwt.decode(token, secret, algorithms=algorithm, issuer=issuer)
        if payload["iss"] != issuer:
            log("ERROR", f"Token from {ip} has invalid issuer")
            return None, None
        user_check = check_user(payload["sub"], payload["admin"], session)
        if user_check == False:
            log("ERROR", f"Token from {ip} has invalid user")
            return None, None
        log("INFO", f"Token from {ip} decoded successfully")
        return payload["sub"], payload["admin"]
    except jwt.ExpiredSignatureError:
        log("ERROR", f"Token from {ip} has expired")
        return None, None
    except jwt.InvalidTokenError:
        log("ERROR", f"Token from {ip} is invalid")
        return None, None