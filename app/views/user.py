from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    create_access_token, set_access_cookies,
    jwt_required, jwt_optional, current_user, get_raw_jwt
)


from app.exceptions import MissingParameters, require_args

from app.database.models import User, College
from app.database.schemas import UserSchema
from app.exceptions.models import InvalidPassword, AlreadyRegistered
from app.views.__helpers__ import blacklist

blueprint = Blueprint('users', __name__)


@blueprint.route('/auth', methods=['POST', 'DELETE'])
@jwt_optional
@use_kwargs(UserSchema)
def authenticate_user(username=None, password=None, **_):
    if request.method == 'POST':
        if not username or not password:
            raise MissingParameters('username', 'password')
        return login_user(username, password)
    elif request.method == 'DELETE':
        return logout_user()


def login_user(username, password):
    user: User = User.get(username=username)

    if not user.valid_password(password):
        raise InvalidPassword

    user.token = create_access_token(user)

    data = UserSchema().dump(user).data
    return jsonify(token=user.token, **data)


def logout_user():
    user: User = current_user
    if not user:
        return jsonify(False)

    blacklist(get_raw_jwt())
    return jsonify(True)


@blueprint.route('/read', methods=['GET'])
@jwt_required
@marshal_with(UserSchema)
def show_user():
    return current_user


@blueprint.route('/update', methods=['PATCH'])
@jwt_required
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
def update_user(password=None, username=None, **_):
    user: User = current_user
    user.update(password, username)

    return user


@blueprint.route('/free', methods=['GET'])
@use_kwargs(UserSchema)
@require_args
def is_free(username, **_):
    exists = User.check_by_key_value(username=username)

    return not exists
