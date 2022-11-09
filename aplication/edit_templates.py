from database.car_db import *

def insert_car_table(file):
    data = fetch_car_records()
    html_string =""
    for row in data:
        html_string +="<tr>"
        for col in row[1:]:
            html_string += "<td>" + str(col) + "</td>"
        html_string += "<td> <a href=\"car_info?car_id=" + str(row[0])  + "\"><button class=\"button\">Wyświetl</button></a></td>"
        html_string +="</tr>"
    
    result = file.replace("$tabela", html_string)
    return result

def insert_serached_cars(file, brand):
    data = fetch_car_records_by_brand(brand)
    html_string =""
    for row in data:
        html_string +="<tr>"
        for col in row[1:]:
            html_string += "<td>" + str(col) + "</td>"
        html_string += "<td> <a href=\"car_info?car_id=" + str(row[0])  + "\"><button class=\"buttontransparent\">Wyświetl</button></a></td>"
        html_string +="</tr>"
    
    result = file.replace("$tabela", html_string)
    return result

def insert_login_button(self, file, sessions):
    cookies = self.parse_cookies(self.headers["Cookie"])
    if "sid" in cookies:
         
        if (cookies["sid"] in sessions):
            self.user = cookies["sid"]
            file = file.replace("$logowanie", "<a href=\"messages\"><button class=\"icon\"><img src=\"messages.png\" width=\"30px\"></button></a> <a href=\"profile_page\"><button class=\"button\">Profil</button></a><a href=\"log_out\"><button class=\"button\">Wyloguj się</button></a>")
        else:
            file = file.replace("$logowanie","<a href=\"login_page\"><button class=\"button\">Zaloguj się</button></a><a href=\"register_page\"><button class=\"button\">Zarejestruj się</button></a>")
            self.user = False
    else:
        file = file.replace("$logowanie","<a href=\"login_page\"><button class=\"button\">Zaloguj się</button></a><a href=\"register_page\"><button class=\"button\">Zarejestruj się</button></a>")

        
    return file


def insert_autocomplete_data(file):
    brands = fetch_all_brands()
    models = fetch_all_models()
    
    html_string =""
    
    for brand in brands:
        html_string += "\"" + str(brand[0]) + "\", "
    
    for model in models:
        html_string += "\"" + str(model[0]) + "\", "
    
    html_string = html_string[:-2]

    result = file.replace("$autocompleteData", html_string)
    return result    


def insert_username_to_edit_data(file, username):
    result = file.replace("$username", username)
    return result

def insert_car_info(file, carId):
    car = fetch_car_by_id(carId)[0]
    
    file = file.replace("$carname", car[1] + " - " + car[2])
    file = file.replace("$brand", car[1])
    file = file.replace("$model", car[2])
    file = file.replace("$car_type", car[3])
    file = file.replace("$production_year", str(car[4]))
    file = file.replace("$fuel_type", car[5])
    file = file.replace("$gearbox_type", car[6])
    file = file.replace("$price", str(car[7]))
    file = file.replace("$city", car[8])

    return file