from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "database/user.db"  

# create database inside database folder if not exists
connection = connect(DB_NAME)
cursor = connection.cursor()

def create_user_table():
    # create table user inside database if not exists
    table_script = '''CREATE TABLE IF NOT EXISTS User(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(150) NOT NULL UNIQUE,
                    password VARCHAR(150) NOT NULL,
                    name VARCHAR(150),
                    surname VARCHAR(150),
                    email VARCHAR(150)
                );
                '''
    cursor.executescript(table_script)
    connection.commit()

def insert_user_record(username, password):
    cursor.execute("INSERT INTO User(username, password) VALUES(?, ?)",
                   (username, password))
    connection.commit()

def insert_user_record(username, password, name, surname, email):
    cursor.execute("INSERT INTO User(username, password, name, surname, email) VALUES(?, ?, ?, ?, ?)",
                   (username, password, name, surname, email))
    connection.commit()

def insert_all_user_info(username, password, name, surname, email):
    cursor.execute("INSERT INTO User(username, password, name, surname, email) VALUES(?, ?, ?, ?, ?)",
                   (username, password, name, surname, email))
    connection.commit()

def fetch_user_records():
    data = cursor.execute("SELECT * FROM User")
    return data

def fetch_user_passwrd_by_username(username):
    data = cursor.execute("SELECT password FROM User WHERE username = ?", [username])
    records = cursor.fetchall()
    return records

def delete_user_record_by_username(username):
    data = cursor.execute("DELETE FROM User WHERE username = ?", [username])
    return data