import smtplib
import ssl
from email.message import EmailMessage
from time import sleep
from datetime import datetime, timedelta 
from uuid import uuid4
from database.user_db import *


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
