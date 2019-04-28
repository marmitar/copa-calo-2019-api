from app.database.schema import Schema, fields, validate, EnumField
from app.tracks import Sex


class AthleteSchema(Schema):

    name = fields.String(
        allow_none = False,
        validate   = validate.Length(min=5, max=64)
    )

    rg = fields.String(
        allow_none = False,
        validate   = validate.Length(max=20)
    )

    rg_orgao = fields.String(
        allow_none = False,
        validate   = validate.Length(max=10)
    )

    sex = EnumField(
        Sex,
        allow_none = False,
        by_value   = True,
    )

    extra = fields.Boolean(
        allow_none = False
    )

    college = fields.String(
        attribute  = 'college_initials',
        allow_none = False,
        validate   = validate.Length(max=5),
        dump_only  = True
    )

    tracks = fields.Nested(
        'TrackSchema',
        many       = True,
        allow_none = False,
        dump_only  = True
    )
