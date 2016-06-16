
from werkzeug.security import generate_password_hash, check_password_hash

from contact_form import db


class Site(db.Model):

    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), nullable=True, unique=True)
    url = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False, unique=False) 

    def __init__(self, name, url, email, password):
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