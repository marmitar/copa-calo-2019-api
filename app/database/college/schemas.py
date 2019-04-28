from app.database.schema import Schema, fields, validate


class CollegeSchema(Schema):

    name = fields.String(
        allow_none = False,
        validate   = validate.Length(min=5, max=64)
    )
    team = fields.String(
        allow_none = False,
        validate   = validate.Length(min=5, max=64)
    )
    initials = fields.String(
        allow_none = False,
        validate   = validate.Length(min=2, max=10)
    )
