

from Flask import .
from flask.ext.mail import FlaskMail

app = Flask(__init__)

@app.route('/'):
def index():
    return 'Contact Form for Static Websites'


@app.route('/submit/<user>', methods=['POST', 'GET'])
def submit(user=None):
    if user is None:
        return redirect()(url_for('index'))
    else:
        pass
        



"""
jobnownow_website
~~~~~~~~~~~~~~~~~

Pre-launch website for collecting subscription emails
for when the JobNowNow app launches.

:author: Krohx Technologies (krohxinc@gmail.com)
:copyright: (c) 2016 by Krohx Technologies
:license: see LICENSE for details.
"""

# standard lib imports
import os

# library imports
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask import redirect, request
from lepl.apps.rfc3696 import Email # for email validation

# local imports
from config import Config, DevConfig

#export JOBNOWNOW_EMAIL_CFG=dev
app = Flask(__name__)
cfg = 'dev' #os.getenv('JOBNOWNOW_EMAIL_CFG') 

# if cfg is None or cfg != 'dev':
#     app.config.from_object(Config)
# else:
#     app.config.from_object(DevConfig)

# Instantiate Flask extensions
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
mail = Mail(app)

# email validator
validator = Email()

import db_ops # to avoid issue around circular imports

HOME_URL = 'http://jobnownow.com/'
REDIRECT_URL = 'http://jobnownow.com/thankyou.html'


@app.route('/index/')
@app.route('/')
def index():
    return redirect(HOME_URL)


@app.route('/send_mail/', methods=['POST'])
def subscribe(email=''):
    form = request.form
    name = form['name'].decode('utf-8')
    email = form['email'].decode('utf-8')
    message = form['message'].decode('utf-8')

    print
    print
    print
    print name # DEBUG
    print email # DEBUG
    print message # DEBUG
    print request.referrer # DEBUG
    print
    print
    print

    # if validate_email(email):

    #     db_ops.insert_val(db_ops.Subscription, dict(email=email))
    #     print "URL Email Registered!"
    # else:
    #     db_ops.insert_val(db_ops.InvalidSub, dict(email=email))
    #     print "URL Email Failed!"

    return redirect(REDIRECT_URL)

    
# @app.route('/subscribe/', methods=['GET', 'POST'])
# def subscribe_form():
#     form = request.form
#     email = form['email'].decode('utf-8')

#     print email
#     if validate_email(email):
#         db_ops.insert_val(db_ops.Subscription, dict(email=email))
#         print "Form Email Registered!"
#     else:
#         db_ops.insert_val(db_ops.InvalidSub, dict(email=email))
#         print "Form Email Failed!"

#     return redirect(REDIRECT_URL)


@app.errorhandler(500)
def server_error(error):
    return redirect(url_for(REDIRECT_URL)), 500

@app.errorhandler(404)
def _404(error):
    return redirect(url_for(REDIRECT_URL)), 404


def validate_email(email):
    return validator(email)



if __name__ == '__main__':
    db.create_all()
    app.run()

