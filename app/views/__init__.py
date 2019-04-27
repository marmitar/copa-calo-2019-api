from flask import Flask
from app.views.user import blueprint as user_blueprint
from app.views.college import blueprint as college_blueprint


def register_blueprints(app: Flask):
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(college_blueprint, url_prefix='/college')
