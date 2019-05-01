from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from sqlalchemy.exc import IntegrityError

from app.exceptions import require_args, ForbiddenAccess
from app.exceptions.models import ResourceNotFound, AlreadyRegistered, RegistrationLimit
from app.database.models import Event, Track
from app.database.schemas import EventSchema
from app.tracks import TrackType
from .__helpers__ import Permision, permission_required

blueprint = Blueprint('event', __name__)


@blueprint.route('/create', methods=['PUT'])
@permission_required(Permision.admin)
@use_kwargs(EventSchema)
@marshal_with(EventSchema)
@require_args
def create_event(name, track_type, sex, time, status=None, last_ev_name=None, **_):
    track = Track.get(track_type=track_type, sex=sex)
    if not track:
        raise ResourceNotFound('prova')

    try:
        event = Event(track, name, time, status)
    except IntegrityError:
        raise AlreadyRegistered('evento')

    last_ev = Event.get(track_id=track.id, name=name)
    if last_ev:
        event.update(last_ev=last_ev)

    return event


@blueprint.route('/read', methods=['GET'])
@use_kwargs(EventSchema)
@marshal_with(EventSchema(many=True))
def get_event(**kwargs):
    for key, val in kwargs.items():
        if not val:
            del kwargs[key]
    return Track.query.filter(**kwargs)


@blueprint.route('/status', methods=['PATCH'])
@permission_required(Permision.admin, Permision.arbiter)
@use_kwargs(EventSchema)
def change_status(name, track_type, sex, status, **_):
    track = Track.get(track_type=track_type, sex=sex)
    if not track:
        raise ResourceNotFound('prova')

    event = Event.get(track_id=track.id, name=name)
    if not event:
        raise ResourceNotFound('evento')

    event.update(status=status)
    return jsonify()


@blueprint.route('/all', methods=['GET'])
@marshal_with(EventSchema(many=True))
def all_events():
    return Event.query.all()
