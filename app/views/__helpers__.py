from flask_jwt_extended import current_user, jwt_required, decode_token
from app.exceptions import ForbiddenAccess
from app.extensions import jwt
from app.database.user import Permision, User
from functools import wraps


def permission_required(*permissions):
    def wrapper(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            user: User = current_user
            if user.permission not in permissions:
                raise ForbiddenAccess
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
