from database.car_db import *
from database.user_db import *
from database.messages_db import *
from database.reservation_db import *
import json

def get_cars_for_admin():
    data = fetch_car_records()
    return data

def get_reservations_for_admin():
    data = fetch_reservation_records()
    reservations = []
    for row in data:

        record = ['']*8
        record[0] = str(row[1])
        record[1] = str(row[2])
        record[2] = str(row[3])
        car = fetch_car_by_id(row[4])[0]
        record[3] = str(car[1] + " - " + car[2])
        record[4] = str(row[6])
        record[5] = str(row[7])
        record[6] = str(row[8])
        record[7] = str(row[9])

        reservations.append(record)

    return reservations

def get_edit_car_info(car_id):
    car = fetch_car_by_id(car_id)
    info = []
    info.append(str(car[0][0])) #carid
    info.append(car[0][1]) #brand
    info.append(car[0][2]) #model
    info.append(car[0][3]) #cartype
    info.append(str(car[0][4])) #productionyear
    info.append(car[0][5]) #fueltype
    info.append(car[0][6]) #gearboxtype
    info.append(str(car[0][7])) #price
    info.append(car[0][8]) #city

    return info

def get_empty_info():
    info = []
    info.append("") #carid
    info.append("") #brand
    info.append("") #model
    info.append("") #cartype
    info.append("") #productionyear
    info.append("") #fueltype
    info.append("") #gearboxtype
    info.append("") #price
    info.append("") #city

    return info

def get_serached_cars(search):
    data = fetch_car_records_by_brand(search)
    data2 = fetch_car_records_by_model(search)

    for i in data2:
        data.append(i)

    return data

def get_filtered_cars(brand, car_type, fuel_type, gearbox_type, city):
    data = fetch_car_records_by_filter_conditions(brand, car_type, fuel_type, gearbox_type, city)
    return data  

def get_autocomplete_data():
    brands = fetch_all_brands()
    models = fetch_all_models()
    
    data = []
    for brand in brands:
        data.append(brand[0])

    for model in models:
        data.append(model[0])
    
    return data   

def get_car_info(carId):
    car = fetch_car_by_id(carId)[0]
    info = []
    info.append(str(carId)) #carid
    info.append(car[1] + " - " + car[2]) #carname
    info.append(car[1]) #brand
    info.append(car[2]) #model
    info.append(car[3]) #car_type
    info.append(str(car[4])) #production_year
    info.append(car[5]) #fuel_type
    info.append(car[6]) #gearbox_type
    info.append(str(car[7])) #price
    info.append(car[8]) #city
    return info


def get_filter_options():
    brandsdb = fetch_all_brands()
    car_typesdb = fetch_all_car_types()
    fuel_optionsdb = fetch_all_fuel_types()
    gearbox_optionsdb = fetch_all_gearbox_types()
    citiesdb = fetch_all_cities()

    data = []
    brands = []
    car_types = []
    fuel_options = []
    gearbox_options = []
    cities = []

    for brand in brandsdb:
        brands.append(brand[0])
    
    for type in car_typesdb:
        car_types.append(type[0])
    
    for option in fuel_optionsdb:
        fuel_options.append(option[0])

    for option in gearbox_optionsdb:
        gearbox_options.append(option[0])
    
    for city in citiesdb:
        cities.append(city[0])

    data.append(brands)
    data.append(car_types)
    data.append(fuel_options)
    data.append(gearbox_options)
    data.append(cities)
    return data

def get_cities():
    citiesdb = fetch_all_cities()
    cities = []
    for city in citiesdb:
        cities.append(city[0])

    return cities
    
def get_messages(username):
    user_id = get_user_id_by_username(username)   
    data = fetch_message_records_by_user_id(user_id)
            
    for row in data:
        message_id = row[0]
        status = row[3]

        if(status == "unread"):
            change_message_status_by_id(message_id, "read")

    return data

def check_for_unread_messages(username):
    user_id = get_user_id_by_username(username)
    data = fetch_message_records_by_user_id(user_id)

    for row in data:
        if(row[3] == "unread"):
            return True
    
    return False

def get_reservation_form_info(carId, username):
    car = fetch_car_by_id(carId)[0]
    userId = get_user_id_by_username(username)

    info = []
    info.append(car[1] + " - " + car[2])
    info.append(str(carId))
    info.append(str(userId))

    return info
                    
def get_company_info():
    file = open('database/data/companyinfo.json', "r", encoding='utf8')
    json_object = json.load(file)

    info = []
    info.append(json_object["description"])
    info.append(json_object["phonenr"])
    info.append(json_object["email"])

    return info

def save_info(description, phonenr, email):
    file = open("database/data/companyinfo.json", "r", encoding='utf8')
    json_object = json.load(file)
    file.close()

    json_object["description"] = description
    json_object["phonenr"] = phonenr
    json_object["email"] = email

    file = open("database/data/companyinfo.json", "w", encoding='utf8')
    json.dump(json_object, file)
    file.close()

def get_user_new_message(username):
    user_id = get_user_id_by_username(username)
    message = get_newest_message_by_user_id(user_id)

    return message