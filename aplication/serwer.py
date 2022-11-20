import re
import sys
import cgi
from http.client import HTTP_PORT
from http.server import HTTPServer, BaseHTTPRequestHandler
from random import randint
import datetime

from matplotlib.style import use

from database.user_db import *
from database.reservation_db import *
from database.car_db import *
from database.administrator_db import *
from database.messages_db import *
from login_service import *
from edit_templates import *

HOST = "0.0.0.0"
PORT = 8080
SESSIONS = {}

def read_html_template(path):
    try:
        with open(path, encoding='utf-8') as f:
            file = f.read()
    except Exception as e:
        file = e
    return file

def read_bytes_from_file(path):

    file = open(path,"rb")
    data = file.read()
    file.close()
    
    return data




class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        cookies = self.parse_cookies(self.headers["Cookie"])
        if "sid" in cookies:
            if (cookies["sid"] in SESSIONS):
                self.user = cookies["sid"]

        if self.path == '/':
            self.path = './templates/customer/start_page.html'
            file = read_html_template(self.path)

            file = insert_login_button(self, file, SESSIONS)
                
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))  

        if self.path == '/oferta':
            self.path = './templates/customer/offer.html'
            file = read_html_template(self.path)
            
            file = insert_car_table(file)
            file = insert_login_button(self, file, SESSIONS)
            file = insert_autocomplete_data(file)
            file = insert_filter_options(file)
                
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))  

        if self.path == '/login_page':
            self.path = './templates/customer/login_page.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/log_out':
            self.logout()
            html = f"<html><head></head><body><h1>Wylogowano</h1> <a href=\"/\"><button class=\"button\">Powrót</button></a></body></html>"
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(html, 'utf-8'))

        if self.path == '/register_page':
            self.path = './templates/customer/register_page.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/profile_page':
            self.path = './templates/customer/profile_page.html'
            file = read_html_template(self.path)
            file = insert_login_button(self, file, SESSIONS)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/data_edit':
            self.path = './templates/customer/data_edit.html'
            file = read_html_template(self.path)
            username = SESSIONS[self.user][0]
            file = file.replace("$username", username)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path[0:10] == '/car_info?':
            carId = int(self.path[17:])
            self.path = './templates/customer/car_info.html'
            file = read_html_template(self.path)

            file = insert_car_info(file, carId)
            file = insert_login_button(self, file, SESSIONS)
                
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path[-4:] == '.png' or self.path[-4] == '.jpg':
            self.path = "templates/" + self.path.partition("/")[-1]
            data = read_bytes_from_file(self.path)
            
            self.send_response(200, "OK")
            self.send_header('Content-type', 'image/*')
            self.end_headers()
            self.wfile.write(data)

        if self.path == '/miasta':
            self.path = './templates/customer/cities.html'
            file = read_html_template(self.path)
            file = insert_login_button(self, file, SESSIONS)
            file = insert_cities_buttons(file)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/oNas':
            self.path = './templates/customer/aboutus.html'
            file = read_html_template(self.path)
            file = insert_login_button(self, file, SESSIONS)
            #file = insert_contact_information(file)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path[:25] == '/getImageFromCarDb?carId=':
            carId = self.path[25:]
            data = getImageFromDBByCarId(carId)
            
            self.send_response(200, "OK")
            self.send_header('Content-type', 'image/*')
            self.end_headers()
            self.wfile.write(data)

        if self.path[0:13] == '/oferta?city=':
            city = self.path[13:]
            brand = "any"
            car_type = "any"
            fuel_type = "any"
            gearbox_type = "any"

            self.path = './templates/customer/offer.html'
            file = read_html_template(self.path)
            file = insert_filtered_cars(file, brand, car_type, fuel_type, gearbox_type, city)
            file = insert_login_button(self, file, SESSIONS)
        
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))
        
        if self.path == '/messages':
            self.path = './templates/customer/messages.html'
            file = read_html_template(self.path)
            file = insert_messages(self, file, SESSIONS)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path[-10:] == 'styles.css':
            self.path = './static/css/styles.css'
            file = read_html_template(self.path)
            
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        

        #admin -------------------------------------------------

        if self.path == '/admin':
            self.path = './templates/admin/admin_start_page.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/admin/cars':
            self.path = './templates/admin/admin_car_list.html'
            file = read_html_template(self.path)
            file = insert_car_table_for_admin(file)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path[:23] == '/admin/edit_car?car_id=':
            car_id = int(self.path[23:])
            self.path = './templates/admin/add_car.html'
            file = read_html_template(self.path)
            file = insert_edit_car_info(file, car_id)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path[:23] == '/admin/add_car':
            self.path = './templates/admin/add_car.html'
            file = read_html_template(self.path)
            file = insert_empty_info(file)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/admin/send_message':
            self.path = './templates/admin/send_message.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))


    

    def do_POST(self):
        cookies = self.parse_cookies(self.headers["Cookie"])
        if "sid" in cookies:
            if (cookies["sid"] in SESSIONS):
                self.user = cookies["sid"]
                
        if self.path == '/logIn':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                username = fields.get("username")[0]
                password = fields.get("password")[0]


            #sprawdzanie zgodnosci hasla
            verification = check_login_info(username, password)

            if verification == True:
                sid = self.generate_sid()
                self.cookie = "sid={}".format(sid)
                SESSIONS[sid] = [username]
                html = f"<html><head></head><body><h1>Poprawne logowanie</h1> <a href=\"/\"><button class=\"button\">Powrót</button></a></body></html>"
                #html = read_html_template('./templates/start_page.html')
            else:
                html = f"<html><head></head><body><h1>Niepoprawne dane</h1></body></html>"

                
            self.send_response(200, "OK")
            self.send_header('Content-type','text/html')
            if self.cookie:
                    self.send_header('Set-Cookie', self.cookie)
            self.end_headers()
            self.wfile.write(bytes(html, "utf-8"))


        if self.path == '/register':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                username = fields.get("username")[0]
                password = fields.get("password")[0]
                passwordRetype = fields.get("password_retype")[0]

                
                if password == passwordRetype:

                    #sprawdzanie czy juz jest taki uzytkownik
                    records = fetch_user_passwrd_by_username(username)
                    if len(records) <= 0 :
                        #dodawanie rekordu
                        insert_user_record(username, hash_password(password), "", "", "")
                        html = f"<html><head></head><body><h1>Poprawna rejestracja</h1></body></html> <a href=\"/\"><button class=\"button\">Powrót</button></a></body></html>"
                    else:
                        html = f"<html><head></head><body><h1>Taki uzytkownik juz istnieje</h1></body></html> <a href=\"/register_page\"><button class=\"button\">Powrót</button></a></body></html>"

                else:
                    html = f"<html><head></head><body><h1>Hasla nie pokrywaja sie</h1></body></html> <a href=\"/register_page\"><button class=\"button\">Powrót</button></a></body></html>"


                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(html, "utf-8"))


        if self.path == '/addCar':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                car_id = fields.get("car_id")[0]
                brand = fields.get("brand")[0]
                model = fields.get("model")[0]
                car_type = fields.get("car_type")[0]
                production_year = fields.get("production_year")[0]
                fuel_type = fields.get("fuel_type")[0]
                gearbox_type = fields.get("gearbox_type")[0]
                price = fields.get("price")[0]
                city = fields.get("city")[0]
                nr_of_cars = fields.get("nr_of_cars")[0]
                image = fields.get("img")[0]

            if car_id == "":
                insert_car_record(brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image)
                html = f"<html><head></head><body><h1>Dodano</h1></body></html>"
            else:
                edit_car_record(car_id, brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image)
                html = f"<html><head></head><body><h1>Zmieniono</h1></body></html>"
                
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(html, "utf-8"))

        if self.path == '/search_cars':
            
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            csearch = form.getvalue("csearch")

            self.path = './templates/customer/offer.html'
            file = read_html_template(self.path)
            file = insert_serached_cars(file, csearch)
            file = insert_login_button(self, file, SESSIONS)
            file = insert_autocomplete_data(file)
            file = insert_filter_options(file)
        
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))

        if self.path == '/filter_cars':
            
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            brand = form.getvalue("brand")
            car_type = form.getvalue("car_type")
            fuel_type = form.getvalue("fuel_type")
            gearbox_type = form.getvalue("gearbox_type")
            city = form.getvalue("city")

            self.path = './templates/customer/offer.html'
            file = read_html_template(self.path)
            file = insert_filtered_cars(file, brand, car_type, fuel_type, gearbox_type, city)
            file = insert_login_button(self, file, SESSIONS)
            file = insert_autocomplete_data(file)
            file = insert_filter_options(file)
        
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))

        if self.path == '/data_edit':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                username = fields.get("username")[0]
                password = fields.get("password")[0]
                passwordRetype = fields.get("password_retype")[0]
                name = fields.get("name")[0]
                surname = fields.get("surname")[0]
                email = fields.get("email")[0]

                
                if password == passwordRetype:
                    delete_user_record_by_username(username)
                    insert_user_record(username, hash_password(password), name, surname, email)
                    html = f"<html><head></head><body><h1>Dane zmienione</h1></body></html> <a href=\"/register_page\"><button class=\"button\">Powrót</button></a></body></html>"

                else:
                    html = f"<html><head></head><body><h1>Hasla nie pokrywaja sie</h1></body></html> <a href=\"/register_page\"><button class=\"button\">Powrót</button></a></body></html>"


                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(html, "utf-8"))

        if self.path == '/send_message':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                username = fields.get("username")[0]
                content = fields.get("content")[0]
                currentDateTime = datetime.datetime.now()

                if 0 == 0:
                    #TODO sprawdzanie odbiorcy
                    user_id = get_user_id_by_username(username)[0][0]
                    insert_message_record(user_id, content, "unread", currentDateTime)


                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes("ok", "utf-8"))



    def generate_sid(self):
        return "".join(str(randint(1,9)) for _ in range(100))

    def parse_cookies(self, cookie_list):
        return dict(((c.split("=")) for c in cookie_list.split(";"))) if cookie_list else {}
    
    def logout(self):
        if not self.user:
            return "Can't Log Out: No User Logged In"
        self.cookie = "sid="
        del SESSIONS[self.user]
        return "Logged Out"



if __name__ == "__main__":
    create_user_table()
    create_car_table()
    create_reservation_table()
    create_administrator_table()
    create_messages_table()

    server = HTTPServer((HOST, PORT), MyServer)
    print(f"Server started http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped successfully")
        sys.exit(0)


 