from flask import Flask
from app.views.user import blueprint as user_blueprint


def register_blueprints(app: Flask):
    app.register_blueprint(user_blueprint, url_prefix='/users')
