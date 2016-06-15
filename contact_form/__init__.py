"""
contact_form
~~~~~~~~~~~~

Contact form app for static websites

:author: Krohx Technologies (krohxinc@gmail.com)
:copyright: (c) 2016 by Krohx Technologies
:license: see LICENSE for details.
"""

# standard lib imports
import os

# library imports
from flask import Flask, redirect, url_for, redirect, request, render_template
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from lepl.apps.rfc3696 import Email # for email validation

import config

app = Flask(__name__)
app.config.from_object(config)


# Instantiate Flask extensions
mail = Mail(app)
db = SQLAlchemy(app)


import db_ops # circular import guard
#db.create_all()

# email validator
validator = Email()

@app.route('/index/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        form_dict = dict(request.form)

        data_fields = ['name', 'phone', 'email', 'message']
        data = dict()

        try:
            for k,v in form_dict.iteritems():
                if k in data_fields and bool(v[0]):
                    data[k] = unicode(v[0]).decode('utf-8')
        except:
            print 'Failed to handle form:\n\t%r' % request.form # DEBUG
            return render_template('failure.html',
                goto=request.referrer,
                message="There was an error. Your message was not sent. Please try again."
            )

        if data.get('email'):
            print '\nREFERRER %s\n' % request.referrer # DEBUG
            site = db_ops.ret_val(db_ops.Site, dict(url=request.referrer))
            if site is not None:
                if send_email(app, data.get('email'), message=data.get('message'), sender=config.MAIL_SENDER, subject="Contact-Form: New message from your website."):
                    return render_template('success.html',
                        goto=request.referrer,
                        message="Your message was sent successfully."
                    )

        print 'Error! Not sending mail...\n\t%r' % request.form # DEBUG
        return render_template('failure.html',
            goto=request.referrer,
            message="There was an error. Your message was not sent. Please try again."
        )

    return redirect(url_for('signup'))


# @app.route('/send_mail/', methods=['POST'])
# def submit_message():
#     form_dict = dict(request.form)

#     data_fields = ['name', 'phone', 'email', 'message']
#     data = dict()

#     try:
#         for k,v in form_dict.iteritems():
#             if k in data_fields and bool(v[0]):
#                 data[k] = unicode(v[0]).decode('utf-8')
#     except:
#         print 'Failed to handle form:\n\t%r' % request.form # DEBUG
#         return render_template('failure.html',
#             goto=request.referrer,
#             message="There was an error. Your message was not sent. Please try again."
#         )

#     if data.get('email'):
#         print '\nREFERRER %s\n' % request.referrer # DEBUG
#         site = db_ops.ret_val(db_ops.Site, dict(url=request.referrer))
#         if site is not None:
#             if send_email(app, data.get('email'), message=data.get('message'), sender=config.MAIL_SENDER, subject="Contact-Form: New message from your website."):
#                 return render_template('success.html',
#                     goto=request.referrer,
#                     message="Your message was sent successfully."
#                 )

#     print 'Error! Not sending mail...\n\t%r' % request.form # DEBUG
#     return render_template('failure.html',
#         goto=request.referrer,
#         message="There was an error. Your message was not sent. Please try again."
#     )


@app.route('/signup/', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        db_ops.rollback()
        form_dict = dict(request.form)
        param_dict = dict()

        try:
            param_dict['name'] = form_dict.get('name')[0]
            param_dict['url'] = form_dict.get('url')[0]
            param_dict['email'] = form_dict.get('email')[0]
            param_dict['password'] = form_dict.get('password')[0]

            # Need to cleanup this code
            if validate_email(param_dict.get('email', 'invalid_email')):
                if db_ops.insert_val(db_ops.Site, param_dict, rollback_on_fail=True):
                    return render_template('success.html',
                        goto=request.referrer,
                        message="Thank you. Your site has been registered with us."
                    )
                else:
                    assert False
            else:
                assert False
        except:
            print 'Error! Failed to register new site:\n\t%r' % request.form # DEBUG
            return render_template('failure.html',
                goto=request.referrer,
                message="There was an error. Your registration was unsuccessful. Please try again."
            )
        finally:
            param_dict.clear()

    return render_template('signup.html')


@app.errorhandler(500)
def server_error(error):
    return redirect(request.referrer), 500


@app.errorhandler(404)
def _404(error):
    return redirect(request.referrer), 404


def validate_email(email):
    return validator(email)


def send_email(app, recp, message, sender=None, subject="Someone sent a message from your website."):

    # if recipient is passed as a string,
    # remove whitespaces and commas, splitting
    # the string into a list of recipients
    if isinstance(recp, str) or isinstance(recp, unicode):
        recp = [k.strip() for k in recp.split(',')]
    
    if sender is None:
        sender=config.MAIL_SENDER
    try:
        mail_msg = Message(
            subject=subject,
            recipients=recp,
            html=message,
            sender=sender
        )

        mail.send(mail_msg)
        return True
    except:
        print 'Error formatting and sending email!' # DEBUG
        return False


if __name__ == '__main__':
    db.create_all()
    app.run()