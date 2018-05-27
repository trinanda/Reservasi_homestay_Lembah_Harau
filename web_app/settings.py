DEBUG = True

# database connection
SQLALCHEMY_DATABASE_URI = 'postgresql://ta:12345@service_postgresql_di_dalam_docker/ta'
SQLALCHEMY_TRACK_MODIFICATIONS = False

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