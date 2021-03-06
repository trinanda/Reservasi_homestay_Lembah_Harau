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
# MAIL_USERNAME = 'your_email@gmail.com'
# MAIL_PASSWORD = 'yourpassword12345'

#############################################################################################################

#twilio
# Your Account SID from twilio.com/console

# this upgraded SID for user
TWLIO_ACCOUNT_SID_UPGRADED_FOR_USER = "YOUR_TWILIO_SID"

# this non upgrade SID for admin
TWLIO_ACCOUNT_SID_NONE_UPGRADED_FOR_ADMIN = "YOUR_TWILIO_AUTH_TOKEN"


# Your Auth Token from twilio.com/console

# this upgraded auth_token for user
TWLIO_AUTH_TOKEN_UPGRADED_FOR_USER = "YOUR_TWILIO_SID"

# this none upgraded auth_token for admin
TWLIO_AUTH_TOKEN_NONE_UPGRADED_FOR_ADMIN = "YOUR_TWILIO_AUTH_TOKEN"


#############################################################################################################


#############################################################################################################
# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
# SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
# SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
#############################################################################################################


#############################################################################################################
# credentials for loading map tiles from mapbox
# https://www.mapbox.com/studio/tilesets/
# MAPBOX_MAP_ID = 'mapbox.satellite'
MAPBOX_MAP_ID = 'mapbox.streets'
#https://www.mapbox.com/account/
MAPBOX_ACCESS_TOKEN = 'YOUR_MAP_BOX_ACCESS_TOKEN'
#############################################################################################################


#############################################################################################################
## Adding reCAPTCHA to your site
# https://www.google.com/recaptcha/admin#site/341690749?setup
# Site key
RECAPTCHA_PUBLIC_KEY = 'YOUR_RECAPTCHA_PUBLIC_KEY'
# Secret key
RECAPTCHA_PRIVATE_KEY = 'YOUR_RECAPTCHA_PRIVATE_KEY'
TESTING = False
#############################################################################################################


#############################################################################################################
#google map API
# https://developers.google.com/places/web-service/get-api-key
# https://developers.google.com/maps/documentation/javascript/get-api-key?hl=ID#key
GOOGLE_MAP_API = "YOUR_GOOGLE_MAP_API_KEY"
# or
# GOOGLEMAPS_KEY = "key"
# if got some error try this solution:
# https://stackoverflow.com/questions/37403731/this-page-didnt-load-google-maps-correctly-see-the-javascript-console-for-tech
#############################################################################################################

#############################################################################################################
UPLOADED_PHOTOS_DEST = 'web_app/files/'
#############################################################################################################

#############################################################################################################
PDF_FOLDER = 'web_app/files/pdf/'
TEMPLATE_FOLDER = 'web_app/templates/'
#############################################################################################################