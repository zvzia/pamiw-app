import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from barcode import EAN13
from barcode.writer import ImageWriter
import dotenv, random, string, os


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

def create_receipt(self, reservation_nr, name, surname, car_name, start, end):
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

    file = read_bytes_from_file("tmp/Potwierdzenie.pdf")
    self.send_response(200, "OK")
    self.send_header('Content-type', 'application/pdf')
    self.end_headers()
    self.wfile.write(file)

    os.remove("tmp/ean.png")
    os.remove("tmp/Potwierdzenie.pdf")

def generate_state(length=30):
  char = string.ascii_letters + string.digits
  rand = random.SystemRandom()
  return ''.join(rand.choice(char) for _ in range(length))