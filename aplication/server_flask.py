import re
import sys
import cgi
import os
from http.client import HTTP_PORT
from http.server import HTTPServer, BaseHTTPRequestHandler
from random import randint
import datetime

from flask import Flask
from flask import request, render_template
from flask import make_response
app = Flask(__name__)

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from barcode import EAN13
from barcode.writer import ImageWriter
import uuid

from socketserver import ThreadingMixIn

from matplotlib.style import use

from database.user_db import *
from database.reservation_db import *
from database.car_db import *
from database.administrator_db import *
from database.messages_db import *
from login_service import *
from edit_templates import *
from server_service import *
#from web_sockets import *

HOST = "0.0.0.0"
PORT = 8080
SESSIONS = {}







# cookies = self.parse_cookies(self.headers["Cookie"])
# if "sid" in cookies:
#     if (cookies["sid"] in SESSIONS):
#         self.user = cookies["sid"]

# if self.path == '/test':
#     self.path = './templates/test.php'
#     file = read_html_template(self.path)

        
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))  

@app.route('/', methods=["GET"])
def start_page():
    template_path = 'customer/start_page.html'
    file = read_html_template(template_path)
    #file = insert_login_button(self, file, SESSIONS)

    return render_template(file)

# if self.path == '/oferta':
#     self.path = './templates/customer/offer.html'
#     file = read_html_template(self.path)
    
#     file = insert_car_table(file)
#     file = insert_login_button(self, file, SESSIONS)
#     file = insert_autocomplete_data(file)
#     file = insert_filter_options(file)
        
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))  

# if self.path == '/login_page':
#     self.path = './templates/customer/login_page.html'
#     file = read_html_template(self.path)
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path == '/log_out':
#     self.logout()
#     file = read_html_template('./templates/customer/info.html')
#     file = file.replace("$info", "Wylogowano")
#     file = file.replace("$href", "")
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path == '/register_page':
#     self.path = './templates/customer/register_page.html'
#     file = read_html_template(self.path)
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path == '/profile_page':
#     self.path = './templates/customer/profile_page.html'
#     file = read_html_template(self.path)
#     file = insert_login_button(self, file, SESSIONS)
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path == '/data_edit':
#     self.path = './templates/customer/data_edit.html'
#     file = read_html_template(self.path)
#     username = SESSIONS[self.user][0]
#     file = file.replace("$username", username)
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path[0:10] == '/car_info?':
#     carId = int(self.path[17:])
#     self.path = './templates/customer/car_info.html'
#     file = read_html_template(self.path)

#     file = insert_car_info(file, carId)
#     file = insert_login_button(self, file, SESSIONS)
        
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path[0:18] == '/make_reservation?':
#     carId = int(self.path[25:])
#     self.path = './templates/customer/make_reservation.html'

#     if(hasattr(self, "user")):
#         username = SESSIONS[self.user][0]

#         dates_to_exclude = get_dates_to_exclude(carId)

#         file = read_html_template(self.path)
#         file = insert_login_button(self, file, SESSIONS)
#         file = insert_reservation_form_info(file, carId, username, dates_to_exclude)
#     else:
#         file = "Musisz się zalogować"

#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))


# if self.path[-4:] == '.png' or self.path[-4] == '.jpg':
#     self.path = "templates/" + self.path.partition("/")[-1]
#     data = read_bytes_from_file(self.path)
    
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'image/*')
#     self.end_headers()
#     self.wfile.write(data)

# if self.path == '/miasta':
#     self.path = './templates/customer/cities.html'
#     file = read_html_template(self.path)
#     file = insert_login_button(self, file, SESSIONS)
#     file = insert_cities_buttons(file)
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path == '/oNas':
#     self.path = './templates/customer/aboutus.html'
#     file = read_html_template(self.path)
#     file = insert_login_button(self, file, SESSIONS)
#     #file = insert_contact_information(file)
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path[:25] == '/getImageFromCarDb?carId=':
#     carId = self.path[25:]
#     data = getImageFromDBByCarId(carId)
    
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'image/*')
#     self.end_headers()
#     self.wfile.write(data)

# if self.path[0:13] == '/oferta?city=':
#     city = self.path[13:]
#     brand = "any"
#     car_type = "any"
#     fuel_type = "any"
#     gearbox_type = "any"

#     self.path = './templates/customer/offer.html'
#     file = read_html_template(self.path)
#     file = insert_filtered_cars(file, brand, car_type, fuel_type, gearbox_type, city)
#     file = insert_login_button(self, file, SESSIONS)

#     self.send_response(200, "OK")
#     self.end_headers()
#     self.wfile.write(bytes(file, "utf-8"))

# if self.path == '/messages':
#     self.path = './templates/customer/messages.html'
#     file = read_html_template(self.path)
#     file = insert_messages(self, file, SESSIONS)
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path[-4:] == '.css':
#     self.path = "./" + self.path.partition("/")[-1]
#     file = read_html_template(self.path)
    
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/css')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path[-3:] == '.js':
#     self.path = "./" + self.path.partition("/")[-1]
#     file = read_html_template(self.path)
    
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/js')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))



