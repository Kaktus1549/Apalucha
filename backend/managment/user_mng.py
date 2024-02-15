from sqlalchemy import *
from sqlalchemy.orm import *
from sys import path
from os import getenv
apalucha = getenv("apalucha")
if apalucha is None:
    apalucha = "."
path.append(apalucha)

from sql.sql_init import User, Admin
from auth.login import create_admin
from auth.tokens import generate_jwt
from managment.pdf_generator import generate_pdf

def add_user(session, isAdmin=False, username=None, password=None, pdfs_settings=None, jwt_settings=None):
    try:
        if isAdmin:
            status = create_admin(username, password, session)
            if status == False:
                print(f"Failed to create admin {username}")
                return False
            return True
        else:
            if jwt_settings == None or pdfs_settings == None:
                print("jwt_settings and pdfs_settings must be provided")
                return False
            user = User()
            session.add(user)
            session.commit()
            user_id = user.ID
            token = generate_jwt(jwt_settings["secret"], jwt_settings["expiration"], jwt_settings["issuer"], jwt_settings["algorithm"], user_id)
            if token == None:
                print(f"Failed to generate token for user {user_id}")
                return False
            url = f"{pdfs_settings['loginUrl']}?token={token}"
            template = pdfs_settings['path'] + pdfs_settings['template']
            new_pdf = pdfs_settings['path'] + f"{user_id}.pdf"
            status = generate_pdf(url, template, new_pdf)
            if status == False:
                print(f"Failed to generate PDF for user {user_id}")
                return False
            return user_id
    except Exception as e:
        print(f"Got exception while adding user {username} with password {password}: {e}")
        return False
def remove_user(session, user_id, isAdmin=False):
    try:
        if isAdmin:
            admin = session.query(Admin).filter_by(Username=user_id).first()
            if admin == None:
                print(f"Admin {user_id} not found")
                return False
            session.delete(admin)
            session.commit()
            return True
        else:
            user = session.query(User).filter_by(ID=user_id).first()
            if user == None:
                print(f"User {user_id} not found")
                return False
            session.delete(user)
            session.commit()
            return True
    except Exception as e:
        print(f"Got exception while removing user {user_id}: {e}")
        return False
def user_reset(session, deletion=False):
    try:
        if deletion == False:
            # sets users vote count to null
            session.query(User).update({User.Vote: None})
            session.commit()
            return True
        else:
            # deletes all users
            session.query(User).delete()
            session.commit()
            return True
    except Exception as e:
        print(f"Got exception while resetting users: {e}")
        return False