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

def create_admin(username, password, session):
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_admin = Admin(Username=username, PasswordHash=hashed_password)
        session.add(new_admin)
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False
def login_admin(username, password, session, jwt_settings):
    try:
        if jwt_settings == None:
            print("jwt_settings must be provided")
            return False
        admin = session.query(Admin).filter_by(Username=username).first()
        if admin == None:
            return False
        if bcrypt.checkpw(password.encode('utf-8'), admin.PasswordHash.encode('utf-8')):
            token = generate_jwt(jwt_settings["secret"], jwt_settings["expiration"], jwt_settings["issuer"], jwt_settings["algorithm"], username, isAdmin=True)
            if token == None:
                print(f"Failed to generate token for admin {username}")
                return False
            return token
        return False
    except Exception as e:
        print(e)
        return False