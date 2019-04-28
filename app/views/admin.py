from flask import Blueprint, jsonify
from flask_apispec import use_kwargs, marshal_with
from sqlalchemy.exc import IntegrityError

from app.database.models import User, College
from app.database.schemas import UserSchema
from app.exceptions.models import InvalidPassword, AlreadyRegistered
from app.exceptions import require_args
from .__helpers__ import permission_required, Permision

blueprint = Blueprint('admins', __name__)


@blueprint.route('/admin/start', methods=['GET'])
def start_admin():

    User('admin', 'tipo1programa', Permision.admin)

    return jsonify()


@blueprint.route('/admin/create', methods=['PUT'])
@permission_required(Permision.admin)
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
@require_args
def create_admin(username, password, **_):
    try:
        admin = User(username, password, Permision.admin)
    except IntegrityError:
        raise AlreadyRegistered(username)

    return admin


@blueprint.route('/dm/create', methods=['PUT'])
@permission_required(Permision.admin)
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
@require_args
def create_dm(username, password, college_initials, **_):
    college = College.get(initials=college_initials)

    try:
        dm = User(username, password, Permision.dm, college)
    except IntegrityError:
        raise AlreadyRegistered(username)

    return dm


@blueprint.route('/arbiter/create', methods=['PUT'])
@permission_required(Permision.admin)
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
@require_args
def create_arbiter(username, password, **_):
    try:
        arbiter = User(username, password, Permision.arbiter)
    except IntegrityError:
        raise AlreadyRegistered(username)

    return arbiter
