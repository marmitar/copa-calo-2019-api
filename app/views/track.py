from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from sqlalchemy.exc import IntegrityError

from app.exceptions import require_args, ForbiddenAccess
from app.exceptions.models import ResourceNotFound, AlreadyRegistered, RegistrationLimit
from app.database.models import Athlete, College, Track, Registration
from app.database.schemas import TrackSchema, RegistrationSchema, TrackTypeSchema
from app.tracks import TrackType
from .__helpers__ import Permision, permission_required

blueprint = Blueprint('track', __name__)


@blueprint.route('/create', methods=['PUT'])
@permission_required(Permision.admin)
@use_kwargs(TrackSchema)
@marshal_with(TrackSchema)
@require_args
def create_track(track_type, sex, **_):
    try:
        track = Track(track_type, sex)
    except IntegrityError:
        raise AlreadyRegistered('track')

    return track


@blueprint.route('/read', methods=['GET'])
@use_kwargs(TrackSchema)
@marshal_with(TrackSchema)
@require_args
def get_track(track_type, sex, **_):
    return Track.get(track_type=track_type, sex=sex)


@blueprint.route('/register', methods=['POST'])
@permission_required(Permision.admin, Permision.dm)
@use_kwargs(RegistrationSchema)
@marshal_with(RegistrationSchema)
@require_args
def register_athlete(athlete_name, athlete_rg, track, best_mark=None, extra=None, **_):
    athlete = Athlete.get(name=athlete_name, rg=athlete_rg)
    if len(athlete.tracks) == 3:
        raise RegistrationLimit

    user = current_user
    if not user.is_admin() and user.college != athlete.college:
        raise ForbiddenAccess

    track = Track.get(track_type=track, sex=athlete.sex)

    try:
        reg = Registration(athlete, track, best_mark, extra)
    except IntegrityError:
        raise AlreadyRegistered('atleta na prova')

    return reg


@blueprint.route('/types', methods=['GET'])
@marshal_with(TrackTypeSchema(many=True))
def track_types():
    return TrackType


@blueprint.route('/all', methods=['GET'])
@marshal_with(TrackSchema(many=True, exclude=('athletes',)))
def all_tracks():
    return Track.query.all()
