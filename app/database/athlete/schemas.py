from app.database.schema import Schema, fields, validate, EnumField
from app.database.athlete import Sex


class AthleteSchema(Schema):

    name = fields.String(
        allow_none = False,
        validate   = validate.Length(min=5, max=64)
    )

    rg = fields.String(
        allow_none = False,
        validate   = validate.Length(max=16)
    )

    sex = EnumField(
        Sex,
        allow_none = False,
        by_value = True,
    )

    extra = fields.Boolean(
        allow_none = False
    )

    college = fields.String(
        attribute  = 'college_initials',
        allow_none = False,
        validate   = validate.Length(max=5)
    )
