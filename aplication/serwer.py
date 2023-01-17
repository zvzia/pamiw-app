from flask import Flask, render_template, request, make_response, redirect, Response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from os.path import exists
from collections import deque
import os
from datetime import datetime
import uuid
import json

from requests import Request, post, get

from database.user_db import *
from database.reservation_db import *
from database.car_db import *
from database.messages_db import *

from services.email_service import *
from services.server_service import *
from services.login_service import *
from services.templates_service import *


HOST = "0.0.0.0"
PORT = 8080
SESSIONS = {}

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
dotenv.load_dotenv(verbose=True)

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = "2c27100cd9cc4fb382205bfaf222a17c14f617c58fda485da16b0f6a14b4fd1c"

DATABASE = "./databese/car_rental.db"

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username is None:
        return None

    row = get_user_by_username(username)
    try:
        username = row[1]
        password = row[2]
    except:
        return None

    user = User()
    user.id = username
    user.username = username
    user.password = password
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = user_loader(username)
    return user

recent_users = deque(maxlen=3)


@app.route("/", methods=['GET'])
def start():
    if request.method == 'GET':
        
        if current_user.is_authenticated:
            logged = True
            username = current_user.username
            unread_messages = check_for_unread_messages(username)
        else:
            logged = False
            unread_messages = False

        return render_template("customer/start_page.html", logged=logged, unread_messages=unread_messages)

@app.route("/oferta", methods=['GET'])
def offer():
    if request.method == 'GET':
        city  = request.args.get('city', None)

        if current_user.is_authenticated:
            logged = True
            username = current_user.username
            unread_messages = check_for_unread_messages(username)
        else:
            logged = False
            unread_messages = False
        
        autocomplete_data = get_autocomplete_data()
        filter_options = get_filter_options()

        if city is None:
            cars = fetch_car_records()
            return render_template("customer/offer.html", logged=logged, unread_messages=unread_messages, cars=cars, autocompleteData=json.dumps(autocomplete_data), filterOptions=filter_options )

        else:
            brand = "any"
            car_type = "any"
            fuel_type = "any"
            gearbox_type = "any"

            cars = fetch_car_records_by_filter_conditions(brand, car_type, fuel_type, gearbox_type, city)
            return render_template("customer/offer.html", logged=logged, unread_messages=unread_messages, cars=cars, autocompleteData=json.dumps(autocomplete_data), filterOptions=filter_options)

@app.route("/search_cars", methods=['POST'])
def search_cars():
    if request.method == 'POST':
        csearch = request.form.get("csearch")

        if current_user.is_authenticated:
            logged = True
            username = current_user.username
            unread_messages = check_for_unread_messages(username)
        else:
            logged = False
            unread_messages = False

        cars = get_serached_cars(csearch)
        autocomplete_data = get_autocomplete_data()
        filter_options = get_filter_options()

        return render_template("customer/offer.html", logged=logged, unread_messages=unread_messages, cars=cars, autocompleteData=json.dumps(autocomplete_data), filterOptions=filter_options)

@app.route("/filter_cars", methods=['POST'])
def filter_cars():
    if request.method == 'POST':
        brand = request.form.get("brand")
        car_type = request.form.get("car_type")
        fuel_type = request.form.get("fuel_type")
        gearbox_type = request.form.get("gearbox_type")
        city = request.form.get("city")

        if current_user.is_authenticated:
            logged = True
            username = current_user.username
            unread_messages = check_for_unread_messages(username)
        else:
            logged = False
            unread_messages = False

        cars = get_filtered_cars( brand, car_type, fuel_type, gearbox_type, city)
        autocomplete_data = get_autocomplete_data()
        filter_options = get_filter_options()

        return render_template("customer/offer.html", logged=logged, unread_messages=unread_messages, cars=cars, autocompleteData=json.dumps(autocomplete_data), filterOptions=filter_options)


