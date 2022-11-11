from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "database/car_rental.db"  

# create database inside database folder if not exists
connection = connect(DB_NAME)
cursor = connection.cursor()

def create_reservation_table():
    # create table user inside database if not exists
    table_script = '''CREATE TABLE IF NOT EXISTS Reservation(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reservation_nr INTEGER NOT NULL UNIQUE,
                    start_time TEXT,
                    end_time TEXT,
                    car_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (car_id) REFERENCES Car(id),
                    FOREIGN KEY (user_id) REFERENCES User(id)
                );
                '''
    cursor.executescript(table_script)
    connection.commit()

def insert_reservation_record(reservation_nr, start_time, end_time, car_id, user_id):
    cursor.execute("INSERT INTO Reservation(reservation_nr, start_time, end_time, car_id, user_id) VALUES(?, ?, ?, ?, ?)",
                   (reservation_nr, start_time, end_time, car_id, user_id))
    connection.commit()

def fetch_reservation_records():
    data = cursor.execute("SELECT * FROM Reservation")
    return data