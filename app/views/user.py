from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    create_access_token, set_access_cookies,
    create_refresh_token, set_refresh_cookies,
    jwt_required, jwt_optional, jwt_refresh_token_required,
    current_user, unset_jwt_cookies
)


from app.exceptions import MissingParameters, require_args

from app.database.models import User, College
from app.database.schemas import UserSchema
from app.exceptions.models import InvalidPassword, AlreadyRegistered

blueprint = Blueprint('users', __name__)


@blueprint.route('/create', methods=['PUT'])
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
@require_args
def create_user(username, password, college_initials, **_):
    college = College.get(initials=college_initials)

    try:
        user = User(username, password, college)
    except IntegrityError:
        raise AlreadyRegistered(username)

    return user


@blueprint.route('/auth', methods=['POST', 'DELETE'])
@use_kwargs(UserSchema)
def authenticate_user(username=None, password=None, **_):
    if request.method == 'POST':
        if not username or not password:
            MissingParameters('username', 'password')
        return login_user(username, password)
    elif request.method == 'DELETE':
        return logout_user()


def login_user(username, password):
    user: User = User.get(username=username)

    if not user.valid_password(password):
        raise InvalidPassword

    user.access_token = create_access_token(user)
    user.refresh_token = create_refresh_token(user)

    data = UserSchema().dump(user).data
    response = jsonify(**data)

    set_access_cookies(response, user.access_token)
    set_refresh_cookies(response, user.refresh_token)
    return response


def logout_user():
    response = jsonify(True)
    unset_jwt_cookies(response)
    return response


@blueprint.route('/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh_login():
    user: User = current_user
    user.access_token = create_access_token(user)

    response = jsonify(True)
    set_access_cookies(response, user.access_token)
    return response


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
