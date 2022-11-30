import re
import sys
import cgi
import os
from http.client import HTTP_PORT
from http.server import HTTPServer, BaseHTTPRequestHandler
from random import randint
import datetime
import uuid
import json

from requests import Request, post, get
from socketserver import ThreadingMixIn

from database.user_db import *
from database.reservation_db import *
from database.car_db import *
from database.messages_db import *
from login_service import *
from edit_templates import *
from server_service import *


HOST = "0.0.0.0"
PORT = 8080
SESSIONS = {}

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
dotenv.load_dotenv(verbose=True)


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

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
            file = read_html_template('./templates/customer/info.html')
            file = file.replace("$info", "Wylogowano")
            file = file.replace("$href", "")
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/register_page':
            self.path = './templates/customer/register_page.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/profile_page':
            self.path = './templates/customer/profile_page.html'

            if(hasattr(self, "user")):
                file = read_html_template(self.path)
                username = SESSIONS[self.user][0]
                file = insert_dataedit_button(file, username)
                file = insert_admin_page_button(file, username)
                file = insert_login_button(self, file, SESSIONS)
            else:
                file = "Musisz się zalogować"
            
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/data_edit':
            self.path = './templates/customer/data_edit.html'
            if(hasattr(self, "user")):
                file = read_html_template(self.path)
                username = SESSIONS[self.user][0]
                file = file.replace("$username", username)
            else:
                file = "Musisz się zalogować"

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

        if self.path[0:18] == '/make_reservation?':
            carId = int(self.path[25:])
            self.path = './templates/customer/make_reservation.html'

            if(hasattr(self, "user")):
                username = SESSIONS[self.user][0]

                dates_to_exclude = get_dates_to_exclude(carId)

                file = read_html_template(self.path)
                file = insert_login_button(self, file, SESSIONS)
                file = insert_reservation_form_info(file, carId, username, dates_to_exclude)
            else:
                file = "Musisz się zalogować"

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

            if(hasattr(self, "user")):
                file = read_html_template(self.path)
                file = insert_messages(self, file, SESSIONS)
            else:
                file = "Musisz się zalogować"

            
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path[-4:] == '.css':
            self.path = "./" + self.path.partition("/")[-1]
            file = read_html_template(self.path)
            
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path[-3:] == '.js':
            self.path = "./" + self.path.partition("/")[-1]
            file = read_html_template(self.path)
            
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/js')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))


        if self.path == '/githubauth':
            random_state = generate_state()
            params = {
                "client_id": CLIENT_ID,
                "redirect_uri": "http://localhost:8080/callback",
                "scope": "repo user",
                "state": random_state
            }

            authorize = Request("GET", "https://github.com/login/oauth/authorize", params=params).prepare()

            cookie = "state={}".format(random_state)
            self.send_response(302)
            self.send_header('Location',authorize.url)
            self.send_header('Set-Cookie', cookie)
            self.end_headers()

        if self.path[:9] == '/callback':
            file = read_html_template('./templates/customer/info.html')
            code = (re.search('code=(.*)&state=', self.path)).group(1)
            state = self.path.split("&state=",1)[1]

            if ("state" or " state" in cookies):
                if ("state" in cookies and state != cookies["state"]):
                    file = file.replace("$info", "State does not match. Possible authorization_code injection attempt")
                    file = file.replace("$href", "login_page")
                    
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(bytes(file, 'utf-8'))
                if (" state" in cookies and state != cookies[" state"]):
                    file = file.replace("$info", "State does not match. Possible authorization_code injection attempt")
                    file = file.replace("$href", "login_page")
                    
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(bytes(file, 'utf-8'))
            else:
                file = file.replace("$info", "Błąd autoryzacji")
                file = file.replace("$href", "login_page")

                self.send_response(400)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(bytes(file, 'utf-8'))

            #request token
            params = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code
            }
            resp = post("https://github.com/login/oauth/access_token", params=params)
            access_token = resp.text

            #request user data
            param = 'token ' + access_token[13:-36]
            url = 'https://api.github.com/user'
            headers = {"Authorization": param}

            respUserData = get(url=url, headers=headers)

            userData = json.loads(respUserData.text)
            username = "ghUser-" + userData["login"]

            add_gh_user(username)
            sid = self.generate_sid()
            self.cookie = "sid={}".format(sid)
            SESSIONS[sid] = [username]
            
            file = file.replace("$info", "Zalogowano przez GitHub OAuth Server")
            file = file.replace("$href", "")
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            if hasattr(self, 'cookie'):
                self.send_header('Set-Cookie', self.cookie)
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))
        



        #admin -------------------------------------------------

        if self.path == '/admin':
            verification = check_if_admin(self, SESSIONS)

            if verification == True:
                self.path = './templates/admin/admin_start_page.html'
                file = read_html_template(self.path)
            else:
                self.path = './templates/customer/info.html'
                file = read_html_template(self.path)
                file = file.replace("$info", "Nie jesteś adminem")
                file = file.replace("$href", "")

            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/admin/cars':
            verification = check_if_admin(self, SESSIONS)

            if verification == True:
                self.path = './templates/admin/admin_car_list.html'
                file = read_html_template(self.path)
                file = insert_car_table_for_admin(file)

            else:
                self.path = './templates/customer/info.html'
                file = read_html_template(self.path)
                file = file.replace("$info", "Nie jesteś adminem")
                file = file.replace("$href", "")

            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path[:23] == '/admin/edit_car?car_id=':
            
            verification = check_if_admin(self, SESSIONS)

            if verification == True:
                car_id = int(self.path[23:])
                self.path = './templates/admin/add_car.html'
                file = read_html_template(self.path)
                file = insert_edit_car_info(file, car_id)
            else:
                self.path = './templates/customer/info.html'
                file = read_html_template(self.path)
                file = file.replace("$info", "Nie jesteś adminem")
                file = file.replace("$href", "")

            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path[:23] == '/admin/add_car':
            verification = check_if_admin(self, SESSIONS)

            if verification == True:
                self.path = './templates/admin/add_car.html'
                file = read_html_template(self.path)
                file = insert_empty_info(file)
            else:
                self.path = './templates/customer/info.html'
                file = read_html_template(self.path)
                file = file.replace("$info", "Nie jesteś adminem")
                file = file.replace("$href", "")

            
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/admin/send_message':
            verification = check_if_admin(self, SESSIONS)

            if verification == True:
                self.path = './templates/admin/send_message.html'
                file = read_html_template(self.path)
            else:
                self.path = './templates/customer/info.html'
                file = read_html_template(self.path)
                file = file.replace("$info", "Nie jesteś adminem")
                file = file.replace("$href", "")

            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/admin/reservations':
            verification = check_if_admin(self, SESSIONS)

            if verification == True:
                self.path = './templates/admin/admin_reservations.html'
                file = read_html_template(self.path)
                file = insert_reservation_table_for_admin(file)

            else:
                self.path = './templates/customer/info.html'
                file = read_html_template(self.path)
                file = file.replace("$info", "Nie jesteś adminem")
                file = file.replace("$href", "")

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
            file = read_html_template('./templates/customer/info.html')

            if verification == True:
                sid = self.generate_sid()
                self.cookie = "sid={}".format(sid)
                SESSIONS[sid] = [username]

                userId = get_user_id_by_username(username)
                role = get_role_by_userid(userId)

                if role == "admin":
                    file = file.replace("$info", "Zalogowano jako admin <br><br> <a href=\"/\"><button class=\"button\">Wyświetl strone jaki klient</button></a><a href=\"/admin\"><button class=\"button\">Wyświetl strone admina</button></a>")
                    file = file.replace("$href", "")
                else:
                    file = file.replace("$info", "Zalogowano")
                    file = file.replace("$href", "")

            else:
                file = file.replace("$info", "Niepoprawne dane")
                file = file.replace("$href", "login_page")

                
            self.send_response(200, "OK")
            self.send_header('Content-type','text/html')
            if hasattr(self, 'cookie'):
                self.send_header('Set-Cookie', self.cookie)
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))


        if self.path == '/register':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            file = read_html_template('./templates/customer/info.html')

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
                        insert_user_record(username, hash_password(password), "", "", "", "client")
                        file = file.replace("$info", "Zarejestrowano")
                        file = file.replace("$href", "")
                    else:
                        file = file.replace("$info", "Taki użytkownik już istnieje")
                        file = file.replace("$href", "register_page")

                else:
                    file = file.replace("$info", "Hasła nie pokrywają się")
                    file = file.replace("$href", "register_page")


                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(file, "utf-8"))


        if self.path == '/addCar':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            file = read_html_template('./templates/customer/info.html')

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
                file = file.replace("$info", "Dodano")
                file = file.replace("$href", "admin")
            else:
                edit_car_record(car_id, brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image)
                file = file.replace("$info", "Zmieniono")
                file = file.replace("$href", "admin")
                
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))

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

            file = read_html_template('./templates/customer/info.html')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                username = fields.get("username")[0]
                password = fields.get("password")[0]
                passwordRetype = fields.get("password_retype")[0]
                name = fields.get("name")[0]
                surname = fields.get("surname")[0]
                email = fields.get("email")[0]

                
                if password == passwordRetype:
                    update_user_record(username, hash_password(password), name, surname, email)
                    file = file.replace("$info", "Dane zostały zmienione")
                    file = file.replace("$href", "data_edit")

                else:
                    file = file.replace("$info", "Hasła nie pokrywają się")
                    file = file.replace("$href", "data_edit")

                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(file, "utf-8"))

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
                    user_id = get_user_id_by_username(username)
                    insert_message_record(user_id, content, "unread", currentDateTime)


                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes("ok", "utf-8"))

        if self.path == '/makeReservation':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                car_id = fields.get("car_id")[0]
                user_id = fields.get("user_id")[0]
                start = fields.get("start")[0]
                end = fields.get("end")[0]
                name = fields.get("name")[0]
                surname = fields.get("surname")[0]
                phonenr = fields.get("phonenr")[0]
                email = fields.get("email")[0]

                car = fetch_car_by_id(car_id)

                car_name = car[0][1] + " - " + car[0][2]
                reservation_nr = str(uuid.uuid4().int)[:13]
                
                create_receipt(self, reservation_nr, name, surname, car_name, start, end)
                insert_reservation_record(reservation_nr ,start, end, car_id, user_id, name, surname, email, phonenr)

                
            

#------------------------------------------------------------------------------

    def generate_sid(self):
        return "".join(str(randint(1,9)) for _ in range(100))

    def parse_cookies(self, cookie_list):
        return dict(((c.split("=")) for c in cookie_list.split("; "))) if cookie_list else {}
    
    def logout(self):
        if not self.user:
            return "Can't Log Out: No User Logged In"
        self.cookie = "sid="
        del SESSIONS[self.user]
        return "Logged Out"

#------------------------------------------------------------------------------



#http server
def serve_on_port(port):
    print(f"Server started http://{HOST}:{port}")
    server = ThreadingHTTPServer((HOST,port), MyServer)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped successfully")
        sys.exit(0)


def start_app():
    create_user_table()
    create_car_table()
    create_reservation_table()
    create_messages_table()
    
    serve_on_port(8080)


if __name__ == "__main__":
    start_app()
 