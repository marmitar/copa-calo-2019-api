from flask_jwt_extended import current_user, jwt_required
from app.exceptions import ForbiddenAccess
from app.database.user import Permision
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
