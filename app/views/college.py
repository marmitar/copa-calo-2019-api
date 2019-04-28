from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from sqlalchemy.exc import IntegrityError

from app.exceptions import require_args, MissingParameters
from app.exceptions.models import ResourceNotFound, AlreadyRegistered
from app.database.models import College, User
from app.database.schemas import CollegeSchema, AthleteSchema
from .__helpers__ import Permision, permission_required

blueprint = Blueprint('college', __name__)


@blueprint.route('/create', methods=['PUT'])
@permission_required(Permision.admin)
@use_kwargs(CollegeSchema)
@marshal_with(CollegeSchema)
@require_args
def create_college(name, team, initials, **_):
    try:
        college = College(name, team, initials)
    except IntegrityError:
        raise AlreadyRegistered('college')

    return college


@blueprint.route('/read', methods=['GET'])
@jwt_optional
@use_kwargs(CollegeSchema)
@marshal_with(CollegeSchema)
def get_college(name=None, initials=None, **_):
    if name:
        return College.get(name=name)

    elif initials:
        return College.get(initials=initials)

    user: User = current_user
    if user:
        return user.college

    raise MissingParameters('name')


@blueprint.route('/update', methods=['PATCH'])
@jwt_required
@use_kwargs(CollegeSchema)
@marshal_with(CollegeSchema)
def update_college(name=None, team=None, initials=None, **_):
    user: User = current_user
    user.college.update(name=name, team=team, initials=initials)
    return user.college


@blueprint.route('/athletes', methods=['GET'])
@jwt_optional
@use_kwargs(CollegeSchema)
@marshal_with(AthleteSchema(many=True))
def get_athletes(name=None, team=None, initials=None, **_):
    if name:
        college = College.get(name=name)
    elif team:
        college = College.get(team=team)
    elif initials:
        college = College.get(initials=initials)
    else:
        user: User = current_user
        if user and user.is_dm():
            college = user.college
        else:
            raise MissingParameters('name', 'team', 'initials')

    return college.athletes


@blueprint.route('/all', methods=['GET'])
@marshal_with(CollegeSchema(many=True))
def all_colleges(**_):
    return College.query.all()
