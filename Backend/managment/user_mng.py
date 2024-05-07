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
from backend_logging.apalucha_logging import log

def add_user(session, isAdmin=False, username=None, password=None, pdfs_settings=None, jwt_settings=None, admin="-----", ip="-----"):
    try:
        if isAdmin:
            status = create_admin(username, password, session)
            if status == False:
                log("ERROR", f"{admin} from IP address {ip} failed to create new admin \"{username}\"")
                return False
            log("INFO", f"{admin} from IP address {ip} created new admin \"{username}\"")
            return True
        else:
            if jwt_settings == None or pdfs_settings == None:
                log("ERROR","jwt_settings and pdfs_settings must be provided")
                return False
            user = User()
            session.add(user)
            session.commit()
            log("INFO", f"User {user.ID} added by admin \"{admin}\" from IP address {ip}")
            user_id = user.ID
            token = generate_jwt(jwt_settings["secret"], jwt_settings["expiration"], jwt_settings["issuer"], jwt_settings["algorithm"], user_id)
            if token == None:
                log("ERROR", f"Failed to generate token for user {user_id}")
                return False
            log("INFO", f"Token generated for user {user_id}")
            url = f"{pdfs_settings['loginUrl']}?token={token}"
            template = pdfs_settings['path'] + pdfs_settings['template']
            new_pdf = pdfs_settings['path'] + f"{user_id}.pdf"
            status = generate_pdf(url, template, new_pdf)
            if status == False:
                log("ERROR", f"Failed to generate PDF for user {user_id}")
                return False
            log("INFO", f"PDF generated for user {user_id}")
            return user_id
    except Exception as e:
        print(f"Got exception while adding user: {e}")
        return False
def remove_user(session, user_id, isAdmin=False, admin="-----", ip="-----"):
    try:
        if isAdmin:
            remove_admin = session.query(Admin).filter_by(Username=user_id).first()
            if remove_admin == None:
                log("ERROR", f"{admin} from IP address {ip} failed to remove admin \"{user_id}\"")
                return False
            session.delete(remove_admin)
            session.commit()
            log("INFO", f"{admin} from IP address {ip} removed admin \"{user_id}\"")
            return True
        else:
            user = session.query(User).filter_by(ID=user_id).first()
            if user == None:
                log("ERROR", f"Admin \"{admin}\" from IP address {ip} failed to remove user \"{user_id}\"")
                return False
            session.delete(user)
            session.commit()
            log("INFO", f"Admin \"{admin}\" from IP address {ip} removed user \"{user_id}\"")
            return True
    except Exception as e:
        log("ERROR", f"Got exception while removing user: {e}")
        return False
def user_reset(session, deletion=False, admin="-----", ip="-----"):
    try:
        log("WARNING", f"Resetting users requested by admin \"{admin}\" from IP address {ip}")
        if deletion == False:
            # sets users vote count to null
            log("WARNING", f"Resetting vote count")
            session.query(User).update({User.Vote: None})
            session.commit()
            log("INFO", f"Vote count reset")
            return True
        else:
            # deletes all users
            log("WARNING", f"Deleting all users")
            session.query(User).delete()
            session.commit()
            log("INFO", f"All users deleted")
            return True
    except Exception as e:
        log("ERROR", f"Got exception while resetting users: {e}")
        return False