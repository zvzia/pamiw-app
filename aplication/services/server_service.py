import random, string
from database.user_db import *
from services.email_service import *

def read_bytes_from_file(path):

    file = open(path,"rb")
    data = file.read()
    file.close()
    
    return data

def generate_state(length=30):
  char = string.ascii_letters + string.digits
  rand = random.SystemRandom()
  return ''.join(rand.choice(char) for _ in range(length))

def check_if_admin(username):
    role = get_role_by_username(username)

    if role[0] == "admin":
        return True
    else:
        return False
