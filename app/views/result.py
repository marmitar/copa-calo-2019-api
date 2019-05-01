from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from sqlalchemy.exc import IntegrityError

from app.exceptions import require_args, ForbiddenAccess
from app.exceptions.models import ResourceNotFound, AlreadyRegistered, RegistrationLimit
from app.database.models import Event, Track, Athlete, Result
from app.database.schemas import ResultSchema, AthleteSchema
from app.tracks import TrackType
from .__helpers__ import Permision, permission_required

blueprint = Blueprint('result', __name__)


@blueprint.route('/create', methods=['PUT'])
@permission_required(Permision.admin, Permision.arbiter)
@use_kwargs(ResultSchema)
@marshal_with(ResultSchema)
@require_args
def create_result(track_type, athlete_name, athlete_rg, value=None, removed=None, reason=None, **_):
    athlete = Athlete.get(name=athlete_name, rg=athlete_rg)
    if not athlete:
        raise ResourceNotFound('atleta')

    track = Track.get(track_type=track_type, sex=athlete.sex)
    if not track:
        raise ResourceNotFound('prova')

    event = Event.get(track_id=track.id)
    if not event:
        raise ResourceNotFound('evento')

    try:
        result = Result(event, athlete, value, removed, reason)
    except IntegrityError:
        raise AlreadyRegistered('resultado')

    return result


@blueprint.route('/update', methods=['PATCH'])
@permission_required(Permision.admin, Permision.arbiter)
@use_kwargs(ResultSchema)
@marshal_with(ResultSchema)
@require_args
def update_result(id, value=None, removed=None, reason=None, **_):
    result = Result.get_by_id(id)
    if not result:
        raise ResourceNotFound('resultado')

    if value:
        result.value = value
    if removed:
        result.removed = removed
    if reason:
        result.reason = reason
    result.save()
    return result