# #admin -------------------------------------------------

# if self.path == '/admin':
#     self.path = './templates/admin/admin_start_page.html'
#     file = read_html_template(self.path)
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path == '/admin/cars':
#     self.path = './templates/admin/admin_car_list.html'
#     file = read_html_template(self.path)
#     file = insert_car_table_for_admin(file)
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path[:23] == '/admin/edit_car?car_id=':
#     car_id = int(self.path[23:])
#     self.path = './templates/admin/add_car.html'
#     file = read_html_template(self.path)
#     file = insert_edit_car_info(file, car_id)
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path[:23] == '/admin/add_car':
#     self.path = './templates/admin/add_car.html'
#     file = read_html_template(self.path)
#     file = insert_empty_info(file)
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))

# if self.path == '/admin/send_message':
#     self.path = './templates/admin/send_message.html'
#     file = read_html_template(self.path)
#     self.send_response(200, "OK")
#     self.send_header('Content-type', 'text/html; charset=utf-8')
#     self.end_headers()
#     self.wfile.write(bytes(file, 'utf-8'))





    

#     def do_POST(self):
#         cookies = self.parse_cookies(self.headers["Cookie"])
#         if "sid" in cookies:
#             if (cookies["sid"] in SESSIONS):
#                 self.user = cookies["sid"]
                
#         if self.path == '/logIn':
#             ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
#             pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

#             if ctype == 'multipart/form-data':
#                 fields = cgi.parse_multipart(self.rfile, pdict)
#                 username = fields.get("username")[0]
#                 password = fields.get("password")[0]


#             #sprawdzanie zgodnosci hasla
#             verification = check_login_info(username, password)
#             file = read_html_template('./templates/customer/info.html')

#             if verification == True:
#                 sid = self.generate_sid()
#                 self.cookie = "sid={}".format(sid)
#                 SESSIONS[sid] = [username]
#                 file = file.replace("$info", "Zalogowano")
#                 file = file.replace("$href", "")

#             else:
#                 file = file.replace("$info", "Niepoprawne dane")
#                 file = file.replace("$href", "login_page")

                
#             self.send_response(200, "OK")
#             self.send_header('Content-type','text/html')
#             if hasattr(self, 'cookie'):
#                 self.send_header('Set-Cookie', self.cookie)
#             self.end_headers()
#             self.wfile.write(bytes(file, "utf-8"))


#         if self.path == '/register':
#             ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
#             pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
#             file = read_html_template('./templates/customer/info.html')

#             if ctype == 'multipart/form-data':
#                 fields = cgi.parse_multipart(self.rfile, pdict)
#                 username = fields.get("username")[0]
#                 password = fields.get("password")[0]
#                 passwordRetype = fields.get("password_retype")[0]

                
#                 if password == passwordRetype:

#                     #sprawdzanie czy juz jest taki uzytkownik
#                     records = fetch_user_passwrd_by_username(username)
#                     if len(records) <= 0 :
#                         #dodawanie rekordu
#                         insert_user_record(username, hash_password(password), "", "", "")
#                         file = file.replace("$info", "Zarejestrowano")
#                         file = file.replace("$href", "")
#                     else:
#                         file = file.replace("$info", "Taki użytkownik już istnieje")
#                         file = file.replace("$href", "register_page")

#                 else:
#                     file = file.replace("$info", "Hasła nie pokrywają się")
#                     file = file.replace("$href", "register_page")


#                 self.send_response(200, "OK")
#                 self.end_headers()
#                 self.wfile.write(bytes(file, "utf-8"))


#         if self.path == '/addCar':
#             ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
#             pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
#             file = read_html_template('./templates/customer/info.html')

#             if ctype == 'multipart/form-data':
#                 fields = cgi.parse_multipart(self.rfile, pdict)
#                 car_id = fields.get("car_id")[0]
#                 brand = fields.get("brand")[0]
#                 model = fields.get("model")[0]
#                 car_type = fields.get("car_type")[0]
#                 production_year = fields.get("production_year")[0]
#                 fuel_type = fields.get("fuel_type")[0]
#                 gearbox_type = fields.get("gearbox_type")[0]
#                 price = fields.get("price")[0]
#                 city = fields.get("city")[0]
#                 nr_of_cars = fields.get("nr_of_cars")[0]
#                 image = fields.get("img")[0]

#             if car_id == "":
#                 insert_car_record(brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image)
#                 file = file.replace("$info", "Dodano")
#                 file = file.replace("$href", "admin")
#             else:
#                 edit_car_record(car_id, brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, nr_of_cars, image)
#                 file = file.replace("$info", "Zmieniono")
#                 file = file.replace("$href", "admin")
                
#             self.send_response(200, "OK")
#             self.end_headers()
#             self.wfile.write(bytes(file, "utf-8"))

#         if self.path == '/search_cars':
            
