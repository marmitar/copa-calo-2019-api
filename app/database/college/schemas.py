from app.database.schema import Schema, fields, validate


class CollegeSchema(Schema):
    __schema__ = 'college'

    name = fields.String(
        allow_none = False,
        validate   = validate.Length(min=5, max=64)
    )
    initials = fields.String(
        allow_none = False,
        validate   = validate.Length(max=5)
    )
    logo = fields.Raw(
        allow_none = False
    )
