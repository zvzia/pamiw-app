import re
import sys
import cgi
from http.client import HTTP_PORT
from http.server import HTTPServer, BaseHTTPRequestHandler


from numpy import record
from database.user_db import *
from database.reservation_db import *
from database.car_db import *
from database.administrator_db import *
from passwd_crypt import *

HOST = "localhost"
PORT = 8080

def read_html_template(path):
    try:
        with open(path, encoding='utf-8') as f:
            file = f.read()
    except Exception as e:
        file = e
    return file

def check_login_info(username, password):
    records = fetch_user_record_by_username(username)
    if (len(records) > 0):
        passwordInDb = records[0][0]
        return check_password(password, passwordInDb)
    
    return False

def insert_car_table(file):
    data = fetch_car_records()
    html_string =""
    for row in data:
        html_string +="<tr>"
        for col in row:
            html_string += "<td>" + str(col) + "</td>"
        html_string +="</tr>"
    
    result = file.replace("tabelatutaj", html_string)
    return result



class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = './templates/start_page.html'
            file = read_html_template(self.path)
            
            file = insert_car_table(file)

            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/login_page':
            self.path = './templates/login_page.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/register_page':
            self.path = './templates/register_page.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/admin_start_page':
            self.path = './templates/admin_start_page.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

        if self.path == '/admin_start_page/cars':
            self.path = './templates/admin_car_list.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(file, 'utf-8'))

    def do_POST(self):
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
                html = f"<html><head></head><body><h1>Poprawne logowanie</h1></body></html>"
            else:
                html = f"<html><head></head><body><h1>Niepoprawne dane</h1></body></html>"

                
            self.send_response(200, "OK")
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
                    records = fetch_user_record_by_username(username)
                    if len(records) <= 0 :
                        #dodawanie rekordu
                        insert_user_record(username, hash_password(password))
                        html = f"<html><head></head><body><h1>Poprawna rejestracja</h1></body></html>"
                    else:
                        html = f"<html><head></head><body><h1>Taki uzytkownik juz istnieje</h1></body></html>"

                else:
                    html = f"<html><head></head><body><h1>Hasla nie pokrywaja sie</h1></body></html>"


                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(html, "utf-8"))


        if self.path == '/addCar':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                brand = fields.get("brand")[0]
                model = fields.get("model")[0]
                car_type = fields.get("car_type")[0]
                production_year = fields.get("production_year")[0]
                fuel_type = fields.get("fuel_type")[0]
                gearbox_type = fields.get("gearbox_type")[0]
                price = fields.get("price")[0]
                city = fields.get("city")[0]
                model = fields.get("model")[0]

            
            insert_car_record(brand, model, car_type, production_year, fuel_type, gearbox_type, price, city)

            html = f"<html><head></head><body><h1>Poprawna rejestracja</h1></body></html>"
                
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(html, "utf-8"))



if __name__ == "__main__":
    create_user_table()
    create_car_table()
    create_reservation_table()
    create_administrator_table()

    server = HTTPServer((HOST, PORT), MyServer)
    print(f"Server started http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped successfully")
        sys.exit(0)


 