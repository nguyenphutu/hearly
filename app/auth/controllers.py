import datetime
import re
from flask import Blueprint, render_template, request, redirect, flash, g, json
from flask_login import UserMixin, login_user, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import exc
from app import login_manager, app
from app.helpers.sendConfirmEmail import send_confirmation_email
from app.models import Users, db, InviteCode
import bugsnag

# Initialize blueprint for auth
auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


# Sample user
class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)


@auth.before_request
def before_request():
    g.user = current_user


####################
#### ajax login ####
####################
@auth.route('/ajax/login', methods=['POST'])
def ajaxlogin():
    email = request.form['email']
    password = request.form['password']
    registered_user = Users.query.filter_by(email=email).first()
    if registered_user is not None and registered_user.check_password(password):
        login_user(registered_user, remember=True)
        registered_user.authenticated = True
        db.session.add(registered_user)
        db.session.commit()
        return json.dumps({'status': 'OK', 'content': 'Login successful, redirecting to home...'})
    else:
        return json.dumps({'status': 'FAILED', 'content': 'Invalid credential. Try Again!'})


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@auth.route('/ajax/register', methods=['POST'])
def register():
    coupon_code = request.form['coupon_code']
    coupon = InviteCode.query.filter_by(invite_code=coupon_code).first()
    if coupon is not None:
        try:
            email = request.form['email']
            email_pattern = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
            if not email_pattern.match(email):
                return json.dumps({'status': 'FAILED', 'content': 'Invalid email format! The email is formatted like abc@example.com'})
            try:
                user = Users(password=request.form['password'], email=email, username=email.split('@')[0],fullname=request.form['fullname'], bio='Becoming Hollywood Citizen', country='VN')
                db.session.add(user)
                db.session.commit()
            except:
                bugsnag.notify('Error when insert data to users table')
            # Send Email
            send_confirmation_email(request.form['email'])
            login_user(user, remember='True')
            # delete coupon
            db.session.delete(coupon)
            db.session.commit()
            return json.dumps({'status': 'OK', 'content': 'Thanks for registered with Hearly. Please check your inbox to verify email!'})
        except exc.IntegrityError:
            bugsnag.notify("Data duplicate on User table")
            db.session.rollback()
            return json.dumps({'status': 'FAILED', 'content': 'This email already associated with an account!'})
    else:
        return json.dumps({'status': 'FAILED', 'content': 'Invalid invite code!'})


@auth.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='HOLY_SHIT', max_age=604800)
    except:
        return "The confirmation link is invalid or has expired."

    user = Users.query.filter_by(email=email).first()

    if user.email_confirmed:
        return "Account already confirmed. Please login."
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        return "Thank you for confirming your email address! You can close this windows."

    return redirect('/home')


@auth.route('/forgot')
def auth_forgot_password():
    return render_template('forgot-password.html')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect('/')
