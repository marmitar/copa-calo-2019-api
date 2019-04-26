import os
import datetime as dt


class Config(object):
    """Base configuration"""

    SECRET_KEY = os.environ['HASH_SECRET_KEY']
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    MIGRATIONS_DIR = '.migrations'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 12
    CACHE_TYPE = 'simple'

    JWT_TOKEN_LOCATION = 'cookies'
    JWT_COOKIE_CSRF_PROTECT = False

    CORS_ORIGIN_WHITELIST = [
        'http://0.0.0.0:8000',
        'http://localhost:8000',
    ]


class ProdConfig(Config):
    """Production configuration"""

    ENV = 'prod'
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class DevConfig(Config):
    """Development configuration"""

    ENV = 'dev'
    DEBUG = True

    DB_NAME = '.dev.db'
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
