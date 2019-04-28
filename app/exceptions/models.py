from app.exceptions import JSONException, InvalidParameter


class InvalidPassword(InvalidParameter):
    code = 401
    description = 'Given password does not match user password'

    def __init__(self):
        super().__init__(parameter='password')


class AlreadyRegistered(JSONException):
    code = 409
    description = 'Resource already registered'

    def __init__(self, resource=None):
        kw = {'resource': resource} if resource else {}
        super().__init__(**kw)


class ResourceNotFound(JSONException):
    code = 404
    description = 'Resource not found'

    def __init__(self, resource=None):
        kw = {'resource': resource} if resource else {}
        super().__init__(**kw)


class RegistrationLimit(JSONException):
    code = 409
    description = 'Limit of registrations for this athlete'
