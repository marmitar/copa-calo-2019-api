from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    create_access_token, set_access_cookies,
    create_refresh_token, set_refresh_cookies,
    jwt_required, jwt_optional, jwt_refresh_token_required,
    current_user
)

from app.extensions import db
from app.exceptions import MissingParameters, require_args

from app.database.models import User, College
from app.database.schemas import UserSchema
from app.exceptions.users import UserAlreadyRegistered, UserNotFound, InvalidPassword

blueprint = Blueprint('users', __name__)


@blueprint.route('/create', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
@require_args
def register_user(username, password, college_initials):
    college = College.get(initials=college_initials)

    try:
        user = User(username, password, college)

    except IntegrityError as err:
        raise UserAlreadyRegistered(integrityError=str(err))

    return user


@blueprint.route('/auth', methods=['POST'])
@use_kwargs(UserSchema)
@require_args
def login_user(username, password):
    user: User = User.get(username=username)

    if not user:
        raise UserNotFound
    elif not user.valid_password(password):
        raise InvalidPassword

    user.access_token = create_access_token(user)
    user.refresh_token = create_refresh_token(user)

    response = jsonify()

    set_access_cookies(response, user.access_token)
    set_refresh_cookies(response, user.refresh_token)
    return response


@blueprint.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh_login():
    user: User = current_user
    user.access_token = create_access_token(user)

    response = jsonify()
    set_access_cookies(response, user.access_token)
    return response


@blueprint.route('/read', methods=['GET'])
@jwt_required
@marshal_with(UserSchema)
def show_user():
    return current_user


@blueprint.route('/update', methods=['POST'])
@jwt_required
@use_kwargs(UserSchema)
@require_args
def update_user(password, new_password):
    user: User = current_user
    user.update(password, new_password)

    return {}


@blueprint.route('/delete', methods=['DELETE'])
@jwt_required
@use_kwargs(UserSchema)
@require_args
def delete_user(password):
    user: User = current_user
    user.delete(password)

    return {}


@blueprint.route('/free', methods=['GET'])
@use_kwargs(UserSchema)
@require_args
def is_free(username):
    exists = User.check_by_key_value(username=username)

    return {
        'username': username,
        'free': not exists
    }
