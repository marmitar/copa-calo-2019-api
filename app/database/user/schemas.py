from app.database.schema import Schema, fields, validate

from app.exceptions import InvalidParameter


class UserSchema(Schema):
    __schema__ = 'user'

    username = fields.String(
        allow_none = False,
        validate   = validate.Length(min=5, max=32)
    )
    college_initials = fields.String(
        allow_none = False,
        validate   = validate.Length(max=5)
    )

    password = fields.String(
        allow_none = False,
        load_only  = True
    )
    new_password = fields.String(
        allow_none = False,
        load_only  = True
    )
