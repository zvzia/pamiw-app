from sqlite3 import connect
from sqlite3.dbapi2 import Cursor
from datetime import date, timedelta

DB_NAME = "database/car_rental.db"  

#connection = connect(DB_NAME, check_same_thread=False)
#cursor = connection.cursor()
def connect_to_db():
    connection = connect(DB_NAME, check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor

def create_reservation_table():
    connection, cursor = connect_to_db()
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
    connection.close()

def insert_reservation_record(reservation_nr, start_time, end_time, car_id, user_id):
    connection, cursor = connect_to_db()
    cursor.execute("INSERT INTO Reservation(reservation_nr, start_time, end_time, car_id, user_id) VALUES(?, ?, ?, ?, ?)",
                   (reservation_nr, start_time, end_time, car_id, user_id))
    connection.commit()
    connection.close()

def fetch_reservation_records():
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT * FROM Reservation")
    records = cursor.fetchall()
    connection.close()
    return records

def get_dates_to_exclude(car_id):
    connection, cursor = connect_to_db()
    from datetime import date
    data = cursor.execute("SELECT * FROM Reservation WHERE car_id = ?", [car_id])
    records = cursor.fetchall()
    dates_to_exclude = []

    for row in records:
        start = row[2]
        end = row[3]

        start_array = start.split("-")
        end_array = end.split("-")

        date_start = date(int(start_array[0]), int(start_array[1]), int(start_array[2]))
        date_end = date(int(end_array[0]), int(end_array[1]), int(end_array[2]))

        date_to_add = date_start

        while(date_to_add != date_end):
            dates_to_exclude.append(str(date_to_add))
            date_to_add = date_to_add + timedelta(days=1)

        dates_to_exclude.append(str(date_end))
    
    connection.close()
    return dates_to_exclude

