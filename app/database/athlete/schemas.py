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

    rgOrgao = fields.String(
        attribute  = 'rg_orgao',
        allow_none = False,
        validate   = validate.Length(max=10)
    )

    sex = EnumField(
        Sex,
        allow_none = False,
        by_value   = True,
    )

    college = fields.String(
        attribute  = 'college_initials',
        allow_none = True,
        validate   = validate.Length(max=10)
    )

    tracks = fields.Nested(
        'RegistrationSchema',
        attribute  = 'registrations',
        exclude    = ('athletes',),
        many       = True,
        allow_none = False,
        dump_only  = True
    )
