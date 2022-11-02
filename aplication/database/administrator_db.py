from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "database/administrator.db"  

# create database inside database folder if not exists
connection = connect(DB_NAME)
cursor = connection.cursor()

def create_administrator_table():
    # create table user inside database if not exists
    table_script = '''CREATE TABLE IF NOT EXISTS Administrator(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(150) NOT NULL UNIQUE,
                    password VARCHAR(150) NOT NULL
                );
                '''
    cursor.executescript(table_script)
    connection.commit()

def insert_administrator_record(username, password):
    cursor.execute("INSERT INTO Administrator(username, password) VALUES(?, ?)",
                   (username, password))
    connection.commit()

def fetch_administrator_records():
    data = cursor.execute("SELECT * FROM Administrator")
    return data