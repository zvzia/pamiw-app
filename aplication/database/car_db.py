from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "database/car_rental.db"  

#connection = connect(DB_NAME, check_same_thread=False)
#cursor = connection.cursor()
def connect_to_db():
    connection = connect(DB_NAME, check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor

def create_car_table():
    connection, cursor = connect_to_db()
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
    connection.close()

def insert_car_record(brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image):
    connection, cursor = connect_to_db()
    cursor.execute("INSERT INTO Car(brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image))
    connection.commit()
    connection.close()

def edit_car_record(car_id, brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image):
    connection, cursor = connect_to_db()
    query = "UPDATE Car SET "
    if(brand != ""):
        query += "brand = '" + brand + "', "
    if(model != ""):
        query += "model = '" + model + "', "
    if(car_type != ""):
        query += "car_type = '" + car_type + "', "
    if(production_year != ""):
        query += "production_year = '" + production_year + "', "
    if(fuel_type != ""):
        query += "fuel_type = '" + fuel_type + "', "
    if(gearbox_type != ""):
        query += "gearbox_type = '" + gearbox_type + "', "
    if(price != ""):
        query += "price = '" + price + "', "
    if(city != ""):
        query += "city = '" + city + "', "
    if(nr_of_cars != ""):
        query += "nr_of_cars = '" + nr_of_cars + "', "
    if(image != b''):
        query += "image = '" + image + "', "

    query = query[:-2]
    query += " WHERE id = " + car_id

    cursor.execute(query)
    connection.commit()
    connection.close()

def fetch_car_records():
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT id, brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image FROM Car")
    records = cursor.fetchall()
    connection.close()
    return records

def fetch_car_by_id(id):
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT id, brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image FROM Car WHERE id = ?", [id])
    records = cursor.fetchall()
    connection.close()
    return records

def fetch_car_records_by_brand(brand):
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT id, brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, image FROM Car WHERE brand = ?", [brand])
    records = cursor.fetchall()
    connection.close()
    return records

def fetch_car_records_by_model(model):
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT id, brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, image FROM Car WHERE model = ?", [model])
    records = cursor.fetchall()
    connection.close()
    return records

def fetch_car_records_by_filter_conditions(brand, car_type, fuel_type, gearbox_type, city):
    connection, cursor = connect_to_db()
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
    connection.close()
    return records

def fetch_all_brands():
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT DISTINCT brand FROM car ORDER BY brand")
    records = cursor.fetchall()
    connection.close()
    return records

def fetch_all_models():
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT DISTINCT model FROM car ORDER BY model")
    records = cursor.fetchall()
    connection.close()
    return records

def fetch_all_car_types():
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT DISTINCT car_type FROM car ORDER BY car_type")
    records = cursor.fetchall()
    connection.close()
    return records

def fetch_all_fuel_types():
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT DISTINCT fuel_type FROM car ORDER BY fuel_type")
    records = cursor.fetchall()
    connection.close()
    return records

def fetch_all_gearbox_types():
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT DISTINCT gearbox_type FROM car ORDER BY gearbox_type")
    records = cursor.fetchall()
    connection.close()
    return records

def fetch_all_cities():
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT DISTINCT city FROM car ORDER BY city")
    records = cursor.fetchall()
    connection.close()
    return records


def getImageFromDBByCarId(id):
    connection, cursor = connect_to_db()
    data = cursor.execute("SELECT image FROM Car WHERE id = ?", [id])
    records = cursor.fetchall()
    image = records[0][0]
    connection.close()
    return image


