from sqlalchemy import *
from sqlalchemy.orm import *
from sys import path
from os import getenv
apalucha = getenv("apalucha")
if apalucha is None:
    apalucha = "."
path.append(apalucha)

from sql.sql_init import Films

def add_film(session, title, team):
    try:
        film = Films(Title=title, Team=team)
        session.add(film)
        session.commit()
        return True
    except Exception as e:
        print(f"Got exception while adding film {title} with team {team}: {e}")
        return False
def remove_film(session, film_id):
    try:
        # Searches for film with given id or title
        film = session.query(Films).filter(or_(Films.ID == film_id, Films.Title == film_id)).first()
        if film == None:
            print(f"Film {film_id} not found")
            return False
        session.delete(film)
        session.commit()
        return True
    except Exception as e:
        print(f"Got exception while removing film {film_id}: {e}")
        return False
def film_reset(session, deletion=False):
    try:
        if deletion == False:
            # Sets films final vote count to 0
            session.query(Films).update({Films.FinalVoteCount: 0})
            session.commit()
            return True
        else:
            # Deletes all films
            session.query(Films).delete()
            session.commit()
            return True
    except Exception as e:
        print(f"Got exception while resetting films: {e}")
        return False