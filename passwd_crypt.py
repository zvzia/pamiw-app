import bcrypt

def hash_password(password):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt)

def check_password(given_password, db_password):
    passwrd_bytes = given_password.encode("utf-8")
    return bcrypt.checkpw(passwrd_bytes, db_password)