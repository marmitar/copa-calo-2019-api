from app.exceptions import JSONException, InvalidParameter


class InvalidPassword(InvalidParameter):
    code = 401
    description = 'Given password does not match user password'

    def __init__(self):
        super().__init__(parameter='password')


class UserAlreadyRegistered(JSONException):
    code = 409
    description = 'Username or Email already registered'


class UserNotFound(JSONException):
    code = 404
    description = 'Email not associated with any user'
