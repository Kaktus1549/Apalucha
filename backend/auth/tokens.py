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

def generate_secret(length=64):
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
        print(e)
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
def decode_jwt(secret, token, session, algorithm="HS256", issuer=None):
    try:
        payload = jwt.decode(token, secret, algorithms=algorithm, issuer=issuer)
        if payload["iss"] != issuer:
            return None, None
        user_check = check_user(payload["sub"], payload["admin"], session)
        if user_check == False:
            return None, None
        return payload["sub"], payload["admin"]
    except jwt.ExpiredSignatureError:
        return None, None
    except jwt.InvalidTokenError:
        return None, None