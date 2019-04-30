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
    description = 'Recurso não encontrado'

    def __init__(self, resource=None):
        kw = {'resource': resource} if resource else {}
        super().__init__(**kw)


class RegistrationLimit(JSONException):
    code = 409
    description = 'Limite de inscrições para o atleta'


class UnathorizedAcces(JSONException):
    code = 401
    description = 'Sem autorização para acessar esta recurso'


class ExpiredToken(JSONException):
    code = 401
    description = 'Token expirou'


class InvalidToken(JSONException):
    code = 422
    description = 'Token inválido'


class RevokedToken(JSONException):
    code = 401
    description = 'Token revoked'


class EndOfRegistrationPeriod(UnathorizedAcces):
    description = 'Acabou o período de inscrição'
