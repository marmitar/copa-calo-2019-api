from marshmallow import Schema, pre_load, post_dump
from marshmallow.fields import String, Email, DateTime
from marshmallow.validate import Length


class UserSchema(Schema):
    username = String(allow_none=False, validate=Length(min=5, max=32))
    email = Email(required=True, allow_none=False, validate=Length(max=48))

    password = String(allow_none=False, load_only=True)
    old_password = String(allow_none=False, load_only=True)
    token = String(allow_none=False, dump_only=True)

    createdAt = DateTime(attribute='created_at', dump_only=True)
    updatedAt = DateTime(attribute='updated_at', dump_only=True)


    @post_dump
    def dump_user(self, data):
        return {'user': data}

    def handle_error(error, data):
        pass

    class Meta:
        strict = True
