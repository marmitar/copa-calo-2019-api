from app.database.schema import Schema, fields, validate, EnumField
from app.tracks import Sex, TrackType


class TrackSchema(Schema):

    track_type = EnumField(
        TrackType,
        allow_none = False
    )

    sex = EnumField(
        Sex,
        allow_none = False,
        by_value   = True,
    )
