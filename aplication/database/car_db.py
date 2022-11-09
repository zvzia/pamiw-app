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
                    city VARCHAR(100) NOT NULL,
                    nr_of_cars INTEGER NOT NULL,
                    image BLOB NOT NULL
                );
                '''
    cursor.executescript(table_script)
    connection.commit()

def insert_car_record(brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image):
    cursor.execute("INSERT INTO Car(brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image))
    connection.commit()

def fetch_car_records():
    data = cursor.execute("SELECT id, brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image FROM Car")
    records = cursor.fetchall()
    return records

def fetch_car_by_id(id):
    data = cursor.execute("SELECT id, brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image FROM Car WHERE id = ?", [id])
    records = cursor.fetchall()
    return records

def fetch_car_records_by_brand(brand):
    data = cursor.execute("SELECT id, brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, image FROM Car WHERE brand = ?", [brand])
    records = cursor.fetchall()
    return records

def fetch_all_brands():
    data = cursor.execute("SELECT DISTINCT brand FROM car ORDER BY brand")
    records = cursor.fetchall()
    return records

def fetch_all_models():
    data = cursor.execute("SELECT DISTINCT model FROM car ORDER BY model")
    records = cursor.fetchall()
    return records


