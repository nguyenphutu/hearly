from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user

from app.models import Users, Score

profile = Blueprint('profile', __name__, url_prefix='/profile', template_folder='templates')


@profile.route('/')
@login_required
def get_username():
    username = current_user.username
    return redirect('/profile/@' + username)


@profile.route('/@<username>')
@login_required
def profile_index(username):
    user_profile = Users.query.filter_by(username=username).first()
    user_score = Score.query.filter_by(user_u_email=current_user.email).first()
    return render_template('profile.html', user_profile=user_profile, user_score=user_score)



@profile.route('/settings')
def settings_account():
    return render_template('settings-account.html')


@profile.route('/settings/social')
def settings_social():
    return render_template('settings-social.html')


@profile.route('/settings/password')
def settings_password():
    return render_template('settings-password.html')
