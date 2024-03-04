from sqlalchemy import *
from sqlalchemy.orm import *
from sys import path
from os import getenv
apalucha = getenv("apalucha")
if apalucha is None:
    apalucha = "."
path.append(apalucha)

from sql.sql_init import User

def vote_film(film_id, user_id, session):
    try:
        user = session.query(User).filter_by(ID=user_id).first()
        if user == None:
            print(f"User {user_id} not found")
            return False
        user.Vote = int(film_id)
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False