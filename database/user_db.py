from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "database/user.db"  

# create database inside database folder if not exists
connection = connect(DB_NAME)
cursor = connection.cursor()

def create_user_table():
    """function to create table inside database"""
    # create table user inside database if not exists
    table_script = '''CREATE TABLE IF NOT EXISTS User(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(150) NOT NULL UNIQUE,
                    password VARCHAR(150) NOT NULL
                );
                '''
    cursor.executescript(table_script)
    connection.commit()

def insert_user_record(username, password):
    """function to insert record inside table"""
    cursor.execute("INSERT INTO User(username, password) VALUES(?, ?)",
                   (username, password))
    connection.commit()

def fetch_user_records():
    """function to fetch User records"""
    data = cursor.execute("SELECT * FROM User")
    return data

def fetch_user_record_by_username(username):
    """function to fetch User records"""
    data = cursor.execute("SELECT password FROM User WHERE username = ?", [username])
    records = cursor.fetchall()
    return records