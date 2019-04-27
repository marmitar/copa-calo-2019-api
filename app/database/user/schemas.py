from app.database.schema import Schema, fields, validate

from app.exceptions import InvalidParameter


class UserSchema(Schema):

    username = fields.String(
        allow_none = False,
        validate   = validate.Length(min=5, max=32)
    )
    college = fields.String(
        attribute  = 'college_initials',
        allow_none = False,
        validate   = validate.Length(max=5),
        load_only  = True
    )

    password = fields.String(
        allow_none = False,
        load_only  = True
    )
    new_password = fields.String(
        allow_none = False,
        load_only  = True
    )
