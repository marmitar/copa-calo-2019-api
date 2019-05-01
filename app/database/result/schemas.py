from app.database.schema import Schema, fields, validate, EnumField, pre_dump
from app.tracks import Sex, TrackType


class ResultSchema(Schema):

    trackType = EnumField(
        TrackType,
        attribute  = 'track_type',
        allow_none = False,
        load_only  = True
    )

    athleteName = fields.String(
        attribute  = 'athlete_name',
        allow_none = False,
        load_only  = True,
    )

    athleteRg = fields.String(
        attribute  = 'athlete_rg',
        allow_none = False,
        load_only  = True,
    )

    value = fields.Integer(
        allow_none = True,
    )

    removed = fields.Boolean(
        allow_none = True
    )

    reason = fields.String(
        allow_none = True
    )

    athlete = fields.Nested(
        'AthleteSchema',
        exclude   = ('tracks',),
        dump_only = True
    )

    track = fields.Nested(
        'TrackSchema',
        dump_only = True
    )

    id = fields.Integer(
        allow_none = True
    )
