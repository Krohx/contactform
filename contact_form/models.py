'''
    Database Models
'''
# stdlib imports
import datetime
from textwrap import dedent

# library imports
from werkzeug.security import generate_password_hash, check_password_hash

# local imports
from contact_form import db


class Site(db.Model):

    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), nullable=True, unique=False)
    url = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False, unique=False)
    reg_datetime = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False, unique=False)

    def __init__(self, url, email, password, name=None):
        self.name = name
        self.url = url
        self.email = email
        self.password = password
        self.reg_datetime = datetime.datetime.now()

    def __repr__(self):
        return '<Site: %r; Email: %r>' % (self.url, self.email)

    def __str__(self):
        return self.__repr__()

    @property
    def password(self):
        '''
        A write-only property: 'password'
        '''
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        '''
        Access the 'setter' method of the `password` property (set
        with '@property')
        '''
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        '''
        Verify if the given `password` generates the
        same hash as the hash stored in the DB
        '''
        return check_password_hash(self.password_hash, password)


class Message(db.Model):

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default='', nullable=True, unique=False)
    email = db.Column(db.String, default='', nullable=True, unique=False)
    phone = db.Column(db.String, default='', nullable=True, unique=False)
    subject = db.Column(db.String, default='', nullable=True, unique=False)
    text = db.Column(db.String, default='', nullable=True, unique=False)
    msg_datetime = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False, unique=False)
    source_url = db.Column(db.String, nullable=True, unique=False)

    def __init__(self, name=None, email=None, phone=None, subject=None, text=None, source_url=None):
        self.site_id = site_id
        self.name = name or ''
        self.email = email or ''
        self.phone = phone or ''
        self.subject = subject or ''
        self.text = text or ''
        self.msg_datetime = datetime.datetime.now()
        self.source_url = source_url or ''

    def __repr__(self):
        return dedent(
            '''
                Name: {name}
                Email: {email}
                Phone: {phone}
                
                Source URL: {url}

                Subject: {subject}
                Text: {text}
            '''.format(
                name=self.name,
                email=self.email,
                phone=self.phone,
                url=self.source_url,
                subject=self.subject,
                text=self.text
            )
        )

    def __str__(self):
        return self.__repr__()
