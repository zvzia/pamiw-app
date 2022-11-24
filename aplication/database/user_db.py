from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "database/car_rental.db"  

#connection = connect(DB_NAME, check_same_thread=False)
#cursor = connection.cursor()
def connect_to_db():
    connection = connect(DB_NAME, check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor

def create_user_table():
    connection, cursor = connect_to_db()
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
    connection.close()


def insert_user_record(username, password, name, surname, email):
    connection, cursor = connect_to_db()
    cursor.execute("INSERT INTO User(username, password, name, surname, email) VALUES(?, ?, ?, ?, ?)",
                   (username, password, name, surname, email))
    connection.commit()
    connection.close()

def insert_all_user_info(username, password, name, surname, email):
    connection, cursor = connect_to_db()
    cursor.execute("INSERT INTO User(username, password, name, surname, email) VALUES(?, ?, ?, ?, ?)",
                   (username, password, name, surname, email))
    connection.commit()
    connection.close()

def fetch_user_records():
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT * FROM User")
    records = cursor.fetchall()
    connection.close()
    return records

def fetch_user_passwrd_by_username(username):
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT password FROM User WHERE username = ?", [username])
    records = cursor.fetchall()
    connection.close()
    return records

def delete_user_record_by_username(username):
    connection, cursor = connect_to_db()
    data = cursor.execute("DELETE FROM User WHERE username = ?", [username])
    connection.close()
    return data

def get_user_id_by_username(username):
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT id FROM User WHERE username = ?", [username])
    records = cursor.fetchall()
    connection.close()
    return records