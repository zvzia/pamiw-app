from database.car_db import *
from database.user_db import *
from database.messages_db import *

def insert_car_table_for_admin(file):
    data = fetch_car_records()
    html_string =""
    for row in data:
        html_string +="<tr>"
        for col in row[1:-1]:
            html_string += "<td>" + str(col) + "</td>"
        html_string += "<td> <a href=\"edit_car?car_id=" + str(row[0]) + "\"><button class=\"button\">Edytuj</button></a></td>"
        html_string +="</tr>"
    
    result = file.replace("$cartable", html_string)
    return result

def insert_edit_car_info(file, car_id):
    car = fetch_car_by_id(car_id)

    file = file.replace("$carid", str(car[0][0]))
    file = file.replace("$brand", car[0][1])
    file = file.replace("$model", car[0][2])
    file = file.replace("$cartype", car[0][3])
    file = file.replace("$productionyear", str(car[0][4]))
    file = file.replace("$fueltype", car[0][5])
    file = file.replace("$gearboxtype", car[0][6])
    file = file.replace("$price", str(car[0][7]))
    file = file.replace("$city", car[0][8])
    file = file.replace("$nrofcars", str(car[0][9]))

    return file

def insert_empty_info(file):
    file = file.replace("$carid", "")
    file = file.replace("$brand", "")
    file = file.replace("$model", "")
    file = file.replace("$cartype", "")
    file = file.replace("$productionyear", "")
    file = file.replace("$fueltype", "")
    file = file.replace("$gearboxtype", "")
    file = file.replace("$price", "")
    file = file.replace("$city", "")
    file = file.replace("$nrofcars", "")

    return file


def insert_serached_cars(file, search):
    data = fetch_car_records_by_brand(search)
    data2 = fetch_car_records_by_model(search)
    html_string = ""
    
    for row in data:
        carId = row[0]
        carname = row[1] + " - " + row[2]
        productionyear = str(row[4])
        price = str(row[7])

        html_string += "<div class=\"center\" id=\"wrapper\">"
        html_string += "<div id=\"first\" style=\"margin-left: 10%;\">" + "<img class=\"centered-and-cropped\" width=\"600px\" height=\"400px\" src=\"getImageFromCarDb?carId="+ str(carId) + "\" />" + "</div>"

        html_string += "<div id=\"seccond\">" + "<br><br><br>" + "<h1>" + carname + "</h1>" + "<p>" + productionyear + "</p>" + "<p>" + price + " /doba</p>" + "</div>"
        html_string += "<br><br><br>"
        html_string += "<a href=\"car_info?car_id=" + str(row[0])  + "\"><button class=\"buttontransparent\">Wyświetl</button></a>" + "</div>" + "<br><br>"

    for row in data2:
        carId = row[0]
        carname = row[1] + " - " + row[2]
        productionyear = str(row[4])
        price = str(row[7])

        html_string += "<div class=\"center\" id=\"wrapper\">"
        html_string += "<div id=\"first\" style=\"margin-left: 10%;\">" + "<img class=\"centered-and-cropped\" width=\"600px\" height=\"400px\" src=\"getImageFromCarDb?carId="+ str(carId) + "\" />" + "</div>"

        html_string += "<div id=\"seccond\">" + "<br><br><br>" + "<h1>" + carname + "</h1>" + "<p>" + productionyear + "</p>" + "<p>" + price + " /doba</p>" + "</div>"
        html_string += "<br><br><br>"
        html_string += "<a href=\"car_info?car_id=" + str(row[0])  + "\"><button class=\"buttontransparent\">Wyświetl</button></a>" + "</div>" + "<br><br>"

        
    
    result = file.replace("$tabela", html_string)
    return result

def insert_car_table(file):
    data = fetch_car_records()
    html_string = ""
    
    for row in data:
        carId = row[0]
        carname = row[1] + " - " + row[2]
        productionyear = str(row[4])
        price = str(row[7])

        html_string += "<div class=\"center\" id=\"wrapper\">"
        html_string += "<div id=\"first\" style=\"margin-left: 10%;\">" + "<img class=\"centered-and-cropped\" width=\"600px\" height=\"400px\" src=\"getImageFromCarDb?carId="+ str(carId) + "\" />" + "</div>"

        html_string += "<div id=\"seccond\">" + "<br><br><br>" + "<h1>" + carname + "</h1>" + "<p>" + productionyear + "</p>" + "<p>" + price + " /doba</p>" + "</div>"
        html_string += "<br><br><br>"
        html_string += "<a href=\"car_info?car_id=" + str(row[0])  + "\"><button class=\"buttontransparent\">Wyświetl</button></a>" + "</div>" + "<br><br>"

        
    
    result = file.replace("$tabela", html_string)
    return result

