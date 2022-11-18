from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "database/car_rental.db"  

connection = connect(DB_NAME)
cursor = connection.cursor()

def create_messages_table():
    table_script = '''CREATE TABLE IF NOT EXISTS Message(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    content  VARCHAR(600),
                    status VARCHAR(30),
                    date TEXT,
                    FOREIGN KEY (user_id) REFERENCES User(id)
                );
                '''
    cursor.executescript(table_script)
    connection.commit()

def insert_message_record(user_id, content, status, date):
    cursor.execute("INSERT INTO Message(user_id, content, status, date) VALUES(?, ?, ?, ?)",
                   (user_id, content, status, date))
    connection.commit()

def fetch_message_records_by_user_id(user_id):
    data = cursor.execute("SELECT * FROM Message WHERE user_id = ?",[user_id])
    return data

def change_message_status_by_id(id, status):
    data = cursor.execute("UPDATE Message SET status = ? WHERE id = ?", [status, id])
    return data