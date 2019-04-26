from app.database.user import User

from app.extensions import jwt
from app.database.user import UserNotFound


@jwt.user_loader_callback_loader
def get_user_by_id(id):
    return User.get_by_id(id)


@jwt.user_identity_loader
def get_id_of_user(user: User):
    return user.id


@jwt.user_loader_error_loader
def id_erro(id):
    return UserNotFound(description='could not find any user associated with the id', id=id)
