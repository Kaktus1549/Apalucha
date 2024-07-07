from sqlalchemy import *
from sqlalchemy.orm import *
from sys import path
from os import getenv
apalucha = getenv("apalucha")
if apalucha is None:
    apalucha = "."
path.append(apalucha)

from sql.sql_init import Films, BallotBox
from backend_logging.apalucha_logging import log

def add_film(session, title, team, admin="-----", ip="-----"):
    try:
        film = Films(Title=title, Team=team)
        session.add(film)
        session.commit()
        log("INFO", f"Film \"{title}\" by team {team} added by admin \"{admin}\" from IP address {ip}")
        return True
    except Exception as e:
        log("ERROR", f"Got exception while adding film {title} with team {team}: {e}")
        return False
def remove_film(session, film_id, admin="-----", ip="-----"):
    try:
        # Searches for film with given id or title
        film = session.query(Films).filter(or_(Films.ID == film_id, Films.Title == film_id)).first()
        if film == None:
            log("ERROR", f"Film with id or title {film_id} not found")
            return False
        session.delete(film)
        session.commit()
        log("INFO", f"Film {film_id} removed by admin \"{admin}\" from IP address {ip}")
        return True
    except Exception as e:
        log("ERROR", f"Got exception while removing film {film_id}: {e}")
        return False
def film_reset(session, deletion=False, admin="-----", ip="-----"):
    try:
        log("WARNING", f"Admin \"{admin}\" from IP address {ip} initiated film reset!!!")
        # Deletes all votes from ballot box
        log("WARNING", "Deleting all votes from ballot box")
        session.query(BallotBox).delete()
        session.commit()
        if deletion == False:
            # Sets films final vote count to 0
            log("WARNING", "Resetting all films to 0 votes")
            session.query(Films).update({Films.FinalVoteCount: 0})
            session.commit()
            log("INFO", "All films reset to 0 votes")
        else:
            # Deletes all films
            log("WARNING", "Deleting all films!!!")
            session.query(Films).delete()
            session.commit()
            log("INFO", "All films deleted")
        return True
    except Exception as e:
        log("ERROR", f"Got exception while resetting films: {e}")
        return False