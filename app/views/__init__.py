from flask import Flask
from app.views.user import blueprint as user_blueprint
from app.views.admin import blueprint as admin_blueprint
from app.views.college import blueprint as college_blueprint
from app.views.athlete import blueprint as athlete_blueprint
from app.views.track import blueprint as track_blueprint

from app.database.models import User, Permision
from sqlalchemy.exc import IntegrityError


def register_blueprints(app: Flask):
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(admin_blueprint, url_prefix='/user')
    app.register_blueprint(college_blueprint, url_prefix='/college')
    app.register_blueprint(athlete_blueprint, url_prefix='/athlete')
    app.register_blueprint(track_blueprint, url_prefix='/track')
