from flask_login import current_user
from functools import wraps
from flask import abort
import bugsnag

# Decorator to check current user is_admin
def require_admin(func):
    @wraps(func)
    def decorate_funcs(*args, **kwargs):
        if not current_user.is_admin:
            bugsnag.notify('User with email ' + current_user.email + ' try to access admin - Unauthorized access!')
            abort(404)
        return func(*args, **kwargs)
    return decorate_funcs
