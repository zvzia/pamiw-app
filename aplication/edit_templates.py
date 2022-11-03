from database.car_db import *

def insert_car_table(file):
    data = fetch_car_records()
    html_string =""
    for row in data:
        html_string +="<tr>"
        for col in row[1:]:
            html_string += "<td>" + str(col) + "</td>"
        html_string += "<td> <a href=\"?car_id=" + str(row[0])  + "\"><button class=\"buttontransparent\">Wyświetl</button></a></td>"
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
        html_string += "<td> <a href=\"?car_id=" + str(row[0])  + "\"><button class=\"buttontransparent\">Wyświetl</button></a></td>"
        html_string +="</tr>"
    
    result = file.replace("$tabela", html_string)
    return result

def insert_login_button(self, file, sessions):
    cookies = self.parse_cookies(self.headers["Cookie"])
    if "sid" in cookies:
         
        if (cookies["sid"] in sessions):
            self.user = cookies["sid"]
            file = file.replace("$logowanie", "<a href=\"profile_page\"><button class=\"button\">Profil</button></a><a href=\"log_out\"><button class=\"button\">Wyloguj się</button></a>")
        else:
            file = file.replace("$logowanie","<a href=\"login_page\"><button class=\"button\">Zaloguj się</button></a><a href=\"register_page\"><button class=\"button\">Zarejestruj się</button></a>")
            self.user = False
    else:
        file = file.replace("$logowanie","<a href=\"login_page\"><button class=\"button\">Zaloguj się</button></a><a href=\"register_page\"><button class=\"button\">Zarejestruj się</button></a>")

        
    
    return file

def insert_username_to_edit_data(file, username):
    result = file.replace("$username", username)
    return result