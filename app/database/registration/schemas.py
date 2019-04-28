from app.database.schema import Schema, fields, validate, EnumField

from app.tracks import TrackType


class RegistrationSchema(Schema):

    name = fields.String(
        allow_none = False,
        load_only  = True
    )

    track = EnumField(
        TrackType,
        allow_none = False
    )

    best_mark = fields.Float(
        allow_none = True
    )

    athlete = fields.Nested(
        'AthleteSchema',
        allow_none = False,
        dump_only = True
    )
