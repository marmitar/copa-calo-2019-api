from app.database.schema import Schema, fields, validate, EnumField
from app.tracks import Sex, Status


class EventSchema(Schema):

    name = fields.String(
        allow_none = False,
        dump_only  = True,
    )

    trackName = fields.String(
        attribute  = 'track_name',
        allow_none = False,
        load_only  = True
    )

    sex = EnumField(
        Sex,
        allow_none = False,
        load_only  = True
    )

    time = fields.DateTime(
        allow_none = False
    )

    status = EnumField(
        Status,
        allow_none = True
    )

    track = fields.Nested(
        'TrackSchema',
        exclude   = ('athletes',),
        dump_only = True
    )
