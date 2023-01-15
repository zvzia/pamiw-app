from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "database/car_rental.db"  

#connection = connect(DB_NAME, check_same_thread=False)
#cursor = connection.cursor()
def connect_to_db():
    connection = connect(DB_NAME, check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor

def create_messages_table():
    connection, cursor = connect_to_db()
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
    connection.close()

def insert_message_record(user_id, content, status, date):
    connection, cursor = connect_to_db()
    cursor.execute("INSERT INTO Message(user_id, content, status, date) VALUES(?, ?, ?, ?)",
                   (user_id, content, status, date))
    connection.commit()
    connection.close()

def fetch_message_records_by_user_id(user_id):
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT * FROM Message WHERE user_id = ?",[user_id])
    records = cursor.fetchall()
    connection.close()
    return records

def change_message_status_by_id(id, status):
    connection, cursor = connect_to_db()
    data = cursor.execute("UPDATE Message SET status = '" + status + "' WHERE id = " + str(id))
    connection.commit()
    connection.close()

def get_newest_message_by_user_id(user_id):
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT * FROM Message WHERE user_id = ? AND status = 'unread' ORDER BY id DESC",[user_id])
    records = cursor.fetchone()
    connection.close()
    return records
    