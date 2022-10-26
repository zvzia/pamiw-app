from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "database/car.db"  

# create database inside database folder if not exists
connection = connect(DB_NAME)
cursor = connection.cursor()

def create_car_table():
    # create table user inside database if not exists
    table_script = '''CREATE TABLE IF NOT EXISTS Car(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand VARCHAR(100) NOT NULL,
                    model VARCHAR(100) NOT NULL,
                    car_type VARCHAR(100) NOT NULL,
                    production_year INTEGER NOT NULL,
                    fuel_type VARCHAR(100) NOT NULL,
                    gearbox_type VARCHAR(100) NOT NULL,
                    price REAL NOT NULL,
                    city VARCHAR(100) NOT NULL
                );
                '''
    cursor.executescript(table_script)
    connection.commit()

def insert_car_record(brand, model, car_type, production_year, fuel_type, gearbox_type, city):
    cursor.execute("INSERT INTO Car(ubrand, model, car_type, production_year, fuel_type, gearbox_type, city) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   (brand, model, car_type, production_year, fuel_type, gearbox_type, city))
    connection.commit()

def fetch_car_records():
    data = cursor.execute("SELECT * FROM Car")
    return data
