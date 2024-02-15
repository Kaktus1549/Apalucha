from sqlalchemy import *
from sqlalchemy.orm import *
from sys import path
from os import getenv
apalucha = getenv("apalucha")
if apalucha is None:
    apalucha = "."
path.append(apalucha)

from sql.sql_init import User, Films

def count_votes(session):
    # Goes through all users and counts their votes, in column Vote is the film id
    # At the end, sets the FinalVoteCount of the film to the sum of all votes
    try:
        # Sets all FinalVoteCounts to 0
        films = session.query(Films).all()
        for film in films:
            film.FinalVoteCount = 0
        session.commit()
        # Counts all votes
        users = session.query(User).all()
        for user in users:
            film_id = user.Vote
            try:
                film = session.query(Films).filter_by(ID=film_id).first()
                film.FinalVoteCount += 1
            except Exception as e:
                print(f"Got exception while processing user {user.ID} for film {film_id}: {e}")
                continue
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False
def unsorted_films(session):
    # Returns all films in the database, unsorted
    # Returns it in form Films{ 1: "Film1", 2: "Film2", ... }
    try:
        films = session.query(Films).all()
        film_dict = {}
        for film in films:
            film_dict[film.ID] = film.Title
        return film_dict
    except Exception as e:
        print(e)
        return False
def sorted_films(session):
    # Returns all films in the database, sorted by FinalVoteCount
    # Returns it in form Films{ filmRank: "Film1", ... }
    try:
        films = session.query(Films).order_by(Films.FinalVoteCount.desc()).all()
        film_dict = {}
        final_votes = []
        for i in range(len(films)):
            film_dict[i+1] = films[i].Title
            if films[i].FinalVoteCount != null:
                final_votes.append(films[i].FinalVoteCount)
            else:
                final_votes.append(0)
        return film_dict, final_votes
    except Exception as e:
        print(e)
        return False, False