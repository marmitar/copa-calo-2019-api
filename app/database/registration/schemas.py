from app.database.schema import Schema, fields, validate, EnumField

from app.tracks import TrackType


class RegistrationSchema(Schema):

    athlete = fields.String(
        attribute  = 'athlete_rg',
        allow_none = False
    )

    track = EnumField(
        TrackType,
        allow_none = False
    )