#             form = cgi.FieldStorage(
#                 fp=self.rfile,
#                 headers=self.headers,
#                 environ={'REQUEST_METHOD': 'POST'}
#             )
#             csearch = form.getvalue("csearch")

#             self.path = './templates/customer/offer.html'
#             file = read_html_template(self.path)
#             file = insert_serached_cars(file, csearch)
#             file = insert_login_button(self, file, SESSIONS)
#             file = insert_autocomplete_data(file)
#             file = insert_filter_options(file)
        
#             self.send_response(200, "OK")
#             self.end_headers()
#             self.wfile.write(bytes(file, "utf-8"))

#         if self.path == '/filter_cars':
            
#             form = cgi.FieldStorage(
#                 fp=self.rfile,
#                 headers=self.headers,
#                 environ={'REQUEST_METHOD': 'POST'}
#             )
            
#             brand = form.getvalue("brand")
#             car_type = form.getvalue("car_type")
#             fuel_type = form.getvalue("fuel_type")
#             gearbox_type = form.getvalue("gearbox_type")
#             city = form.getvalue("city")

#             self.path = './templates/customer/offer.html'
#             file = read_html_template(self.path)
#             file = insert_filtered_cars(file, brand, car_type, fuel_type, gearbox_type, city)
#             file = insert_login_button(self, file, SESSIONS)
#             file = insert_autocomplete_data(file)
#             file = insert_filter_options(file)
        
#             self.send_response(200, "OK")
#             self.end_headers()
#             self.wfile.write(bytes(file, "utf-8"))

#         if self.path == '/data_edit':
#             ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
#             pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

#             file = read_html_template('./templates/customer/info.html')

#             if ctype == 'multipart/form-data':
#                 fields = cgi.parse_multipart(self.rfile, pdict)
#                 username = fields.get("username")[0]
#                 password = fields.get("password")[0]
#                 passwordRetype = fields.get("password_retype")[0]
#                 name = fields.get("name")[0]
#                 surname = fields.get("surname")[0]
#                 email = fields.get("email")[0]

                
#                 if password == passwordRetype:
#                     delete_user_record_by_username(username)
#                     insert_user_record(username, hash_password(password), name, surname, email)
#                     file = file.replace("$info", "Dane zostały zmienione")
#                     file = file.replace("$href", "data_edit")

#                 else:
#                     file = file.replace("$info", "Hasła nie pokrywają się")
#                     file = file.replace("$href", "data_edit")

#                 self.send_response(200, "OK")
#                 self.end_headers()
#                 self.wfile.write(bytes(file, "utf-8"))

#         if self.path == '/send_message':
#             ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
#             pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

#             if ctype == 'multipart/form-data':
#                 fields = cgi.parse_multipart(self.rfile, pdict)
#                 username = fields.get("username")[0]
#                 content = fields.get("content")[0]
#                 currentDateTime = datetime.datetime.now()

#                 if 0 == 0:
#                     #TODO sprawdzanie odbiorcy
#                     user_id = get_user_id_by_username(username)[0][0]
#                     insert_message_record(user_id, content, "unread", currentDateTime)


#                 self.send_response(200, "OK")
#                 self.end_headers()
#                 self.wfile.write(bytes("ok", "utf-8"))

#         if self.path == '/makeReservation':
#             ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
#             pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

#             if ctype == 'multipart/form-data':
#                 fields = cgi.parse_multipart(self.rfile, pdict)
#                 car_id = fields.get("car_id")[0]
#                 user_id = fields.get("user_id")[0]
#                 start = fields.get("start")[0]
#                 end = fields.get("end")[0]
#                 name = fields.get("name")[0]
#                 surname = fields.get("surname")[0]

#                 car = fetch_car_by_id(car_id)

#                 car_name = car[0][1] + " - " + car[0][2]
#                 reservation_nr = str(uuid.uuid4().int)[:13]
                
#                 create_receipt(self, reservation_nr, name, surname, car_name, start, end)
#                 insert_reservation_record(reservation_nr ,start, end, car_id, user_id)

                
            



#     def generate_sid(self):
#         return "".join(str(randint(1,9)) for _ in range(100))

#     def parse_cookies(self, cookie_list):
#         return dict(((c.split("=")) for c in cookie_list.split(";"))) if cookie_list else {}
    
#     def logout(self):
#         if not self.user:
#             return "Can't Log Out: No User Logged In"
#         self.cookie = "sid="
#         del SESSIONS[self.user]
#         return "Logged Out"

# #------------------------------------------------------------------------------



# #http server
# def serve_on_port(port):
#     print(f"Server started http://{HOST}:{port}")
#     server = ThreadingHTTPServer((HOST,port), MyServer)
#     try:
#         server.serve_forever()
#     except KeyboardInterrupt:
#         server.server_close()
#         print("Server stopped successfully")
#         sys.exit(0)


# def start_app():
#     create_user_table()
#     create_car_table()
#     create_reservation_table()
#     create_administrator_table()
#     create_messages_table()
    
#     serve_on_port(8080)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
 