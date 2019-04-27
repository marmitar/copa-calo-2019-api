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
from app.database.models import College
from app.database.schemas import CollegeSchema

blueprint = Blueprint('college', __name__)


@blueprint.route('/create', methods=['POST'])
@use_kwargs(CollegeSchema)
@marshal_with(CollegeSchema)
@require_args
def register_college(name, initials):
    try:
        college = College(name, initials)

    except IntegrityError as err:
        pass

    return college
