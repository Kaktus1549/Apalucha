from sys import path
from sqlalchemy import *
from sqlalchemy.orm import *
path.append(".")

from Database.tables import User, Admin, Films


def check_user_exists(session, user_id, is_admin):
    if is_admin:
        return session.query(Admin).filter(Admin.Username == user_id).count() > 0
    else:
        return session.query(User).filter(User.ID == user_id).count() > 0
def check_film_exists(session, film_id):
    return session.query(Films).filter(Films.ID == film_id).count() > 0
def delete_film(session, film_id):
    session.query(Films).filter(Films.ID == film_id).delete()
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