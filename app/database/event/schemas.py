from app.database.schema import Schema, fields, validate, EnumField
from app.tracks import Sex, Status


class EventSchema(Schema):

    name = fields.String(
        allow_none = False
    )

    trackType = fields.String(
        attribute  = 'track_type',
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
        dump_by    = EnumField.VALUE,
        allow_none = True
    )

    after = fields.String(
        attribute  = 'last_ev_name',
        allow_none = True,
    )

    track = fields.Nested(
        'TrackSchema',
        exclude   = ('athletes', 'events'),
        dump_only = True
    )
