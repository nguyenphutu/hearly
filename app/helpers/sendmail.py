from app import mail
from flask_mail import Message
from app import app
import threading
from flask import render_template

# Handling Async, run in background
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

# Helpers to send mail
def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = threading.Thread(target=send_async_email, args=[msg])
    thr.start()
