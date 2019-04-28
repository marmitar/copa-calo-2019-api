from app.database.user import User
from app.database.college import College
from app.database.athlete import Athlete
from app.database.track import Track
from app.database.registration import Registration

from app.extensions import jwt
from app.exceptions.models import ResourceNotFound


@jwt.user_loader_callback_loader
def get_user_by_id(id):
    return User.get_by_id(id)


@jwt.user_identity_loader
def get_id_of_user(user: User):
    return user.id


@jwt.user_loader_error_loader
def id_erro(id):
    return ResourceNotFound('logged in user')
