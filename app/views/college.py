from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from sqlalchemy.exc import IntegrityError

from app.exceptions import require_args
from app.exceptions.models import ResourceNotFound, AlreadyRegistered
from app.database.models import College, User
from app.database.schemas import CollegeSchema

blueprint = Blueprint('college', __name__)


@blueprint.route('/create', methods=['POST'])
@use_kwargs(CollegeSchema)
@marshal_with(CollegeSchema)
@require_args
def create_college(name, initials, **_):
    try:
        college = College(name, initials)
    except IntegrityError:
        raise AlreadyRegistered('college')

    return college


@blueprint.route('/read', methods=['GET'])
@jwt_optional
@use_kwargs(CollegeSchema)
@marshal_with(CollegeSchema)
def get_college(name=None, initials=None, **_):
    user: User = current_user
    if user:
        return user.college

    if name:
        return College.get(name=name)

    elif initials:
        return College.get(initials=initials)

    raise ResourceNotFound('College')


@blueprint.route('/update', methods=['PATCH'])
@jwt_required
@use_kwargs(CollegeSchema)
@marshal_with(CollegeSchema)
def update_college(name=None, initials=None, logo=None, **_):
    user: User = current_user
    user.college.update(name=name, initials=initials, logo=logo)
    return user.college


@blueprint.route('/all', methods=['GET'])
@marshal_with(CollegeSchema(many=True))
def all_colleges(**_):
    return College.query.all()
