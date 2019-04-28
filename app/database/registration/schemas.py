from app.database.schema import Schema, fields, validate, EnumField

from app.tracks import TrackType


class RegistrationSchema(Schema):

    athlete_rg = fields.String(
        allow_none = False,
        load_only  = True
    )

    track = EnumField(
        TrackType,
        allow_none = False
    )

    athlete = fields.Nested(
        'AthleteSchema',
        allow_none = False,
        dump_only = True
    )
