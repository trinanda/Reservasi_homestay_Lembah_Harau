DEBUG = True

# database connection
SQLALCHEMY_DATABASE_URI = 'postgresql://ta:12345@service_postgresql_di_dalam_docker/ta'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

# Create dummy secrey key so we can use sessions
SECRET_KEY = '12345'


#flask mail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'zidanecr7kaka@gmail.com'
MAIL_PASSWORD = 'm@Fu7Ur3#'


#twilio
# Your Account SID from twilio.com/console
TWLIO_ACCOUNT_SID = "ACe211524106753eb639d9fae6ebd35bb2"
# Your Auth Token from twilio.com/console
TWLIO_AUTH_TOKEN = "2d7c15d4df5846d341c3a67a7fec9b9b"


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
