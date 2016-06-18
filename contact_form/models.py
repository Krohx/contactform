'''
    Database Models
'''
# stdlib imports
from textwrap import dedent

# library imports
from werkzeug.security import generate_password_hash, check_password_hash

# local imports
from contact_form import db


class Site(db.Model):

    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), nullable=True, unique=False)
    url = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False, unique=False) 

    def __init__(self, url, email, password, name=None):
        self.name = name
        self.url = url
        self.email = email
        self.password = password

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
    recp_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=True, unique=False)
    recp = db.relationship('Site', uselist=False, backref=db.backref('messages', uselist=True))

    def __repr__(self):
        return dedent(
            '''
                Name: {name}
                Email: {email}
                Phone: {phone}
                
                Recepient: {recp}

                Subject: {subject}
                Text: {text}
            '''.format(
                name=self.name,
                email=self.email,
                phone=self.phone,
                recp=self.recp,
                subject=self.subject,
                text=self.text
            )
        )

    def __str__(self):
        return self.__repr__()
