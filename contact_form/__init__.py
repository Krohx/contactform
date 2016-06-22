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
import logging
from urlparse import urlparse

# library imports
import requests
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
db.create_all()

# email validator
validator = Email()

# setup logging
#logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', datefmt='%a %b, %Y (%I:%M:%S %p)', filename='app_log.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)
if app.config.get('DEBUG', False):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(config.LOG_FILE)
file_handler.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s:\t%(message)s', datefmt='%a %b, %Y (%I:%M:%S %p)')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_newline(num_lines=1):
    for i in range(num_lines):
        logger.info('\n')


def log_break():
    logger.info('\n\n---\n\n')


def validate_and_get_domain(url):
    logger.info('Validating URL... %s', url)
    link = urlparse(url)
    scheme = link.scheme or 'http'
    domain = ''.join([scheme, '://', link.netloc])

    try:
        if requests.get(domain).status_code != 200:
            raise InvalidURLError
    except Exception, e:
        logger.error('Error validating URL', exc_info=True)
        return None

    logger.info('URL is valid.')
    return domain


def validate_email(email):
    if validator(email):
        return True
    else:
        raise EmailValidationError


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
    except Exception, e:
        #print 'Error formatting and sending email!' # DEBUG
        logger.error('Error formatting and sending email!', exc_info=True)
        return False


def format_msg_html(**kwargs):
    param_dict = dict()

    param_dict['name'] = kwargs.get('name', 'None').title()
    param_dict['email'] = kwargs.get('email', 'None')
    param_dict['phone'] = kwargs.get('phone', 'None')
    subject = kwargs.get('subject', 'No subject')
    message = kwargs.get('message', 'No message')

    return render_template(
        'email_html.html',
        param_dict=param_dict,
        subject=subject,
        message=message
    )


def analytics_store(kw_dict, site):
    kw_dict['text'] = kw_dict.pop('message', '')
    if site is not None:
        try:
            kw_dict['site_id'] = site.id
        except: # AttributeError
            kw_dict['site_id'] = None
    try:
        db_ops.insert_val(db_ops.Message, kw_dict)
        logger.info('Analytics data saved.')
    except Exception, e:
        logger.error('Error saving analytics details!\n\t%r', kw_dict, exc_info=True)


class EmailValidationError(Exception):
    pass


class InvalidURLError(Exception):
    pass


@app.route('/index/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        log_newline(2)
        logger.info('New contact-us form received!')
        logger.info('Site: %s', str(request.referrer))
        form_dict = dict(request.form)
        logger.info('Form: %s', str(form_dict))

        data_fields = ['name', 'phone', 'email', 'subject', 'message']
        data = dict()
        
        try:
            for k,v in form_dict.iteritems():
                if k in data_fields and bool(v[0]):
                    data[k] = unicode(v[0]).decode('utf-8')
            logger.info('Form->Dict Serialize: %s', str(data))
        except Exception, e:
            #print 'Failed to handle form:\n\t%r' % request.form # DEBUG
            logger.error('Serialize Fail!', exc_info=True)
            return render_template('failure.html',
                goto=request.referrer,
                message="There was an error. Your message was not sent. Please try again."
            )

        if data.get('email'):
            url = validate_and_get_domain(request.referrer)
            try:
                site = db_ops.ret_val(db_ops.Site, dict(url=url))
                logger.info('Site found in records!')
                recp = site.email
            except Exception, e:
                logger.error('Error retrieving site data from DB!', exc_info=True)
                recp = None
            #message = '{subj}\n\n{msg}'.format(subj=data.get('subject', ''), msg=data.get('message', '')).strip()
            analytics_store(data, site) # store received data for future analytics    

            # For debug purposes
            if app.config.get('DEBUG', False):
                logger.debug('Sending mail to debug email: %s', config.MAIL_SENDER)
                recp = config.MAIL_SENDER
            
            if recp is not None:
                message = format_msg_html(**data)
                logger.info('Email HTML formatted')
                
                if send_email(app, recp=recp, message=message, sender=config.MAIL_SENDER, subject="ContactForm: New message from your website."):
                    logger.info('Email sent to %s', recp)
                    return render_template('success.html',
                        goto=request.referrer,
                        message="Your message was sent successfully."
                    )
            else:
                logger.error('Site not found in records!')

        logger.error('Email not sent!\n\t%s', str(request.form))
        log_break()
        #print 'Error! Not sending mail...\n\t%r' % request.form # DEBUG
        return render_template('failure.html',
            goto=request.referrer,
            message="There was an error. Your message was not sent. Please try again."
        )

    logger.info('Home page hit, redirecting to signup...')
    log_newline()
    return redirect(url_for('signup'))


@app.route('/signup/', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        log_newline(2)
        logger.info('New signup form received!')
        form_dict = dict(request.form)
        logger.info('Form: %s', str(form_dict))
        param_dict = dict()

        try:
            param_dict['name'] = form_dict.get('name')[0]
            param_dict['url'] = form_dict.get('url')[0]
            param_dict['email'] = form_dict.get('email')[0]
            param_dict['password'] = form_dict.get('password')[0]
            #verifyurl
            # Need to cleanup this code
            if validate_email(param_dict.get('email', 'invalid_email')) and validate_and_get_domain(param_dict.get('url')):
                if db_ops.insert_val(db_ops.Site, param_dict, rollback_on_fail=True):
                    logger.info('New user subscribed!')
                    return render_template('success.html',
                        goto=request.referrer,
                        message="Thank you. Your site has been registered with us."
                    )
        except Exception, e:
            #print 'Error! Failed to register new site:\n\t%r' % request.form # DEBUG
            logger.error('Error signing-up new user!', exc_info=True)
            return render_template('failure.html',
                goto=request.referrer,
                message="There was an error. Your registration was unsuccessful. Please try again."
            )
        finally:
            log_break()
            param_dict.clear()

    return render_template('signup.html')


@app.errorhandler(500)
def server_error(error):
    return redirect(request.referrer), 500


@app.errorhandler(404)
def _404(error):
    return redirect(request.referrer), 404


if __name__ == '__main__':
    app.run()