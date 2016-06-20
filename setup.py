from setuptools import setup

setup(name='ContactForm',
    version='0.1',
    description='Contact-Us Form backend for static sites',
    author='Tosin Damilare James Animashaun',
    author_email='acetakwas@gmail.com',
    url='https://github.com/Krohx/contactform',
    install_requires=[
        'Flask==0.11.1',
        'Flask-Bootstrap==3.3.6.0',
        'Flask-Mail==0.9.1',
        'Flask-SQLAlchemy==2.1',
        'Jinja2==2.8',
        'LEPL==5.1.3',
        'MarkupSafe==0.23',
        'SQLAlchemy==1.0.13',
        'Werkzeug==0.11.10',
        'argparse==1.2.1',
        'blinker==1.4',
        'click==6.6',
        'dominate==2.2.0',
        'itsdangerous==0.24',
        'requests==2.10.0',
        'visitor==0.1.3',
        'wsgiref==0.1.2'
    ],
)