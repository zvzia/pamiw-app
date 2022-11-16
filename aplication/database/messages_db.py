from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "database/car_rental.db"  

connection = connect(DB_NAME)
cursor = connection.cursor()

def create_reservation_table():
    table_script = '''CREATE TABLE IF NOT EXISTS Message(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    content  VARCHAR(600)
                    FOREIGN KEY (user_id) REFERENCES User(id)
                );
                '''
    cursor.executescript(table_script)
    connection.commit()

def insert_message_record(user_id, content):
    cursor.execute("INSERT INTO Message(user_id, content) VALUES(?, ?)",
                   (user_id, content))
    connection.commit()

def fetch_message_records():
    data = cursor.execute("SELECT * FROM Messages")
    return data