from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
import bugsnag
from bugsnag.flask import handle_exceptions
from flask_assets import Environment, Bundle

# Define the WSGI application object
app = Flask(__name__, static_url_path='/assets')

# Assets
assets = Environment(app)

bundles = {
    'js_player': Bundle('js/jquery-3.2.1.min.js', 'js/owl.carousel.min.js', 'js/bootstrap.min.js', 'js/app.js',
                        'js/analytics.js', 'js/sweetalert.min.js', 'js/plyr.js', 'js/player.js', filters='jsmin',
                        output='js/packed.js'),
    'js_main': Bundle('js/jquery-3.2.1.min.js', 'js/owl.carousel.min.js', 'js/bootstrap.min.js', 'js/app.js',
                      'js/analytics.js', filters='jsmin', output='js/packed1.js'),
    'js_index': Bundle('js/jquery-3.2.1.min.js', 'js/owl.carousel.min.js', 'js/bootstrap.min.js', 'js/app.js', 'js/notify.min.js', 'js/ajax.js',
                      'js/analytics.js', filters='jsmin', output='js/packed2.js'),
    'player_css': Bundle('css/bootstrap.min.css', 'css/owl.carousel.min.css', 'css/owl.customize.css', 'css/app.css',
                         'css/player.css', 'css/sweetalert.css', filters='cssmin', output='css/packed.css'),
    'main_css': Bundle('css/bootstrap.min.css', 'css/owl.carousel.min.css', 'css/owl.customize.css', 'css/app.css',
                       filters='cssmin', output='css/packed1.css'),
    'index_css': Bundle('css/bootstrap.min.css', 'css/owl.carousel.min.css', 'css/owl.customize.css', 'css/app.css',
                       filters='cssmin', output='css/packed2.css')
}
assets.register(bundles)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Configure Bugsnag
bugsnag.configure(
    api_key="803859ba9866c35b46740e1e26a0159e",
    project_root=app.config['BASE_DIR'],
)

# Attach Bugsnag to Flask's exception handler
handle_exceptions(app)

###############
#### login ####
###############
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

# Mail Initialize
mail = Mail(app)

# Initial Migration
migrate = Migrate(app, db)


######################
#### error handle ####
######################
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


#######################
#### import module ####
#######################
from app.auth.controllers import auth as auth_module
from app.watch.controllers import watch as watch_module
from app.admin.controllers import admin as admin_module
from app.home.controllers import home_module
from app.users.controllers import profile as profile_module

################
#### module ####
################
app.register_blueprint(auth_module)
app.register_blueprint(watch_module)
app.register_blueprint(admin_module)
app.register_blueprint(home_module)
app.register_blueprint(profile_module)

db.create_all()
