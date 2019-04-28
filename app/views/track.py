from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from sqlalchemy.exc import IntegrityError

from app.exceptions import require_args, ForbiddenAccess
from app.exceptions.models import ResourceNotFound, AlreadyRegistered
from app.database.models import Athlete, College, User
from app.database.schemas import AthleteSchema
from .__helpers__ import Permision, permission_required

blueprint = Blueprint('athlete', __name__)


@blueprint.route('/create', methods=['PUT'])
@permission_required(Permision.admin, Permision.dm)
@use_kwargs(AthleteSchema)
@marshal_with(AthleteSchema)
@require_args
def create_athlete(name, rg, rg_orgao, sex, extra, college_initials=None):
    user: User = current_user
    if user.is_dm():
        college = user.college
    else:
        college = college.get(initials=college_initials)

    try:
        athlete = Athlete(name, rg, rg_orgao, sex, extra, college)
    except IntegrityError:
        raise AlreadyRegistered('athlete')

    return athlete


@blueprint.route('/read', methods=['GET'])
@use_kwargs(AthleteSchema)
@marshal_with(AthleteSchema)
def get_athlete(name=None, rg=None, **_):
    if name:
        return Athlete.get(name=name)

    elif rg:
        return Athlete.get(rg=rg)

    raise ResourceNotFound('athlete')


@blueprint.route('/update', methods=['PATCH'])
@permission_required(Permision.admin, Permision.dm)
@use_kwargs(AthleteSchema)
@marshal_with(AthleteSchema)
def update_athlete(name=None, rg=None, extra=None, **_):
    if name:
        athlete = Athlete.get(name=name)
    elif rg:
        athlete = Athlete.get(rg=rg)
    else:
        raise ResourceNotFound('athlete')

    user: User = current_user
    if not user.is_admin() and athlete not in user.college.athletes:
        raise ForbiddenAccess

    athlete.update(extra=extra)

    return athlete


@blueprint.route('/all', methods=['GET'])
@marshal_with(AthleteSchema(many=True))
def all_athletes(**_):
    return Athlete.query.all()
