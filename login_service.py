import bcrypt
from database.user_db import *
import serwer

def hash_password(password):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt)

def check_password(given_password, db_password):
    passwrd_bytes = given_password.encode("utf-8")
    return bcrypt.checkpw(passwrd_bytes, db_password)

def check_login_info(username, password):
    records = fetch_user_passwrd_by_username(username)
    if (len(records) > 0):
        passwordInDb = records[0][0]
        return check_password(password, passwordInDb)
    
    return False