@app.route("/login_page", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("customer/login_page.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = user_loader(username)

        if user is None:
            return "Nieprawidłowy login lub hasło", 401
        
        if(password == '' or username == ''):
            return "Nieprawidłowy login lub hasło", 401

        if check_password(password, user.password):
            login_user(user)
            role = get_role_by_username(username)
            if role == "admin":
                return redirect('/admin')
            else:
                return redirect('/')
        else:
            return "Nieprawidłowy login lub hasło", 401

@app.route("/log_out")
def logout():
    logout_user()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("customer/register_page.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_retyped = request.form.get("password_retyped")

        
        if password == password_retyped:
            #sprawdzanie czy juz jest taki uzytkownik
            records = fetch_user_passwrd_by_username(username)
            if len(records) <= 0 :
                #dodawanie rekordu
                insert_user_record(username, hash_password(password), "", "", "", "client")

                user = user_loader(username)
                login_user(user)
                return redirect('/start_page')
            else:
                return render_template("customer/info.html", info="Taki użytkownik już istnieje", href="register_page")
        else:
            return render_template("customer/info.html", info="Hasła nie pokrywają się", href="register_page")

@app.route("/profile_page", methods=['GET'])
@login_required
def profilePage():
    username = current_user.username
    role = get_role_by_username(username)[0]
    unread_messages = check_for_unread_messages(username)

    return render_template("customer/profile_page.html", role=role, logged=True, unread_messages=unread_messages)

@app.route("/data_edit", methods=["GET","POST"])
@login_required
def dataEdit():
    if request.method == "GET":
        return render_template("customer/data_edit.html", username=current_user.username)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_retyped = request.form.get("password_retyped")
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("email")
        
        if password == password_retyped:
            update_user_record(username, hash_password(password), name, surname, email)
            return render_template("customer/info.html", info="Dane zostały zmienione", href="data_edit")
        else:
            return render_template("customer/info.html", info="Hasła nie pokrywają się", href="data_edit")

@app.route("/car_info", methods=['GET'])
def carInfo():
    if request.method == 'GET':
        if current_user.is_authenticated:
            logged = True
            username = current_user.username
            unread_messages = check_for_unread_messages(username)
        else:
            logged = False
            unread_messages = False

        carId  = request.args.get('car_id', None)
        car_info = get_car_info(carId)

        return render_template("customer/car_info.html", logged=logged, unread_messages=unread_messages, info=car_info)

@app.route("/make_reservation", methods=['GET', 'POST'])
@login_required
def make_reservation():
    if request.method == 'GET':
        carId  = request.args.get('car_id', None)

        if current_user.is_authenticated:
            logged = True
            username = current_user.username
            unread_messages = check_for_unread_messages(username)
        else:
            logged = False
            unread_messages = False

        dates_to_exclude = get_dates_to_exclude(carId)

        info = get_reservation_form_info(carId, username)

        return render_template("customer/make_reservation.html", logged=logged, unread_messages=unread_messages, info=info, excludedates=json.dumps(dates_to_exclude))
    
    if request.method == 'POST':
        car_id = request.form.get("car_id")
        user_id = request.form.get("user_id")
        start = request.form.get("start")
        end = request.form.get("end")
        name = request.form.get("name")
        surname = request.form.get("surname")
        phonenr = request.form.get("phonenr")
        email = request.form.get("email")

        car = fetch_car_by_id(car_id)

        car_name = car[0][1] + " - " + car[0][2]
        reservation_nr = str(uuid.uuid4().int)[:13]
                
        create_receipt(reservation_nr, name, surname, car_name, start, end, user_id, email)
        insert_reservation_record(reservation_nr ,start, end, car_id, user_id, name, surname, email, phonenr)

        return render_template("customer/info.html", info="Potwierdzenie rezerwacji zostało wysłane na Twój adres email.", href="")

@app.route("/miasta", methods=['GET'])
def cities():
    if request.method == 'GET':
        if current_user.is_authenticated:
            logged = True
            username = current_user.username
            unread_messages = check_for_unread_messages(username)
        else:
            logged = False
            unread_messages = False

        cities = get_cities()
        return render_template("customer/cities.html", logged=logged, unread_messages=unread_messages, cities=cities)

@app.route("/oNas", methods=['GET'])
def about_us():
    if request.method == 'GET':
        if current_user.is_authenticated:
            logged = True
            username = current_user.username
            unread_messages = check_for_unread_messages(username)
        else:
            logged = False
            unread_messages = False

        #info = get_contact_information()
        return render_template("customer/aboutus.html", logged=logged, unread_messages=unread_messages)

@app.route("/messages", methods=['GET'])
@login_required
def messages():
    if request.method == 'GET':
        
        messages = get_messages(current_user.username)
        return render_template("customer/messages.html", messages=messages, username=current_user.username)

@app.route("/githubauth", methods=['GET'])
def githubauth():
    random_state = generate_state()
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": "http://127.0.0.1:8080/callback",
        "scope": "repo user",
        "state": random_state
    }

    authorize = Request("GET", "https://github.com/login/oauth/authorize", params=params).prepare()

    resp = make_response(redirect(authorize.url))
    resp.set_cookie('state', random_state)

    return resp

@app.route("/callback", methods=['GET'])
def callback():
    code  = request.args.get('code', None)
    state  = request.args.get('state', None)

    state_cookie = request.cookies.get('state')

    if (state_cookie != None):
        if (state != state_cookie):
            return render_template("customer/info.html", info="State does not match. Possible authorization_code injection attempt", href="login_page")
    else:
        return render_template("customer/info.html", info="Błąd autoryzacji", href="login_page")

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

    user = user_loader(username)
    login_user(user)

    return redirect('/')


#admin-----------------------------------------------------------

@app.route("/admin", methods=['GET'])
@login_required
def admin():
    if request.method == 'GET':
        verification = check_if_admin(current_user.username)

        if verification == True:
            return render_template("admin/admin_start_page.html")
        else:
            return render_template("customer/info.html", info="Nie jesteś adminem", href="")

@app.route("/admin/cars", methods=['GET'])
@login_required
def admin_cars():
    if request.method == 'GET':
        verification = check_if_admin(current_user.username)

        if verification == True:
            cars = get_cars_for_admin()
            return render_template("admin/admin_car_list.html", cars=cars)
        else:
            return render_template("customer/info.html", info="Nie jesteś adminem", href="")


@app.route("/admin/edit_car", methods=['GET'])
@login_required
def admin_editcar():
    if request.method == 'GET':
        verification = check_if_admin(current_user.username)

        if verification == True:
            car_id  = request.args.get('car_id', None)
            info = get_edit_car_info( car_id)
            return render_template("admin/add_car.html", info=info)
        else:
            return render_template("customer/info.html", info="Nie jesteś adminem", href="")

@app.route("/admin/add_car", methods=['GET', 'POST'])
@login_required
def admin_addcar():
    if request.method == 'GET':
        verification = check_if_admin(current_user.username)

        if verification == True:
            info = get_empty_info()
            return render_template("admin/add_car.html", info=info)
        else:
            return render_template("customer/info.html", info="Nie jesteś adminem", href="")

    if request.method == 'POST':
        car_id = request.form.get("car_id")
        brand = request.form.get("brand")
        model = request.form.get("model")
        car_type = request.form.get("car_type")
        production_year = request.form.get("production_year")
        fuel_type = request.form.get("fuel_type")
        gearbox_type = request.form.get("gearbox_type")
        price = request.form.get("price")
        city = request.form.get("city")
        image = request.form.get("image")

        if car_id == "":
            insert_car_record(brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, image)
            return render_template("customer/info.html", info="Dodano", href="admin")
        else:
            edit_car_record(car_id, brand, model, car_type, production_year, fuel_type, gearbox_type, price, city, image)
            return render_template("customer/info.html", info="Zmieniono", href="admin")

@app.route("/admin/send_message", methods=['GET', 'POST'])
@login_required
def send_message():
    if request.method == 'GET':
        verification = check_if_admin(current_user.username)

        if verification == True:
            return render_template("admin/send_message.html")
        else:
            return render_template("customer/info.html", info="Nie jesteś adminem", href="")
    
    if request.method == 'POST':
        username = request.form.get("username")
        content = request.form.get("content")
        currentDateTime = datetime.now()

        if 0 == 0:
            #TODO sprawdzanie odbiorcy
            user_id = get_user_id_by_username(username)
            insert_message_record(user_id, content, "unread", currentDateTime)
            global messStatus
            messStatus = True

        return render_template("customer/info.html", info="Wiadomość została wysłana", href="admin")

@app.route("/admin/reservations", methods=['GET'])
@login_required
def reservations():
    if request.method == 'GET':
        verification = check_if_admin(current_user.username)

        if verification == True:
            reservations = get_reservations_for_admin()
            return render_template("admin/admin_reservations.html", reservations=reservations)
        else:
            return render_template("customer/info.html", info="Nie jesteś adminem", href="")

@app.route("/admin/company_info", methods=['GET', 'POST'])
@login_required
def company_info():
    if request.method == 'GET':
        verification = check_if_admin(current_user.username)

        if verification == True:
            info = get_company_info()
            return render_template("admin/company_info.html", info=info)
        else:
            return render_template("customer/info.html", info="Nie jesteś adminem", href="")

    if request.method == 'POST':
        description = request.form.get("description")
        phonenr = request.form.get("phonenr")
        email = request.form.get("email")

        save_info(description, phonenr, email)
        return render_template("customer/info.html", info="Zaktualizowano informacje", href="admin")


#---------------------------------------------------------------
@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'GET':
        verification = check_if_admin(current_user.username)

        if verification == True:
            return render_template("admin/upload_video.html")
        else:
            return render_template("customer/info.html", info="Nie jesteś adminem", href="")

    if request.method == 'POST':
        file = request.files["file"]
        current_chunk = int(request.form["dzchunkindex"])

        if current_chunk == 0:
            if exists("database/data/video.mp4"):
                os.rename("database/data/video.mp4", "database/data/video_old.mp4")

        save_path = "database/data/video.mp4"
        with open(save_path, "ab") as f:
            f.seek(int(request.form["dzchunkbyteoffset"]))
            f.write(file.stream.read())

        total_chunks = int(request.form["dztotalchunkcount"])

        # Add 1 since current_chunk is zero-indexed
        if current_chunk + 1 == total_chunks:
            # This was the last chunk, the file should be complete and the size we expect
            if os.path.getsize(save_path) != int(request.form["dztotalfilesize"]):
                return "Size mismatch.", 500
            if exists("database/data/video_old.mp4"):
                os.remove("database/data/video_old.mp4")

        return "Chunk upload successful.", 200

@app.route("/getImageFromCarDb", methods=['GET'])
def getImage():
    carId  = request.args.get('carId', None)
    data = getImageFromDBByCarId(carId)
    return data

@app.route("/background2.png", methods=['GET'])
def background():
    data = read_bytes_from_file("templates/background2.png")
    return data

@app.route("/database/data/<filename>", methods=['GET'])
def getfile(filename):
    data = read_bytes_from_file("database/data/" + filename)
    return data


messStatus = False

@app.route("/listen/<username>")
def listen(username):
    def respond_to_client():
        global messStatus
        if messStatus:
            messStatus = False
            print("*****")
            message = get_user_new_message(username)
            if message != None:
                content = message[2]
                currentDateTime = message[4][:-10]
                change_message_status_by_id(message[0], "read")

                _data = json.dumps({"content":content, "date":currentDateTime})
                yield f"id: 1\ndata: {_data}\nevent: online\n\n"
    
    return Response(respond_to_client(), mimetype='text/event-stream')



if __name__ == "__main__":
    create_user_table()
    create_car_table()
    create_reservation_table()
    create_messages_table()
    
    app.run(host="0.0.0.0", port=8080)
 