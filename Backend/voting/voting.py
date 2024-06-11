from sqlalchemy import *
from sqlalchemy.orm import *
from sys import path
from os import getenv
apalucha = getenv("apalucha")
if apalucha is None:
    apalucha = "."
path.append(apalucha)

from sql.sql_init import User, BallotBox
from backend_logging.apalucha_logging import log

def vote_film(film_id, user_id, session, ip=None):
    try:
        user = session.query(User).filter_by(ID=user_id).first()
        if user == None:
            log("ERROR", f"User {user_id} not found")
            return False
        user.Vote = int(film_id)
        session.commit()
        log("INFO", f"User {user_id} voted for film {film_id} from IP address {ip}")
        return True
    except Exception as e:
        log("ERROR", f"Got an error while trying to vote for film {film_id} for user {user_id}: {e}")
        return False
def ballotbox_vote(film_id, session, ip=None):
    try:
        new_vote = BallotBox(Vote=int(film_id))
        session.add(new_vote)
        session.commit()
        log("INFO", f"Vote for film {film_id} from IP address {ip} added to ballot box")
        return True
    except Exception as e:
        log("ERROR", f"Got an error while trying to add vote for film {film_id} to ballot box: {e}")
        return False