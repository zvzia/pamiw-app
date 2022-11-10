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

def fetch_car_records_by_filter_conditions(brand, car_type, fuel_type, gearbox_type, city):
    query = "SELECT id, brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, image FROM Car WHERE "
    if brand != "any":
        query += "brand = " + "'" + brand + "'" + " AND "
    if car_type != "any":
        query += "car_type = " + "'" + car_type + "'" + " AND "
    if fuel_type != "any":
        query += "fuel_type = " + "'" + fuel_type + "'" + " AND "
    if gearbox_type != "any":
        query += "gearbox_type = " + "'" + gearbox_type + "'" + " AND "
    if city != "any":
        query += "city = " + "'" + city + "'" + " AND "

    query = query[:-4]
    data = cursor.execute(query)
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

def fetch_all_car_types():
    data = cursor.execute("SELECT DISTINCT car_type FROM car ORDER BY car_type")
    records = cursor.fetchall()
    return records

def fetch_all_fuel_types():
    data = cursor.execute("SELECT DISTINCT fuel_type FROM car ORDER BY fuel_type")
    records = cursor.fetchall()
    return records

def fetch_all_gearbox_types():
    data = cursor.execute("SELECT DISTINCT gearbox_type FROM car ORDER BY gearbox_type")
    records = cursor.fetchall()
    return records

def fetch_all_cities():
    data = cursor.execute("SELECT DISTINCT city FROM car ORDER BY city")
    records = cursor.fetchall()
    return records


def getImageFromDBByCarId(id):
    data = cursor.execute("SELECT image FROM Car WHERE id = ?", [id])
    records = cursor.fetchall()
    image = records[0][0]
    return image


