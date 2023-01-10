import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from barcode import EAN13
from barcode.writer import ImageWriter
import dotenv, random, string, os
from database.user_db import *
from services.email_service import *


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

def create_receipt(self, reservation_nr, name, surname, car_name, start, end, user_id, email):
    my_code = EAN13(reservation_nr, writer=ImageWriter())
    my_code.save("tmp/ean")

    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    my_canvas = canvas.Canvas("tmp/Potwierdzenie.pdf", pagesize=A4)
    my_canvas.setFont("Arial", 14)
    my_canvas.drawString(100, 750, "Numer rezerwacji: " + reservation_nr)
    my_canvas.drawString(100, 730, "Imię i Nazwisko: " + name + " " + surname)
    my_canvas.drawString(100, 710, "Samochód: " + car_name)
    my_canvas.drawString(100, 690, "Od: " + start)
    my_canvas.drawString(100, 670, "Do: " + end)
    my_canvas.drawImage("tmp/ean.png", 350, 650, 200, 107)
    my_canvas.save()

    succes = send_email_with_receipt("tmp/Potwierdzenie.pdf", user_id, email)

    if(succes):
        os.remove("tmp/ean.png")
        os.remove("tmp/Potwierdzenie.pdf")

def generate_state(length=30):
  char = string.ascii_letters + string.digits
  rand = random.SystemRandom()
  return ''.join(rand.choice(char) for _ in range(length))

def check_if_admin(self, sessions):
    if hasattr(self, 'user'):
        username = sessions[self.user][0]
        userId = get_user_id_by_username(username)
        role = get_role_by_userid(userId)
    else:
        return False

    if role == "admin":
        return True
    else:
        return False
