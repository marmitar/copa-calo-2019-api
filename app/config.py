import os
import datetime as dt


class Config(object):
    """Base configuration"""

    SECRET_KEY = os.environ['SECRET_KEY']
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 12
    CACHE_TYPE = 'simple'
    MIGRATIONS_DIR = 'migrations/development'

    JWT_TOKEN_LOCATION = 'headers'
    JWT_ACCESS_TOKEN_EXPIRES = dt.timedelta(1)

    CORS_ORIGIN_WHITELIST = [
        'http://127.0.0.1:8000',
        'http://localhost:8000',
        'http://192.168.1.10:8000',
        'http://127.0.0.1:4200',
        'http://localhost:4200',
        'http://192.168.1.10:4200',
        'http://127.0.0.1:8080',
        'http://localhost:8080',
        'http://192.168.1.10:8080',
        'https://mpesportes.herokuapp.com',
        'https://mpesportes.herokuapp.com/',
    ]


class ProdConfig(Config):
    """Production configuration"""

    ENV = 'prod'
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MIGRATIONS_DIR = 'migrations/production'


class DevConfig(Config):
    """Development configuration"""

    ENV = 'dev'
    DEBUG = True

    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'

    CACHE_TYPE = 'simple'
    JWT_ACCESS_TOKEN_EXPIRES = dt.timedelta(10 ** 6)


class TestConfig(Config):
    """Test configuration"""

    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 4
