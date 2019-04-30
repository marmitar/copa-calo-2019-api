from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from sqlalchemy.exc import IntegrityError

from app.exceptions import require_args, ForbiddenAccess, MissingParameters
from app.exceptions.models import ResourceNotFound, AlreadyRegistered
from app.database.models import Athlete, College, User, Registration
from app.database.schemas import AthleteSchema, RegistrationSchema
from .__helpers__ import Permision, permission_required

blueprint = Blueprint('athlete', __name__)


@blueprint.route('/create', methods=['PUT'])
@permission_required(Permision.admin, Permision.dm, timed=True)
@use_kwargs(AthleteSchema)
@marshal_with(AthleteSchema)
@require_args
def create_athlete(name, rg, rg_orgao, sex, college_initials=None):
    user: User = current_user
    if user.is_dm():
        college = user.college
    elif not college_initials:
        raise MissingParameters('college_initials')
    else:
        college = College.get(initials=college_initials)

    try:
        athlete = Athlete(name, rg, rg_orgao, sex, college)
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

    raise MissingParameters('name', 'rg')


@blueprint.route('/delete', methods=['POST'])
@permission_required(Permision.admin, Permision.dm, timed=True)
@use_kwargs(RegistrationSchema)
def delete_athlete(athlete_name, athlete_rg, track_name=None, **_):
    athlete = Athlete.get(name=athlete_name, rg=athlete_rg)
    if not athlete:
        raise ResourceNotFound('atleta')

    user: User = current_user
    if not user.is_admin() and user.college != athlete.college:
        raise ForbiddenAccess

    if not track_name:
        for reg in athlete.registrations:
            reg.delete()
        athlete.delete()
        return jsonify()

    for reg in athlete.registrations:
        if reg.track_name == track_name:
            reg.delete()
            return jsonify()

    return ResourceNotFound('registro do atleta na prova')


@blueprint.route('/all', methods=['GET'])
@marshal_with(AthleteSchema(many=True))
def all_athletes(**_):
    return Athlete.query.all()
