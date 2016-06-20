import os

#logging config
LOG_FILE = 'app_log.log'

# database config
BASE_URI = os.path.dirname(__file__)
DB_URI = os.path.join(BASE_URI, '.contact_form_data.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

# mail protocol config
MAIL_SENDER = os.environ.get('CONTACT_FORM_EMAIL', 'pythonflask@yahoo.com')
MAIL_SERVER = 'smtp.mail.yahoo.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False

# mail service authentication
MAIL_USERNAME = os.environ.get('CONTACT_FORM_MAIL_USERNAME', MAIL_SENDER)
MAIL_PASSWORD = os.environ.get('CONTACT_FORM_MAIL_PASSWORD', '')

DEBUG = True