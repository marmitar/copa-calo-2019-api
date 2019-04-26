from app.exceptions import JSONException


class MissingParameters(JSONException):
    code = 400
    description = 'Request missing parameters'

    def __init__(self, *args):
        super().__init__(missing=list(args))


class ParameterNotModifiable(JSONException):
    code = 405
    description = 'Parameter not modifiable'

    def __init__(self, **args):
        super().__init__(parameters=list(args))


class InvalidParameter(JSONException):
    code = 401
    description = 'Invalid Parameter'

    def __init__(self, parameter, value=None, error=None):
        kwargs = {'parameter': parameter}
        if value:
            kwargs['value'] = value
        if error:
            kwargs['error'] = error

        super().__init__(**kwargs)
