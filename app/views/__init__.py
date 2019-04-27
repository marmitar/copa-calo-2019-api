from flask import Flask
from app.views.user import blueprint as user_blueprint
from app.views.college import blueprint as college_blueprint
from app.views.athlete import blueprint as athlete_blueptint


def register_blueprints(app: Flask):
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(college_blueprint, url_prefix='/college')
    app.register_blueprint(athlete_blueptint, url_prefix='/athlete')
