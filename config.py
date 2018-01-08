import os

#  Statement for enabling development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

##################
#### database ####
##################
SQLALCHEMY_DATABASE_URI = "mysql://root:LULZSECd96@localhost/demomovie?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECTION_OPTION = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True
# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "b'z\x88\xcaF\x97-\xe4\xb8\xc6\x8c\xd6\xd0\x8c\x9ex\\X\n\x89\x15\xf2\x04\x1f\xc0'"

# Secret key for signing cookies
SECRET_KEY = "b'NC\xed\xccx\xfd5\xeel\xcbw\xdb\xef\x037\x87\xd5c\xd6\xaa$\xb1w0'"

##############
#### smtp ####
##############
MAIL_SERVER = 'smtp-relay.sendinblue.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'lulzsecd@gmail.com'
MAIL_PASSWORD = 'rHdJvDzpF97AEPSs'
MAIL_DEFAULT_SENDER = 'Hearly <lulzsecd@gmail.com>'

# Define Upload forder to store subtitles
UPLOAD_FOLDER = 'app/watch/subtitles'
