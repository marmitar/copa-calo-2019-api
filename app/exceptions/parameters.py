import functools

from app.exceptions import JSONException


class MissingParameters(JSONException):
    code = 400
    description = 'Request missing parameters'

    def __init__(self, *args):
        super().__init__(missing=list(args))


class ParameterNotModifiable(JSONException):
    code = 405
    description = 'Parameter not modifiable'

    def __init__(self, *args):
        super().__init__(parameters=list(args))


class InvalidParameter(JSONException):
    code = 401
    description = 'Request with an invalid parametr'

    def __init__(self, parameter, value=None, description=None):
        kwargs = {
            'invalid_parameter': parameter,
            'description': description
        }
        if value:
            kwargs['values'] = value

        super().__init__(**kwargs)
