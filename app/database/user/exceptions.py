from app.exceptions import JSONException


class InvalidPassword(JSONException):
    code = 401
    description = 'Given password does not match user password'
