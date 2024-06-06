from sys import path
from sqlalchemy import *
from sqlalchemy.orm import *
path.append(".")

from Database.tables import User, Admin, Films

def check_user_exists(session, user_id, is_admin):
    if is_admin:
        user = session.query(Admin).filter_by(Username=user_id).first()
    else:
        user = session.query(User).filter_by(ID=user_id).first()
    return user is not None
def check_film_exists(session, film_id):
    film = session.query(Films).filter_by(Title=film_id).first()
    return film is not None
def delete_film(session, film_id):
    session.query(Films).filter(Films.Title == film_id).delete()
    session.commit()
def create_testing_user(session, user_id, is_admin):
    if is_admin:
        session.add(Admin(Username=user_id, PasswordHash="1234"))
    else:
        session.add(User(ID=user_id, Vote=0))
    session.commit()
def delete_testing_user(session, user_id, is_admin):
    if is_admin:
        session.query(Admin).filter(Admin.Username == user_id).delete()
    else:
        session.query(User).filter(User.ID == user_id).delete()
    session.commit()
def check_user_vote(session, user_id, film_id):
    user = session.query(User).filter_by(ID=user_id).first()
    if user is None:
        return False
    # Gets ID of film
    film = session.query(Films).filter_by(Title=film_id).first()
    return user.Vote == film.ID
def check_film_vote(session, film_id):
    film = session.query(Films).filter_by(Title=film_id).first()
    if film.Votes == 0:
        return False
    return True