def insert_filtered_cars(file, brand, car_type, fuel_type, gearbox_type, city):
    data = fetch_car_records_by_filter_conditions(brand, car_type, fuel_type, gearbox_type, city)
    html_string = ""
    
    for row in data:
        carId = row[0]
        carname = row[1] + " - " + row[2]
        productionyear = str(row[4])
        price = str(row[7])

        html_string += "<div class=\"center\" id=\"wrapper\">"
        html_string += "<div id=\"first\" style=\"margin-left: 10%;\">" + "<img class=\"centered-and-cropped\" width=\"600px\" height=\"400px\" src=\"getImageFromCarDb?carId="+ str(carId) + "\" />" + "</div>"

        html_string += "<div id=\"seccond\">" + "<br><br><br>" + "<h1>" + carname + "</h1>" + "<p>" + productionyear + "</p>" + "<p>" + price + " /doba</p>" + "</div>"
        html_string += "<br><br><br>"
        html_string += "<a href=\"car_info?car_id=" + str(row[0])  + "\"><button class=\"buttontransparent\">Wyświetl</button></a>" + "</div>" + "<br><br>"

        
    
    result = file.replace("$tabela", html_string)
    return result


def insert_login_button(self, file, sessions):
    cookies = self.parse_cookies(self.headers["Cookie"])
    if "sid" in cookies:
         
        if (cookies["sid"] in sessions):
            self.user = cookies["sid"]
            file = file.replace("$logowanie", "<a href=\"messages\"><button class=\"button\">Wiadomości</button></a> <a href=\"profile_page\"><button class=\"button\">Profil</button></a><a href=\"log_out\"><button class=\"button\">Wyloguj się</button></a>")
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
    file = file.replace("$image", "<img class=\"centered-and-cropped\" width=\"600px\" height=\"400px\" src=\"getImageFromCarDb?carId="+ str(carId) + "\" />")

    return file

def insert_filter_options(file):
    brands = fetch_all_brands()
    car_types = fetch_all_car_types()
    fuel_options = fetch_all_fuel_types()
    gearbox_options = fetch_all_gearbox_types()
    cities = fetch_all_cities()

    brand_options_html = ""
    car_type_otions_html = ""
    fuel_options_html = ""
    gearbox_options_html = ""
    city_options_html = ""

    for brand in brands:
        brand_options_html += "<option value=\"" + brand[0] + "\">" + brand[0] +"</option>"
    for type in car_types:
        car_type_otions_html += "<option value=\"" + type[0] + "\">" + type[0] +"</option>"
    for fuel in fuel_options:
        fuel_options_html += "<option value=\"" + fuel[0] + "\">" + fuel[0] +"</option>"
    for gearbox in gearbox_options:
        gearbox_options_html += "<option value=\"" + gearbox[0] + "\">" + gearbox[0] +"</option>"
    for city in cities:
        city_options_html += "<option value=\"" + city[0] + "\">" + city[0] +"</option>"
    
    
    
    file = file.replace("$brandoptions", brand_options_html)
    file = file.replace("$cartypeoptions", car_type_otions_html)
    file = file.replace("$fueltypeoptions", fuel_options_html)
    file = file.replace("$gearboxtypeoptions", gearbox_options_html)
    file = file.replace("$cityoptions", city_options_html)

    return file

def insert_cities_buttons(file):
    cities = fetch_all_cities()

    cities_html = ""
    for city in cities:
        cities_html += "<a href=\"/oferta?city=" + city[0] + "\" method=\"post\"><button class=\"button-big\">" + city[0] + "</button></a><br><br>"

    file = file.replace("$citiesbuttons", cities_html)

    return file
    
def insert_messages(self, file, sessions):
    cookies = self.parse_cookies(self.headers["Cookie"])
    if "sid" in cookies:
        if (cookies["sid"] in sessions):
            username = sessions[self.user][0]
            user_id = get_user_id_by_username(username)[0][0]
            self.user = cookies["sid"]

            
            data = fetch_message_records_by_user_id(user_id)
            html_string = "<hr>"
            
            for row in data:
                content = row[2]
                date = row[4]

                html_string += "<p>" + content + "</p> <br>" + str(date) +"<hr>"

            file = file.replace("$messages", html_string)
        else:
            self.user = False

    return file
                    