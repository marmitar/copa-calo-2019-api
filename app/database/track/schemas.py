from app.database.schema import Schema, fields, validate, EnumField, pre_dump
from app.tracks import Sex, TrackType


class TrackSchema(Schema):

    trackType = EnumField(
        TrackType,
        attribute  = 'track_type',
        load_only  = True,
        allow_none = False
    )

    name = fields.String(
        allow_none = False,
        dump_only  = True,
    )

    sex = EnumField(
        Sex,
        allow_none = False,
        by_value   = True,
    )

    athletes = fields.Nested(
        'RegistrationSchema',
        attribute  = 'registrations',
        exclude    = ('track',),
        many       = True,
        allow_none = False,
        dump_only  = True
    )


class TrackTypeSchema(Schema):
    track_type = EnumField(
        TrackType,
        allow_none = False
    )
