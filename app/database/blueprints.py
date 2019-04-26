from flask import Flask
from app.database.user import user_blueprint


def register_blueprints(app: Flask):
    app.register_blueprint(user_blueprint, url_prefix='/users')
