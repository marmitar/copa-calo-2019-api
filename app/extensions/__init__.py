from flask import Flask

from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate
from app.extensions.jwt import JWT


jwt = JWT()
bcrypt = Bcrypt()
cache = Cache()
cors = CORS()
migrate = Migrate()


def register_extensions(app: Flask):
    jwt.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGIN_WHITELIST'])
    migrate.init_app(app, db=None, directory=app.config['MIGRATIONS_DIR'])
