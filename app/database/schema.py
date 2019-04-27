import marshmallow
from marshmallow import pre_load, pre_dump, post_load, post_dump, fields, validate
from app.exceptions import InvalidParameter


class Schema(marshmallow.Schema):
    __schema__ = 'schema'

    @post_dump
    def dump_user(self, data):
        return {self.__schema__: data}

    def handle_error(self, error, data):
        field_error = list(error.normalized_messages().items())[0]
        field, messages = field_error

        raise InvalidParameter(parameter=field, description=messages[0])
