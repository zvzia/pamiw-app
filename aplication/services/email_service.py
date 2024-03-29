import smtplib, os, ssl, dotenv
from email.message import EmailMessage
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from barcode import EAN13
from barcode.writer import ImageWriter

from database.user_db import *
from services.email_service import *


import dotenv, os
dotenv.load_dotenv(verbose=True)

def send_email(email_receiver, subject, body, receipt_path):
    try:
        email_sender = "carrentalpamiw@gmail.com"
        email_password = os.getenv("EMAIL_PASS")
        
        # create email
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg.set_content(body)

        with open(receipt_path, 'rb') as content_file:
            content = content_file.read()
            msg.add_attachment(content, maintype='application', subtype='pdf', filename='example.pdf')

        context = ssl.create_default_context()
        # send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, msg.as_string())
        return True
    except Exception as e:
        print("Problem during send email")
        print(str(e))
    return False


def send_email_with_receipt(receipt_path, receiver_id, receiver_email):
    #sleep(3)
    user_info = get_user_info_by_id(receiver_id)
    username = user_info[1]
    email = receiver_email

    subject = "Potwierdzenie rezerwacji"
    body = """
    Witaj """ + username + """
    W załączniku znajduję się potwierdzeni twojej rezerwacji
    """ 

    return send_email(email, subject, body, receipt_path)

def create_receipt(reservation_nr, name, surname, car_name, start, end, user_id, email):
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
