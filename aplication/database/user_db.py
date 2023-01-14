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
                    password VARCHAR(150),
                    name VARCHAR(150),
                    surname VARCHAR(150),
                    email VARCHAR(150),
                    role VARCHAR(50) NOT NULL
                );
                '''
    cursor.executescript(table_script)
    connection.commit()
    connection.close()


def insert_user_record(username, password, name, surname, email, role):
    connection, cursor = connect_to_db()
    cursor.execute("INSERT INTO User(username, password, name, surname, email, role) VALUES(?, ?, ?, ?, ?, ?)",
                   (username, password, name, surname, email, role))
    connection.commit()
    connection.close()

def update_user_record(username, password, name, surname, email):
    user_id = get_user_id_by_username(username)
    connection, cursor = connect_to_db()
    cursor.execute("UPDATE User SET username = ?, password = ?, name = ?, surname = ?, email = ? WHERE id =?", [username, password, name, surname, email, user_id])
    connection.commit()
    connection.close()

def add_gh_user(username):
    user = get_user_id_by_username(username)
    if user == 0:
        connection, cursor = connect_to_db()
        cursor.execute("INSERT INTO User(username, role) VALUES(?, ?)",
                    (username, "ghuser"))
        connection.commit()
        connection.close()

def get_user_info_by_id(id):
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT * FROM User WHERE id = ?", [id])
    record = cursor.fetchone()
    connection.close()
    return record

def fetch_user_passwrd_by_username(username):
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT password FROM User WHERE username = ?", [username])
    records = cursor.fetchall()
    connection.close()
    return records

def get_user_id_by_username(username):
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT id FROM User WHERE username = ?", [username])
    records = cursor.fetchall()
    connection.close()
    if len(records) == 0:
        return 0
    else: 
        return records[0][0]

def get_role_by_username(username):
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT role FROM User WHERE username = ?", [username])
    record = cursor.fetchone()
    connection.close()
    return record

def get_user_by_username(username):
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT * FROM User WHERE username = ?", [username])
    record = cursor.fetchone()
    connection.close()
    return record