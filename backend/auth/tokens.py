import jwt
import datetime
import json
import secrets
import os

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
    return token
def decode_jwt(secret, token, algorithm="HS256", issuer=None):
    try:
        payload = jwt.decode(token, secret, algorithms=algorithm, issuer=issuer)
        if payload["iss"] != issuer:
            return None, None
        return payload["sub"], payload["admin"]
    except jwt.ExpiredSignatureError:
        return None, None
    except jwt.InvalidTokenError:
        return None, None