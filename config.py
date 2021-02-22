"""Class based flask config and project variables (paths etc.)"""
from pathlib import Path
from dotenv import load_dotenv
from os import environ


BASE_PATH = Path(__file__).parent
load_dotenv(BASE_PATH / '.env')
# less_path = 'C:\\Users\\Sanchez\\AppData\\Roaming\\npm\\lessc'
# less_path = 'C:/Users/Sanchez/AppData/Roaming/npm/lessc'
# less_path = Path('C:/Users/Sanchez/AppData/Roaming/npm/lessc')

IS_PRODUCTION = environ.get('IS_PROD') == 'True'
DRIVE_FOLDER_ID = environ.get('DRIVE_FOLDER_ID')
DRIVE_DEBUG = True


# See: https://hackersandslackers.com/configure-flask-applications/
class Config:
    """Base config class with basic stuff, should be inherited but specific configs"""
    SECRET_KEY = environ.get('SECRET_KEY')
    # SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    FLASK_APP = 'wsgi.py'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_PATH / 'database.db')

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    """Prod config"""
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    """Dev config"""
    FLASK_ENV = 'development'
    LESS_BIN = environ.get('LESS_BIN')
    DEBUG = True
    TESTING = True
    EXPLAIN_TEMPLATE_LOADING = False
    DRIVE_DEBUG = True

