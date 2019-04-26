from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    create_access_token, set_access_cookies,
    create_refresh_token, set_refresh_cookies,
    jwt_required, jwt_optional,  jwt_refresh_token_required,
    current_user
)

from app.extensions import db
from app.exceptions import MissingArguments, require_args
from .models import User
from .schemas import UserSchema
from .exceptions import UserAlreadyRegistered, UserNotFound, InvalidPassword

blueprint = Blueprint('users', __name__)


@blueprint.route('/create', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
@require_args
def register_user(username, email, password, **_):
    try:
        user = User(username, email, password)

    except IntegrityError as err:
        raise UserAlreadyRegistered(integrityError=str(err))

    return user


@blueprint.route('/auth', methods=['POST'])
@use_kwargs(UserSchema)
def login_user(email, password, **_):
    user: User = User.query.filter_by(email=email).first()

    if not user:
        raise UserNotFound
    elif not password:
        raise MissingArguments('password')
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
def refresh_login(**_):
    user: User = current_user
    user.access_token = create_access_token(user)

    response = jsonify()
    set_access_cookies(response, user.access_token)
    return response


@blueprint.route('/read', methods=['GET'])
@jwt_required
@marshal_with(UserSchema)
def show_user(**_):
    return current_user


@blueprint.route('/update', methods=['POST'])
@jwt_required
@use_kwargs(UserSchema)
def update_user(old_password, **kwargs):
    user: User = current_user
    user.update(old_password, **kwargs)

    return {}


@blueprint.route('/delete', methods=['DELETE'])
@jwt_required
@use_kwargs(UserSchema)
def delete_user(password, **_):
    user: User = current_user
    user.delete(password)

    return {}


@blueprint.route('/free', methods=['GET'])
@use_kwargs(UserSchema)
def is_free(email=None, username=None, **_):
    response = {}

    if email:
        exists = User.check_by_key_value(email=email)
        response['email'] = not exists

    if username:
        exists = User.check_by_key_value(username=username)
        response['username'] = not exists

    return response
