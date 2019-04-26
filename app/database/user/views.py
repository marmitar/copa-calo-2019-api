from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import create_access_token, current_user, jwt_required, jwt_optional
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.exceptions import MissingArguments, require_args
from .models import User
from .schemas import UserSchema
from .exceptions import UserAlreadyRegistered, UserNotFound, InvalidPassword

blueprint = Blueprint('users', __name__)


@blueprint.route('/create', methods=['POST'])
@use_kwargs(UserSchema)
@require_args
def register_user(username, email, password, **_):
    try:
        user = User(username, email, password)

    except IntegrityError as err:
        raise UserAlreadyRegistered(integrityError=str(err))

    user.token = create_access_token(user)
    return user.token


@blueprint.route('/authenticate', methods=['POST'])
@jwt_optional
@use_kwargs(UserSchema)
def login_user(email, password=None, **_):
    user: User = current_user
    if user and user.email == email:
        return user

    user = User.query.filter_by(email=email).first()

    if not user:
        raise UserNotFound
    elif not password:
        raise MissingArguments('password')
    elif not user.valid_password(password):
        raise InvalidPassword

    user.token = create_access_token(user)
    return user.token


@blueprint.route('/test', methods=['GET'])
@jwt_required
@marshal_with(UserSchema)
def test(**_):
    return current_user


# @blueprint.route('/validation/username', methods=['POST'])
# @use_kwargs(UserSchema)
# def valid_email(email):
#     result = User.query(User.id).filter_by(email=email).scalar()
#     return result is not None
