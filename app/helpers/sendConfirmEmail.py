from app.helpers.sendmail import send_email
from itsdangerous import URLSafeTimedSerializer
from app import app
from flask import url_for, render_template


def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    confirm_url = url_for(
        'auth.confirm_email',
        token=confirm_serializer.dumps(user_email, salt='HOLY_SHIT'),
        _external=True
    )
    html = render_template(
        'email_confirmation.html',
        confirm_url = confirm_url
    )
    send_email('Confirm Your Email Address', [user_email], 'Confirm Email Address', html)
