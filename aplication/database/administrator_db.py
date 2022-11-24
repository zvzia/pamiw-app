from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "database/car_rental.db"  

#connection = connect(DB_NAME, check_same_thread=False)
#cursor = connection.cursor()
def connect_to_db():
    connection = connect(DB_NAME, check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor

def create_administrator_table():
    connection, cursor = connect_to_db()
    # create table user inside database if not exists
    table_script = '''CREATE TABLE IF NOT EXISTS Administrator(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(150) NOT NULL UNIQUE,
                    password VARCHAR(150) NOT NULL
                );
                '''
    cursor.executescript(table_script)
    connection.commit()
    connection.close()

def insert_administrator_record(username, password):
    connection, cursor = connect_to_db()   
    cursor.execute("INSERT INTO Administrator(username, password) VALUES(?, ?)",
                   (username, password))
    connection.commit()
    connection.close()

def fetch_administrator_records():
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT * FROM Administrator")
    connection.close()
    return data