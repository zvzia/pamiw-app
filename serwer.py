import sys
import cgi
from http.client import HTTP_PORT
from http.server import HTTPServer, BaseHTTPRequestHandler

from numpy import record
from database.db import create_table, insert_record, fetch_records, fetch_record_by_username

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
    records = fetch_record_by_username(username)
    if (len(records) > 0):
        passwordInDb = records[0][0]
        if (password == passwordInDb):
            return True
    
    return False


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = './templates/start_page.html'
            file = read_html_template(self.path)
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

    def do_POST(self):
        if self.path == '/logIn':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                username = fields.get("username")[0]
                password = fields.get("password")[0]

            # tworzenie tabeli jesli pierwszy raz
            create_table()

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
                    #tworzenie tabeli jesli pierwszy raz
                    create_table()

                    #sprawdzanie czy juz jest taki uzytkownik
                    records = fetch_record_by_username(username)
                    if len(records) < 0 :
                        #dodawanie rekordu
                        insert_record(username, password)
                        html = f"<html><head></head><body><h1>Poprawna rejestracja</h1></body></html>"
                    else:
                        html = f"<html><head></head><body><h1>Taki uzytkownik juz istnieje</h1></body></html>"

                else:
                    html = f"<html><head></head><body><h1>Hasla nie pokrywaja sie</h1></body></html>"


                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(html, "utf-8"))



if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), MyServer)
    print(f"Server started http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped successfully")
        sys.exit(0)

"""
server = HTTPServer((HOST, PORT), MyServer)
print("Server running")
server.serve_forever()
server.server_close()
print("Server stopped")
"""
 