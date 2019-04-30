from flask_jwt_extended import current_user, jwt_required, decode_token
from app.exceptions import ForbiddenAccess
from app.exceptions.models import EndOfRegistrationPeriod
from app.extensions import jwt
from app.database.user import Permision, User
from functools import wraps
import os
from datetime import datetime as dt


def registration_ended():
    end_date = os.environ['REGISTRATION_END']
    return dt.now() > dt.strptime(end_date, "%d/%m/%Y %H:%M")


def permission_required(*permissions, timed=False):
    def wrapper(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            user: User = current_user
            if user.permission not in permissions:
                raise ForbiddenAccess
            elif not user.is_admin() and timed and registration_ended():
                raise EndOfRegistrationPeriod
            return function(*args, **kwargs)
        return jwt_required(wrapped)
    return wrapper


blacklisted_tokens = set()


@jwt.token_in_blacklist_loader
def is_blacklisted(token):
    jti = token['jti']
    return jti in blacklisted_tokens


def blacklist(token):
    blacklisted_tokens.add(token['jti'])
