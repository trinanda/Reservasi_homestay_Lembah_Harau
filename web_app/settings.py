DEBUG = True

# database connection
SQLALCHEMY_DATABASE_URI = 'postgresql://ta:12345@service_postgresql_di_dalam_docker/ta'
DATABASE_FILE = SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

# Create dummy secrey key so we can use sessions
SECRET_KEY = '12345'


# #flask mail // fitur ini untuk sementara di non-aktivkan, karena di server vps digital ocean tidak jalan karena port SMPT di block
#selama 60 hari dari pendaftaran
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# MAIL_USE_SSL = False
# MAIL_USERNAME = 'zidanecr7kaka@gmail.com'
# MAIL_PASSWORD = 'yourpassword12345'


#twilio
# Your Account SID from twilio.com/console
TWLIO_ACCOUNT_SID = "ACe211524106753eb639d9fae6ebd35bb2"
# Your Auth Token from twilio.com/console
TWLIO_AUTH_TOKEN = "2d7c15d4df5846d341c3a67a7fec9b9b"


#############################################################################################################
# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
#############################################################################################################


#############################################################################################################
# credentials for loading map tiles from mapbox
# https://www.mapbox.com/studio/tilesets/
# MAPBOX_MAP_ID = 'mapbox.satellite'
MAPBOX_MAP_ID = 'mapbox.streets'
#https://www.mapbox.com/account/
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoidHJpbmFuZGEzIiwiYSI6ImNqaTdzdHpyMzBkZmkzcG1yb21jYzJzenUifQ.iFPWtI22OYctMQcYeBdLLg'
#############################################################################################################


#############################################################################################################
## Adding reCAPTCHA to your site
# https://www.google.com/recaptcha/admin#site/341690749?setup
# Site key
RECAPTCHA_PUBLIC_KEY = '6Ld9yV0UAAAAAO80R7BhJYQij2t4yXAbbEiZbFFW'
# Secret key
RECAPTCHA_PRIVATE_KEY = '6Ld9yV0UAAAAAHMETUy4xdllS-FS4LLFDBC6j5F2'
TESTING = True
#############################################################################################################


#############################################################################################################
#google map API
# https://developers.google.com/places/web-service/get-api-key
# https://developers.google.com/maps/documentation/javascript/get-api-key?hl=ID#key
# GOOGLE_MAP_API = "AIzaSyB9qwTOe5jp5SGiiF00Gku329KeJE1cYa0"
# or
# GOOGLEMAPS_KEY = "key"
#############################################################################################################
